"""Episode action-set rescoring of immutable historical predictions."""

import argparse
import asyncio
import hashlib
import json
import shutil
import time
from copy import deepcopy
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
from .soft_experiment import citation_checks, judge_payload, request


def episode_target(episode):
    # Judge sees included action excerpts only. Full audited tail stays root evaluation artifact.
    projected = deepcopy(episode)
    projected.pop("source_tail", None)
    projected["boundary"].pop("citations", None)
    metadata = {e["event_id"]: e for e in episode["source_tail"]}
    excerpts, seen = [], set()
    for action in episode["actions"]:
        for citation in action["source_citations"]:
            identity = (citation["event_id"], citation["quote"])
            if identity in seen:
                continue
            seen.add(identity)
            event = metadata[citation["event_id"]]
            excerpts.append(
                f"Event {event['event_id']} | included action excerpt | {event['timestamp']} | From: {event['sender']} | To: {event['recipient']}\n{citation['quote']}"
            )
    return {
        "version": "episode-target-v1",
        "visibility": "evaluation_only",
        "episode": projected,
        "necessary_order": [
            {"id": f"order{i + 1:03}", **o} for i, o in enumerate(episode["partial_order"])
        ],
        "source": {"id": f"episode:{episode['checkpoint_id']}", "text": "\n\n".join(excerpts)},
        "annotation_sha256": digest(episode),
        "projection": "Included action citations only; source_tail and boundary citations omitted. Full annotations retained separately.",
    }


def prepare(args):
    source, root = args.source.resolve(), args.output
    root.mkdir(parents=True, exist_ok=False)
    for name in ["manifest.json", "tbox.json", "response-schema.json", "target-review.json"]:
        shutil.copy2(source / name, root / name)
    for name in ["evidence", "prompts"]:
        shutil.copytree(source / name, root / name)
    (root / "targets").mkdir()
    episode_document = json.loads(args.episodes.read_text())
    episodes = {e["checkpoint_id"]: e for e in episode_document["episodes"]}
    assert len(episodes) == 40 and {e["case_id"] for e in episodes.values()} == {
        f"{i:03}" for i in range(1, 41)
    }
    shutil.copy2(args.episodes, root / "episode-annotations.json")
    shutil.copy2("docs/decision-episode-contract.md", root / "episode-annotation-guide.md")
    original = json.loads((source / "experiment.json").read_text())
    write_json(root / "inherited-experiment.json", original)
    config = dict(original)
    config.update(
        {
            "version": "episode-experiment-v1",
            "mode": "judge_only",
            "inherited_experiment_root": str(source),
            "inherited_experiment_sha256": digest(original),
            "judge_version": "episode-judge-v1",
            "hypothesis": "Correct the target unit from one event to agency decision episode; evaluate many-to-many material action coverage separately from support and predictability.",
            "factor": "Target unit and judgment rubric changed; all80 predictions,40evidence packets,Tboxes and decision prompts unchanged. No agent improvement claim.",
            "planned_calls": {"decisions": 0, "judgments": 80, "max_interface_repair_calls": 80},
            "stop_rule": "Judge-only replay of all80 frozen predictions; no decision/extraction calls or prompt changes.",
            "success_interpretation": "Per-action typed mappings and deterministic counts; historical correspondence is not normative choice quality. Boundary-uncertain units reported separately.",
        }
    )
    judge_prompt = Path("experiments/prompts/episode-judge-v1.txt").read_text()
    (root / "judge-prompt.txt").write_text(judge_prompt)
    config["judge_prompt_sha256"] = hashlib.sha256(judge_prompt.encode()).hexdigest()
    config["judge_schema_sha256"] = digest(EpisodeJudgment.model_json_schema())
    write_json(root / "judge-schema.json", EpisodeJudgment.model_json_schema())
    index = json.loads((source / "corpus-index.json").read_text())
    index["version"] = "episode-experiment-v1"
    for entry in index["entries"]:
        packet = json.loads((root / "evidence" / f"{entry['id']}.json").read_text())
        target = episode_target(episodes[entry["id"]])
        write_json(root / "targets" / f"{entry['id']}.json", target)
        entry["target_sha256"] = digest(target)
        for state in entry["arms"].values():
            old, new = source / state["path"], root / state["path"]
            new.mkdir(parents=True)
            for file in old.glob("decisions*"):
                shutil.copy2(file, new / file.name)
            shutil.copy2(old / "judge.json", new / "inherited-judge.json")
            shutil.copy2(old / "judge-validation.json", new / "inherited-judge-validation.json")
            inherited = json.loads((old / "result.json").read_text())
            write_json(new / "inherited-result.json", inherited)
            prediction = json.loads((new / "decisions.json").read_text())
            state.update(
                {"status": "pending", "cost_usd": 0, "frozen_prediction_sha256": digest(prediction)}
            )
            write_json(new / "citation-catalog.json", build_catalog(packet, target, prediction))
    write_json(root / "experiment.json", config)
    write_json(root / "corpus-index.json", index)
    write_json(
        root / "judge-implementation-snapshot.json",
        {
            name: {
                "source": (Path(__file__).parent / name).read_text(),
                "sha256": hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest(),
            }
            for name in [
                "episode_rejudge.py",
                "episode_judge.py",
                "episode_metrics.py",
                "citation_catalog.py",
            ]
        },
    )
    config["settings"]["concurrency"] = 24
    config["settings"]["judge_max_tokens"] = 10000
    write_json(root / "experiment.json", config)


async def run(args):
    root = args.output
    config = json.loads((root / "experiment.json").read_text())
    index = json.loads((root / "corpus-index.json").read_text())
    tbox = json.loads((root / "tbox.json").read_text())
    prompt = (root / "judge-prompt.txt").read_text()
    assert digest(tbox) == config["tboxes"]["sha256"]
    assert hashlib.sha256(prompt.encode()).hexdigest() == config["judge_prompt_sha256"]
    assert digest(EpisodeJudgment.model_json_schema()) == config["judge_schema_sha256"]
    key = dotenv_values(args.env_file)["OPENROUTER_API_KEY"]
    semaphore = asyncio.Semaphore(24)

    async def one(entry, arm, client):
        async with semaphore:
            state = entry["arms"][arm]
            folder = root / state["path"]
            if state["status"] == "completed":
                return json.loads((folder / "result.json").read_text())
            usage = {}
            started = time.monotonic()
            result = {"id": entry["id"], "arm": arm, "status": "running", "mode": "judge_only"}
            try:
                packet = json.loads((root / "evidence" / f"{entry['id']}.json").read_text())
                target = json.loads((root / "targets" / f"{entry['id']}.json").read_text())
                prediction = json.loads((folder / "decisions.json").read_text())
                assert (
                    digest(packet) == entry["evidence_sha256"]
                    and digest(target) == entry["target_sha256"]
                )
                assert digest(prediction) == state["frozen_prediction_sha256"]
                catalog = json.loads((folder / "citation-catalog.json").read_text())
                assert catalog == build_catalog(packet, target, prediction)
                payload = judge_payload(packet, tbox, target, prediction)
                payload["citation_catalog"] = catalog["spans"]
                body = request(
                    payload,
                    prompt,
                    constrained_schema(catalog, target, prediction),
                    config["model"],
                    10000,
                    "judgment",
                )
                async with asyncio.timeout(240):
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
                write_json(folder / "judge-spans.json", spans)
                write_json(folder / "judge.json", judgment)
                write_json(
                    folder / "episode-metrics.json", alignment_metrics(target, prediction, judgment)
                )
                checks = citation_checks(judgment, packet, target, prediction)
                checks["construction"] = (
                    "Selected immutable IDs; host-derived namespace,quote,occurrence and offsets"
                )
                write_json(folder / "judge-validation.json", checks)
                assert not checks["invalid_citations"]
                result.update(
                    {
                        "status": "completed",
                        "evidence_sha256": digest(packet),
                        "prediction_sha256": digest(prediction),
                        "tbox_sha256": digest(tbox),
                        "catalog_sha256": digest(catalog),
                        "judge_request_sha256": digest(body),
                        "decision_request_sha256": digest(
                            json.loads((folder / "decisions-request.json").read_text())
                        ),
                    }
                )
            except (
                ValueError,
                TypeError,
                KeyError,
                IndexError,
                TimeoutError,
                httpx.HTTPError,
                AssertionError,
            ) as error:
                result.update(
                    {"status": "failure", "error_type": type(error).__name__, "error": str(error)}
                )
            result.update(
                {
                    "usage_by_stage": usage,
                    "timings": {"judge_seconds": time.monotonic() - started},
                    "latency_seconds": time.monotonic() - started,
                    "cost_usd": sum(u.get("cost", 0) or 0 for u in usage.values()),
                    "inherited_decision_usage": json.loads(
                        (folder / "inherited-result.json").read_text()
                    ).get("inherited_decision_usage", {}),
                }
            )
            write_json(folder / "result.json", result)
            state.update({"status": result["status"], "cost_usd": result["cost_usd"]})
            write_json(root / "corpus-index.json", index)
            print(
                f"{arm} {entry['id']}: {result['status']} (${result['cost_usd']:.5f})", flush=True
            )
            return result

    run_started = time.monotonic()
    async with httpx.AsyncClient(timeout=150) as client:
        results = await asyncio.gather(
            *[one(e, a, client) for e in index["entries"] for a in e["arms"]]
        )
    write_json(
        root / "summary.json",
        {
            "results": results,
            "wall_clock_seconds": time.monotonic() - run_started,
            "wall_clock_scope": "all judge jobs including queue, retries and local serialization",
            "completed": sum(r["status"] == "completed" for r in results),
            "cost_usd": sum(r["cost_usd"] for r in results),
            "meaning": "Episode target/action-set judgment correction; predictions unchanged",
        },
    )

    # Persist judged outputs first; packaging never causes model stages to be repeated.
    from .finalization import finalize_run

    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "run"])
    parser.add_argument("--source", type=Path, default=Path("runs/decision-soft-judge-v2"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, default=Path("/Users/ryan/code/plasm/.env"))
    parser.add_argument(
        "--episodes", type=Path, default=Path("annotations/decision-episodes-v1.json")
    )
    args = parser.parse_args()
    prepare(args) if args.mode == "prepare" else asyncio.run(run(args))


if __name__ == "__main__":
    main()
