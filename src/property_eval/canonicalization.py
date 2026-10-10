"""Auditable source alignment and host-derived redundant extraction metadata.

Never rewrite assertion values or claim semantic entailment. Original model output
belongs beside this canonical form in the run archive.
"""

from copy import deepcopy

from .grounding import resolve_mentions, resolve_span
from .models import MentionExtraction, RecordExtraction
from .validation import validate_records


def _normalized(text):
    chars, positions = [], []
    for index, char in enumerate(text):
        translated = char.translate(str.maketrans({"’": "'", "‘": "'"})).casefold()
        for value in translated:
            if value.isspace():
                if chars and chars[-1] == " ":
                    continue
                value = " "
            chars.append(value)
            positions.append(index)
    return "".join(chars), positions


def _positions(text, expression):
    positions, start = [], 0
    while (found := text.find(expression, start)) >= 0:
        positions.append(found)
        start = found + 1
    return positions


def align_reference(span, units):
    """Return literal reference + audit, accepting only unique normalized matches."""
    original = span.model_dump() if hasattr(span, "model_dump") else deepcopy(span)
    try:
        resolved = resolve_span(original, units)
        if resolved["alignment"] == "exact":
            return original, None
        source = next(u for u in units if u["id"] == original["source_id"])
        surface = resolved["source_expression"]
        start = resolved["start"] - source["start"]
    except ValueError:
        source = next((u for u in units if u["id"] == original["source_id"]), None)
        if source is None:
            raise ValueError("outside_prefix") from None
        normalized, positions = _normalized(source["text"])
        expression, _ = _normalized(original["expression"])
        matches = _positions(normalized, expression) if expression.strip() else []
        # Multiple normalized matches require human/model disambiguation; no guessing.
        if len(matches) != 1 or original["occurrence"] != 1:
            raise ValueError("ambiguous_or_unmatched_source_expression") from None
        match = matches[0]
        start = positions[match]
        end = positions[match + len(expression) - 1] + 1
        surface = source["text"][start:end]
    occurrence = _positions(source["text"], surface).index(start) + 1
    canonical = {**original, "expression": surface, "occurrence": occurrence}
    return canonical, {
        "operation": "source_alignment",
        "submitted": original,
        "canonical": canonical,
        "event_start": source["start"] + start,
        "event_end": source["start"] + start + len(surface),
        "rule": "case_apostrophe_whitespace_alignment; original source retained",
    }


def canonicalize_mentions(raw, units, case_id):
    data = raw.model_dump() if hasattr(raw, "model_dump") else deepcopy(raw)
    trace, unresolved = [], []
    for index, mention in enumerate(data["mentions"]):
        try:
            aligned, change = align_reference(mention, units)
            data["mentions"][index] = aligned
            if change:
                trace.append(change)
        except ValueError as error:
            unresolved.append({"index": index, "code": str(error), "submitted": mention})
    unique = []
    for mention in data["mentions"]:
        if mention not in unique:
            unique.append(mention)
        else:
            trace.append({"operation": "deduplicate_identical_mention", "mention": mention})
    data["mentions"] = unique
    result = resolve_mentions(MentionExtraction.model_validate(data), units, case_id)
    result["canonicalization"] = trace
    result["unresolved_alignment"] = unresolved
    result["canonical_candidates"] = data
    return result


def align_references(span, units):
    """Align an evidence quote across wrapped lines in its cited event only."""
    try:
        aligned, change = align_reference(span, units)
        return [aligned], change
    except ValueError:
        source = next((u for u in units if u["id"] == span["source_id"]), None)
        if source is None:
            raise ValueError("outside_prefix") from None
    context = source.get("anchor_namespace", source["event_id"])
    event_units = [u for u in units if u.get("anchor_namespace", u["event_id"]) == context]
    # A wrong line identifier can be repaired only for one exact occurrence
    # in the same event. This does not establish that the quotation entails the claim.
    occurrences = [(u, p) for u in event_units for p in _positions(u["text"], span["expression"])]
    if len(occurrences) == 1 and span["occurrence"] == 1:
        unit, _ = occurrences[0]
        corrected = {**span, "source_id": unit["id"]}
        return [corrected], {
            "operation": "unique_same_event_line_reference",
            "submitted": span,
            "canonical": [corrected],
        }
    tail = event_units[event_units.index(source) :]
    text, locations = "", []
    for index, unit in enumerate(tail):
        if index:
            text += " "
            locations.append(None)
        text += unit["text"]
        locations.extend((unit["id"], p) for p in range(len(unit["text"])))
    normalized, position_map = _normalized(text)
    expression, _ = _normalized(span["expression"])
    matches = _positions(normalized, expression) if expression.strip() else []
    if len(matches) != 1 or span["occurrence"] != 1:
        raise ValueError("ambiguous_or_unmatched_source_expression")
    start = position_map[matches[0]]
    end = position_map[matches[0] + len(expression) - 1] + 1
    if locations[start] is None or locations[start][0] != source["id"]:
        raise ValueError("quote_does_not_start_in_cited_line")
    grouped = {}
    for location in locations[start:end]:
        if location is not None:
            grouped.setdefault(location[0], []).append(location[1])
    output = []
    for source_id, offsets in grouped.items():
        unit = next(u for u in tail if u["id"] == source_id)
        surface = unit["text"][min(offsets) : max(offsets) + 1]
        output.append(
            {
                "source_id": source_id,
                "expression": surface,
                "occurrence": _positions(unit["text"], surface).index(min(offsets)) + 1,
            }
        )
    return output, {
        "operation": "split_wrapped_source_quote",
        "submitted": span,
        "canonical": output,
    }


def canonicalize_links(raw, units):
    data = raw.model_dump() if hasattr(raw, "model_dump") else deepcopy(raw)
    trace, issues = [], []
    for link in data["links"]:
        for index, span in enumerate(link["evidence"]):
            try:
                aligned, change = align_reference(span, units)
                link["evidence"][index] = aligned
                if change:
                    trace.append(change)
            except ValueError as error:
                issues.append({"code": str(error), "span": span})
    return {"data": data, "canonicalization": trace, "issues": issues}


def canonicalize_records(raw, entities, units, *, source_texts=None):
    data = raw.model_dump() if hasattr(raw, "model_dump") else deepcopy(raw)
    trace, alignment_issues = [], []
    for record in data["records"]:
        combined = {}
        for item in record["field_evidence"]:
            combined.setdefault(item["field"], []).extend(item["spans"])
        nested = [s for cause in record.get("causes", []) for s in cause["evidence"]]
        if nested:
            combined.setdefault("causes", []).extend(deepcopy(nested))
        fields = []
        for field, spans in combined.items():
            unique = []
            for span in spans:
                try:
                    aligned_spans, change = align_references(span, units)
                    if change:
                        trace.append({"record_id": record["id"], "field": field, **change})
                except ValueError as error:
                    aligned_spans = [span]
                    alignment_issues.append(
                        {"owner": record["id"], "field": field, "code": str(error)}
                    )
                for aligned in aligned_spans:
                    if aligned not in unique:
                        unique.append(aligned)
            fields.append({"field": field, "spans": unique})
        if record["field_evidence"] != fields:
            trace.append(
                {
                    "operation": "merge_field_evidence_and_derive_cause_container",
                    "record_id": record["id"],
                }
            )
        record["field_evidence"] = fields
        for cause in record.get("causes", []):
            cause_spans = []
            for span in cause["evidence"]:
                try:
                    aligned, change = align_references(span, units)
                    cause_spans.extend(aligned)
                    if change:
                        trace.append({"record_id": record["id"], **change})
                except ValueError:
                    cause_spans.append(span)  # Retain the diagnosed unsupported citation.
            cause["evidence"] = cause_spans
        prior = record["provenance"]["source_ids"]
        derived = sorted(set(prior) | {s["source_id"] for f in fields for s in f["spans"]})
        if prior != derived:
            trace.append(
                {
                    "operation": "derive_provenance_union",
                    "record_id": record["id"],
                    "before": prior,
                    "after": derived,
                }
            )
        record["provenance"]["source_ids"] = derived
    parsed = RecordExtraction.model_validate(data)
    checks = validate_records(parsed, entities, units, source_texts=source_texts)
    # Remaining issues must remain inspectable; do not erase unsupported fields.
    field_spans = []
    for record in parsed.records:
        for field in record.field_evidence:
            for span in field.spans:
                try:
                    field_spans.append(
                        {"record_id": record.id, "field": field.field, **resolve_span(span, units)}
                    )
                except ValueError:
                    continue
    return {
        "data": data,
        "canonicalization": trace,
        "validation": checks,
        "unresolved_alignment": alignment_issues,
        "field_spans": field_spans,
        "semantic_correctness": "not_assessed",
    }
