from property_eval.benchmark_context import context_for_case
from property_eval.response import DecisionResponse, validate_response


def test_known_contextual_landlord_needs_no_invented_person():
    context = context_for_case("property-001")
    response = DecisionResponse.model_validate(
        {
            "ontology_version": "property-response-v4",
            "case_id": "property-001",
            "disposition": "act",
            "rationale": {
                "selected_because": "Ask the known landlord role for permission.",
                "evidence": [{"source_id": "s1", "expression": "Door stuck", "occurrence": 1}],
                "uncertainties": [],
                "assumptions": ["Landlord is addressable by benchmark context"],
                "alternatives_considered": [],
            },
            "actions": [
                {
                    "id": "a1",
                    "type": "request_approval",
                    "request_id": "r1",
                    "basis_record_ids": ["issue"],
                    "basis_gap_ids": [],
                    "depends_on_action_ids": [],
                    "recipient_id": context["addressable_roles"][0],
                    "scope": ["inspect"],
                    "proposed_amount_minor": None,
                    "currency": None,
                }
            ],
            "conclusion_record_ids": [],
            "human_interventions": [],
        }
    )
    packet = {
        "case_id": "property-001",
        "entities": [{"id": "r1", "kind": "maintenance_request"}],
        "records": [{"id": "issue", "request_id": "r1"}],
        "gaps": [],
        "sources": [{"id": "s1", "text": "Door stuck", "event_id": "001", "start": 0}],
    }
    assert validate_response(response, packet, context)["valid"]
    assert "invalid_party" in validate_response(response, packet)["issues"]
    wrong_context = context_for_case("property-002")
    assert "invalid_party" in validate_response(response, packet, wrong_context)["issues"]
    assert len(packet["entities"]) == 1  # No fabricated landlord entity.
