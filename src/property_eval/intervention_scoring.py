"""Deterministic reviewed boundary probes, scoped to selected source events."""

import argparse
import json
from pathlib import Path


def evidence_sources(record):
    sources = set(record["provenance"]["source_ids"])
    sources.update(span["source_id"] for item in record["field_evidence"] for span in item["spans"])
    sources.update(
        span["source_id"] for cause in record.get("causes", []) for span in cause["evidence"]
    )
    return sources


def score_interventions(reference, directory):
    output = directory / "records.json"
    if not output.exists():
        return {"id": reference["id"], "status": "not_scored_missing_records", "probes": []}
    records = json.loads(output.read_text())["records"]
    target = [
        r
        for r in records
        if any(s.startswith(reference["target_event"] + ":") for s in evidence_sources(r))
    ]
    interventions = [r for r in target if r["type"] == "human_intervention"]
    failures = [
        r
        for r in target
        if r["type"] == "workflow_failure" and reference["error_source"] in evidence_sources(r)
    ]
    probes = [{"id": "workflow-error-preserved", "passed": bool(failures)}]
    if reference["expected_intervention"]:
        review = [r for r in interventions if reference["review_source"] in evidence_sources(r)]
        probes.extend(
            [
                {"id": "review-requirement-detected", "passed": bool(review)},
                {
                    "id": "required-not-executed",
                    "passed": bool(review)
                    and all(r["status"] == reference["status"] for r in review),
                },
                {
                    "id": "intervention-kind",
                    "passed": any(
                        r["requested_intervention"] == reference["requested_intervention"]
                        for r in review
                    ),
                },
                {
                    "id": "responsible-human-unresolved",
                    "passed": bool(review)
                    and all(
                        r["responsible_role"] == reference["role"]
                        and r["responsible_party_id"] is None
                        for r in review
                    ),
                },
                {
                    "id": "no-unobserved-release",
                    "passed": bool(review)
                    and all(r["blocking_effect"] != "released" for r in review),
                },
            ]
        )
    else:
        probes.append({"id": "error-does-not-invent-human-escalation", "passed": not interventions})
    probes.append(
        {
            "id": "adjacency-not-asserted-cause",
            "passed": not any(
                c["category"] == reference["forbidden_cause_assertion"]
                and c["causal_status"] == "asserted"
                for r in interventions
                for c in r["causes"]
            ),
        }
    )
    return {
        "id": reference["id"],
        "status": "scored",
        "probes": probes,
        "passed": sum(p["passed"] for p in probes),
        "total": len(probes),
        "intervention_ids": [r["id"] for r in interventions],
        "meaning": "Development event-boundary probes; not overall extraction accuracy or decision validity",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    refs = json.loads(args.references.read_text())["references"]
    args.output.write_text(
        json.dumps({"scores": [score_interventions(r, args.run / r["id"]) for r in refs]}, indent=2)
        + "\n"
    )


if __name__ == "__main__":
    main()
