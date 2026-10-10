import json

import pytest

from property_eval.client import request_body
from property_eval.models import EntityExtraction, RecordExtraction
from property_eval.prefix import load_prefix
from property_eval.response import DecisionResponse, validate_response
from property_eval.validation import (
    decision_packet,
    source_units,
    validate_entities,
    validate_records,
)


@pytest.fixture
def data(tmp_path):
    directory = tmp_path / "012"
    directory.mkdir(parents=True)
    (directory / "index.md").write_text("SECRET_OUTCOME")
    (directory / "history.md").write_text("""# Case
## 2026-04-19 10:00 UTC — event 001
- **Channel:** Note
- **From:** Agency / system
- **To:** Tenant

Request: Dishwasher broken. Landlord approved GS to inspect.
## 2026-04-20 10:00 UTC — event 002
- **Channel:** Note
- **From:** Agency / system
- **To:** Tenant

SECRET_FUTURE
""")
    prefix = load_prefix(tmp_path, "012", 1)
    units = source_units(prefix)
    source = units[-1]["id"]
    entities = EntityExtraction.model_validate(
        {
            "entities": [
                {"id": i, "kind": k, "label": s, "mentions": [{"source_id": source, "surface": s}]}
                for i, k, s in [
                    ("req", "maintenance_request", "Request"),
                    ("asset", "asset", "Dishwasher"),
                    ("ll", "unresolved_party", "Landlord"),
                    ("gs", "unresolved_party", "GS"),
                ]
            ]
        }
    )
    records = RecordExtraction.model_validate(
        {
            "records": [
                {
                    "id": "approval",
                    "type": "authorization",
                    "provenance": {
                        "source_ids": [source],
                        "asserted_by_entity_id": None,
                        "origin": "attributed_report",
                        "modality": "actual",
                        "polarity": "positive",
                    },
                    "request_id": "req",
                    "grantor_id": "ll",
                    "grantee_id": "gs",
                    "scope": ["inspect"],
                    "decision": "approved",
                    "amount_minor": None,
                    "currency": None,
                    "conditions": [],
                    "field_evidence": [
                        {
                            "field": field,
                            "spans": [
                                {
                                    "source_id": source,
                                    "expression": "Landlord approved GS to inspect.",
                                    "occurrence": 1,
                                }
                            ],
                        }
                        for field in [
                            "request_id",
                            "grantor_id",
                            "grantee_id",
                            "scope",
                            "decision",
                            "provenance.origin",
                            "provenance.modality",
                            "provenance.polarity",
                        ]
                    ],
                }
            ],
            "gaps": [],
        }
    )
    return prefix, units, entities, records


def test_prefix_and_spans(data):
    prefix, units, entities, _records = data
    body = json.dumps(request_body(prefix, units, "test", 100))
    assert "SECRET" not in body
    checks = validate_entities(entities, units)
    assert checks["valid"]
    for span in checks["spans"]:
        assert prefix.events[0].text[span["start"] : span["end"]]


def test_dynamic_ids_and_closed_static_schema(data):
    prefix, units, entities, _ = data
    schema = request_body(prefix, units, "test", 100, entities)["response_format"]["json_schema"][
        "schema"
    ]
    assert schema["$defs"]["AuthorizationRecord"]["properties"]["request_id"]["enum"] == ["req"]
    assert set(schema["$defs"]["OwnershipRecord"]["properties"]["owner_id"]["enum"]) == {"ll", "gs"}
    for obj in [schema, *schema["$defs"].values()]:
        if obj.get("type") == "object":
            assert obj["additionalProperties"] is False
            assert set(obj["required"]) == set(obj["properties"])


def test_record_domain_and_provenance(data):
    prefix, units, entities, records = data
    assert validate_records(records, entities, units)["valid"]
    records.records[0].grantor_id = "asset"
    records.records[0].provenance.source_ids = ["002:L1"]
    codes = {i["code"] for i in validate_records(records, entities, units)["issues"]}
    assert codes == {"invalid_range", "outside_prefix", "field_source_missing_from_provenance"}
    with pytest.raises(ValueError, match="Invalid extraction"):
        decision_packet(prefix, entities, records, units)


def test_decision_packet_preserves_report_not_truth(data):
    prefix, units, entities, records = data
    packet = decision_packet(prefix, entities, records, units)
    assert packet["records"][0]["provenance"]["origin"] == "attributed_report"
    assert packet["records"][0]["amount_minor"] is None
    assert packet["sources"] == units
    records.records[0].scope = ["replace"]
    assert packet["records"][0]["scope"] == ["inspect"]
    assert validate_records(records, entities, units)["valid"]  # entailment isn't proven


def test_response_scope_grounding(data):
    prefix, units, entities, records = data
    packet = decision_packet(prefix, entities, records, units)
    decision = DecisionResponse.model_validate(
        {
            "ontology_version": "property-response-v4",
            "rationale": {
                "selected_because": "Inspection permission was reported.",
                "evidence": [
                    {
                        "source_id": units[-1]["id"],
                        "expression": "Landlord approved GS to inspect.",
                        "occurrence": 1,
                    }
                ],
                "uncertainties": [],
                "assumptions": [],
                "alternatives_considered": [],
            },
            "human_interventions": [],
            "case_id": prefix.case_id,
            "disposition": "act",
            "conclusion_record_ids": [],
            "actions": [
                {
                    "id": "a1",
                    "type": "instruct_provider",
                    "request_id": "req",
                    "basis_record_ids": ["approval"],
                    "basis_gap_ids": [],
                    "depends_on_action_ids": [],
                    "provider_id": "gs",
                    "scope": ["inspect"],
                    "authorization_record_ids": ["approval"],
                    "conditions": [],
                }
            ],
        }
    )
    assert validate_response(decision, packet)["valid"]
    decision.actions[0].scope = ["replace"]
    assert "authorization_scope_mismatch" in validate_response(decision, packet)["issues"]
    decision.actions[0].basis_record_ids = ["made-up"]
    assert "unknown_basis_record" in validate_response(decision, packet)["issues"]


def test_unknown_record_class_rejected():
    with pytest.raises(ValueError):
        RecordExtraction.model_validate({"records": [{"type": "invented_relation"}], "gaps": []})
