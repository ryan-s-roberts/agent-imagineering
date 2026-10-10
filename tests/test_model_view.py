from property_eval.model_view import ModelView


def test_global_aliases_roundtrip_preserves_prose_and_batch_groups():
    sources = [
        {"id": "event:L1", "event_id": "001", "text": "Original name", "start": 0, "end": 13},
        {
            "id": "long:attachment:hash:p1:L1",
            "event_id": "002",
            "text": "Quoted claim",
            "start": 0,
            "end": 12,
            "origin": "attachment",
            "page_number": 1,
        },
    ]
    view = ModelView(sources)
    view.extend_mentions([{"id": "mention:long"}])
    view.extend_entities([{"id": "entity:long"}])
    view.extend_records([{"id": "record:long"}])
    value = {
        "source_id": sources[1]["id"],
        "subject_id": "entity:long",
        "record_ids": ["record:long"],
        "left_mention_id": "mention:long",
        "expression": "entity:long",
        "rationale": "entity:long",
    }
    compact = view.encode_output(value)
    assert compact["subject_id"] == "e1"
    assert compact["expression"] == compact["rationale"] == "entity:long"
    assert view.decode_output(compact) == value
    schema = {"properties": {"source_id": {"type": "string", "enum": [sources[1]["id"]]}}}
    full, encoded_schema = view.encode_call({"sources": sources}, schema)
    subset, _ = view.encode_call({"sources": sources[1:]}, schema)
    assert subset["sources"] == full["sources"][1:]
    assert [row["text"] for row in full["sources"]] == [row["text"] for row in sources]
    assert encoded_schema["properties"]["source_id"]["enum"] == [compact["source_id"]]
    assert all(set(row) == {"id", "text", "group_id"} for row in full["sources"])


def test_extending_map_never_renumbers_existing_id():
    view = ModelView([])
    view.extend_entities([{"id": "z"}])
    view.extend_entities([{"id": "a"}, {"id": "z"}])
    assert view.alias_artifact()["maps"]["entity"] == {"z": "e1", "a": "e2"}


def test_body_preserves_common_prefix_and_aliases_last_ownership_message():
    import json

    sources = [{"id": "original", "event_id": "001", "text": "Raw prose", "start": 0, "end": 9}]
    view = ModelView(sources)
    body = {
        "messages": [
            {"role": "system", "content": "Instructions refer to original literally."},
            {"role": "user", "content": json.dumps({"sources": sources})},
            {"role": "user", "content": json.dumps({"primary_source_ids": ["original"]})},
        ],
        "response_format": {
            "json_schema": {"schema": {"properties": {"source_id": {"enum": ["original"]}}}}
        },
    }
    encoded = view.encode_body(body)
    assert encoded["messages"][0] == body["messages"][0]
    assert json.loads(encoded["messages"][-1]["content"]) == {"primary_source_ids": ["s1"]}
    assert json.loads(encoded["messages"][1]["content"])["sources"][0]["text"] == "Raw prose"
    assert json.loads(body["messages"][-1]["content"])["primary_source_ids"] == ["original"]


def test_current_typed_reference_inventory_is_complete():
    from property_eval.models import (
        EntityExtraction,
        LinkExtraction,
        MentionExtraction,
        RecordExtraction,
    )
    from property_eval.response import DecisionResponse

    intentional = {
        "case_id",
        "basis_gap_ids",
        "outstanding_gap_ids",
        "gap_ids",
        "depends_on_action_ids",
        "blocked_action_ids",
        "escalation_action_id",
    }
    for model in (
        MentionExtraction,
        LinkExtraction,
        EntityExtraction,
        RecordExtraction,
        DecisionResponse,
    ):
        schema = model.model_json_schema()
        for name, node in {"ROOT": schema, **schema.get("$defs", {})}.items():
            for field in node.get("properties", {}):
                if field.endswith(("_id", "_ids")):
                    assert field in intentional or ModelView._kind(field), (name, field)


def test_v2_complete_references_and_historical_v1_projection():
    current = ModelView([])
    current.extend_records([{"id": "b001:r1"}])
    current.extend_entities([{"id": "appointment:original"}])
    original = {
        "supersedes_record_id": "b001:r1",
        "responds_to_record_id": "b001:r1",
        "constrains_record_id": "b001:r1",
        "previous_intervention_record_id": "b001:r1",
        "completion_record_ids": ["b001:r1"],
        "authorization_record_ids": ["b001:r1"],
        "about_record_ids": ["b001:r1"],
        "obligation_record_id": "b001:r1",
        "replaces_appointment_id": "appointment:original",
    }
    compact = current.encode_output(original)
    assert {str(v) for v in compact.values()} == {"r1", "['r1']", "e1"}
    assert current.decode_output(compact) == original
    historical = ModelView([], version="model-view-v1")
    historical.maps = current.maps
    assert historical.encode_output(original) == original
    assert current.alias_artifact()["version"] == "model-view-v2"
