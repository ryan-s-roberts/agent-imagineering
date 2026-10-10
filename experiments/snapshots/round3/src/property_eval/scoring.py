"""Frozen reference probes: deterministic recall, not an exhaustive accuracy judge."""

import argparse
import json
from pathlib import Path

from .grounding import resolve_span


def get_field(record, field):
    value = record
    for part in field.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value


def score_reference(reference, directory):
    sources = json.loads((directory / "sources.json").read_text())["sources"]
    prefix = json.loads((directory / "input.json").read_text())
    if prefix["source_sha256"] != reference["prefix_sha256"]:
        raise ValueError("Reference/input prefix digest mismatch")

    def read(name, default):
        path = directory / name
        return json.loads(path.read_text()) if path.exists() else default

    mentions = read("mentions.json", {"mentions": []})["mentions"]
    records = read("records.json", {"records": []})["records"]
    entities = {e["id"]: e for e in read("entities.json", {"entities": []})["entities"]}
    links = read("links.json", {"links": []})["links"]
    result = {"id": reference["id"], "split": reference["split"], "probes": []}

    def field_matches(actual, expected):
        if isinstance(expected, dict) and "entity_kind" in expected:
            entity = entities.get(actual, {})
            if entity.get("kind") not in expected["entity_kind"]:
                return False
            if "surface" in expected:
                return any(m["surface"] in expected["surface"] for m in entity["mentions"])
            return True
        return actual == expected

    def assertion_matches(record, alternative):
        if record["type"] != alternative["type"]:
            return False
        if not all(
            field_matches(get_field(record, field), value)
            for field, value in alternative["fields"].items()
        ):
            return False
        for field, gold_spans in alternative.get("evidence", {}).items():
            proposed = [
                span
                for item in record["field_evidence"]
                if item["field"] == field
                for span in item["spans"]
            ]
            for gold in gold_spans:
                target = resolve_span(gold, sources)
                covered = False
                for span in proposed:
                    try:
                        resolved = resolve_span(span, sources)
                    except ValueError:
                        continue
                    if (
                        resolved["event_id"] == target["event_id"]
                        and resolved["start"] <= target["start"]
                        and resolved["end"] >= target["end"]
                    ):
                        covered = True
                if not covered:
                    return False
        return True

    for probe in reference["probes"]:
        matched = False
        if probe["kind"] == "mention":
            for alternative in probe["alternatives"]:
                target = resolve_span(alternative, sources)
                matched |= any(
                    m["event_id"] == target["event_id"]
                    and m["start"] == target["start"]
                    and m["end"] == target["end"]
                    and m["kind"] == alternative["kind"]
                    for m in mentions
                )
        elif probe["kind"] == "assertion":
            matched = any(assertion_matches(r, a) for r in records for a in probe["alternatives"])
        elif probe["kind"] == "link":
            matched = any(
                all(link.get(k) == v for k, v in alternative.items())
                for link in links
                for alternative in probe["alternatives"]
            )
        else:
            raise ValueError(f"Unknown probe kind: {probe['kind']}")
        result["probes"].append(
            {
                "id": probe["id"],
                "kind": probe["kind"],
                "choice_coverage": probe.get("choice_coverage", []),
                "matched": bool(matched),
            }
        )
    result["matched"] = sum(p["matched"] for p in result["probes"])
    result["total"] = len(result["probes"])
    result["metric"] = "reviewed probe recall; not exhaustive precision or decision accuracy"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--run", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    references = json.loads(args.references.read_text())["references"]
    scores = [score_reference(reference, args.run / reference["id"]) for reference in references]
    args.output.write_text(json.dumps({"scores": scores}, indent=2) + "\n")


if __name__ == "__main__":
    main()
