"""Render every indexed development checkpoint, including incomplete jobs."""

import argparse
import json
from pathlib import Path

from .corpus_page import PAGE
from .render import read_json, render_job


def summarize_checkpoint(artifacts, entry: dict, number: int) -> dict:
    result = read_json(artifacts, "result.json", {})
    decisions = read_json(artifacts, "decisions.json", {})
    response = decisions.get("response", decisions)
    checks = read_json(artifacts, "decisions-validation.json", {})
    review = read_json(artifacts, "decision-review.json", {})
    records = read_json(artifacts, "records.json", {})
    evidence_checks = read_json(artifacts, "records-validation.json", {})
    prefix = read_json(artifacts, "input.json", {})
    case = str(entry.get("case", prefix.get("case_id", entry["id"])))
    cutoff = entry.get("cutoff", prefix.get("cutoff"))
    actions = response.get("actions", [])
    rationale = response.get("rationale", {})
    repair = (
        (
            checks.get("structurally_valid") is False
            and any(issue != "cross_request_evidence" for issue in checks.get("issues", []))
        )
        or result.get("status")
        in {
            "invalid_entities",
            "invalid_records",
            "error",
            "interface_failure",
            "extraction_failure",
        }
        or review.get("status") in {"schema_error", "invalid_schema", "invalid_response"}
    )
    support_review = not repair and (
        checks.get("evidence_compatible") is False
        or "cross_request_evidence" in checks.get("issues", [])
    )
    row = {
        "id": entry["id"],
        "case": case,
        "split": entry.get("split"),
        "historical_correspondence": read_json(artifacts, "judge.json", {}).get("overall_correspondence"),
        "cutoff": cutoff,
        "label": f"{case} · event {cutoff}",
        "href": f"case-{number:03}.html",
        "title": next(
            (r["description"] for r in records.get("records", []) if r["type"] == "issue"),
            "Case evidence",
        ),
        "status": entry.get("status", result.get("status", "pending")),
        "actions": len(actions),
        "has_decision": bool(response.get("ontology_version")),
        "disposition": response.get("disposition"),
        "records": len(records.get("records", [])),
        "gaps": len(records.get("gaps", [])),
        "evidence_checks": len(evidence_checks.get("issues", [])),
        "uncertainties": len(rationale.get("uncertainties", [])),
        "assumptions": len(rationale.get("assumptions", [])),
        "repair": repair,
        "support_review": support_review,
        "review_state": "Reference review"
        if repair
        else "Support review"
        if support_review
        else "Evidence review"
        if records.get("gaps") or rationale.get("uncertainties") or evidence_checks.get("issues")
        else "Unreviewed",
    }
    return row


def render_corpus(run: Path, output: Path) -> Path:
    run = run.resolve()
    index = read_json(run, "corpus-index.json", {})
    entries = index.get("entries")
    if not isinstance(entries, list) or not entries:
        raise ValueError("corpus-index.json must contain nonempty entries")
    prepared = []
    for number, entry in enumerate(entries, 1):
        path = Path(entry["path"])
        directory = (path if path.is_absolute() else run / path).resolve()
        if not directory.is_relative_to(run):
            raise ValueError("Indexed job paths must remain inside the run directory")
        row = summarize_checkpoint(directory, entry, number)
        prepared.append((directory, row))
    output.mkdir(parents=True, exist_ok=False)
    rows = [row for _, row in prepared]
    for directory, row in prepared:
        metadata = {"entries": rows, "current": row["href"], "entry": row}
        (output / row["href"]).write_text(render_job(directory, corpus=metadata), encoding="utf-8")
    payload = {
        "run": run.name,
        "entries": rows,
        "metadata": {
            **{key: value for key, value in index.items() if key != "entries"},
            "run_settings": read_json(run, "run-settings.json", {}),
        },
    }
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    destination = output / "index.html"
    destination.write_text(PAGE.replace("__CORPUS_PAYLOAD__", data), encoding="utf-8")
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--output", type=Path, required=True, help="New review directory")
    args = parser.parse_args()
    print(render_corpus(args.run, args.output).resolve())


if __name__ == "__main__":
    main()
