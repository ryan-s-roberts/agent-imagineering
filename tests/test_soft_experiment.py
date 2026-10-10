import json
from pathlib import Path

from property_eval.soft_eval import HistoricalTarget
from property_eval.soft_experiment import citation_checks, decision_payload, judge_payload


def test_decision_receives_both_tboxes_and_prefix_only():
    packet = {"case_id": "property-001", "sources": []}
    tbox = {
        "evidence": {"schema": "evidence"},
        "result": {"schema": "response"},
        "semantics": "open world",
    }
    payload = decision_payload(packet, tbox)
    assert set(payload) == {"ontology_tbox", "prefix_evidence"}
    assert payload["ontology_tbox"]["evidence"] and payload["ontology_tbox"]["result"]
    assert "target" not in payload


def test_targets_preserve_unknown_identity_and_original_anchors():
    rows = json.loads(Path("annotations/historical-targets-v1.json").read_text())["targets"]
    assert len(rows) == 40
    for row in rows:
        target = HistoricalTarget.model_validate(row)
        assert target.visibility == "evaluation_only"
        assert all(actor.prefix_entity_id is None for actor in target.actors)
        for item in target.actions:
            assert item.action.request_id is None
            assert "request_id" in item.unknown_slots
            assert item.evidence[0].expression in target.source["text"]


def test_judge_blinding_and_citation_validation():
    packet = {"sources": [{"id": "s1", "text": "Reported fault"}]}
    target = {"source": {"id": "t1", "text": "Please inspect"}}
    prediction = {"actions": []}
    payload = judge_payload(packet, {}, target, prediction)
    assert "arm" not in payload
    judgment = {
        "support_citations": [
            {"origin": "prefix", "source_id": "s1", "expression": "Reported fault", "occurrence": 1}
        ]
    }
    assert not citation_checks(judgment, packet, target, prediction)["invalid_citations"]
    judgment["support_citations"][0]["expression"] = "Invented"
    assert citation_checks(judgment, packet, target, prediction)["invalid_citations"]
