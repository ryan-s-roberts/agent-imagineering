from property_eval.models import EntityExtraction, ObservationRecord, RecordExtraction
from property_eval.validation import validate_records


def observation():
    expression = "Sensor appears to read 18 C"
    data = {
        "id": "o1",
        "type": "observation",
        "subject_id": "sensor",
        "location_text": None,
        "observation_kind": "measurement",
        "attribute": "temperature",
        "value": {"kind": "number", "value": 18.0, "unit": "C"},
        "quoted_expression": expression,
        "epistemic_status": "appears",
        "observed_at_text": None,
        "provenance": {
            "source_ids": ["s1"],
            "asserted_by_entity_id": None,
            "origin": "document_report",
            "modality": "actual",
            "polarity": "positive",
        },
        "field_evidence": [],
    }
    fields = [
        "subject_id",
        "observation_kind",
        "attribute",
        "value",
        "quoted_expression",
        "epistemic_status",
        "provenance.origin",
        "provenance.modality",
        "provenance.polarity",
    ]
    data["field_evidence"] = [
        {"field": f, "spans": [{"source_id": "s1", "expression": expression, "occurrence": 1}]}
        for f in fields
    ]
    return data


def check(data):
    entities = EntityExtraction.model_validate(
        {
            "entities": [
                {
                    "id": "sensor",
                    "kind": "asset",
                    "label": "Sensor",
                    "mentions": [{"source_id": "s1", "surface": "Sensor"}],
                }
            ]
        }
    )
    return validate_records(
        RecordExtraction(records=[ObservationRecord.model_validate(data)], gaps=[]),
        entities,
        [{"id": "s1", "event_id": "001", "start": 0, "text": "Sensor appears to read 18 C"}],
    )


def test_observation_preserves_document_report_and_hedge():
    assert check(observation())["valid"]


def test_observation_cannot_rewrite_quoted_expression():
    data = observation()
    data["quoted_expression"] = "Sensor reads 18 C"
    assert "observation_quote_not_exact" in {x["code"] for x in check(data)["issues"]}


def test_presence_requires_boolean():
    data = observation()
    data["observation_kind"] = "presence"
    assert "presence_requires_boolean" in {x["code"] for x in check(data)["issues"]}


def test_wrapped_quote_requires_verified_whitespace_between_spans():
    data = observation()
    data["quoted_expression"] += " with label"
    field = next(f for f in data["field_evidence"] if f["field"] == "quoted_expression")
    field["spans"].append({"source_id": "s2", "expression": "with label", "occurrence": 1})
    entities = EntityExtraction.model_validate(
        {
            "entities": [
                {
                    "id": "sensor",
                    "kind": "asset",
                    "label": "Sensor",
                    "mentions": [{"source_id": "s1", "surface": "Sensor"}],
                }
            ]
        }
    )
    records = RecordExtraction(records=[ObservationRecord.model_validate(data)], gaps=[])
    first = "Sensor appears to read 18 C"
    for gap, accepted in [("\n", True), (" hidden words ", False)]:
        text = first + gap + "with label"
        units = [
            {"id": "s1", "event_id": "001", "start": 0, "text": first},
            {"id": "s2", "event_id": "001", "start": len(first + gap), "text": "with label"},
        ]
        result = validate_records(records, entities, units, source_texts={"001": text})
        quote_errors = [e for e in result["issues"] if e["code"] == "observation_quote_not_exact"]
        assert (not quote_errors) is accepted
        assert bool(result["quote_normalizations"]) is accepted
