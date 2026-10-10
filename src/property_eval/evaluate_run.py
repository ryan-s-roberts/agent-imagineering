"""Evaluate a saved single-arm run using frozen episode references; no decision reruns."""

import argparse
import asyncio
import json
import os
import time
from collections import Counter, defaultdict
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .citation_catalog import build_catalog
from .cli import write_json
from .decision_replay import digest, structured_call
from .episode_judge import (
    EpisodeJudgment,
    EpisodeValidator,
    constrained_schema,
    materialize_episode,
)
from .episode_metrics import alignment_metrics
from .episode_rejudge import episode_target
from .finalization import finalize_run
from .soft_experiment import citation_checks, judge_payload, request

PROJECT_ROOT = Path(__file__).resolve().parents[2]


async def evaluate(args):
    root = args.run
    manifest = json.loads((root / "manifest.json").read_text())
    settings = json.loads((root / "run-settings.json").read_text())
    tbox = json.loads((root / "tbox.json").read_text())
    prompt = (PROJECT_ROOT / "experiments/prompts/episode-judge-v1.txt").read_text()
    annotations = [json.loads(path.read_text()) for path in args.episodes]
    episodes = {e["checkpoint_id"]: e for doc in annotations for e in doc["episodes"]}
    ids = {j["id"] for j in manifest["jobs"]}
    if len(episodes) != sum(len(doc["episodes"]) for doc in annotations) or set(episodes) != ids:
        raise ValueError("Episode annotations must cover each checkpoint exactly once")
    if (root / "evaluation-summary.json").exists():
        raise ValueError("Evaluation already completed; preserve it rather than overwrite")
    key = (
        dotenv_values(args.env_file).get("OPENROUTER_API_KEY")
        if args.env_file
        else os.getenv("OPENROUTER_API_KEY")
    )
    if not key:
        raise ValueError("Provide OPENROUTER_API_KEY or --env-file")
    write_json(
        root / "episode-annotations.json",
        {"visibility": "evaluation_only", "episodes": list(episodes.values())},
    )
    (root / "judge-prompt.txt").write_text(prompt)
    write_json(
        root / "judge-implementation-snapshot.json",
        {
            name: {
                "source": (Path(__file__).parent / name).read_text(),
                "content_sha256": digest((Path(__file__).parent / name).read_text()),
            }
            for name in (
                "evaluate_run.py",
                "episode_judge.py",
                "episode_metrics.py",
                "episode_rejudge.py",
                "citation_catalog.py",
            )
        },
    )
    write_json(
        root / "evaluation-settings.json",
        {
            "model": settings["model"],
            "concurrency": 24,
            "max_tokens": 10000,
            "judge": "episode-judge-v1",
            "prompt_sha256": digest(prompt),
            "schema_sha256": digest(EpisodeJudgment.model_json_schema()),
            "annotations_sha256": digest(annotations),
            "prediction_reruns": 0,
            "semantics": "Historical correspondence is advisory; deterministic counts summarize model labels.",
        },
    )
    semaphore = asyncio.Semaphore(24)

    async def one(job, client):
        folder = root / job["id"]
        target = episode_target(episodes[job["id"]])
        write_json(folder / "episode-target.json", target)
        result = {"id": job["id"], "split": job["split"], "status": "unassessed"}
        usage, started = {}, time.monotonic()
        if not (folder / "decisions.json").exists():
            result["reason"] = "No completed prediction; retained in denominator"
            write_json(folder / "judge-result.json", result)
            return result
        try:
            packet = json.loads((folder / "evidence-packet.json").read_text())
            prediction = json.loads((folder / "decisions.json").read_text())
            catalog = build_catalog(packet, target, prediction)
            write_json(folder / "citation-catalog.json", catalog)
            payload = judge_payload(packet, tbox, target, prediction)
            payload["citation_catalog"] = catalog["spans"]
            body = request(
                payload,
                prompt,
                constrained_schema(catalog, target, prediction),
                settings["model"],
                10000,
                "judgment",
            )
            async with semaphore:
                async with asyncio.timeout(300):
                    selected = await structured_call(
                        client,
                        key,
                        body,
                        EpisodeValidator(catalog, target, prediction),
                        folder,
                        "judge",
                        usage,
                    )
            write_json(folder / "judge-selections.json", selected.model_dump())
            judgment, spans = materialize_episode(selected.model_dump(), catalog)
            write_json(folder / "judge.json", judgment)
            write_json(folder / "judge-spans.json", spans)
            checks = citation_checks(judgment, packet, target, prediction)
            if checks["invalid_citations"]:
                raise ValueError("Selected judge citations failed source alignment")
            write_json(folder / "judge-validation.json", checks)
            metrics = alignment_metrics(target, prediction, judgment)
            write_json(folder / "episode-metrics.json", metrics)
            result.update(
                status="completed",
                overall_correspondence=judgment["overall_correspondence"],
                metrics=metrics,
                citation_count=checks["citation_count"],
                prediction_sha256=digest(prediction),
                evidence_sha256=digest(packet),
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            IndexError,
            TimeoutError,
            httpx.HTTPError,
        ) as error:
            result.update(status="failure", error_type=type(error).__name__, error=str(error))
        result.update(
            usage_by_stage=usage,
            latency_seconds=time.monotonic() - started,
            reported_cost_usd=sum(u.get("cost", 0) or 0 for u in usage.values()),
            missing_cost_receipts=sum(u.get("cost") is None for u in usage.values()),
        )
        write_json(folder / "judge-result.json", result)
        print(f"judge {job['id']}: {result['status']}", flush=True)
        return result

    started = time.monotonic()
    async with httpx.AsyncClient(timeout=180) as client:
        results = await asyncio.gather(*(one(job, client) for job in manifest["jobs"]))
    splits = defaultdict(list)
    for result in results:
        splits[result["split"]].append(result)
    summaries = {}
    for split, rows in splits.items():
        counts, support = defaultdict(Counter), Counter()
        for row in rows:
            for kind, values in row.get("metrics", {}).get("coverage_by_materiality", {}).items():
                counts[kind].update(values)
            support.update(row.get("metrics", {}).get("prediction_supportedness", {}))
        jobs = [j for j in manifest["jobs"] if j["split"] == split]
        valid, compatible, actions, records_clean = 0, 0, 0, 0
        for job in jobs:
            folder = root / job["id"]

            def read(name, folder=folder):
                path = folder / name
                return json.loads(path.read_text()) if path.exists() else {}

            checks = read("decisions-validation.json")
            valid += checks.get("structurally_valid") is True
            compatible += checks.get("evidence_compatible") is True
            actions += len(read("decisions.json").get("actions", []))
            record_checks = read("records-validation.json")
            records_clean += bool(record_checks) and not record_checks.get("issues")
        summaries[split] = {
            "denominator": len(rows),
            "judge_completed": sum(r["status"] == "completed" for r in rows),
            "overall_correspondence": dict(
                Counter(r.get("overall_correspondence", "unassessed") for r in rows)
            ),
            "decision_structurally_valid": valid,
            "decision_evidence_compatible": compatible,
            "records_without_validation_issues": records_clean,
            "proposed_actions": actions,
            "coverage_by_materiality": {k: dict(v) for k, v in counts.items()},
            "prediction_supportedness": dict(support),
            "full_operational_coverage": sum(
                r.get("metrics", {}).get("full_operational_coverage", False) for r in rows
            ),
        }
    write_json(
        root / "evaluation-summary.json",
        {
            "splits": summaries,
            "results": results,
            "judge_wall_clock_seconds": time.monotonic() - started,
            "reported_judge_cost_usd": sum(r.get("reported_cost_usd", 0) for r in results),
            "meaning": "Development, holdout and previously exposed holdout reported separately; historical coverage is model-assisted, not ground-truth accuracy.",
        },
    )
    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--episodes", type=Path, nargs="+", required=True)
    parser.add_argument("--env-file", type=Path)
    asyncio.run(evaluate(parser.parse_args()))


if __name__ == "__main__":
    main()
