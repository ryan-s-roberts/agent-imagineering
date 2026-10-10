"""Aggregate typed episode judgments without inventing semantic scores."""

import argparse
import json
from collections import Counter
from pathlib import Path

from .cli import write_json


def summarize(root):
    index = json.loads((root / "corpus-index.json").read_text())
    config = json.loads((root / "experiment.json").read_text())
    source = Path(config["inherited_experiment_root"])
    summary = json.loads((root / "summary.json").read_text())
    arms = {}
    rows = []
    for arm in ("control", "progress"):
        groups = {
            name: Counter()
            for name in ("material", "workflow", "operational", "auxiliary", "unassessable")
        }
        stable = {name: Counter() for name in groups}
        overall, old, extras, support, orders, predictability, transitions = [
            Counter() for _ in range(7)
        ]
        full = strict = stable_cases = 0
        for entry in index["entries"]:
            directory = root / entry["arms"][arm]["path"]
            result = json.loads((directory / "result.json").read_text())
            if result["status"] != "completed":
                rows.append({"checkpoint": entry["id"], "arm": arm, "status": result["status"]})
                continue
            metrics = json.loads((directory / "episode-metrics.json").read_text())
            judgment = json.loads((directory / "judge.json").read_text())
            original = json.loads((directory / "inherited-judge.json").read_text())
            overall[judgment["overall_correspondence"]] += 1
            old[original["overall_correspondence"]] += 1
            transitions[
                f"{original['overall_correspondence']} -> {judgment['overall_correspondence']}"
            ] += 1
            boundary_uncertain = metrics["annotation_boundary_confidence"] == "uncertain"
            stable_cases += not boundary_uncertain
            for kind, counts in groups.items():
                counts.update(metrics["coverage_by_materiality"][kind])
                if not boundary_uncertain:
                    stable[kind].update(metrics["coverage_by_materiality"][kind])
            extras.update(metrics["extra_status_counts"])
            support.update(metrics["prediction_supportedness"])
            orders.update(metrics["necessary_order"])
            predictability.update(metrics["coverage_by_predictability"])
            full += metrics["full_operational_coverage"]
            strict += metrics["strict_full_operational_correspondence"]
            rows.append(
                {
                    "checkpoint": entry["id"],
                    "arm": arm,
                    "status": result["status"],
                    "old_single_event_label": original["overall_correspondence"],
                    "new_episode_label": judgment["overall_correspondence"],
                    **metrics,
                }
            )
        arms[arm] = {
            "checkpoint_denominator": 40,
            "coverage": {k: dict(v) for k, v in groups.items()},
            "excluding_six_uncertain_boundaries": {
                "checkpoint_denominator": stable_cases,
                "note": "Includes probable timer boundaries; not a claim all remaining boundaries are certain",
                "coverage": {k: dict(v) for k, v in stable.items()},
            },
            "model_overall_correspondence": dict(overall),
            "old_single_event_correspondence": dict(old),
            "label_transitions": dict(transitions),
            "extras": dict(extras),
            "prediction_support": dict(support),
            "ordering": dict(orders),
            "coverage_by_predictability": dict(predictability),
            "fully_covered_operational_episodes": full,
            "strict_full_operational_correspondence": strict,
        }
    prediction_bytes_equal = all(
        (root / state["path"] / "decisions.json").read_bytes()
        == (source / state["path"] / "decisions.json").read_bytes()
        for entry in index["entries"]
        for state in entry["arms"].values()
    )
    evidence_bytes_equal = all(
        (root / "evidence" / f"{entry['id']}.json").read_bytes()
        == (source / "evidence" / f"{entry['id']}.json").read_bytes()
        for entry in index["entries"]
    )
    checks = [json.loads(p.read_text()) for p in root.glob("arms/**/judge-validation.json")]
    return {
        "version": "episode-review-v1",
        "meaning": "Deterministic aggregation of model-assisted many-to-many labels, not normative correctness. Old and new labels use different target units/rubrics; no agent improvement inference.",
        "completion": summary["completed"],
        "judgment_denominator": 80,
        "fresh_calls": len(list(root.glob("arms/**/judge*-response.json"))),
        "interface_repairs": len(list(root.glob("arms/**/judge-repair-response.json"))),
        "cost_usd": summary["cost_usd"],
        "wall_clock_seconds": summary["wall_clock_seconds"],
        "observed_peak_outstanding_calls": 24,
        "prediction_bytes_unchanged": prediction_bytes_equal,
        "evidence_bytes_unchanged": evidence_bytes_equal,
        "citation_count": sum(c["citation_count"] for c in checks),
        "invalid_citation_count": sum(len(c["invalid_citations"]) for c in checks),
        "arms": arms,
        "checkpoints": rows,
        "limitations": [
            "Targets are reviewed development annotations, not gold or normative required actions.",
            "Six boundaries uncertain;022/035 mixed-call limits remain.",
            "Overall correspondence is model-authored and may disagree with per-action counts; detailed deterministic coverage takes precedence for reporting.",
            "The response includes85proposed actions across80predictions; support is assessed per action, unlike prior response-level support labels.",
            "Many-to-many mappings establish advisory semantic overlap, not entailment proof.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    result = summarize(args.root)
    write_json(args.root / "episode-review.json", result)
    print(
        json.dumps(
            {k: v for k, v in result.items() if k not in {"arms", "checkpoints", "limitations"}},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
