"""Project canonical run decisions into the hackathon ANSWERS directory layout."""

import argparse
import hashlib
import json
import os
from collections import Counter
from pathlib import Path
from urllib.parse import quote

from .run_artifact import resolve_artifacts, validate_artifact


def fenced(value):
    return "```json\n" + json.dumps(value, ensure_ascii=False, indent=2) + "\n```\n"


def export_answers(
    document, destination, arm_id=None, source_artifact=None, preserve_case_ids=False
):
    issues = validate_artifact(document)
    if issues:
        raise ValueError("Invalid source artifact: " + "; ".join(issues))
    if document["format_version"] == "property-run-v2" and arm_id not in document["arm_ids"]:
        raise ValueError("Select an explicit declared arm for a multi-arm submission")
    if document["format_version"] == "property-run-v1" and arm_id is not None:
        raise ValueError("The baseline artifact has no named arms")
    cases = [
        str(c["case_id"]) if preserve_case_ids else str(int(c["case_id"]))
        for c in document["checkpoints"]
    ]
    case_counts = Counter(cases)
    destination.mkdir(parents=True, exist_ok=False)
    mapping = []
    for checkpoint, case in zip(document["checkpoints"], cases, strict=True):
        files = resolve_artifacts(document, checkpoint, arm_id)
        decision = files.get("decisions.json")
        folder = destination / case
        if case_counts[case] > 1:
            folder = folder / "checkpoints" / checkpoint["id"]
        folder.mkdir(parents=True)
        header = (
            f"Case {case}; checkpoint `{checkpoint['id']}`; prefix ends at event "
            f"`{checkpoint['cutoff']}`. Run `{document['run_id']}`, "
            f"artifact SHA-256 `{document['content_sha256']}`.\n\n"
        )
        if arm_id is not None:
            header += f"Selected prompt arm: `{arm_id}`.\n\n"
        evidence_dir = folder / "evidence"
        evidence_dir.mkdir()
        bundle_files = []
        for name, content in sorted(files.items()):
            if Path(name).name != name:
                raise ValueError(f"Evidence artifact name is not a basename: {name}")
            path = evidence_dir / name
            if name.endswith(".json"):
                encoded = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
            elif isinstance(content, str):
                encoded = content
            else:
                encoded = json.dumps(content, ensure_ascii=False, indent=2) + "\n"
            path.write_text(encoded, encoding="utf-8")
            bundle_files.append(
                {
                    "path": name,
                    "sha256": hashlib.sha256(encoded.encode("utf-8")).hexdigest(),
                    "bytes": len(encoded.encode("utf-8")),
                }
            )
        (evidence_dir / "README.md").write_text(
            "# Case evidence bundle\n\n"
            f"- Case: `{case}`\n"
            f"- Checkpoint: `{checkpoint['id']}`\n"
            f"- Full-history cutoff: event `{checkpoint['cutoff']}`\n"
            f"- Run: `{document['run_id']}`\n"
            f"- Run artifact SHA-256: `{document['content_sha256']}`\n"
            f"- Prefix SHA-256: `{checkpoint.get('prefix_sha256')}`\n\n"
            "This bundle contains the saved checkpoint inputs, extracted evidence, "
            "model requests and responses, decisions, and validation artifacts. "
            "The output is the system's recorded result; this bundle does not claim "
            "that its interpretation is correct. File hashes are in `bundle-manifest.json`.\n",
            encoding="utf-8",
        )
        (evidence_dir / "bundle-manifest.json").write_text(
            json.dumps(
                {
                    "run_id": document["run_id"],
                    "run_artifact_sha256": document["content_sha256"],
                    "checkpoint_id": checkpoint["id"],
                    "case_id": case,
                    "files": bundle_files,
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        header += "[Case evidence bundle](evidence/README.md).\n\n"
        answer = "# Proposed answer\n\n" + header
        answer += (
            "## Execution status\n\n"
            "This system has no external execution environment, so it did not carry out "
            "any proposed actions. Actions and outcomes recorded in the case history are "
            "evidence; the actions below are recommendations. The case evidence bundle "
            "contains the supplied history and extracted support.\n\n"
        )
        reasoning = "# Decision rationale and evidence\n\n" + header
        if decision:
            answer += f"Disposition: **{decision.get('disposition', 'unknown')}**.\n\n"
            answer += "## Proposed actions\n\n"
            for action in decision.get("actions", []):
                answer += f"### {action['type'].replace('_', ' ').capitalize()}\n\n"
                answer += fenced(action) + "\n"
            answer += "## Action dependencies\n\n"
            dependency_rows = [
                f"- `{action['id']}` depends on `{dependency}`."
                for action in decision.get("actions", [])
                for dependency in action.get("depends_on_action_ids", [])
            ]
            answer += (
                "\n".join(dependency_rows)
                if dependency_rows
                else "No action dependencies were proposed."
            )
            answer += "\n\n"
            answer += "## Human interventions\n\n" + fenced(decision.get("human_interventions", []))
            answer += (
                "\nConclusion records: "
                + json.dumps(decision.get("conclusion_record_ids", []))
                + "\n"
            )
            rationale = decision.get("rationale", {})
            reasoning += str(rationale.get("selected_because", "No rationale supplied.")) + "\n\n"
            for field in ("assumptions", "uncertainties", "alternatives_considered"):
                reasoning += f"## {field.replace('_', ' ').capitalize()}\n\n"
                reasoning += (
                    "\n".join("- " + str(v) for v in rationale.get(field, [])) or "None supplied."
                )
                reasoning += "\n\n"
            packet = files.get("evidence-packet.json", {})
            sources = {s["id"]: s for s in packet.get("sources", [])}
            reasoning += "## Cited prefix evidence\n\n"
            for citation in rationale.get("evidence", []):
                source = sources.get(citation.get("source_id"))
                reasoning += fenced(citation)
                if source:
                    if source.get("origin") == "attachment":
                        reasoning += (
                            f"Document `{source['document_id']}` "
                            f"(`{source.get('relative_path', 'file path unavailable')}`), "
                            f"page {source['page_number']}, "
                            f"source `{source['id']}`, extracted page Unicode character range "
                            f"[{source['start']}, {source['end']}); available at events "
                            f"{', '.join(source.get('available_at_event_ids', []))}.\n\n"
                        )
                    else:
                        reasoning += (
                            f"Event `{source['event_id']}`, source `{source['id']}`, "
                            f"event character range [{source['start']}, {source['end']}).\n\n"
                        )
                    reasoning += (
                        "\n".join("> " + line for line in source["text"].splitlines()) + "\n\n"
                    )
                else:
                    reasoning += "Source reference unresolved in the generated evidence packet.\n\n"
            record_ids = set(decision.get("conclusion_record_ids", []))
            gap_ids = set()
            for action in decision.get("actions", []):
                record_ids.update(action.get("basis_record_ids", []))
                gap_ids.update(action.get("basis_gap_ids", []))
            reasoning += "## Action evidence records and gaps\n\n"
            reasoning += fenced(
                {
                    "records": [r for r in packet.get("records", []) if r["id"] in record_ids],
                    "gaps": [g for g in packet.get("gaps", []) if g["id"] in gap_ids],
                }
            )
        else:
            answer += "Decision unavailable; no answer has been invented.\n"
            reasoning += "Decision unavailable; no rationale has been invented.\n"
        # The required ANSWER is self-contained; the companion remains separately readable.
        reasoning_body = reasoning.removeprefix("# Decision rationale and evidence\n\n" + header)
        answer += "\n## Evidence and reasoning\n\n" + reasoning_body
        (folder / "ANSWER.md").write_text(answer)
        (folder / "REASONING.md").write_text(reasoning)
        mapping.append(
            {
                "case_number": int(case),
                "checkpoint_id": checkpoint["id"],
                "answer": str((folder / "ANSWER.md").relative_to(destination)),
                "reasoning": str((folder / "REASONING.md").relative_to(destination)),
            }
        )
    for case, count in case_counts.items():
        if count <= 1:
            continue
        source = source_artifact or destination.parent / "run.json"
        link = quote(os.path.relpath(source.resolve(), (destination / case).resolve()), safe="/.")
        text = f"# Case {case}: decision checkpoints\n\n[Full source JSON]({link}).\n\nEach checkpoint has its own prefix, proposals and recorded rationale.\n\n"
        for row in mapping:
            if row["case_number"] == int(case):
                relative = str(Path(row["answer"]).relative_to(case))
                text += f"- [{row['checkpoint_id']}]({relative})\n"
        (destination / case / "ANSWER.md").write_text(text)
        (destination / case / "REASONING.md").write_text(text)
    (destination / "index.json").write_text(
        json.dumps(
            {
                "run_id": document["run_id"],
                "content_sha256": document["content_sha256"],
                "selected_arm": arm_id,
                "semantics": "Deterministic projection of saved decisions; no future targets or semantic corrections.",
                "cases": mapping,
            },
            indent=2,
        )
        + "\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--arm")
    parser.add_argument(
        "--preserve-case-ids",
        action="store_true",
        help="Keep source case IDs such as 001 for challenge formats that require padding",
    )
    args = parser.parse_args()
    export_answers(
        json.loads(args.artifact.read_text()),
        args.output,
        args.arm,
        args.artifact,
        args.preserve_case_ids,
    )
    print(args.output)


if __name__ == "__main__":
    main()
