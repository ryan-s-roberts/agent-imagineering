"""Exploratory model-assisted divergence taxonomy; never rewrites decisions or scores."""

import argparse
import asyncio
import json
import time
from collections import Counter
from pathlib import Path
from typing import Literal

import httpx
from dotenv import dotenv_values

from .cli import write_json
from .decision_replay import structured_call
from .grounding import resolve_span
from .models import StrictModel
from .response import EvidenceRef
from .soft_experiment import request


class TargetReview(StrictModel):
    target_action_id: str
    importance: Literal[
        "operational", "workflow_bookkeeping", "communication", "courtesy", "uncertain"
    ]
    prefix_warrant: Literal[
        "required_now", "reasonable_now", "not_yet_warranted", "not_inferable", "uncertain"
    ]
    effect_coverage: Literal["equivalent", "partial", "absent", "contrary", "unassessable"]
    prediction_action_ids: list[str]
    explanation: str
    evidence: list[EvidenceRef]


class PredictionReview(StrictModel):
    prediction_action_id: str
    progress: Literal[
        "advances",
        "justified_wait",
        "redundant",
        "unnecessary_blocker",
        "unsupported",
        "unassessable",
    ]
    uncertainty_origin: Literal[
        "source_conflict",
        "missing_authority",
        "missing_operational_fact",
        "extraction_fragmentation",
        "representation_limit",
        "none",
        "unclear",
    ]
    explanation: str
    evidence: list[EvidenceRef]


class Difference(StrictModel):
    category: Literal[
        "material_omission",
        "workflow_omission",
        "communication_omission",
        "partial_scope",
        "dependency_difference",
        "extraction_induced_blocker",
        "unnecessary_clarification",
        "unnecessary_escalation",
        "reasonable_alternative",
        "equivalent_effect",
        "target_not_prefix_warranted",
        "boundary_or_annotation_issue",
        "representation_limit",
        "no_material_divergence",
    ]
    target_action_ids: list[str]
    prediction_action_ids: list[str]
    explanation: str
    evidence: list[EvidenceRef]


class DivergenceReview(StrictModel):
    version: Literal["divergence-review-v1"]
    targets: list[TargetReview]
    predictions: list[PredictionReview]
    differences: list[Difference]
    summary: str
    limitations: list[str]


class ReviewValidator:
    def __init__(self, sources, target_ids, prediction_ids, original=None):
        self.sources, self.targets, self.predictions = sources, set(target_ids), set(prediction_ids)
        self.original = original

    def model_validate(self, raw):
        result = DivergenceReview.model_validate(raw)

        def semantics(value):
            if isinstance(value, list):
                return [semantics(v) for v in value]
            if isinstance(value, dict):
                return {
                    k: semantics(v)
                    for k, v in value.items()
                    if k
                    not in {
                        "evidence",
                        "target_action_id",
                        "target_action_ids",
                        "prediction_action_id",
                        "prediction_action_ids",
                    }
                }
            return value

        if self.original is not None and semantics(raw) != semantics(self.original):
            raise ValueError(
                "Reference repair must preserve all labels and explanation text exactly"
            )
        for rows, field, expected in (
            (result.targets, "target_action_id", self.targets),
            (result.predictions, "prediction_action_id", self.predictions),
        ):
            ids = [getattr(r, field) for r in rows]
            if set(ids) != expected or len(ids) != len(expected):
                raise ValueError(f"Assess each {field} exactly once: {sorted(expected)}")
        for row in [*result.targets, *result.predictions, *result.differences]:
            for ref in row.evidence:
                resolve_span(ref, self.sources)
            if not set(getattr(row, "prediction_action_ids", [])) <= self.predictions:
                raise ValueError("Unknown prediction reference")
            if not set(getattr(row, "target_action_ids", [])) <= self.targets:
                raise ValueError("Unknown target reference")
        return result


async def run(args):
    root = args.run
    read = lambda path: json.loads(path.read_text())
    manifest = read(root / "manifest.json")
    if any(j["split"] != "development" for j in manifest["jobs"]):
        raise ValueError("This exploratory rubric review is development-only")
    episodes = {
        e["checkpoint_id"]: e for e in read(root / "frozen-agent-only-episodes.json")["episodes"]
    }
    prompt = (
        Path(__file__).resolve().parents[2] / "experiments/prompts/divergence-review-v1.txt"
    ).read_text()
    if (root / "divergence-review-summary.json").exists() and not args.repair_interfaces:
        raise ValueError("Preserve completed review")
    key = dotenv_values(args.env_file).get("OPENROUTER_API_KEY")
    if not key:
        raise ValueError("Missing OPENROUTER_API_KEY")
    model = read(root / "run-settings.json")["model"]
    write_json(
        root
        / (
            "divergence-interface-repair-settings.json"
            if args.repair_interfaces
            else "divergence-review-settings.json"
        ),
        {
            "prompt": prompt,
            "schema": DivergenceReview.model_json_schema(),
            "model": model,
            "concurrency": 24,
            "implementation": Path(__file__).read_text(),
            "semantics": "Exploratory development review; existing judgments remain unchanged; labels overlap",
        },
    )
    semaphore = asyncio.Semaphore(24)

    async def one(job, client):
        folder = root / job["id"]
        original = None
        if args.repair_interfaces:
            previous = read(folder / "divergence-review-result.json")
            if previous["status"] == "completed":
                return previous
            write_json(folder / "divergence-review-before-interface-repair.json", previous)
            response_path = folder / "divergence-review-repair-response.json"
            if not response_path.exists():
                response_path = folder / "divergence-review-response.json"
            original = json.loads(read(response_path)["choices"][0]["message"]["content"])
        usage, started = {}, time.monotonic()
        result = {"checkpoint_id": job["id"], "status": "failure"}
        try:
            packet, prediction = (
                read(folder / "evidence-packet.json"),
                read(folder / "decisions.json"),
            )
            target = episodes[job["id"]]
            sources = [{"id": s["id"], "text": s["text"]} for s in packet["sources"]]
            payload = {
                "prefix_sources": sources,
                "prediction": prediction,
                "reference_validation": read(folder / "decisions-validation.json"),
                "historical_actions": target["actions"],
                "target_limits": target.get("limits", []),
                "extracted_entities": [
                    {k: e[k] for k in ("id", "kind", "label") if k in e} for e in packet["entities"]
                ],
                "extracted_gaps": packet["gaps"],
                "record_request_associations": [
                    {k: r[k] for k in ("id", "type", "request_id") if k in r}
                    for r in packet["records"]
                ],
            }
            tids, pids = (
                [a["id"] for a in target["actions"]],
                [a["id"] for a in prediction["actions"]],
            )
            schema = DivergenceReview.model_json_schema()
            schema["$defs"]["EvidenceRef"]["properties"]["source_id"]["enum"] = [
                s["id"] for s in sources
            ]
            for definition, field, ids in (
                ("TargetReview", "target_action_id", tids),
                ("PredictionReview", "prediction_action_id", pids),
            ):
                if ids:
                    schema["$defs"][definition]["properties"][field]["enum"] = ids
            for field, ids in (("targets", tids), ("predictions", pids)):
                schema["properties"][field].update(minItems=len(ids), maxItems=len(ids))
            body = request(payload, prompt, schema, model, 6500, "divergence_review")
            if original is not None:
                body["messages"].extend(
                    [
                        {"role": "assistant", "content": json.dumps(original)},
                        {
                            "role": "user",
                            "content": "Repair ONLY reference IDs and evidence quotes/occurrences. Preserve every category, label, explanation, summary, limitation and row order exactly. Return the complete corrected review. "
                            + json.dumps(
                                {
                                    "error": previous["error"],
                                    "target_ids": tids,
                                    "prediction_ids": pids,
                                }
                            ),
                        },
                    ]
                )
            async with semaphore:
                async with asyncio.timeout(300):
                    review = await structured_call(
                        client,
                        key,
                        body,
                        ReviewValidator(packet["sources"], tids, pids, original),
                        folder,
                        "divergence-interface-repair"
                        if args.repair_interfaces
                        else "divergence-review",
                        usage,
                    )
            write_json(folder / "divergence-review.json", review.model_dump())
            write_json(
                folder / "divergence-review-spans.json",
                {
                    "spans": [
                        {
                            "section": section,
                            "row": index,
                            "evidence": [
                                resolve_span(ref, packet["sources"]) for ref in row.evidence
                            ],
                        }
                        for section in ("targets", "predictions", "differences")
                        for index, row in enumerate(getattr(review, section))
                    ]
                },
            )
            result.update(
                status="completed",
                categories=sorted({d.category for d in review.differences}),
                target_importance=dict(Counter(t.importance for t in review.targets)),
                target_warrant=dict(Counter(t.prefix_warrant for t in review.targets)),
                prediction_progress=dict(Counter(p.progress for p in review.predictions)),
            )
        except (
            ValueError,
            TypeError,
            KeyError,
            IndexError,
            TimeoutError,
            httpx.HTTPError,
        ) as error:
            result["error"] = str(error)
        result.update(usage_by_stage=usage, seconds=time.monotonic() - started)
        write_json(folder / "divergence-review-result.json", result)
        print(f"divergence {job['id']}: {result['status']}", flush=True)
        return result

    started = time.monotonic()
    if args.repair_interfaces:
        write_json(
            root / "divergence-summary-before-interface-repair.json",
            read(root / "divergence-review-summary.json"),
        )
    async with httpx.AsyncClient(timeout=180) as client:
        results = await asyncio.gather(*(one(j, client) for j in manifest["jobs"]))
    write_json(
        root / "divergence-review-summary.json",
        {
            "denominator": len(results),
            "completed": sum(r["status"] == "completed" for r in results),
            "category_checkpoint_counts": dict(
                Counter(c for r in results for c in r.get("categories", []))
            ),
            "results": results,
            "seconds": time.monotonic() - started,
            "meaning": "Overlapping model-assisted categories; unassessed checkpoints remain in denominator",
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--env-file", type=Path, required=True)
    parser.add_argument("--repair-interfaces", action="store_true")
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
