"""Build an offline case-review workspace from one extraction job."""

import argparse
import json
from pathlib import Path

from .decision_output import decision_output
from .review_page import PAGE


def read_json(directory, name, default):
    if isinstance(directory, dict):
        return directory.get(name, default)
    path = directory / name
    return json.loads(path.read_text()) if path.exists() else default


def render_job(
    directory: Path,
    decisions_path: Path | None = None,
    corpus: dict | None = None,
    artifacts: dict | None = None,
) -> str:
    """Render evidence and optional proposals; never synthesize an agent decision."""
    reader = directory if artifacts is None else artifacts
    packet_name = (
        "evidence-packet.json"
        if read_json(reader, "evidence-packet.json", None) is not None
        else "decision-state.json"
    )
    packet = read_json(reader, packet_name, {})
    entities = read_json(reader, "entities.json", {}).get("entities", [])
    records = read_json(reader, "records.json", {})
    decision_path = decisions_path or directory / "decisions.json"
    decisions = (
        json.loads(decision_path.read_text())
        if decisions_path
        else read_json(reader, "decisions.json", None)
    )
    prefix = read_json(reader, "input.json", {})
    if not prefix and corpus:
        prefix = {
            "case_id": corpus["entry"]["case"],
            "cutoff": corpus["entry"]["cutoff"],
            "events": [],
        }
    payload = {
        "job": directory.name,
        "run": directory.parent.name,
        "prefix": prefix,
        "result": read_json(
            reader, "result.json", {"status": corpus["entry"]["status"]} if corpus else {}
        ),
        "sources": read_json(reader, "sources.json", {}).get("sources", []),
        "attachments": read_json(reader, "attachments.json", {}),
        "entities": entities,
        "records": records.get("records", []),
        "gaps": records.get("gaps", []),
        "field_spans": packet.get("field_spans", []),
        "mentions": read_json(reader, "mentions.json", {}).get("mentions", []),
        "checks": {
            stage: read_json(reader, f"{stage}-validation.json", {})
            for stage in ("entities", "records")
        },
        "packet_available": bool(packet),
        "packet_validated": packet.get(
            "validated_decision_state", packet_name == "decision-state.json" and bool(packet)
        ),
        "packet_semantics": packet.get("semantics"),
        "packet_diagnostics": packet.get("diagnostics", {}),
        "interface_repairs": {
            "records": read_json(reader, "records-canonicalization.json", {}),
            "decisions": read_json(reader, "decisions-canonicalization.json", {}),
        },
        "decisions": decisions,
        "decision_agent_output": decision_output(
            {
                name: read_json(reader, name, None)
                for name in (
                    "decisions.json",
                    "decisions-raw-parsed.json",
                    "decisions-response.json",
                    "decisions-repair-response.json",
                    "decisions-canonicalization.json",
                    "decisions-validation.json",
                )
                if read_json(reader, name, None) is not None
            }
        ),
        "decision_checks": read_json(reader, "decisions-validation.json", {}),
        "evidence_assessment": read_json(reader, "evidence-response-judgment.json", {}),
        "divergence_review": read_json(reader, "divergence-review.json", {}),
        "evidence_assessment_catalog": read_json(reader, "evidence-citation-catalog.json", {}),
        "decision_review": read_json(reader, "decision-review.json", {}),
        "decision_raw": read_json(reader, "decisions-response.json", {}),
        "observed_later": read_json(reader, "observed-later.json", {}),
        "corpus": corpus,
    }
    # Escaping '<' prevents source data from terminating the inert JSON script element.
    data = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    return PAGE.replace("__EVIDENCE_PAYLOAD__", data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job", type=Path, help="One extraction job directory")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, help="Optional decision response JSON")
    args = parser.parse_args()
    if not (args.job / "input.json").is_file():
        parser.error("Job directory must contain input.json")
    if args.output.exists():
        parser.error("Output already exists; choose a new path")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_job(args.job, args.decisions), encoding="utf-8")
    print(args.output.resolve())


if __name__ == "__main__":
    main()
