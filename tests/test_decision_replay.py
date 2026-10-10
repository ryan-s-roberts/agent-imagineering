import asyncio
import json

import pytest

from property_eval.decision_replay import decision_request
from property_eval.response import DecisionResponse, validate_response


def test_resume_reuses_exact_response_without_network(tmp_path, monkeypatch):
    from property_eval import decision_replay

    body = {"model": "test", "messages": []}
    raw = {"usage": {"cost": 0.12}}
    (tmp_path / "sample-request.json").write_text(json.dumps(body))
    (tmp_path / "sample-response.json").write_text(json.dumps(raw))
    monkeypatch.setattr(decision_replay, "parse_response", lambda response, _: response)

    async def forbidden(*args):
        raise AssertionError("Paid cached stage must not repeat")

    monkeypatch.setattr(decision_replay, "complete", forbidden)
    usage = {}
    output = asyncio.run(
        decision_replay.structured_call(None, None, body, None, tmp_path, "sample", usage)
    )
    assert output == raw
    assert usage == {"sample": {"cost": 0.12}}
    with pytest.raises(ValueError, match="differs"):
        asyncio.run(
            decision_replay.structured_call(
                None, None, {"model": "changed"}, None, tmp_path, "sample", {}
            )
        )


def test_request_contains_only_supplied_prefix_packet():
    packet = {
        "case_id": "property-001",
        "records": [],
        "sources": [{"id": "001:L1", "text": "Prefix only"}],
    }
    request = decision_request(packet, "baseline", "openai/gpt-6-luna", 1000)
    assert json.loads(request["messages"][1]["content"]) == packet
    assert "target" not in request["messages"][1]["content"]
    assert request["response_format"]["json_schema"]["schema"]["properties"]["rationale"]


def test_wrong_or_unsupported_decision_remains_parseable_and_reviewable():
    response = DecisionResponse.model_validate(
        {
            "ontology_version": "property-response-v4",
            "case_id": "property-001",
            "disposition": "wait",
            "rationale": {
                "selected_because": "Maybe the provider will respond.",
                "evidence": [],
                "uncertainties": ["Provider unknown"],
                "assumptions": ["A request may have been sent"],
                "alternatives_considered": ["Ask for clarification"],
            },
            "actions": [
                {
                    "id": "a1",
                    "type": "await_response",
                    "request_id": "wrong-request",
                    "basis_record_ids": [],
                    "basis_gap_ids": [],
                    "depends_on_action_ids": [],
                    "responsible_party_id": None,
                    "awaited": "approval",
                }
            ],
            "human_interventions": [],
            "conclusion_record_ids": [],
        }
    )
    checks = validate_response(
        response,
        {"case_id": "property-001", "entities": [], "records": [], "gaps": [], "sources": []},
    )
    assert not checks["valid"]
    assert {"missing_rationale_citations", "unsupported_action_basis", "invalid_request"} <= set(
        checks["issues"]
    )
