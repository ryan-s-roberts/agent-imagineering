"""Development-only extraction -> decision replay and cached prompt-only arms."""

import argparse
import asyncio
import hashlib
import json
import os
import shutil
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .canonicalization import canonicalize_links, canonicalize_mentions, canonicalize_records
from .cli import write_json
from .client import complete, parse_response, request_body
from .grounding import link_entities
from .models import EVIDENCE_ONTOLOGY_VERSION, LinkExtraction, MentionExtraction, RecordExtraction
from .prefix import load_prefix
from .response import DecisionResponse, validate_response


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def decision_request(packet, prompt, model, max_tokens):
    # Deliberate whitelist boundary: no target/observed-later/manifest enters this payload.
    return {
        "model": model,
        "max_tokens": max_tokens,
        "provider": {"require_parameters": True},
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(packet, ensure_ascii=False)},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "property_decision",
                "strict": True,
                "schema": DecisionResponse.model_json_schema(),
            },
        },
    }


class OutputLimitError(ValueError):
    """A retained length-limited response requires a smaller extraction unit."""


async def execute_record_subdivisions(batch, units, execute_leaf, persist_split):
    """Keep successful leaves; subdivide only the unit whose retained output overflowed."""
    from .record_batches import subdivide_record_batch

    try:
        return [(batch["id"], await execute_leaf(batch))]
    except OutputLimitError:
        children = subdivide_record_batch(batch, units)
        persist_split({"parent": batch, "children": children, "reason": "output_length"})
        parts = await asyncio.gather(
            *(
                execute_record_subdivisions(child, units, execute_leaf, persist_split)
                for child in children
            )
        )
        return [item for part in parts for item in part]


async def structured_call(
    client,
    key,
    body,
    response_type,
    directory,
    stage,
    usage,
    *,
    model_view=None,
    request_semaphore=None,
    subdivide_on_length=False,
):
    """One bounded interface-only repair. Preserve both responses and every error."""
    if model_view is not None:
        from .record_wire import derive_record_source_ids

        cache_key = digest({"ontology": EVIDENCE_ONTOLOGY_VERSION, "sources": model_view.sources})
        body = {**body, "session_id": cache_key, "prompt_cache_key": cache_key}
        write_json(directory / f"{stage}-canonical-request.json", body)
        body = model_view.encode_body(
            body, omit_record_source_ids=response_type is RecordExtraction
        )
        write_json(directory / f"{stage}-aliases.json", model_view.alias_artifact())

    call_timings = []

    async def invoke(request):
        queued = time.monotonic()
        started = None
        try:
            if request_semaphore is None:
                started = time.monotonic()
                return await complete(client, key, request)
            async with request_semaphore:
                started = time.monotonic()
                request_semaphore.observed_active = (
                    getattr(request_semaphore, "observed_active", 0) + 1
                )
                request_semaphore.observed_peak = max(
                    getattr(request_semaphore, "observed_peak", 0),
                    request_semaphore.observed_active,
                )
                try:
                    return await complete(client, key, request)
                finally:
                    request_semaphore.observed_active -= 1
        finally:
            ended = time.monotonic()
            call_timings.append(
                {
                    "attempt": len(call_timings) + 1,
                    "queue_seconds": (started or ended) - queued,
                    "request_seconds": None if started is None else ended - started,
                    "includes_transport_retries": True,
                }
            )
            write_json(directory / f"{stage}-timings.json", {"calls": call_timings})

    def parse(raw_response):
        if model_view is None:
            return parse_response(raw_response, response_type)
        choice = raw_response["choices"][0]
        if choice.get("finish_reason") != "stop":
            raise ValueError(f"Incomplete response: {choice.get('finish_reason')}")
        decoded = model_view.decode_output(json.loads(choice["message"]["content"]))
        if response_type is RecordExtraction:
            decoded = derive_record_source_ids(decoded)
        write_json(directory / f"{stage}-canonical-response.json", decoded)
        return response_type.model_validate(decoded)

    request_path = directory / f"{stage}-request.json"
    response_path = directory / f"{stage}-response.json"
    cached = response_path.exists() and request_path.exists()
    if cached and digest(json.loads(request_path.read_text())) != digest(body):
        raise ValueError(f"Cached {stage} request differs; refusing silent recomputation")
    write_json(request_path, body)
    response = json.loads(response_path.read_text()) if cached else await invoke(body)
    write_json(directory / f"{stage}-response.json", response)
    usage[stage] = response.get("usage", {})
    try:
        return parse(response)
    except (ValueError, TypeError, KeyError, IndexError) as error:
        error_text = str(error)
        write_json(
            directory / f"{stage}-interface-error.json", {"error": error_text, "repair_limit": 1}
        )
        if (
            subdivide_on_length
            and response.get("choices", [{}])[0].get("finish_reason") == "length"
        ):
            existing_repair = directory / f"{stage}-repair-response.json"
            if existing_repair.exists():
                retained = json.loads(existing_repair.read_text())
                usage[stage + "_repair"] = retained.get("usage", {})
                if retained.get("choices", [{}])[0].get("finish_reason") != "length":
                    return parse(retained)
            raise OutputLimitError(f"{stage} exceeded output budget; source subdivision required")
        repair = dict(body)
        repair["messages"] = [
            *body["messages"],
            {
                "role": "assistant",
                "content": response.get("choices", [{}])[0].get("message", {}).get("content", ""),
            },
            {
                "role": "user",
                "content": "Repair only the JSON/schema interface errors below, preserving supported semantic values and citing only supplied sources. Do not invent facts to fill mandatory values; use allowed null/unknown/empty values. Return the full response in the supplied schema. This is interface repair, not a new decision. Errors: "
                + error_text,
            },
        ]
        write_json(directory / f"{stage}-repair-request.json", repair)
        repair_path = directory / f"{stage}-repair-response.json"
        response = (
            json.loads(repair_path.read_text()) if repair_path.exists() else await invoke(repair)
        )
        write_json(directory / f"{stage}-repair-response.json", response)
        usage[stage + "_repair"] = response.get("usage", {})
        if (
            subdivide_on_length
            and response.get("choices", [{}])[0].get("finish_reason") == "length"
        ):
            raise OutputLimitError(
                f"{stage} repair exceeded output budget; source subdivision required"
            )
        return parse(response)


async def extract_packet(job, args, directory, client, key, usage):
    prefix = load_prefix(args.source, job["case"], job["cutoff"])
    if prefix.source_sha256 != job["prefix_sha256"]:
        raise ValueError("Prefix changed after checkpoint selection")
    from .source_context import prefix_source_context

    context = await asyncio.to_thread(prefix_source_context, args.source, job["case"], prefix)
    if job.get("context_sha256") and context["context_sha256"] != job["context_sha256"]:
        raise ValueError("Attachment context changed after freeze")
    units = context["sources"]
    write_json(directory / "attachments.json", context["attachments"])
    write_json(directory / "input.json", prefix.model_dump())
    write_json(directory / "sources.json", {"sources": units})
    view = None
    if getattr(args, "compact_model_view", False):
        from .model_view import ModelView

        view = ModelView(units)

    async def call(*positional):
        return await structured_call(
            *positional,
            model_view=view,
            request_semaphore=getattr(args, "request_semaphore", None),
            subdivide_on_length=bool(getattr(args, "record_batch_chars", None))
            and positional[3] is RecordExtraction,
        )

    candidates = await call(
        client,
        key,
        request_body(prefix, units, args.model, args.max_tokens),
        MentionExtraction,
        directory,
        "mentions",
        usage,
    )
    if getattr(args, "mention_coverage", False):
        from .mention_coverage import coverage_request

        write_json(directory / "mention-preliminary.json", candidates.model_dump())
        candidates = await call(
            client,
            key,
            coverage_request(prefix, units, candidates, args.model, args.max_tokens),
            MentionExtraction,
            directory,
            "mention-coverage",
            usage,
        )
    write_json(directory / "mention-candidates.json", candidates.model_dump())
    mentions = canonicalize_mentions(candidates, units, prefix.case_id)
    write_json(directory / "mentions.json", mentions)
    # Unmatched mentions remain explicit semantic uncertainty; resolved mentions are usable.
    mention_rows = mentions["mentions"]
    if view is not None:
        view.extend_mentions(mention_rows)
    links_raw = await call(
        client,
        key,
        request_body(prefix, units, args.model, args.max_tokens, mentions=mention_rows),
        LinkExtraction,
        directory,
        "links",
        usage,
    )
    write_json(directory / "links-raw.json", links_raw.model_dump())
    links_canonical = canonicalize_links(links_raw, units)
    links = LinkExtraction.model_validate(links_canonical["data"])
    entities, linking = link_entities(links, mention_rows, units)
    write_json(directory / "links-canonicalization.json", links_canonical)
    write_json(directory / "links.json", linking)
    write_json(directory / "entities.json", entities.model_dump())
    if view is not None:
        view.extend_entities(entities.model_dump()["entities"])
    batch_limit = getattr(args, "record_batch_chars", None)
    batch_issues = []
    if batch_limit:
        from .record_batches import (
            BATCH_INSTRUCTION,
            combine_record_batches,
            plan_record_batches,
            validate_batch_ownership,
        )

        plan = plan_record_batches(units, max_primary_chars=batch_limit)
        if (
            job.get("record_batch_plan_sha256")
            and hashlib.sha256(json.dumps(plan, sort_keys=True).encode()).hexdigest()
            != job["record_batch_plan_sha256"]
        ):
            raise ValueError("Record batch plan changed after freeze")
        write_json(directory / "record-batches.json", plan)

        subdivisions = []

        async def record_batch(batch):
            body = request_body(
                prefix, units, args.model, args.max_tokens, entities, mentions=mention_rows
            )
            body["messages"][0]["content"] += "\n" + BATCH_INSTRUCTION
            body["messages"].append(
                {
                    "role": "user",
                    "content": json.dumps({"primary_source_ids": batch["primary_source_ids"]}),
                }
            )
            output = await call(
                client, key, body, RecordExtraction, directory, "records-" + batch["id"], usage
            )
            try:
                validate_batch_ownership(output.model_dump(), batch, plan["context_source_ids"])
            except ValueError as error:
                batch_issues.append(
                    {
                        "batch_id": batch["id"],
                        "code": "batch_source_ownership",
                        "detail": str(error),
                    }
                )
            return output

        def persist_split(split):
            subdivisions.append(split)
            write_json(directory / "record-subdivisions.json", {"subdivisions": subdivisions})

        batch_outputs = await asyncio.gather(
            *(
                execute_record_subdivisions(batch, units, record_batch, persist_split)
                for batch in plan["batches"]
            )
        )
        combined, lineage = combine_record_batches(
            [item for part in batch_outputs for item in part]
        )
        write_json(
            directory / "record-batch-lineage.json", {"lineage": lineage, "issues": batch_issues}
        )
        records_raw = RecordExtraction.model_validate(combined)
    else:
        records_raw = await call(
            client,
            key,
            request_body(
                prefix, units, args.model, args.max_tokens, entities, mentions=mention_rows
            ),
            RecordExtraction,
            directory,
            "records",
            usage,
        )
    write_json(directory / "records-raw.json", records_raw.model_dump())
    canonical = canonicalize_records(
        records_raw, entities, units, source_texts=context["source_texts"]
    )
    write_json(directory / "records.json", canonical["data"])
    write_json(directory / "records-validation.json", canonical["validation"])
    write_json(directory / "records-canonicalization.json", canonical)
    diagnostics = {
        "mentions": mentions["issues"],
        "mention_alignment": mentions["unresolved_alignment"],
        "links": linking["issues"],
        "link_alignment": links_canonical["issues"],
        "records": canonical["validation"]["issues"],
        "record_alignment": canonical["unresolved_alignment"],
        "batch_ownership": batch_issues,
    }
    return {
        "ontology_version": EVIDENCE_ONTOLOGY_VERSION,
        "case_id": prefix.case_id,
        "cutoff": prefix.cutoff,
        "prefix_sha256": prefix.source_sha256,
        "context_sha256": context["context_sha256"],
        "attachments": {k: v for k, v in context["attachments"].items() if k != "pages"},
        "development_diagnostic": True,
        "validated_decision_state": False,
        "semantics": "Partial extracted evidence with explicit support uncertainty; not authoritative world state or a certified packet. Unsupported fields are visible for exploration.",
        "diagnostics": diagnostics,
        "entities": entities.model_dump()["entities"],
        "records": canonical["data"]["records"],
        "gaps": canonical["data"]["gaps"],
        "sources": units,
        "mentions": mention_rows,
        "identity_links": linking,
        "field_spans": canonical["field_spans"],
    }


def correspondence(response, target):
    proposed = sorted({a.type for a in response.actions})
    candidates = target["candidate_action_types"]
    return {
        "proposed_action_types": proposed,
        "observed_candidate_types": candidates,
        "type_overlap": sorted(set(proposed) & set(candidates)),
        "candidate_review_status": target["review_status"],
        "semantic_support_review": "unreviewed",
        "choice_quality": "not_automatically_judged",
        "meaning": "Coarse observed-action correspondence only; matching history does not establish a warranted or correct choice",
    }


async def run(args):
    manifest = json.loads(args.manifest.read_text())
    jobs = manifest["jobs"]
    if {j["case"] for j in jobs} != {f"{i:03}" for i in range(1, 41)} or len(jobs) != 40:
        raise ValueError(
            "This development baseline requires exactly cases001–040; holdout forbidden"
        )
    if args.concurrency < 1:
        raise ValueError("Concurrency must be positive")
    targets = {t["id"]: t for t in json.loads(args.targets.read_text())["targets"]}
    prompt = args.prompt.read_text()
    if args.evidence_root:
        prior_schema = json.loads((args.evidence_root / "response-schema.json").read_text())
        prior_settings = json.loads((args.evidence_root / "run-settings.json").read_text())
        if digest(prior_schema) != digest(DecisionResponse.model_json_schema()):
            raise ValueError("Response schema changed: this is not a prompt-only arm")
        if prior_settings["model"] != args.model or prior_settings["max_tokens"] != args.max_tokens:
            raise ValueError("Model/token settings changed: this is not a prompt-only arm")
    key = (
        dotenv_values(args.env_file).get("OPENROUTER_API_KEY")
        if args.env_file
        else os.environ.get("OPENROUTER_API_KEY")
    )
    if not key:
        raise ValueError("OPENROUTER_API_KEY is unavailable")
    if args.resume:
        settings = json.loads((args.output / "run-settings.json").read_text())
        if (
            settings["model"] != args.model
            or settings["max_tokens"] != args.max_tokens
            or settings["prompt_sha256"] != hashlib.sha256(prompt.encode()).hexdigest()
            or settings["schema_sha256"] != digest(DecisionResponse.model_json_schema())
        ):
            raise ValueError("Resume changed model, token budget, prompt or schema")
        if digest(json.loads((args.output / "manifest.json").read_text())) != digest(manifest):
            raise ValueError("Resume manifest changed")
    args.output.mkdir(parents=True, exist_ok=args.resume)
    (args.output / "decision-prompt.txt").write_text(prompt)
    write_json(args.output / "response-schema.json", DecisionResponse.model_json_schema())
    write_json(args.output / "manifest.json", manifest)
    implementation = {}
    for name in [
        "models.py",
        "client.py",
        "prompt.py",
        "grounding.py",
        "canonicalization.py",
        "validation.py",
        "response.py",
        "prefix.py",
        "decision_replay.py",
    ]:
        text = (Path(__file__).parent / name).read_text()
        implementation[name] = {"sha256": hashlib.sha256(text.encode()).hexdigest(), "source": text}
    write_json(
        args.output
        / (
            "resume-implementation-snapshot.json" if args.resume else "implementation-snapshot.json"
        ),
        implementation,
    )
    write_json(
        args.output / ("resume-settings.json" if args.resume else "run-settings.json"),
        {
            "model": args.model,
            "max_tokens": args.max_tokens,
            "timeout": args.timeout,
            "concurrency": args.concurrency,
            "prompt_path": str(args.prompt),
            "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
            "schema_sha256": digest(DecisionResponse.model_json_schema()),
            "evidence_root": str(args.evidence_root) if args.evidence_root else None,
            "interface_repair_limit": 1,
            "targets_sha256": digest(list(targets.values())),
        },
    )
    entries = [{**job, "path": job["id"], "status": "pending"} for job in jobs]
    index = {
        "version": "decision-dev-v1",
        "denominator": 40,
        "holdout_excluded": "041-050",
        "entries": entries,
    }
    if args.resume:
        index = json.loads((args.output / "corpus-index.json").read_text())
        entries = index["entries"]
    write_json(args.output / "corpus-index.json", index)
    semaphore = asyncio.Semaphore(args.concurrency)

    async def one(job, entry, client):
        async with semaphore:
            directory = args.output / job["id"]
            if args.resume and entry["status"] == "decision_generated":
                return json.loads((directory / "decision-review.json").read_text())
            if directory.exists():
                archive = args.output / "interrupted-attempts" / job["id"]
                archive.parent.mkdir(exist_ok=True)
                shutil.move(str(directory), archive)
                shutil.copytree(archive, directory)
            else:
                directory.mkdir()
            start = time.monotonic()
            usage = {}
            review = {
                "id": job["id"],
                "diagnostic": True,
                "status": "running",
                "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                "model": args.model,
            }
            write_json(directory / "observed-later.json", targets[job["id"]])
            try:
                async with asyncio.timeout(args.timeout):
                    if args.evidence_root:
                        prior = args.evidence_root / job["id"]
                        packet = json.loads((prior / "evidence-packet.json").read_text())
                        if packet["prefix_sha256"] != job["prefix_sha256"]:
                            raise ValueError("Cached prefix digest mismatch")
                        prior_review = json.loads((prior / "decision-review.json").read_text())
                        if digest(packet) != prior_review.get("evidence_sha256"):
                            raise ValueError("Cached evidence changed since its baseline decision")
                        for name in [
                            "input.json",
                            "sources.json",
                            "entities.json",
                            "records.json",
                            "records-validation.json",
                            "mentions.json",
                            "links.json",
                            "records-canonicalization.json",
                        ]:
                            path = prior / name
                            if path.exists():
                                (directory / name).write_bytes(path.read_bytes())
                    else:
                        packet = await extract_packet(job, args, directory, client, key, usage)
                    write_json(directory / "evidence-packet.json", packet)
                    review["evidence_sha256"] = digest(packet)
                    body = decision_request(packet, prompt, args.model, args.max_tokens)
                    review["decision_request_sha256"] = digest(body)
                    response = await structured_call(
                        client, key, body, DecisionResponse, directory, "decisions", usage
                    )
                    write_json(directory / "decisions.json", response.model_dump())
                    checks = validate_response(response, packet)
                    write_json(directory / "decisions-validation.json", checks)
                    review.update(
                        {
                            "status": "decision_generated",
                            "response": response.model_dump(),
                            "checks": checks,
                            "observed_correspondence": correspondence(response, targets[job["id"]]),
                            "semantic_review_status": "unreviewed",
                        }
                    )
            except (
                httpx.HTTPError,
                TimeoutError,
                ValueError,
                TypeError,
                KeyError,
                IndexError,
                FileNotFoundError,
            ) as error:
                review.update(
                    {
                        "status": "interface_failure"
                        if any(k.startswith("decisions") for k in usage)
                        else "extraction_failure",
                        "error_type": type(error).__name__,
                        "error": str(error),
                    }
                )
            review["usage_by_stage"] = usage
            review["latency_seconds"] = round(time.monotonic() - start, 3)
            review["cost_usd"] = sum(u.get("cost", 0) or 0 for u in usage.values())
            write_json(directory / "decision-review.json", review)
            write_json(
                directory / "result.json",
                {
                    k: v
                    for k, v in review.items()
                    if k not in {"response", "observed_correspondence"}
                },
            )
            entry.update(
                {
                    "status": review["status"],
                    "cost_usd": review["cost_usd"],
                    "checks": review.get("checks"),
                    "evidence_sha256": review.get("evidence_sha256"),
                }
            )
            write_json(args.output / "corpus-index.json", index)
            print(f"{job['id']}: {review['status']} (${review['cost_usd']:.5f})", flush=True)
            return review

    async with httpx.AsyncClient(timeout=httpx.Timeout(150)) as client:
        results = await asyncio.gather(
            *[one(j, e, client) for j, e in zip(jobs, entries, strict=True)]
        )
    write_json(
        args.output / "summary.json",
        {
            "denominator": 40,
            "decisions_generated": sum(r["status"] == "decision_generated" for r in results),
            "cost_usd": sum(r["cost_usd"] for r in results),
            "results": results,
            "semantics": "Development diagnostics; no automated semantic or choice-quality judge",
        },
    )
    from .finalization import finalize_run

    finalize_run(args.output)
    return 0 if all(r["status"] == "decision_generated" for r in results) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--evidence-root", type=Path)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--model", default="openai/gpt-6-luna")
    parser.add_argument("--max-tokens", type=int, default=16000)
    parser.add_argument("--timeout", type=float, default=360)
    parser.add_argument("--concurrency", type=int, default=24)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args)))


if __name__ == "__main__":
    main()
