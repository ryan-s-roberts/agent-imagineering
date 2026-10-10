"""Judge-only replay over immutable predictions, using enum-selected citations."""

import argparse
import asyncio
import hashlib
import json
import shutil
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .citation_catalog import SelectedJudgment, build_catalog, materialize, selection_schema
from .cli import write_json
from .decision_replay import digest, structured_call
from .soft_experiment import citation_checks, judge_payload, request


class SelectionValidator:
    def __init__(self, catalog):
        self.catalog = catalog

    def model_validate(self, data):
        result = SelectedJudgment.model_validate(data)
        try:
            materialize(result.model_dump(), self.catalog)
        except KeyError as error:
            raise ValueError(f"Select only allowed citation span IDs: {error}") from error
        return result


def prepare(args):
    source, root = args.source.resolve(), args.output
    root.mkdir(parents=True, exist_ok=False)
    for name in ["manifest.json", "tbox.json", "response-schema.json", "target-review.json"]:
        shutil.copy2(source / name, root / name)
    for name in ["evidence", "targets", "prompts"]:
        shutil.copytree(source / name, root / name)
    original = json.loads((source / "experiment.json").read_text())
    write_json(root / "inherited-experiment.json", original)
    config = dict(original)
    config.update(
        {
            "version": "soft-experiment-judge-v2",
            "mode": "judge_only",
            "inherited_experiment_root": str(source),
            "inherited_experiment_sha256": digest(original),
            "judge_version": "soft-judge-v2",
            "hypothesis": "Selecting immutable host spans eliminates invalid literal citations while keeping semantic relevance separately reviewable.",
            "factor": "Judge citation interface only; all80 predictions,40evidence packets,targets,Tboxes and decision prompts unchanged.",
            "planned_calls": {"decisions": 0, "judgments": 80, "max_interface_repair_calls": 80},
            "stop_rule": "Judge-only replay of all80 frozen predictions; no decision/extraction calls or prompt changes.",
            "success_interpretation": "Zero invalid materialized citations; evaluate relevance and predictability stability separately, not as a new decision-performance headline.",
        }
    )
    judge_prompt = Path("experiments/prompts/soft-judge-v2.txt").read_text()
    (root / "judge-prompt.txt").write_text(judge_prompt)
    config["judge_prompt_sha256"] = hashlib.sha256(judge_prompt.encode()).hexdigest()
    config["judge_schema_sha256"] = digest(SelectedJudgment.model_json_schema())
    write_json(root / "judge-schema.json", SelectedJudgment.model_json_schema())
    index = json.loads((source / "corpus-index.json").read_text())
    index["version"] = "soft-experiment-judge-v2"
    for entry in index["entries"]:
        packet = json.loads((root / "evidence" / f"{entry['id']}.json").read_text())
        target = json.loads((root / "targets" / f"{entry['id']}.json").read_text())
        for state in entry["arms"].values():
            old, new = source / state["path"], root / state["path"]
            new.mkdir(parents=True)
            for file in old.glob("decisions*"):
                shutil.copy2(file, new / file.name)
            shutil.copy2(old / "mechanical.json", new / "mechanical.json")
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
            for name in ["rejudge_spans.py", "citation_catalog.py", "citation_triage.py"]
        },
    )
    shutil.copy2("annotations/judge-citation-triage-v1.json", root / "citation-triage.json")


async def run(args):
    root = args.output
    config = json.loads((root / "experiment.json").read_text())
    index = json.loads((root / "corpus-index.json").read_text())
    tbox = json.loads((root / "tbox.json").read_text())
    prompt = (root / "judge-prompt.txt").read_text()
    assert digest(tbox) == config["tboxes"]["sha256"]
    assert hashlib.sha256(prompt.encode()).hexdigest() == config["judge_prompt_sha256"]
    assert digest(SelectedJudgment.model_json_schema()) == config["judge_schema_sha256"]
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
                    payload, prompt, selection_schema(catalog), config["model"], 6000, "judgment"
                )
                async with asyncio.timeout(240):
                    selected = await structured_call(
                        client, key, body, SelectionValidator(catalog), folder, "judge", usage
                    )
                write_json(folder / "judge-selections.json", selected.model_dump())
                judgment, spans = materialize(selected.model_dump(), catalog)
                write_json(folder / "judge-spans.json", spans)
                write_json(folder / "judge.json", judgment)
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
                    )["usage_by_stage"]["decisions"],
                }
            )
            write_json(folder / "result.json", result)
            state.update({"status": result["status"], "cost_usd": result["cost_usd"]})
            write_json(root / "corpus-index.json", index)
            print(
                f"{arm} {entry['id']}: {result['status']} (${result['cost_usd']:.5f})", flush=True
            )
            return result

    async with httpx.AsyncClient(timeout=150) as client:
        results = await asyncio.gather(
            *[one(e, a, client) for e in index["entries"] for a in e["arms"]]
        )
    write_json(
        root / "summary.json",
        {
            "results": results,
            "completed": sum(r["status"] == "completed" for r in results),
            "cost_usd": sum(r["cost_usd"] for r in results),
            "meaning": "Judge-only citation-interface replay; predictions unchanged",
        },
    )
    from .finalization import finalize_run

    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "run"])
    parser.add_argument("--source", type=Path, default=Path("runs/decision-soft-v1"))
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, default=Path("/Users/ryan/code/plasm/.env"))
    args = parser.parse_args()
    prepare(args) if args.mode == "prepare" else asyncio.run(run(args))


if __name__ == "__main__":
    main()
