from property_eval.models import EntityExtraction, RecordExtraction
from property_eval.validation import validate_records


def fixture():
    text = "Request R17: A supervisor review is required because the two inspections disagree."
    units = [{"id": "001:L1", "event_id": "001", "start": 0, "text": text}]
    entities = EntityExtraction.model_validate(
        {
            "entities": [
                {
                    "id": "request",
                    "kind": "maintenance_request",
                    "label": "R17",
                    "mentions": [{"source_id": "001:L1", "surface": "Request R17"}],
                }
            ]
        }
    )
    span = {"source_id": "001:L1", "expression": text, "occurrence": 1}
    record = {
        "id": "review",
        "type": "human_intervention",
        "request_id": "request",
        "provenance": {
            "source_ids": ["001:L1"],
            "asserted_by_entity_id": None,
            "origin": "system_record",
            "modality": "requested",
            "polarity": "positive",
        },
        "status": "required",
        "responsible_role": "supervisor",
        "responsible_party_id": None,
        "requested_intervention": "adjudicate_evidence",
        "intervention_detail": "Review conflicting inspections",
        "causes": [
            {
                "category": "conflicting_evidence",
                "explanation": "Two inspections disagree",
                "causal_status": "asserted",
                "evidence": [span],
                "record_ids": [],
            }
        ],
        "blocking_context": None,
        "blocked_record_ids": [],
        "blocking_effect": "unknown",
        "response_record_ids": [],
        "previous_intervention_record_id": None,
    }
    fields = [
        k
        for k, v in record.items()
        if k not in {"id", "type", "provenance"} and v is not None and v != []
    ]
    fields += ["provenance.origin", "provenance.modality", "provenance.polarity"]
    record["field_evidence"] = [{"field": name, "spans": [span]} for name in fields]
    return RecordExtraction.model_validate({"records": [record], "gaps": []}), entities, units


def test_required_review_preserves_asserted_cause_without_sent_action():
    records, entities, units = fixture()
    assert validate_records(records, entities, units)["valid"]
    assert records.records[0].status == "required"
    assert records.records[0].responsible_party_id is None
    assert records.records[0].causes[0].causal_status == "asserted"


def test_resolution_requires_response_and_release_is_not_implied():
    records, entities, units = fixture()
    record = records.records[0]
    record.status = "resolved"
    codes = {i["code"] for i in validate_records(records, entities, units)["issues"]}
    assert {"missing_human_response", "unobserved_intervention_transition"} <= codes
    record.status = "required"
    record.blocking_effect = "released"
    assert "unsupported_blocker_release" in {
        i["code"] for i in validate_records(records, entities, units)["issues"]
    }


def test_cause_evidence_and_causal_uncertainty_remain_distinct():
    records, entities, units = fixture()
    cause = records.records[0].causes[0]
    cause.causal_status = "unresolved"
    assert validate_records(records, entities, units)["valid"]
    cause.evidence[0].source_id = "002:L1"
    assert "outside_prefix" in {
        i["code"] for i in validate_records(records, entities, units)["issues"]
    }


def test_response_must_be_an_answered_communication_not_the_intervention_itself():
    records, entities, units = fixture()
    records.records[0].response_record_ids = ["review"]
    codes = {i["code"] for i in validate_records(records, entities, units)["issues"]}
    assert "invalid_record_reference" in codes
    assert "response_not_answered" in codes
