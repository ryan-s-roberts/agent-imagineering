import json

import pytest

from property_eval.citation_catalog import (
    build_catalog,
    json_leaf_spans,
    materialize,
    selection_schema,
)


def catalog():
    return build_catalog(
        {"sources": [{"id": "p1", "text": "Reported fault"}]},
        {"source": {"id": "t1", "text": "Please inspect\nPlease inspect"}},
        {"actions": [], "message": 'Quoted "text" and café', "recipient_id": None},
    )


def judgment(ref):
    dimension = {"verdict": "partial", "explanation": "Compare", "citations": [{"span_id": ref}]}
    return {
        "version": "soft-judge-v2",
        "overall_correspondence": "partial",
        **{
            k: dimension
            for k in [
                "action_intent",
                "participants_roles",
                "scope_conditions",
                "sequencing",
                "omissions_extras",
            ]
        },
        "target_predictability": "uncertain",
        "unobservable_target_specifics": [],
        "prediction_supportedness": "uncertain",
        "support_explanation": "Unknown",
        "support_citations": [],
        "target_encoding_concerns": [],
        "confidence": "low",
    }


def test_json_leaf_positions_are_exact_for_escapes_unicode_null_empty():
    value = {"repeated": ["same", "same"], "text": 'Quote " here', "null": None, "empty": []}
    text, spans = json_leaf_spans(value)
    assert text == json.dumps(value, ensure_ascii=False, sort_keys=True)
    assert all(json.loads(text[s["start"] : s["end"]]) is not ... for s in spans)
    assert len([s for s in spans if text[s["start"] : s["end"]] == '"same"']) == 2


def test_catalog_exact_spans_repeated_occurrences_and_enum_namespace():
    data = catalog()
    sources = {(s["origin"], s["id"]): s["text"] for s in data["sources"]}
    for span in data["spans"]:
        assert (
            sources[(span["origin"], span["source_id"])][span["start"] : span["end"]]
            == span["expression"]
        )
    assert [s["occurrence"] for s in data["spans"] if s["origin"] == "target"] == [1, 2]
    schema = selection_schema(data)
    assert schema["$defs"]["PrefixSpanSelection"]["properties"]["span_id"]["enum"] == ["span0001"]


def test_materialization_cannot_accept_unknown_or_world_support_from_prediction():
    data = catalog()
    valid, spans = materialize(judgment("span0001"), data)
    assert valid["action_intent"]["citations"][0]["expression"] == "Reported fault"
    assert len(spans) == 5
    with pytest.raises(KeyError):
        materialize(judgment("invented"), data)
    bad = judgment("span0001")
    bad["support_citations"] = [
        {"span_id": next(s["id"] for s in data["spans"] if s["origin"] == "prediction")}
    ]
    with pytest.raises(ValueError, match="prefix"):
        materialize(bad, data)
