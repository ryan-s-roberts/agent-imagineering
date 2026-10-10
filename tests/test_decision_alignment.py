from property_eval.decision_alignment import align_decision


def test_citation_normalization_does_not_change_choice_or_rationale():
    original = {
        "rationale": {
            "selected_because": "Review is required.",
            "evidence": [{"source_id": "001:L1", "expression": "manual review", "occurrence": 1}],
        },
        "actions": [{"type": "escalate", "request_id": "unresolved", "basis_record_ids": []}],
    }
    units = [{"id": "001:L1", "event_id": "001", "text": "Manual review required.", "start": 0}]
    result = align_decision(original, units)
    assert result["response"]["actions"] == original["actions"]
    assert (
        result["response"]["rationale"]["selected_because"]
        == original["rationale"]["selected_because"]
    )
    assert result["response"]["rationale"]["evidence"][0]["expression"] == "Manual review"
    assert original["rationale"]["evidence"][0]["expression"] == "manual review"
    assert result["canonicalization"]


def test_missing_quote_is_retained_as_unsupported_citation():
    original = {
        "evidence": [{"source_id": "001:L1", "expression": "approval granted", "occurrence": 1}]
    }
    units = [{"id": "001:L1", "event_id": "001", "text": "Approval requested.", "start": 0}]
    result = align_decision(original, units)
    assert result["response"] == original
    assert result["unresolved_citations"]
