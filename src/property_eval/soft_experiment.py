"""Frozen two-arm development prompt comparison with blinded advisory judging."""

import argparse
import asyncio
import hashlib
import json
import time
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .cli import write_json
from .decision_alignment import align_decision
from .decision_replay import digest, structured_call
from .models import EntityExtraction, LinkExtraction, MentionExtraction, RecordExtraction
from .response import DecisionResponse, validate_response
from .soft_eval import HistoricalTarget, SemanticJudgment, mechanical_comparison


def request(payload, prompt, schema, model, tokens, name):
    return {
        "model": model,
        "seed": 42,
        "max_tokens": tokens,
        "provider": {"require_parameters": True},
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": name, "strict": True, "schema": schema},
        },
    }


def decision_payload(packet, tbox):
    # Explicit whitelist. Targets, suffix, comparison outputs and arm names are absent.
    return {"ontology_tbox": tbox, "prefix_evidence": packet}


def judge_payload(packet, tbox, target, prediction):
    return {
        "ontology_tbox": tbox,
        "prefix_evidence": packet,
        "historical_target": target,
        "prediction": prediction,
        "prediction_source": {
            "id": "prediction",
            "text": json.dumps(prediction, ensure_ascii=False, sort_keys=True),
        },
    }


def citation_checks(judgment, packet, target, prediction):
    sources = {("prefix", s["id"]): s["text"] for s in packet["sources"]}
    sources[("target", target["source"]["id"])] = target["source"]["text"]
    sources[("prediction", "prediction")] = json.dumps(
        prediction, ensure_ascii=False, sort_keys=True
    )
    failures, count = [], 0

    def walk(value):
        nonlocal count
        if isinstance(value, dict):
            if {"origin", "source_id", "expression", "occurrence"} <= value.keys():
                count += 1
                text = sources.get((value["origin"], value["source_id"]))
                if (
                    text is None
                    or not value["expression"]
                    or text.count(value["expression"]) < value["occurrence"]
                ):
                    failures.append(value)
            else:
                for child in value.values():
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(judgment)
    return {
        "citation_count": count,
        "invalid_citations": failures,
        "meaning": "Literal source alignment only, not entailment or judgment correctness",
    }


def prepare(args):
    root = args.output
    root.mkdir(parents=True, exist_ok=False)
    baseline = args.baseline.resolve()
    manifest = json.loads((baseline / "manifest.json").read_text())
    targets = {
        t["id"]: HistoricalTarget.model_validate(t).model_dump()
        for t in json.loads(args.targets.read_text())["targets"]
    }
    assert len(manifest["jobs"]) == 40 and {j["case"] for j in manifest["jobs"]} == {
        f"{i:03}" for i in range(1, 41)
    }
    tbox = {
        "version": "property-tbox-v1",
        "evidence_ontology_version": "property-evidence-v4",
        "response_ontology_version": DecisionResponse.model_json_schema()["properties"][
            "ontology_version"
        ]["const"],
        "semantics": Path("docs/ontology-semantics-v1.md").read_text(),
        "evidence": {
            m.__name__: m.model_json_schema()
            for m in (MentionExtraction, LinkExtraction, EntityExtraction, RecordExtraction)
        },
        "result": DecisionResponse.model_json_schema(),
    }
    base = Path("experiments/prompts/decision-baseline-v1.txt").read_text()
    common = "\nThe input explicitly supplies both ontology T-boxes: evidence definitions and result action definitions, with shared interpretation rules. Use them to interpret the prefix and express the proposal.\n"
    control = base + common
    progress = (
        control
        + "\nAssess each uncertainty by whether it blocks the next useful workflow step. Advance a supported, reversible communication or request when its material prerequisites are established. Reserve extra clarification or human escalation for uncertainty that changes that next step, and explain the specific blocking consequence. Keep unresolved bookkeeping or nonessential detail explicit without automatically converting it into an operational blocker. Preserve all authority, evidence and execution distinctions.\n"
    )
    prompts = {"control": control, "progress": progress}
    write_json(root / "manifest.json", manifest)
    write_json(root / "tbox.json", tbox)
    write_json(root / "response-schema.json", DecisionResponse.model_json_schema())
    write_json(root / "judge-schema.json", SemanticJudgment.model_json_schema())
    write_json(
        root / "target-review.json",
        json.loads(Path("annotations/historical-target-review-v1.json").read_text()),
    )
    judge = Path("experiments/prompts/soft-judge-v1.txt").read_text()
    (root / "judge-prompt.txt").write_text(judge)
    (root / "targets").mkdir()
    (root / "evidence").mkdir()
    (root / "prompts").mkdir()
    entries = []
    for job in manifest["jobs"]:
        packet = json.loads((baseline / job["id"] / "evidence-packet.json").read_text())
        prior = json.loads((baseline / job["id"] / "decision-review.json").read_text())
        assert (
            digest(packet) == prior["evidence_sha256"]
            and packet["prefix_sha256"] == job["prefix_sha256"]
        )
        write_json(root / "evidence" / f"{job['id']}.json", packet)
        write_json(root / "targets" / f"{job['id']}.json", targets[job["id"]])
        entries.append(
            {
                "id": job["id"],
                "case": job["case"],
                "baseline_path": str(baseline / job["id"]),
                "evidence_sha256": digest(packet),
                "target_sha256": digest(targets[job["id"]]),
                "arms": {
                    a: {"path": f"arms/{a}/{job['id']}", "status": "pending"} for a in prompts
                },
            }
        )
    for arm, prompt in prompts.items():
        (root / "prompts" / f"{arm}.txt").write_text(prompt)
    experiment = {
        "version": "soft-experiment-v1",
        "baseline_root": str(baseline),
        "model": "openai/gpt-6-luna",
        "hypothesis": "A general instruction to distinguish blocking from nonblocking uncertainty reduces unnecessary clarification/escalation and improves historical workflow correspondence without reducing evidence support.",
        "factor": "One workflow-progress paragraph; common Tboxes/evidence/model/schema/judge/settings fixed",
        "scope": "Exploratory development only001–040; previously inspected. No held-out generalization claim.",
        "interface_change": "Prior baseline already supplied response JSON schema; new common interface additionally supplies evidence schemas and explicit semantics for both ontologies. Prior-v1 differences are not pure prompt effects.",
        "arms": [
            {
                "id": a,
                "prompt_path": f"prompts/{a}.txt",
                "prompt_sha256": hashlib.sha256(p.encode()).hexdigest(),
            }
            for a, p in prompts.items()
        ],
        "tboxes": {"combined": "tbox.json", "sha256": digest(tbox)},
        "response_schema_sha256": digest(DecisionResponse.model_json_schema()),
        "judge_schema_sha256": digest(SemanticJudgment.model_json_schema()),
        "judge_prompt_sha256": hashlib.sha256(judge.encode()).hexdigest(),
        "settings": {
            "seed": 42,
            "temperature": "unsupported/omitted",
            "reasoning_effort": "provider_default/unchanged",
            "decision_max_tokens": 8000,
            "judge_max_tokens": 6000,
            "concurrency": 24,
            "timeout_seconds": 240,
        },
        "stop_rule": "Exactly two decision arms,40cases each,one blinded judge each. At most one syntax repair per response; no prompt/judge tuning after results.",
        "success_interpretation": "Report paired categorical correspondence and support changes plus predictability strata. No aggregate correctness score, no confirmatory success threshold on these exposed development cases.",
        "planned_calls": {"decisions": 80, "judgments": 80, "max_interface_repair_calls": 160},
        "pricing_snapshot": {
            "prompt_usd_per_token": 0.0000001,
            "completion_usd_per_token": 0.0000005,
            "source": "https://openrouter.ai/api/v1/models",
            "cost_estimate_usd": "1–2 expected;8 planning ceiling incl bounded repairs; no provider billing cap",
        },
    }
    write_json(root / "experiment.json", experiment)
    write_json(
        root / "corpus-index.json",
        {"version": "soft-experiment-v1", "denominator": 40, "entries": entries},
    )
    write_json(
        root / "implementation-snapshot.json",
        {
            name: {
                "source": (Path(__file__).parent / name).read_text(),
                "sha256": hashlib.sha256((Path(__file__).parent / name).read_bytes()).hexdigest(),
            }
            for name in [
                "soft_experiment.py",
                "soft_eval.py",
                "decision_replay.py",
                "response.py",
                "models.py",
                "client.py",
                "canonicalization.py",
                "decision_alignment.py",
            ]
        },
    )
    print(
        json.dumps(
            {
                "prepared": str(root),
                "calls": experiment["planned_calls"],
                "tbox_sha256": digest(tbox),
            }
        )
    )


async def execute(args):
    root = args.output
    config = json.loads((root / "experiment.json").read_text())
    index = json.loads((root / "corpus-index.json").read_text())
    tbox = json.loads((root / "tbox.json").read_text())
    assert digest(tbox) == config["tboxes"]["sha256"]
    assert digest(DecisionResponse.model_json_schema()) == config["response_schema_sha256"]
    assert digest(SemanticJudgment.model_json_schema()) == config["judge_schema_sha256"]
    judge_prompt = (root / "judge-prompt.txt").read_text()
    assert hashlib.sha256(judge_prompt.encode()).hexdigest() == config["judge_prompt_sha256"]
    prompts = {a["id"]: (root / a["prompt_path"]).read_text() for a in config["arms"]}
    assert all(
        hashlib.sha256(prompts[a["id"]].encode()).hexdigest() == a["prompt_sha256"]
        for a in config["arms"]
    )
    key = dotenv_values(args.env_file)["OPENROUTER_API_KEY"]
    semaphore = asyncio.Semaphore(config["settings"]["concurrency"])

    async def one(entry, arm, client):
        async with semaphore:
            state = entry["arms"][arm]
            folder = root / state["path"]
            folder.mkdir(parents=True, exist_ok=True)
            if state["status"] == "completed":
                return json.loads((folder / "result.json").read_text())
            usage, timings = {}, {}
            started = time.monotonic()
            result = {"id": entry["id"], "arm": arm, "status": "running"}
            try:
                packet = json.loads((root / "evidence" / f"{entry['id']}.json").read_text())
                target = json.loads((root / "targets" / f"{entry['id']}.json").read_text())
                assert (
                    digest(packet) == entry["evidence_sha256"]
                    and digest(target) == entry["target_sha256"]
                )
                async with asyncio.timeout(config["settings"]["timeout_seconds"]):
                    decision = request(
                        decision_payload(packet, tbox),
                        prompts[arm],
                        DecisionResponse.model_json_schema(),
                        config["model"],
                        8000,
                        "decision",
                    )
                    before = time.monotonic()
                    predicted = await structured_call(
                        client, key, decision, DecisionResponse, folder, "decisions", usage
                    )
                    timings["decision_seconds"] = time.monotonic() - before
                    write_json(folder / "decisions-raw-parsed.json", predicted.model_dump())
                    aligned = align_decision(predicted.model_dump(), packet["sources"])
                    write_json(folder / "decisions-canonicalization.json", aligned)
                    prediction = DecisionResponse.model_validate(aligned["response"])
                    write_json(folder / "decisions.json", prediction.model_dump())
                    write_json(
                        folder / "decisions-validation.json", validate_response(prediction, packet)
                    )
                    write_json(
                        folder / "mechanical.json",
                        mechanical_comparison(prediction.model_dump(), target),
                    )
                    body = request(
                        judge_payload(packet, tbox, target, prediction.model_dump()),
                        judge_prompt,
                        SemanticJudgment.model_json_schema(),
                        config["model"],
                        6000,
                        "judgment",
                    )
                    before = time.monotonic()
                    judgment = await structured_call(
                        client, key, body, SemanticJudgment, folder, "judge", usage
                    )
                    timings["judge_seconds"] = time.monotonic() - before
                    write_json(folder / "judge.json", judgment.model_dump())
                    write_json(
                        folder / "judge-validation.json",
                        citation_checks(
                            judgment.model_dump(), packet, target, prediction.model_dump()
                        ),
                    )
                    result.update(
                        {
                            "status": "completed",
                            "evidence_sha256": digest(packet),
                            "tbox_sha256": digest(tbox),
                            "prediction_sha256": digest(prediction.model_dump()),
                            "decision_request_sha256": digest(decision),
                            "judge_request_sha256": digest(body),
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
                    "timings": timings,
                    "latency_seconds": time.monotonic() - started,
                    "cost_usd": sum(u.get("cost", 0) or 0 for u in usage.values()),
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
            *[one(e, a, client) for e in index["entries"] for a in prompts]
        )
    write_json(
        root / "summary.json",
        {
            "results": results,
            "completed": sum(r["status"] == "completed" for r in results),
            "cost_usd": sum(r["cost_usd"] for r in results),
            "meaning": "Model-assisted development judgments; no deterministic semantic truth",
        },
    )
    from .finalization import finalize_run

    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "run"])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, default=Path("runs/decision-dev-v1"))
    parser.add_argument(
        "--targets", type=Path, default=Path("annotations/historical-targets-v1.json")
    )
    parser.add_argument("--env-file", type=Path, default=Path("/Users/ryan/code/plasm/.env"))
    args = parser.parse_args()
    prepare(args) if args.mode == "prepare" else asyncio.run(execute(args))


if __name__ == "__main__":
    main()
