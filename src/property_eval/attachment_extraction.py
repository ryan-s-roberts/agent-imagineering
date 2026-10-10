"""Unified event and prefix-linked attachment entity/assertion extraction diagnostic."""

import argparse
import asyncio
import hashlib
import json
import os
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .cli import write_json
from .decision_alignment import align_decision
from .decision_replay import extract_packet, structured_call
from .models import (
    EVIDENCE_ONTOLOGY_VERSION,
    EntityExtraction,
    LinkExtraction,
    MentionExtraction,
    RecordExtraction,
)
from .prefix import load_prefix
from .response import DecisionResponse, validate_response
from .soft_experiment import decision_payload, request
from .source_context import prefix_source_context

JOBS = [("010", 13), ("020", 17)]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DECISION_PROMPT = PROJECT_ROOT / "experiments/prompts/decision-role-v1.txt"


def prepare(args):
    # Inputs belong to versioned source; run directories contain frozen outputs.
    decision_prompt = DECISION_PROMPT.read_text(encoding="utf-8")
    selected = (
        json.loads(args.manifest.read_text())
        if getattr(args, "manifest", None)
        else {"jobs": [{"case": case, "cutoff": cutoff} for case, cutoff in JOBS]}
    )
    selected_jobs = selected["jobs"]
    if not selected_jobs:
        raise ValueError("Manifest must contain at least one job")
    root = args.output
    root.mkdir(parents=True, exist_ok=False)
    jobs = []
    from .record_batches import plan_record_batches

    for selection in selected_jobs:
        case, cutoff = selection["case"], selection["cutoff"]
        prefix = load_prefix(args.source, case, cutoff)
        context = prefix_source_context(args.source, case, prefix)
        batch_plan = plan_record_batches(context["sources"], max_primary_chars=4000)
        jobs.append(
            {
                "id": f"{case}-at-{cutoff:03}",
                "case": case,
                "cutoff": cutoff,
                "prefix_sha256": prefix.source_sha256,
                "context_sha256": context["context_sha256"],
                "record_batch_count": len(batch_plan["batches"]),
                "record_batch_plan_sha256": hashlib.sha256(
                    json.dumps(batch_plan, sort_keys=True).encode()
                ).hexdigest(),
                "split": selection.get("split", "development_diagnostic"),
            }
        )
    if len({job["id"] for job in jobs}) != len(jobs):
        raise ValueError("Duplicate manifest checkpoint")
    write_json(
        root / "manifest.json",
        {
            "version": "attachment-extraction-v2",
            "mode": "prefix_evaluation",
            "jobs": jobs,
            "selection": selected.get("selection", "two attachment diagnostic prefixes"),
        },
    )
    write_json(
        root / "run-settings.json",
        {
            "model": "openai/gpt-6-luna",
            "max_tokens": 14000,
            "concurrency": 24,
            "mention_coverage": True,
            "compact_model_view": True,
            "cache_policy": "automatic provider caching; stable session_id and prompt_cache_key from ontology and full source context; shared batch prefix with ownership last; no serial warmup",
            "record_batch_chars": 4000,
            "ontology_version": EVIDENCE_ONTOLOGY_VERSION,
            "decision_prompt_asset": "experiments/prompts/decision-role-v1.txt",
            "decision_prompt_sha256": hashlib.sha256(decision_prompt.encode()).hexdigest(),
            "planned_calls": sum(4 + j["record_batch_count"] for j in jobs),
            "no_judge": True,
        },
    )
    write_json(
        root / "tbox.json",
        {
            "version": "attachment-tbox-v2",
            "evidence_ontology_version": EVIDENCE_ONTOLOGY_VERSION,
            "evidence": {
                m.__name__: m.model_json_schema()
                for m in (MentionExtraction, LinkExtraction, EntityExtraction, RecordExtraction)
            },
            "result": DecisionResponse.model_json_schema(),
            "semantics": (PROJECT_ROOT / "docs/ontology-semantics-v1.md").read_text()
            + "\n"
            + (PROJECT_ROOT / "docs/role-identity-v5.md")
            .read_text()
            .split("The intervention evaluates")[0]
            + "\n"
            + (PROJECT_ROOT / "docs/observation-ontology-v7.md").read_text()
            + "\nAttachment-origin records are document reports, not verified state. Source document_id is an ingestion handle distinct from an extracted entity ID. Availability is not assertion date. Unsupported document fact kinds remain explicit ontology gaps.",
        },
    )
    (root / "decision-prompt.txt").write_text(decision_prompt, encoding="utf-8")
    write_json(root / "response-schema.json", DecisionResponse.model_json_schema())
    write_json(
        root / "extraction-schemas.json",
        {
            m.__name__: m.model_json_schema()
            for m in (MentionExtraction, LinkExtraction, EntityExtraction, RecordExtraction)
        },
    )
    write_json(
        root / "implementation-snapshot.json",
        {
            name: {
                "source": (Path(__file__).parent / name).read_text(),
                "sha256": hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest(),
            }
            for name in (
                "attachments.py",
                "source_context.py",
                "models.py",
                "prompt.py",
                "mention_coverage.py",
                "grounding.py",
                "canonicalization.py",
                "decision_replay.py",
                "attachment_extraction.py",
                "model_view.py",
                "record_batches.py",
                "record_wire.py",
                "validation.py",
                "client.py",
            )
        },
    )


async def run(args):
    root = args.output
    settings = json.loads((root / "run-settings.json").read_text())
    manifest = json.loads((root / "manifest.json").read_text())
    args.model, args.max_tokens, args.mention_coverage = (
        settings["model"],
        settings["max_tokens"],
        True,
    )
    args.compact_model_view = settings.get("compact_model_view", False)
    args.record_batch_chars = settings.get("record_batch_chars")
    args.request_semaphore = asyncio.Semaphore(settings["concurrency"])
    key = (
        dotenv_values(args.env_file).get("OPENROUTER_API_KEY")
        if args.env_file
        else os.environ.get("OPENROUTER_API_KEY")
    )
    if not key:
        raise ValueError("Provide OPENROUTER_API_KEY or --env-file")
    semaphore = asyncio.Semaphore(settings["concurrency"])

    async def one(job, client):
        async with semaphore:
            folder = root / job["id"]
            folder.mkdir(exist_ok=True)
            started, usage = time.monotonic(), {}
            result = {
                "id": job["id"],
                "model": args.model,
                "status": "running",
                "mode": "prefix_evaluation",
                "split": job["split"],
                "prefix_sha256": job["prefix_sha256"],
            }
            try:
                async with asyncio.timeout(600):
                    packet = await extract_packet(job, args, folder, client, key, usage)
                    if packet["context_sha256"] != job["context_sha256"]:
                        raise ValueError("Attachment context changed after freeze")
                    write_json(folder / "evidence-packet.json", packet)
                    tbox = json.loads((root / "tbox.json").read_text())
                    body = request(
                        decision_payload(packet, tbox),
                        (root / "decision-prompt.txt").read_text(),
                        DecisionResponse.model_json_schema(),
                        args.model,
                        8000,
                        "decision",
                    )
                    view = None
                    if args.compact_model_view:
                        from .model_view import ModelView

                        view = ModelView(packet["sources"])
                        view.extend_mentions(packet["mentions"])
                        view.extend_entities(packet["entities"])
                        view.extend_records(packet["records"])
                        write_json(folder / "id-aliases.json", view.alias_artifact())
                    raw = await structured_call(
                        client,
                        key,
                        body,
                        DecisionResponse,
                        folder,
                        "decisions",
                        usage,
                        model_view=view,
                        request_semaphore=args.request_semaphore,
                    )
                    write_json(folder / "decisions-raw-parsed.json", raw.model_dump())
                    aligned = align_decision(raw.model_dump(), packet["sources"])
                    write_json(folder / "decisions-canonicalization.json", aligned)
                    decision = DecisionResponse.model_validate(aligned["response"])
                    write_json(folder / "decisions.json", decision.model_dump())
                    write_json(
                        folder / "decisions-validation.json", validate_response(decision, packet)
                    )

                    result.update(
                        {
                            "status": "completed",
                            "context_sha256": packet["context_sha256"],
                            "diagnostics": packet["diagnostics"],
                        }
                    )
            except (
                ValueError,
                TypeError,
                KeyError,
                IndexError,
                TimeoutError,
                httpx.HTTPError,
            ) as error:
                result.update(
                    {"status": "failure", "error": str(error), "error_type": type(error).__name__}
                )
            result.update(
                {
                    "usage_by_stage": usage,
                    "latency_seconds": time.monotonic() - started,
                    "cost_usd": sum(v.get("cost", 0) or 0 for v in usage.values()),
                }
            )
            write_json(folder / "result.json", result)
            print(f"{job['id']}: {result['status']} (${result['cost_usd']:.5f})", flush=True)
            return result

    started = time.monotonic()
    async with httpx.AsyncClient(timeout=180) as client:
        results = await asyncio.gather(*[one(j, client) for j in manifest["jobs"]])
    write_json(
        root / "summary.json",
        {
            "results": results,
            "denominator": len(manifest["jobs"]),
            "completed": sum(r["status"] == "completed" for r in results),
            "wall_clock_seconds": time.monotonic() - started,
            "observed_peak_requests": getattr(args.request_semaphore, "observed_peak", 0),
            "cost_usd": sum(r["cost_usd"] for r in results),
            "meaning": "Extracted attachment entities and assertions share the event graph; not a decision-quality benchmark.",
        },
    )
    from .finalization import finalize_run

    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "run"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, help="Optional case/cutoff jobs with split labels")
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args()
    prepare(args) if args.mode == "prepare" else asyncio.run(run(args))


if __name__ == "__main__":
    main()
