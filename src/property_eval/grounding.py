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
        **{
            k: source[k]
            for k in (
                "anchor_namespace",
                "document_id",
                "document_sha256",
                "page_number",
                "text_sha256",
                "offset_basis",
                "available_at_event_ids",
            )
            if k in source
        },
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
            anchor_context = resolved.get("anchor_namespace", resolved["event_id"])
            anchor = f"{case_id}:{anchor_context}:{resolved['start']}:{resolved['end']}"
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
                kinds = {table[left]["kind"], table[right]["kind"]}
                role_named_party = "role_party" in kinds and kinds <= {
                    "role_party",
                    "person",
                    "organization",
                }
                if len(kinds) != 1 and not role_named_party:
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
        # Identity merging is selected by the model above. This only retains the
        # named classification when a grounded role/name identity link exists.
        representative = next(
            (m for m in members if m["kind"] in {"person", "organization"}), members[0]
        )
        entities.append(
            {
                "id": f"entity:{anchor}",
                "kind": representative["kind"],
                "label": representative["source_expression"],
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
