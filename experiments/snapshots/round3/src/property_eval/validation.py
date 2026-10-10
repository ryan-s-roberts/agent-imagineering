"""Grounding, domain/range checks and a deterministic evidence-state projection."""

from .grounding import resolve_span
from .models import EntityExtraction, Prefix, RecordExtraction

PARTY = {"person", "organization", "unresolved_party"}
RANGES = {
    "party_id": PARTY,
    "owner_id": PARTY,
    "provider_id": PARTY,
    "tenant_id": PARTY,
    "grantor_id": PARTY,
    "grantee_id": PARTY,
    "responsible_party_id": PARTY,
    "asserted_by_entity_id": PARTY,
    "sender_id": PARTY,
    "recipient_id": PARTY,
    "request_id": {"maintenance_request", "work_order"},
    "asset_id": {"asset"},
    "property_id": {"property"},
    "appointment_id": {"appointment"},
    "document_id": {"document", "invoice"},
    "context_id": {"property", "maintenance_request", "work_order"},
}


def source_units(prefix: Prefix) -> list[dict]:
    units = []
    for event in prefix.events:
        offset = 0
        for number, line in enumerate(event.text.splitlines(keepends=True), 1):
            text = line.rstrip("\r\n")
            if text.strip():
                units.append(
                    {
                        "id": f"{event.id}:L{number}",
                        "event_id": event.id,
                        "timestamp": event.timestamp,
                        "sender": event.sender,
                        "channel": event.channel,
                        "text": text,
                        "start": offset,
                        "end": offset + len(text),
                    }
                )
            offset += len(line)
    return units


def validate_entities(extraction: EntityExtraction, units: list[dict]) -> dict:
    sources = {u["id"]: u for u in units}
    issues, spans = [], []
    if len({e.id for e in extraction.entities}) != len(extraction.entities):
        issues.append({"code": "duplicate_entity_id"})
    for entity in extraction.entities:
        for mention in entity.mentions:
            source = sources.get(mention.source_id)
            if source is None:
                issues.append({"code": "outside_prefix", "entity": entity.id})
                continue
            start = source["text"].find(mention.surface)
            if start < 0:
                issues.append(
                    {
                        "code": "unmatched_mention",
                        "entity": entity.id,
                        "source_id": mention.source_id,
                    }
                )
                continue
            spans.append(
                {
                    "entity_id": entity.id,
                    "source_id": mention.source_id,
                    "event_id": source["event_id"],
                    "start": source["start"] + start,
                    "end": source["start"] + start + len(mention.surface),
                    "occurrences": source["text"].count(mention.surface),
                }
            )
    return {"valid": not issues, "issues": issues, "spans": spans}


def validate_records(
    extraction: RecordExtraction, entities: EntityExtraction, units: list[dict]
) -> dict:
    table = {e.id: e for e in entities.entities}
    sources = {u["id"] for u in units}
    record_ids = {r.id for r in extraction.records}
    issues = []
    if len(record_ids) != len(extraction.records):
        issues.append({"code": "duplicate_record_id"})
    if len({g.id for g in extraction.gaps}) != len(extraction.gaps):
        issues.append({"code": "duplicate_gap_id"})

    def ref(value, field, owner):
        if value is None:
            return
        if value not in table:
            issues.append({"code": "unknown_entity", "owner": owner, "field": field})
        elif field in RANGES and table[value].kind not in RANGES[field]:
            issues.append({"code": "invalid_range", "owner": owner, "field": field})

    for record in extraction.records:
        data = record.model_dump()
        for field, value in data.items():
            if field.endswith("_id") and not field.endswith("_record_id"):
                ref(value, field, record.id)
            if (
                field.endswith("_record_id")
                and value is not None
                and (value not in record_ids or value == record.id)
            ):
                issues.append(
                    {"code": "invalid_record_reference", "owner": record.id, "field": field}
                )
        required = {
            field
            for field, value in data.items()
            if field not in {"id", "type", "provenance", "field_evidence"}
            and value is not None
            and value != []
        }
        required.update(
            f"provenance.{field}"
            for field, value in data["provenance"].items()
            if field != "source_ids" and value is not None
        )
        supplied = [item.field for item in record.field_evidence]
        if len(supplied) != len(set(supplied)):
            issues.append({"code": "duplicate_field_evidence", "owner": record.id})
        for field in sorted(required - set(supplied)):
            issues.append({"code": "missing_field_evidence", "owner": record.id, "field": field})
        for item in record.field_evidence:
            if item.field not in required:
                issues.append(
                    {"code": "unexpected_field_evidence", "owner": record.id, "field": item.field}
                )
            for span in item.spans:
                try:
                    resolve_span(span, units)
                    if span.source_id not in record.provenance.source_ids:
                        raise ValueError("field_source_missing_from_provenance")
                except ValueError as error:
                    issues.append({"code": str(error), "owner": record.id, "field": item.field})
        ref(record.provenance.asserted_by_entity_id, "asserted_by_entity_id", record.id)
        if any(s not in sources for s in record.provenance.source_ids):
            issues.append({"code": "outside_prefix", "owner": record.id})
        superseded = data.get("supersedes_record_id")
        if superseded is not None:
            target = next((r for r in extraction.records if r.id == superseded), None)
            if target is None or target.type != "appointment" or superseded == record.id:
                issues.append({"code": "invalid_supersession", "owner": record.id})
    for gap in extraction.gaps:
        for entity_id in gap.entity_ids:
            ref(entity_id, "entity_id", gap.id)
        if any(s not in sources for s in gap.source_ids):
            issues.append({"code": "outside_prefix", "owner": gap.id})
    return {"valid": not issues, "issues": issues, "semantic_correctness": "not_assessed"}


def decision_packet(prefix, entities, records, units):
    if (
        not validate_entities(entities, units)["valid"]
        or not validate_records(records, entities, units)["valid"]
    ):
        raise ValueError("Invalid extraction cannot be supplied as decision state")
    by_type = {}
    for record in records.records:
        by_type.setdefault(record.type, []).append(record.id)
    return {
        "ontology_version": "property-evidence-v3",
        "case_id": prefix.case_id,
        "cutoff": prefix.cutoff,
        "prefix_sha256": prefix.source_sha256,
        "semantics": "Evidence state, not authoritative world state; claims can conflict",
        "entities": entities.model_dump()["entities"],
        "records": records.model_dump()["records"],
        "gaps": records.model_dump()["gaps"],
        "record_index": by_type,
        "sources": units,
        "field_spans": [
            {"record_id": r.id, "field": item.field, **resolve_span(span, units)}
            for r in records.records
            for item in r.field_evidence
            for span in item.spans
        ],
    }
