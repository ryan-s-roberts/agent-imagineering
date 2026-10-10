from types import SimpleNamespace

import pytest

from property_eval.agent_action_checkpoints import Span, resolve, wire_schema


def test_citation_cannot_cross_prefix_target_partition():
    span = Span(event_id="002", expression="Approved", occurrence=1)
    with pytest.raises(ValueError, match="outside permitted partition"):
        resolve(span, {"001": SimpleNamespace(text="Await approval")})


def test_exact_repeat_occurrence_is_preserved():
    result = resolve(
        Span(event_id="001", expression="yes", occurrence=2),
        {"001": SimpleNamespace(text="yes or yes")},
    )
    assert (result["start"], result["end"]) == (7, 10)


def test_provider_schema_keeps_action_union_and_requires_nullable_fields():
    schema = wire_schema()
    assert "anyOf" in schema["$defs"]["AgentAct"]["properties"]["action"]

    def check(node):
        if isinstance(node, dict):
            assert "oneOf" not in node
            assert "default" not in node
            if node.get("type") == "object":
                assert set(node["required"]) == set(node["properties"])
            for value in node.values():
                check(value)
        elif isinstance(node, list):
            for value in node:
                check(value)

    check(schema)
