from property_eval.models import RecordExtraction
from property_eval.record_wire import derive_record_source_ids, record_wire_schema


def test_wire_omits_only_redundant_source_ids():
    original = RecordExtraction.model_json_schema()
    wire = record_wire_schema(original)
    assert "source_ids" in original["$defs"]["Provenance"]["properties"]
    assert "source_ids" not in wire["$defs"]["Provenance"]["properties"]
    assert (
        wire["$defs"]["Provenance"]["properties"]["asserted_by_entity_id"]
        == original["$defs"]["Provenance"]["properties"]["asserted_by_entity_id"]
    )


def test_union_preserves_unknown_and_exact_evidence():
    raw = {
        "records": [
            {
                "provenance": {"asserted_by_entity_id": None},
                "field_evidence": [{"spans": [{"source_id": "s2"}, {"source_id": "s2"}]}],
                "causes": [{"evidence": [{"source_id": "s1"}]}],
            }
        ]
    }
    canonical = derive_record_source_ids(raw)
    assert canonical["records"][0]["provenance"] == {
        "asserted_by_entity_id": None,
        "source_ids": ["s1", "s2"],
    }
    assert "source_ids" not in raw["records"][0]["provenance"]


def test_empty_evidence_does_not_manufacture_provenance():
    assert derive_record_source_ids({"records": [{"provenance": {}}]}) == {
        "records": [{"provenance": {"source_ids": []}}]
    }
