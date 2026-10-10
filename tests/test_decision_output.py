from property_eval.decision_output import decision_output


def test_original_messages_and_normalized_response_stay_distinct():
    original = {"content": '{"actions":[{"basis_record_ids":["r1"]}]}'}
    normalized = {"actions": [{"basis_record_ids": ["b001:r1"]}]}
    result = decision_output(
        {
            "decisions-response.json": {"choices": [{"message": original}]},
            "decisions.json": normalized,
        }
    )
    assert result["provider_attempts"][0]["messages"] == [original]
    assert result["normalized_response"] == normalized
    assert result["decoded_before_citation_normalization"] is None


def test_missing_output_is_unavailable():
    result = decision_output({})
    assert result["available"] is False
    assert result["normalized_response"] is None
    assert result["provider_attempts"] == []
