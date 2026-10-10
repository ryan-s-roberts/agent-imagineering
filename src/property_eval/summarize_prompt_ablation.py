"""Paired descriptive statistics for the preregistered 2x2 prompt experiment."""

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from .cli import write_json
from .prompt_ablation import ARMS


def read(path):
    return json.loads(path.read_text()) if path.exists() else {}


def cell(folder):
    result = read(folder / "result.json")
    decision = read(folder / "decisions.json")
    checks = read(folder / "decisions-validation.json")
    metrics = read(folder / "episode-metrics.json")
    judge = read(folder / "judge.json")
    coverage = metrics.get("coverage_by_materiality", {})
    support = metrics.get("prediction_supportedness", {})
    return {
        "completed": result.get("status") == "completed",
        "decision_available": bool(decision),
        "valid": checks.get("valid") is True,
        "issues": checks.get("issues", []),
        "actions": len(decision.get("actions", [])),
        "action_types": dict(Counter(a["type"] for a in decision.get("actions", []))),
        "overall": judge.get("overall_correspondence", "unassessed"),
        "full_operational": int(metrics.get("full_operational_coverage", False)),
        "strict_full_operational": int(
            metrics.get("strict_full_operational_correspondence", False)
        ),
        "material_covered": coverage.get("material", {}).get("covered", 0),
        "material_partial": coverage.get("material", {}).get("partial", 0),
        "workflow_covered": coverage.get("workflow", {}).get("covered", 0),
        "workflow_partial": coverage.get("workflow", {}).get("partial", 0),
        "unsupported": support.get("unsupported", 0),
        "partly_supported": support.get("partly_supported", 0),
        "invalid": int(bool(decision) and checks.get("valid") is not True),
        "coverage": coverage,
        "support": support,
    }


def summarize(root):
    manifest, config = read(root / "manifest.json"), read(root / "experiment.json")
    cells = {
        j["id"]: {a: cell(root / "arms" / a / j["id"]) for a in ARMS} for j in manifest["jobs"]
    }
    summaries = {}
    for arm in ARMS:
        rows = [arms[arm] for arms in cells.values()]
        coverage, support, types = defaultdict(Counter), Counter(), Counter()
        for row in rows:
            for kind, values in row["coverage"].items():
                coverage[kind].update(values)
            support.update(row["support"])
            types.update(row["action_types"])
        summaries[arm] = {
            "denominator": len(rows),
            "completed": sum(r["completed"] for r in rows),
            "decisions": sum(r["decision_available"] for r in rows),
            "valid": sum(r["valid"] for r in rows),
            "actions": sum(r["actions"] for r in rows),
            "mean_actions_per_checkpoint": sum(r["actions"] for r in rows) / len(rows),
            "full_operational": sum(r["full_operational"] for r in rows),
            "strict_full_operational": sum(r["strict_full_operational"] for r in rows),
            "overall": dict(Counter(r["overall"] for r in rows)),
            "action_types": dict(types),
            "support": dict(support),
            "coverage": {k: dict(v) for k, v in coverage.items()},
        }
    measures = (
        "actions",
        "full_operational",
        "material_covered",
        "material_partial",
        "workflow_covered",
        "workflow_partial",
        "unsupported",
        "partly_supported",
        "invalid",
    )
    pairs = {}
    for left, right in (
        ("control", "coverage"),
        ("control", "uncertainty"),
        ("control", "combined"),
        ("coverage", "combined"),
        ("uncertainty", "combined"),
    ):
        valid = [v for v in cells.values() if v[left]["completed"] and v[right]["completed"]]
        deltas = {}
        for measure in measures:
            values = [v[right][measure] - v[left][measure] for v in valid]
            deltas[measure] = {
                "sum": sum(values),
                "mean": sum(values) / len(values) if values else None,
                "higher": sum(v > 0 for v in values),
                "equal": sum(v == 0 for v in values),
                "lower": sum(v < 0 for v in values),
            }
        pairs[f"{right}_minus_{left}"] = {"paired_checkpoints": len(valid), "deltas": deltas}
    complete = [v for v in cells.values() if all(v[a]["completed"] for a in ARMS)]
    effects = {}
    for measure in measures:
        vals = {a: sum(v[a][measure] for v in complete) for a in ARMS}
        n = len(complete)
        effects[measure] = {
            "coverage_main_effect_per_checkpoint": (
                (vals["coverage"] - vals["control"]) + (vals["combined"] - vals["uncertainty"])
            )
            / (2 * n)
            if n
            else None,
            "uncertainty_main_effect_per_checkpoint": (
                (vals["uncertainty"] - vals["control"]) + (vals["combined"] - vals["coverage"])
            )
            / (2 * n)
            if n
            else None,
            "interaction_per_checkpoint": (
                vals["combined"] - vals["coverage"] - vals["uncertainty"] + vals["control"]
            )
            / n
            if n
            else None,
        }
    baseline = Path(config["baseline_root"])
    earlier = {j["id"]: cell(baseline / j["id"]) for j in manifest["jobs"]}
    replay = {
        "earlier_actions": sum(v["actions"] for v in earlier.values()),
        "fresh_control_actions": summaries["control"]["actions"],
        "changed_action_count_checkpoints": sum(
            cells[k]["control"]["actions"] != v["actions"] for k, v in earlier.items()
        ),
        "changed_historical_label_checkpoints": sum(
            cells[k]["control"]["overall"] != v["overall"] for k, v in earlier.items()
        ),
        "meaning": "Descriptive repeat-control variation; not an independent estimate of model or judge error.",
    }
    analysis = {
        "arms": summaries,
        "paired_contrasts": pairs,
        "factorial_complete_checkpoints": len(complete),
        "factorial_effects": effects,
        "control_replay": replay,
        "cells": cells,
        "interpretation": "Development-only descriptive paired effects, one sample per cell. Higher action count alone is not success; no holdout or statistical certainty claim.",
    }
    write_json(root / "ablation-analysis.json", analysis)
    print(json.dumps({"arms": summaries, "control_replay": replay}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    summarize(parser.parse_args().run)
