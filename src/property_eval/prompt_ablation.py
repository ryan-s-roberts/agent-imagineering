"""Frozen decision-prompt arms over unchanged development evidence."""

import argparse
import asyncio
import copy
import json
import os
import random
import shutil
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .citation_catalog import build_catalog
from .cli import write_json
from .decision_alignment import align_decision
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
from .model_view import ModelView
from .response import DecisionResponse, validate_response
from .run_artifact import validate_artifact
from .soft_experiment import citation_checks, judge_payload, request

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARMS = ("control", "coverage", "uncertainty", "combined")


def prepare(args):
    spec = json.loads(args.spec.read_text()) if args.spec else None
    arms = tuple(spec["arms"]) if spec else ARMS
    baseline = args.baseline.resolve()
    document = json.loads((baseline / "run.json").read_text())
    if validate_artifact(document):
        raise ValueError("Baseline artifact failed integrity checks")
    manifest = json.loads((baseline / "manifest.json").read_text())
    manifest["jobs"] = [j for j in manifest["jobs"] if j.get("split") == "development"]
    if not manifest["jobs"] or any(int(j["case"]) > 40 for j in manifest["jobs"]):
        raise ValueError("Ablation requires public development checkpoints only")
    if not spec and {j["case"] for j in manifest["jobs"]} != {f"{i:03}" for i in range(1, 41)}:
        raise ValueError("Ablation requires exactly the existing 40 development checkpoints")
    root = args.output
    root.mkdir(parents=True, exist_ok=False)
    shutil.copy2(baseline / "run.json", root / "baseline-run.json")
    for folder in ("evidence", "targets", "prompts", "inputs"):
        (root / folder).mkdir()
    tbox = json.loads((baseline / "tbox.json").read_text())
    annotations = json.loads(
        (args.episodes or PROJECT_ROOT / "annotations/decision-episodes-v1.json").read_text()
    )
    episodes = {e["checkpoint_id"]: e for e in annotations["episodes"]}
    write_json(root / "manifest.json", manifest)
    write_json(root / "tbox.json", tbox)
    write_json(root / "response-schema.json", DecisionResponse.model_json_schema())
    write_json(root / "judge-schema.json", EpisodeJudgment.model_json_schema())
    write_json(root / "episode-annotations.json", annotations)
    shutil.copy2(
        PROJECT_ROOT / "docs/decision-episode-contract.md", root / "episode-annotation-guide.md"
    )
    shutil.copy2(
        PROJECT_ROOT / "experiments/prompts/episode-judge-v1.txt", root / "judge-prompt.txt"
    )
    prompts = {}
    for arm in arms:
        prompt = (
            (baseline / "decision-prompt.txt").read_text()
            if spec and arm == "control"
            else (
                PROJECT_ROOT
                / (spec["arms"][arm] if spec else f"experiments/prompts/actionset-v1-{arm}.txt")
            ).read_text()
        )
        (root / "prompts" / f"{arm}.txt").write_text(prompt)
        prompts[arm] = {
            "sha256": digest(prompt),
            "coverage": arm in {"coverage", "combined"},
            "uncertainty": arm in {"uncertainty", "combined"},
        }
    if (root / "prompts/control.txt").read_text() != (baseline / "decision-prompt.txt").read_text():
        raise ValueError("Contemporaneous control must use the exact original prompt")
    config = {
        "version": spec["version"] if spec else "actionset-ablation-v1",
        "mode": "prompt_ablation",
        "baseline_root": str(baseline),
        "baseline_artifact_path": str((root / "baseline-run.json").resolve()),
        "baseline_sha256": document["content_sha256"],
        "model": "openai/gpt-6-luna",
        "judge_version": "episode-judge-v1",
        "arms": prompts,
        "protocol": (
            PROJECT_ROOT / (spec["protocol"] if spec else "experiments/actionset-ablation-v1.md")
        ).read_text(),
        "reference_repair": bool(spec and spec.get("reference_repair")),
        "settings": {"concurrency": 24, "judge_max_tokens": 10000, "schedule_seed": 42},
        "tboxes": {"sha256": digest(tbox)},
        "extraction_calls": 0,
    }
    entries = []
    for job in manifest["jobs"]:
        prior = baseline / job["id"]
        packet = json.loads((prior / "evidence-packet.json").read_text())
        target = episode_target(episodes[job["id"]])
        write_json(root / "evidence" / f"{job['id']}.json", packet)
        write_json(root / "targets" / f"{job['id']}.json", target)
        inputs = root / "inputs" / job["id"]
        inputs.mkdir()
        for name in (
            "decisions-canonical-request.json",
            "decisions-request.json",
            "decisions-aliases.json",
        ):
            shutil.copy2(prior / name, inputs / name)
        entries.append(
            {
                **job,
                "evidence_sha256": digest(packet),
                "target_sha256": digest(target),
                "arms": {a: {"path": f"arms/{a}/{job['id']}", "status": "pending"} for a in arms},
            }
        )
    write_json(root / "experiment.json", config)
    write_json(root / "corpus-index.json", {"entries": entries, "holdout": "excluded"})
    write_json(
        root / "implementation-snapshot.json",
        {
            name: {
                "source": (Path(__file__).parent / name).read_text(),
                "sha256": digest((Path(__file__).parent / name).read_text()),
            }
            for name in (
                "prompt_ablation.py",
                "decision_replay.py",
                "decision_alignment.py",
                "model_view.py",
                "response.py",
                "decision_repair.py",
                "episode_judge.py",
                "episode_metrics.py",
            )
        },
    )


async def run(args):
    root = args.output
    config = json.loads((root / "experiment.json").read_text())
    index = json.loads((root / "corpus-index.json").read_text())
    tbox = json.loads((root / "tbox.json").read_text())
    prompt = (root / "judge-prompt.txt").read_text()
    key = (
        dotenv_values(args.env_file).get("OPENROUTER_API_KEY")
        if args.env_file
        else os.getenv("OPENROUTER_API_KEY")
    )
    if not key:
        raise ValueError("Provide OPENROUTER_API_KEY or --env-file")
    if digest(tbox) != config["tboxes"]["sha256"]:
        raise ValueError("Tbox changed after freeze")
    if not args.resume_assessments and any(
        (root / state["path"]).exists() for e in index["entries"] for state in e["arms"].values()
    ):
        raise ValueError("Arm output already exists; refuse semantic rerun")
    semaphore = asyncio.Semaphore(24)

    async def one(entry, arm, client):
        folder = root / entry["arms"][arm]["path"]
        prior = (
            json.loads((folder / "result.json").read_text()) if args.resume_assessments else None
        )
        if prior and (
            prior["status"] == "completed" or "402 Payment Required" not in prior.get("error", "")
        ):
            return prior
        folder.mkdir(parents=True, exist_ok=args.resume_assessments)
        if prior:
            write_json(folder / "result-before-assessment-resume.json", prior)
        usage, timings, started = (
            (dict(prior.get("usage_by_stage", {})) if prior else {}),
            {},
            time.monotonic(),
        )
        result = {"id": entry["id"], "arm": arm, "status": "running"}
        try:
            packet = json.loads((root / "evidence" / f"{entry['id']}.json").read_text())
            target = json.loads((root / "targets" / f"{entry['id']}.json").read_text())
            if (
                digest(packet) != entry["evidence_sha256"]
                or digest(target) != entry["target_sha256"]
            ):
                raise ValueError("Frozen evidence or target changed")
            if not args.resume_assessments:
                body = json.loads(
                    (root / "inputs" / entry["id"] / "decisions-canonical-request.json").read_text()
                )
                arm_prompt = (root / "prompts" / f"{arm}.txt").read_text()
                if digest(arm_prompt) != config["arms"][arm]["sha256"]:
                    raise ValueError("Arm prompt changed")
                control = copy.deepcopy(body)
                body["messages"][0]["content"] = arm_prompt
                control["messages"][0]["content"] = arm_prompt
                if control != body:
                    raise ValueError("Only system prompt may change")
                alias = json.loads(
                    (root / "inputs" / entry["id"] / "decisions-aliases.json").read_text()
                )
                view = ModelView(packet["sources"], version=alias["version"])
                view.maps = alias["maps"]
                write_json(folder / "sources.json", {"sources": packet["sources"]})
                before = time.monotonic()
                async with asyncio.timeout(600):
                    raw = await structured_call(
                        client,
                        key,
                        body,
                        DecisionResponse,
                        folder,
                        "decisions",
                        usage,
                        model_view=view,
                        request_semaphore=semaphore,
                    )
                timings["decision_seconds"] = time.monotonic() - before
                aligned = align_decision(raw.model_dump(), packet["sources"])
                write_json(folder / "decisions-raw-parsed.json", raw.model_dump())
                write_json(folder / "decisions-canonicalization.json", aligned)
                prediction = DecisionResponse.model_validate(aligned["response"])
                write_json(folder / "decisions.json", prediction.model_dump())
                write_json(
                    folder / "decisions-validation.json", validate_response(prediction, packet)
                )
                # Assert actual wire input differs solely in its system prompt too.
                wire = json.loads((folder / "decisions-request.json").read_text())
                original = json.loads(
                    (root / "inputs" / entry["id"] / "decisions-request.json").read_text()
                )
                original["messages"][0]["content"] = arm_prompt
                if wire != original:
                    raise ValueError("Wire request changed beyond the system prompt")
            else:
                prediction = DecisionResponse.model_validate(
                    json.loads((folder / "decisions.json").read_text())
                )
            if config.get("reference_repair"):
                from .decision_repair import repair_decision

                before = time.monotonic()
                await repair_decision(
                    folder,
                    packet,
                    tbox,
                    config["model"],
                    client,
                    key,
                    usage,
                    semaphore,
                    resume_transport=args.resume_assessments,
                )
                timings["reference_repair_seconds"] = time.monotonic() - before
                prediction = DecisionResponse.model_validate(
                    json.loads((folder / "decisions.json").read_text())
                )
            catalog = build_catalog(packet, target, prediction.model_dump())
            write_json(folder / "citation-catalog.json", catalog)
            payload = judge_payload(packet, tbox, target, prediction.model_dump())
            payload["citation_catalog"] = catalog["spans"]
            judge_body = request(
                payload,
                prompt,
                constrained_schema(catalog, target, prediction.model_dump()),
                config["model"],
                10000,
                "judgment",
            )
            old_request = folder / "judge-request.json"
            if (
                args.resume_assessments
                and old_request.exists()
                and json.loads(old_request.read_text()) != judge_body
            ):
                write_json(
                    folder / "interrupted-judge-request.json", json.loads(old_request.read_text())
                )
            before = time.monotonic()
            async with asyncio.timeout(600):
                selected = await structured_call(
                    client,
                    key,
                    judge_body,
                    EpisodeValidator(catalog, target, prediction.model_dump()),
                    folder,
                    "judge",
                    usage,
                    request_semaphore=semaphore,
                )
            timings["judge_seconds"] = time.monotonic() - before
            write_json(folder / "judge-selections.json", selected.model_dump())
            judgment, spans = materialize_episode(selected.model_dump(), catalog)
            write_json(folder / "judge.json", judgment)
            write_json(folder / "judge-spans.json", spans)
            checks = citation_checks(judgment, packet, target, prediction.model_dump())
            if checks["invalid_citations"]:
                raise ValueError("Judge citation alignment failed")
            write_json(folder / "judge-validation.json", checks)
            write_json(
                folder / "episode-metrics.json",
                alignment_metrics(target, prediction.model_dump(), judgment),
            )
            result.update(
                status="completed",
                evidence_sha256=digest(packet),
                prediction_sha256=digest(prediction.model_dump()),
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
            timings=timings,
            latency_seconds=time.monotonic() - started,
            cost_usd=sum(u.get("cost", 0) or 0 for u in usage.values()),
        )
        write_json(folder / "result.json", result)
        entry["arms"][arm]["status"] = result["status"]
        write_json(root / "corpus-index.json", index)
        print(f"{arm} {entry['id']}: {result['status']}", flush=True)
        return result

    jobs = [(entry, arm) for entry in index["entries"] for arm in config["arms"]]
    random.Random(42).shuffle(jobs)
    if args.resume_assessments:
        write_json(
            root / "summary-before-assessment-resume.json",
            json.loads((root / "summary.json").read_text()),
        )
        write_json(
            root / "assessment-resume.json",
            {
                "scope": "Retry payment-interrupted repair/judge calls; no decision generation",
                "implementation": Path(__file__).read_text(),
            },
        )
    started = time.monotonic()
    async with httpx.AsyncClient(timeout=180) as client:
        results = await asyncio.gather(*(one(entry, arm, client) for entry, arm in jobs))
    write_json(
        root / "summary.json",
        {
            "results": results,
            "completed": sum(r["status"] == "completed" for r in results),
            "denominator": len(jobs),
            "wall_clock_seconds": time.monotonic() - started,
            "observed_peak_requests": getattr(semaphore, "observed_peak", 0),
            "cost_usd": sum(r["cost_usd"] for r in results),
            "meaning": "Frozen development-only prompt ablation; no extraction reruns or holdout calls.",
        },
    )
    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "run"])
    parser.add_argument("--baseline", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--env-file", type=Path)
    parser.add_argument("--resume-assessments", action="store_true")
    parser.add_argument("--spec", type=Path, help="Versioned prompt-arm specification")
    parser.add_argument(
        "--episodes", type=Path, help="Frozen agent-action targets for these checkpoints"
    )
    args = parser.parse_args()
    if args.mode == "prepare":
        if not args.baseline:
            parser.error("prepare requires --baseline")
        prepare(args)
    else:
        asyncio.run(run(args))


if __name__ == "__main__":
    main()
