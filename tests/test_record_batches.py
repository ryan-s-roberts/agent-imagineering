import pytest

from property_eval.record_batches import (
    combine_record_batches,
    plan_record_batches,
    validate_batch_ownership,
)


def unit(name, text, event="001", origin="event", namespace=None):
    value = {"id": name, "text": text, "event_id": event, "origin": origin}
    if namespace:
        value["anchor_namespace"] = namespace
    return value


def test_partition_covers_all_sources_once_and_preserves_global_context():
    units = [
        unit("e1", "abc"),
        unit("e2", "def"),
        unit("p1", "abcd", origin="attachment", namespace="doc:p1"),
        unit("p2", "efgh", origin="attachment", namespace="doc:p2"),
    ]
    plan = plan_record_batches(units, max_primary_chars=6)
    assert plan["context_source_ids"] == ["e1", "e2", "p1", "p2"]
    assert [b["primary_source_ids"] for b in plan["batches"]] == [["e1", "e2"], ["p1"], ["p2"]]
    assert all(b["primary_char_count"] <= 6 for b in plan["batches"])


def test_oversize_unit_is_explicit_not_silently_truncated():
    plan = plan_record_batches([unit("s1", "1234567")], max_primary_chars=3)
    assert plan["batches"][0]["oversize_source_ids"] == ["s1"]
    assert plan["batches"][0]["primary_char_count"] == 7


def test_admission_bound_and_duplicate_sources():
    with pytest.raises(ValueError, match="limit"):
        plan_record_batches([unit("s1", "abc"), unit("s2", "def")], 3, max_batches=1)
    with pytest.raises(ValueError, match="unique"):
        plan_record_batches([unit("s1", "abc"), unit("s1", "def")])


def test_batch_ownership_requires_primary_source_without_claiming_entailment():
    output = {
        "records": [{"id": "r1", "provenance": {"source_ids": ["primary", "context"]}}],
        "gaps": [],
    }
    batch = {"id": "b001", "primary_source_ids": ["primary"]}
    validate_batch_ownership(output, batch, ["primary", "context"])
    output["records"][0]["provenance"]["source_ids"] = ["context"]
    with pytest.raises(ValueError, match="No primary"):
        validate_batch_ownership(output, batch, ["primary", "context"])


def test_merge_namespaces_only_typed_refs_and_retains_reports():
    original = {
        "records": [
            {"id": "r1", "description": "r1 is literal text", "subject_id": "entity-one"},
            {"id": "r2", "constrains_record_id": "r1", "quoted_expression": "r1"},
        ],
        "gaps": [{"id": "g1", "description": "g1", "source_ids": ["source-one"]}],
    }
    merged, lineage = combine_record_batches([("b001", original), ("b002", original)])
    assert len(merged["records"]) == 4
    assert merged["records"][1]["constrains_record_id"] == "b001:r1"
    assert merged["records"][3]["constrains_record_id"] == "b002:r1"
    assert merged["records"][0]["description"] == "r1 is literal text"
    assert merged["records"][1]["quoted_expression"] == "r1"
    assert merged["records"][0]["subject_id"] == "entity-one"
    assert original["records"][0]["id"] == "r1"
    assert len(lineage) == 6
