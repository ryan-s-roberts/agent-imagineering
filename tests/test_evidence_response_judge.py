import pytest

from property_eval.evidence_response_judge import evidence_response_payload, validate_judgment


def test_evidence_assessment_rejects_target_sources():
    with pytest.raises(ValueError, match="prefix-only"):
        evidence_response_payload({}, {}, {}, {"spans": [], "sources": [{"origin": "target"}]})


def test_empty_set_requires_nonvacuous_assessment():
    raw = {
        "version": "evidence-response-v1",
        "actions": [],
        "obligations": [],
        "duplicate_action_groups": [],
        "empty_response_assessment": None,
        "representation_limits": [],
    }
    with pytest.raises(ValueError, match="explicit assessment"):
        validate_judgment(raw, {"actions": []}, {"spans": []})
    raw["empty_response_assessment"] = (
        "No actionable requirement can be established from this packet."
    )
    assert validate_judgment(raw, {"actions": []}, {"spans": []}).actions == []


def test_each_generated_action_must_be_assessed():
    raw = {
        "version": "evidence-response-v1",
        "actions": [],
        "obligations": [],
        "duplicate_action_groups": [],
        "empty_response_assessment": None,
        "representation_limits": [],
    }
    with pytest.raises(ValueError, match="exactly once"):
        validate_judgment(raw, {"actions": [{"id": "a1"}]}, {"spans": []})
