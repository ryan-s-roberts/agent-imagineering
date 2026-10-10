"""Descriptive paired development results; no composite correctness score."""

import argparse
import json
from collections import Counter
from pathlib import Path

from .cli import write_json


def summarize(root):
    index = json.loads((root / "corpus-index.json").read_text())
    config = json.loads((root / "experiment.json").read_text())
    arms = [a["id"] for a in config["arms"]]
    aggregates = {
        arm: {
            "status": Counter(),
            "correspondence": Counter(),
            "supportedness": Counter(),
            "predictability": Counter(),
            "dispositions": Counter(),
            "actions": Counter(),
            "cost_usd": 0,
            "judge_invalid_citations": 0,
            "judgments_with_invalid_citations": 0,
            "decision_valid_cases": 0,
            "repairs": 0,
        }
        for arm in arms
    }
    pairs = []
    for entry in index["entries"]:
        pair = {"id": entry["id"], "arms": {}}
        for arm in arms:
            directory = root / entry["arms"][arm]["path"]
            row = aggregates[arm]
            result = json.loads((directory / "result.json").read_text())
            row["status"][result["status"]] += 1
            row["cost_usd"] += result["cost_usd"]
            row["repairs"] += sum("repair" in k for k in result["usage_by_stage"])
            if (directory / "decisions.json").exists():
                decision = json.loads((directory / "decisions.json").read_text())
                row["dispositions"][decision["disposition"]] += 1
                row["actions"].update(a["type"] for a in decision["actions"])
                row["decision_valid_cases"] += json.loads(
                    (directory / "decisions-validation.json").read_text()
                )["valid"]
            if result["status"] != "completed":
                pair["arms"][arm] = {"status": result["status"]}
                continue
            judgment = json.loads((directory / "judge.json").read_text())
            validation = json.loads((directory / "judge-validation.json").read_text())
            invalid = len(validation["invalid_citations"])
            row["judge_invalid_citations"] += invalid
            row["judgments_with_invalid_citations"] += bool(invalid)
            for source, key in [
                ("overall_correspondence", "correspondence"),
                ("prediction_supportedness", "supportedness"),
                ("target_predictability", "predictability"),
            ]:
                row[key][judgment[source]] += 1
            pair["arms"][arm] = {
                key: judgment[key]
                for key in [
                    "overall_correspondence",
                    "prediction_supportedness",
                    "target_predictability",
                    "confidence",
                ]
            }
        pairs.append(pair)
    transitions = {
        key: Counter()
        for key in ["overall_correspondence", "prediction_supportedness", "target_predictability"]
    }
    for pair in pairs:
        for key, counts in transitions.items():
            left, right = pair["arms"][arms[0]], pair["arms"][arms[1]]
            counts[f"{left.get(key, 'missing')} -> {right.get(key, 'missing')}"] += 1
    report = {
        "denominator_cases": 40,
        "arms": aggregates,
        "paired_transition_direction": f"{arms[0]} -> {arms[1]}",
        "paired_transitions": transitions,
        "pairs": pairs,
        "judge_predictability_disagreement_cases": [
            p["id"]
            for p in pairs
            if p["arms"][arms[0]].get("target_predictability")
            != p["arms"][arms[1]].get("target_predictability")
        ],
        "meaning": "Exploratory model-assisted development judgments, not accuracy or deterministic semantic truth. Predictability disagreements are judge instability, not changed prefix availability.",
    }
    write_json(root / "comparison.json", report)
    print(json.dumps({k: v for k, v in report.items() if k != "pairs"}, indent=2))
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    summarize(parser.parse_args().root)


if __name__ == "__main__":
    main()
