"""Auditable span alignment and case-local, source-anchored entity identity."""

from .models import EntityExtraction

APOSTROPHES = str.maketrans({"’": "'", "‘": "'"})


def resolve_span(span, units):
    """Only exact or declared one-codepoint apostrophe alignment; never fuzzy search."""
    data = span.model_dump() if hasattr(span, "model_dump") else span
    source = next((u for u in units if u["id"] == data["source_id"]), None)
    if source is None:
        raise ValueError("outside_prefix")
    expression = data["expression"]
    text = source["text"]
    mode = "exact"
    search_text, search_expression = text, expression
    if expression not in text:
        search_text = text.translate(APOSTROPHES)
        search_expression = expression.translate(APOSTROPHES)
        mode = "apostrophe_alignment"
    offsets = []
    start = search_text.find(search_expression)
    while start >= 0:
        offsets.append(start)
        start = search_text.find(search_expression, start + 1)
    occurrence = data["occurrence"]
    if occurrence < 1 or occurrence > len(offsets):
        raise ValueError("unmatched_expression_or_occurrence")
    start = offsets[occurrence - 1]
    end = start + len(expression)
    return {
        **data,
        "event_id": source["event_id"],
        "start": source["start"] + start,
        "end": source["start"] + end,
        "source_expression": text[start:end],
        "alignment": mode,
        "occurrences": len(offsets),
    }


def resolve_mentions(extraction, units, case_id):
    mentions, issues, seen = [], [], set()
    for index, mention in enumerate(extraction.mentions):
        try:
            resolved = resolve_span(mention, units)
            anchor = f"{case_id}:{resolved['event_id']}:{resolved['start']}:{resolved['end']}"
            if anchor in seen:
                raise ValueError("duplicate_mention_anchor")
            seen.add(anchor)
            mentions.append({"id": anchor, **resolved})
        except ValueError as error:
            issues.append({"index": index, "code": str(error)})
    return {"valid": not issues, "issues": issues, "mentions": mentions}


def link_entities(extraction, mentions, units):
    table = {m["id"]: m for m in mentions}
    parent = {m: m for m in table}
    issues, links = [], []

    def root(value):
        while parent[value] != value:
            value = parent[value]
        return value

    for index, link in enumerate(extraction.links):
        left, right = link.left_mention_id, link.right_mention_id
        try:
            if left not in table or right not in table or left == right:
                raise ValueError("invalid_link_endpoint")
            evidence = [resolve_span(s, units) for s in link.evidence]
            if link.relationship == "same":
                if table[left]["kind"] != table[right]["kind"]:
                    raise ValueError("identity_kind_conflict")
                # Grounded linking is a prediction, not a proven entailment.
                a, b = sorted([root(left), root(right)])
                parent[b] = a
            links.append({**link.model_dump(), "resolved_evidence": evidence})
        except ValueError as error:
            issues.append({"index": index, "code": str(error)})
    for link in links:
        if link["relationship"] == "different" and root(link["left_mention_id"]) == root(
            link["right_mention_id"]
        ):
            issues.append({"code": "identity_link_contradiction"})
    groups = {}
    for mention in mentions:
        groups.setdefault(root(mention["id"]), []).append(mention)
    entities = []
    for anchor, members in sorted(groups.items()):
        entities.append(
            {
                "id": f"entity:{anchor}",
                "kind": members[0]["kind"],
                "label": members[0]["source_expression"],
                "mentions": [
                    {"source_id": m["source_id"], "surface": m["source_expression"]}
                    for m in members
                ],
            }
        )
    return EntityExtraction.model_validate({"entities": entities}), {
        "valid": not issues,
        "issues": issues,
        "links": links,
        "mention_entity_map": {m: f"entity:{root(m)}" for m in table},
    }
