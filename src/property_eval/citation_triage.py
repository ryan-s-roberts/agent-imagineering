"""Classify all original judge citation failures without changing judgments."""

import json
from collections import Counter
from pathlib import Path

from .cli import write_json


def compact_json_text(text):
    output, quoted, escaped = [], False, False
    for char in text:
        if quoted:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
            output.append(char)
        elif not char.isspace():
            output.append(char)
    return "".join(output)


def triage(root):
    failures = []
    for path in sorted(root.glob("arms/*/*/judge-validation.json")):
        payload = json.loads(
            json.loads((path.parent / "judge-request.json").read_text())["messages"][1]["content"]
        )
        sources = {("prefix", s["id"]): s["text"] for s in payload["prefix_evidence"]["sources"]}
        sources[("target", payload["historical_target"]["source"]["id"])] = payload[
            "historical_target"
        ]["source"]["text"]
        sources[("prediction", "prediction")] = payload["prediction_source"]["text"]
        for cite in json.loads(path.read_text())["invalid_citations"]:
            source = sources.get((cite["origin"], cite["source_id"]))
            expression = cite["expression"]
            if (
                source
                and cite["origin"] == "prediction"
                and compact_json_text(expression) in compact_json_text(source)
            ):
                category = "json_whitespace"
                note = "Values exist in supplied prediction; model reserialized JSON spacing instead of quoting canonical source."
            elif cite["origin"] == "prediction" and ',"operation"' in expression.replace(" ", ""):
                category = "json_noncontiguous_reordered_fields"
                note = "Combines existing JSON fields in an order/layout absent from canonical source; not one contiguous quotation."
            elif cite["origin"] == "prefix" and cite["source_id"] == "prediction":
                category = "wrong_namespace"
                note = "Prediction source ID labelled as prefix; generated assumption is not real-world prefix evidence."
            elif expression == "To: Not specified":
                category = "markdown_marker_stripping"
                note = "Display-like text omits Markdown marker characters from supplied original source."
            elif source and expression.casefold() in source.casefold():
                category = "case_normalization"
                note = "Target source sentence starts with uppercase; selected text was lowercased."
            elif expression == "Contractor visit for door lock agreed around half past two.":
                category = "annotation_summary_not_source_quote"
                note = "Exact normalized annotation message is supplied separately but is not a literal quote from its cited historical event."
            elif expression == '"recipient"':
                category = "nonexistent_prediction_field"
                note = "Prediction has no field named recipient; semantic discussion of unknown recipient cannot establish a literal JSON key."
            else:
                raise ValueError(f"Unclassified failure: {cite}")
            failures.append(
                {
                    "index": len(failures) + 1,
                    "arm": path.parts[-3],
                    "checkpoint": path.parts[-2],
                    "raw_citation": cite,
                    "category": category,
                    "diagnosis": note,
                    "claimed_source_supplied": source is not None,
                    "input_omitted": False,
                    "source_text": source,
                    "action": "retain_original_failure; no semantic relabeling or fuzzy repair",
                }
            )
    assert len(failures) == 31
    report = {
        "version": "judge-citation-triage-v1",
        "source_run": str(root),
        "failure_count": 31,
        "category_counts": dict(Counter(f["category"] for f in failures)),
        "failures": failures,
        "conclusion": "Citation transcription/interface defects and source-attribution errors. Do not repair nonliteral claims as if they were exact quotations; replacement interface selects host-owned spans.",
    }
    write_json(Path("annotations/judge-citation-triage-v1.json"), report)
    print(json.dumps(report["category_counts"], indent=2))


if __name__ == "__main__":
    triage(Path("runs/decision-soft-v1"))
