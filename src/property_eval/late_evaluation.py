"""Adapt frozen agent-only targets and assess evidence warrant separately from history."""

import argparse
import asyncio
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

import httpx
from dotenv import dotenv_values

from .citation_catalog import build_catalog
from .cli import write_json
from .decision_replay import digest, structured_call
from .evidence_response_judge import (
    EvidenceResponseJudgment,
    evidence_response_payload,
    validate_judgment,
)
from .finalization import finalize_run
from .prefix import HEADER, load_prefix
from .soft_experiment import request

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def prepare_targets(args):
    for source_name, saved_name in (
        ("experiments/prompts/evidence-response-v1.txt", "evidence-response-prompt.txt"),
        ("docs/evidence-response-rubric-v1.md", "evidence-response-rubric.md"),
        ("experiments/prompts/episode-judge-v1.txt", "judge-prompt.txt"),
    ):
        (args.run / saved_name).write_text((PROJECT_ROOT / source_name).read_text())
    targets = json.loads(args.targets.read_text())["checkpoints"]
    manifest = json.loads((args.run / "manifest.json").read_text())
    if {t["checkpoint_id"] for t in targets} != {j["id"] for j in manifest["jobs"]}:
        raise ValueError("Target set differs from frozen manifest")
    episodes = []
    for target in targets:
        case = target["case"]
        path = args.source / case / "history.md"
        raw = path.read_text()
        headers = list(HEADER.finditer(raw))
        events = load_prefix(args.source, case, len(headers)).events
        actions = []
        for action in target["actions"]:
            citations = []
            for span in action["source_citations"]:
                index = int(span["event_id"]) - 1
                event = events[index]
                if event.text[span["start"] : span["end"]] != span["expression"]:
                    raise ValueError("Frozen target span changed")
                offset = raw.index(event.text, headers[index].end()) + span["start"]
                citations.append(
                    {
                        "event_id": event.id,
                        "source_path": str(path.relative_to(args.source)),
                        "quote": span["expression"],
                        "char_start": offset,
                        "char_end": offset + len(span["expression"]),
                        "line_start": raw.count("\n", 0, offset) + 1,
                        "line_end": raw.count("\n", 0, offset + len(span["expression"])) + 1,
                        "offset_basis": "complete history.md Unicode positions, end exclusive",
                    }
                )
            kind = action["action"]["type"]
            materiality = (
                "auxiliary"
                if kind == "notify"
                else "workflow"
                if kind in {"change_workflow", "await_response", "record_evidence"}
                else "material"
            )
            actions.append(
                {
                    "id": action["id"],
                    "intent": kind,
                    "summary": action["summary"],
                    "materiality": materiality,
                    "source_citations": citations,
                    "observed_action": action["action"],
                    "earliest_knowledge": {
                        "prediction_cutoff": target["cutoff"],
                        "status": "model_audited_prefix_availability",
                    },
                }
            )
        included = sorted({c["event_id"] for a in actions for c in a["source_citations"]})
        episodes.append(
            {
                "checkpoint_id": target["checkpoint_id"],
                "case_id": case,
                "cutoff": target["cutoff"],
                "actions": actions,
                "included_event_ids": included,
                "partial_order": [],
                "boundary": {
                    "event_ids": [],
                    "confidence": "model_audited",
                    "reason": "Only explicit agent action excerpts passing the frozen prefix-availability audit are included; counterparty behavior and information-dependent acts are excluded.",
                    "citations": [],
                },
                "source_tail": [
                    {
                        "event_id": events[int(i) - 1].id,
                        "timestamp": events[int(i) - 1].timestamp,
                        "sender": events[int(i) - 1].sender,
                        "recipient": events[int(i) - 1].recipient,
                    }
                    for i in included
                ],
                "limits": [
                    "Model-assisted targets, not human gold.",
                    "Necessary ordering was not separately annotated; absence of order edges is not proof of independence.",
                    "Historical actions need not be normative or optimal.",
                ],
                "review_status": target["review_status"],
            }
        )
    write_json(
        args.run / "frozen-agent-only-episodes.json",
        {"episodes": episodes, "source_targets_sha256": digest(targets)},
    )
    (args.run / "evaluation-protocol.md").write_text(
        (PROJECT_ROOT / "experiments/late-dev-eval-v1.md").read_text()
    )
    print(json.dumps({"frozen_episodes": len(episodes)}))


class EvidenceValidator:
    def __init__(self, prediction, catalog):
        self.prediction, self.catalog = prediction, catalog

    def model_validate(self, raw):
        return validate_judgment(raw, self.prediction, self.catalog)


async def evidence_evaluate(args):
    root = args.run
    manifest = json.loads((root / "manifest.json").read_text())
    settings = json.loads((root / "run-settings.json").read_text())
    tbox = json.loads((root / "tbox.json").read_text())
    prompt = (root / "evidence-response-prompt.txt").read_text()
    key = dotenv_values(args.env_file).get("OPENROUTER_API_KEY")
    if not key:
        raise ValueError("OPENROUTER_API_KEY missing")
    if (root / "evidence-response-summary.json").exists():
        raise ValueError("Preserve completed assessment")
    (root / "evidence-response-prompt.txt").write_text(prompt)
    write_json(
        root / "evidence-response-settings.json",
        {
            "model": settings["model"],
            "concurrency": 24,
            "max_tokens": 8000,
            "prompt_sha256": digest(prompt),
            "schema": EvidenceResponseJudgment.model_json_schema(),
            "implementation": {
                name: (Path(__file__).parent / name).read_text()
                for name in ("late_evaluation.py", "evidence_response_judge.py")
            },
        },
    )
    sem = asyncio.Semaphore(24)

    async def one(job, client):
        folder = root / job["id"]
        result = {"id": job["id"], "case": job["case"], "status": "unassessed"}
        usage, started = {}, time.monotonic()
        if not (folder / "decisions.json").exists():
            result["reason"] = "Decision unavailable; retained in denominator"
            write_json(folder / "evidence-judge-result.json", result)
            return result
        try:
            packet = json.loads((folder / "evidence-packet.json").read_text())
            prediction = json.loads((folder / "decisions.json").read_text())
            complete = build_catalog(packet, {"source": {"id": "unused", "text": ""}}, prediction)
            catalog = {
                "sources": [s for s in complete["sources"] if s["origin"] == "prefix"],
                "spans": [s for s in complete["spans"] if s["origin"] == "prefix"],
            }
            schema = EvidenceResponseJudgment.model_json_schema()
            schema["$defs"]["PrefixSpanSelection"]["properties"]["span_id"]["enum"] = [
                s["id"] for s in catalog["spans"]
            ]
            ids = [a["id"] for a in prediction["actions"]]
            if ids:
                schema["$defs"]["ActionAssessment"]["properties"]["action_id"]["enum"] = ids
                schema["$defs"]["Obligation"]["properties"]["action_ids"]["items"]["enum"] = ids
            schema["properties"]["actions"].update(minItems=len(ids), maxItems=len(ids))
            body = request(
                evidence_response_payload(packet, tbox, prediction, catalog),
                prompt,
                schema,
                settings["model"],
                8000,
                "evidence_response",
            )
            write_json(folder / "evidence-citation-catalog.json", catalog)
            async with sem:
                async with asyncio.timeout(300):
                    judgment = await structured_call(
                        client,
                        key,
                        body,
                        EvidenceValidator(prediction, catalog),
                        folder,
                        "evidence-judge",
                        usage,
                    )
            write_json(folder / "evidence-response-judgment.json", judgment.model_dump())
            result["status"] = "completed"
            counts = defaultdict(Counter)
            for action in judgment.actions:
                for dimension, value in action.model_dump().items():
                    if dimension != "action_id":
                        counts[dimension][value["verdict"]] += 1
            result["dimensions"] = {k: dict(v) for k, v in counts.items()}
            result["obligations"] = dict(Counter(o.coverage for o in judgment.obligations))
        except (ValueError, KeyError, TypeError, TimeoutError, httpx.HTTPError) as error:
            result.update(status="failure", error=str(error), error_type=type(error).__name__)
        result.update(usage_by_stage=usage, latency_seconds=time.monotonic() - started)
        write_json(folder / "evidence-judge-result.json", result)
        print(f"evidence {job['id']}: {result['status']}", flush=True)
        return result

    started = time.monotonic()
    async with httpx.AsyncClient(timeout=180) as client:
        results = await asyncio.gather(*(one(job, client) for job in manifest["jobs"]))
    counts = defaultdict(Counter)
    for result in results:
        for name, values in result.get("dimensions", {}).items():
            counts[name].update(values)
    write_json(
        root / "evidence-response-summary.json",
        {
            "denominator": len(results),
            "completed": sum(r["status"] == "completed" for r in results),
            "dimensions": {k: dict(v) for k, v in counts.items()},
            "results": results,
            "wall_clock_seconds": time.monotonic() - started,
            "meaning": "Target-free advisory evidence assessment. Counts summarize semantic model labels; unknowns are not passes.",
        },
    )
    finalize_run(root)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare-targets", "evidence"])
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--input-dir", dest="source", type=Path)
    parser.add_argument("--targets", type=Path)
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args()
    prepare_targets(args) if args.mode == "prepare-targets" else asyncio.run(
        evidence_evaluate(args)
    )


if __name__ == "__main__":
    main()
