"""Parallel prefix extraction with independent, auditable output directories."""

import argparse
import asyncio
import hashlib
import json
import os
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .client import complete, parse_response, request_body
from .grounding import link_entities, resolve_mentions
from .models import LinkExtraction, MentionExtraction, RecordExtraction
from .prefix import load_prefix
from .validation import decision_packet, validate_records


def write_json(path: Path, value: dict):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


async def run(args):
    manifest = json.loads(args.manifest.read_text())
    if args.concurrency < 1 or args.max_tokens < 1 or args.timeout <= 0:
        raise ValueError("Concurrency, token limit and timeout must be positive")
    ids = [job["id"] for job in manifest["jobs"]]
    if len(ids) != len(set(ids)) or any(
        not name or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for c in name)
        for name in ids
    ):
        raise ValueError("Job IDs must be unique safe directory names")
    prefixes = [load_prefix(args.source, job["case"], job["cutoff"]) for job in manifest["jobs"]]
    key = os.environ.get("OPENROUTER_API_KEY")
    if args.env_file:
        key = dotenv_values(args.env_file).get("OPENROUTER_API_KEY") or key
    if not args.dry_run and not key:
        raise ValueError("Provide OPENROUTER_API_KEY or --env-file")
    args.output.mkdir(parents=True, exist_ok=False)
    write_json(args.output / "manifest.json", manifest)
    semaphore = asyncio.Semaphore(args.concurrency)

    async def job_run(job, prefix, client):
        async with semaphore:
            directory = args.output / job["id"]
            directory.mkdir()
            from .source_context import prefix_source_context

            context = await asyncio.to_thread(
                prefix_source_context, args.source, job["case"], prefix
            )
            units = context["sources"]
            write_json(directory / "attachments.json", context["attachments"])
            few_shot = getattr(args, "few_shot", False)
            body = request_body(prefix, units, args.model, args.max_tokens, few_shot=few_shot)
            write_json(directory / "input.json", prefix.model_dump())
            write_json(directory / "sources.json", {"sources": units})
            write_json(directory / "mentions-request.json", body)
            start = time.monotonic()
            result = {
                "id": job["id"],
                "status": "prepared",
                "model": args.model,
                "prefix_sha256": prefix.source_sha256,
                "request_sha256": hashlib.sha256(
                    json.dumps(body, sort_keys=True).encode()
                ).hexdigest(),
            }
            if not args.dry_run:
                try:
                    async with asyncio.timeout(args.timeout):
                        response = await complete(client, key, body)
                        write_json(directory / "mentions-response.json", response)
                        result["usage_by_stage"] = {"mentions": response.get("usage", {})}
                        candidates = parse_response(response, MentionExtraction)
                        write_json(directory / "mention-candidates.json", candidates.model_dump())
                        mention_checks = resolve_mentions(candidates, units, prefix.case_id)
                        write_json(directory / "mentions.json", mention_checks)
                        if not mention_checks["valid"]:
                            result["status"] = "invalid_mentions"
                        else:
                            mentions = mention_checks["mentions"]
                            link_body = request_body(
                                prefix,
                                units,
                                args.model,
                                args.max_tokens,
                                mentions=mentions,
                                few_shot=few_shot,
                            )
                            write_json(directory / "links-request.json", link_body)
                            response = await complete(client, key, link_body)
                            write_json(directory / "links-response.json", response)
                            result["usage_by_stage"]["links"] = response.get("usage", {})
                            links = parse_response(response, LinkExtraction)
                            entities, link_checks = link_entities(links, mentions, units)
                            write_json(directory / "links.json", link_checks)
                            write_json(directory / "entities.json", entities.model_dump())
                            if not link_checks["valid"]:
                                raise ValueError("Invalid entity linking; inspect links.json")
                            record_body = request_body(
                                prefix,
                                units,
                                args.model,
                                args.max_tokens,
                                entities,
                                mentions=mentions,
                                few_shot=few_shot,
                            )
                            write_json(directory / "records-request.json", record_body)
                            response = await complete(client, key, record_body)
                            write_json(directory / "records-response.json", response)
                            result["usage_by_stage"]["records"] = response.get("usage", {})
                            records = parse_response(response, RecordExtraction)
                            write_json(directory / "records.json", records.model_dump())
                            checks = validate_records(records, entities, units)
                            write_json(directory / "records-validation.json", checks)
                            result["status"] = "valid" if checks["valid"] else "invalid_records"
                            result["counts"] = {
                                "entities": len(entities.entities),
                                "records": len(records.records),
                                "gaps": len(records.gaps),
                            }
                            if checks["valid"]:
                                packet = decision_packet(prefix, entities, records, units)
                                packet["mentions"] = mentions
                                packet["identity_links"] = link_checks
                                write_json(directory / "decision-state.json", packet)
                except (
                    httpx.HTTPError,
                    TimeoutError,
                    ValueError,
                    TypeError,
                    KeyError,
                    IndexError,
                ) as error:
                    result["status"] = "error"
                    result["error_type"] = type(error).__name__
                    # Transport exceptions omit request headers; never serialize credentials.
                    result["error"] = str(error)
            result["latency_seconds"] = round(time.monotonic() - start, 3)
            write_json(directory / "result.json", result)
            print(f"{job['id']}: {result['status']}", flush=True)
            return result

    async with httpx.AsyncClient(timeout=httpx.Timeout(120)) as client:
        results = await asyncio.gather(
            *[job_run(job, prefix, client) for job, prefix in zip(manifest["jobs"], prefixes)]
        )
    summary = {
        "evaluation": "property-evidence-v6; structural validity is not semantic accuracy",
        "results": results,
        "total": len(results),
        "valid": sum(r["status"] == "valid" for r in results),
    }
    write_json(args.output / "summary.json", summary)
    return 0 if all(r["status"] in {"valid", "prepared"} for r in results) else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", dest="source", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--max-tokens", type=int, default=12000)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--few-shot", action="store_true")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(run(args)))
