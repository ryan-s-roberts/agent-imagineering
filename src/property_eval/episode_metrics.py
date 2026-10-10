"""Deterministic counts over advisory model action alignments; never semantic truth."""

from collections import Counter


def alignment_metrics(target, prediction, judgment):
    annotations = {a["id"]: a for a in target["episode"]["actions"]}
    groups = {
        name: Counter()
        for name in ("material", "workflow", "auxiliary", "unassessable", "operational")
    }
    predictability = Counter()
    strict_rows = []
    for row in judgment["target_assessments"]:
        kind = annotations[row["target_action_id"]]["materiality"]
        groups[kind][row["coverage"]] += 1
        predictability[f"{kind}:{row['prefix_predictability']}:{row['coverage']}"] += 1
        if kind in {"material", "workflow"}:
            groups["operational"][row["coverage"]] += 1
            strict_rows.append(row)
    matched = {a for row in judgment["target_assessments"] for a in row["prediction_action_ids"]}
    return {
        "coverage_by_materiality": {
            k: {"denominator": sum(v.values()), **dict(v)} for k, v in groups.items()
        },
        "coverage_by_predictability": dict(predictability),
        "prediction_count": len(prediction["actions"]),
        "mapped_prediction_count": len(matched),
        "extra_status_counts": dict(
            Counter(r["extra_status"] for r in judgment["prediction_assessments"])
        ),
        "prediction_supportedness": dict(
            Counter(r["supportedness"] for r in judgment["prediction_assessments"])
        ),
        "necessary_order": dict(
            Counter(r["verdict"] for r in judgment["necessary_order_assessments"])
        ),
        "full_operational_coverage": bool(strict_rows)
        and all(r["coverage"] == "covered" for r in strict_rows),
        "strict_full_operational_correspondence": bool(strict_rows)
        and all(
            r["coverage"] == "covered"
            and r["participants"] == "match"
            and r["scope_conditions"] == "match"
            for r in strict_rows
        )
        and all(
            r["verdict"] == "satisfied"
            for r in judgment["necessary_order_assessments"]
            if r["requiredness"] == "required_by_meaning"
        ),
        "annotation_boundary_confidence": target["episode"]["boundary"]["confidence"],
        "judge_boundary_assessability": judgment["boundary_assessability"],
        "meaning": "Counts deduplicate target/prediction IDs, over model-assisted labels. No weighted score or normative accuracy.",
    }
