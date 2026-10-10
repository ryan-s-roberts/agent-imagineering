import json

import pytest

from property_eval.experiment_artifact import (
    assemble_experiment,
    validate_citation_catalog,
    validate_materialization,
)
from property_eval.run_artifact import assemble_run, resolve_artifacts, validate_artifact
from property_eval.submission import export_answers


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def create_inputs(tmp_path):
    baseline_path = tmp_path / "baseline"
    experiment_path = tmp_path / "experiment"
    job = {"id": "001-at-003", "case": "001", "cutoff": "003", "prefix_sha256": "prefix"}
    manifest = {"jobs": [job]}
    packet = {"prefix_sha256": "prefix", "records": [], "sources": []}
    save(baseline_path / "manifest.json", manifest)
    save(baseline_path / job["id"] / "evidence-packet.json", packet)
    baseline = assemble_run(baseline_path)
    save(experiment_path / "manifest.json", manifest)
    save(experiment_path / "experiment.json", {"arms": ["control", "progress"]})
    save(experiment_path / "evidence" / (job["id"] + ".json"), packet)
    save(
        experiment_path / "targets" / (job["id"] + ".json"),
        {"SECRET_TARGET": "never in submission"},
    )
    save(
        experiment_path / "arms" / "control" / job["id"] / "decisions.json",
        {
            "disposition": "wait",
            "actions": [],
            "rationale": {"selected_because": "Only prefix rationale"},
        },
    )
    return experiment_path, baseline, packet


def test_arms_share_exact_evidence_and_keep_denominator(tmp_path):
    root, baseline, _ = create_inputs(tmp_path)
    document = assemble_experiment(root, baseline)
    assert not validate_artifact(document)
    assert document["completion"]["expected_arm_results"] == 2
    assert document["completion"]["decisions_available"] == 1
    checkpoint = document["checkpoints"][0]
    assert (
        checkpoint["arms"]["control"]["evidence_ref"]
        == checkpoint["arms"]["progress"]["evidence_ref"]
    )
    assert "decisions.json" not in resolve_artifacts(document, checkpoint)
    assert "decisions.json" in resolve_artifacts(document, checkpoint, "control")


def test_changed_evidence_refused(tmp_path):
    root, baseline, packet = create_inputs(tmp_path)
    save(root / "evidence" / "001-at-003.json", dict(packet, added="future"))
    with pytest.raises(ValueError, match="changed frozen evidence"):
        assemble_experiment(root, baseline)


def test_submission_requires_explicit_arm_and_excludes_target(tmp_path):
    root, baseline, _ = create_inputs(tmp_path)
    document = assemble_experiment(root, baseline)
    with pytest.raises(ValueError, match="explicit declared arm"):
        export_answers(document, tmp_path / "rejected")
    export_answers(document, tmp_path / "ANSWERS", "control")
    reasoning = (tmp_path / "ANSWERS" / "1" / "REASONING.md").read_text()
    assert "Only prefix rationale" in reasoning
    assert "SECRET_TARGET" not in reasoning
    assert "Selected prompt arm: `control`" in reasoning


def test_decision_tbox_boundary_excludes_future_target(tmp_path):
    root, baseline, packet = create_inputs(tmp_path)
    tbox = {"evidence": {}, "result": {}}
    save(root / "tbox.json", tbox)
    prompts = root / "prompts"
    prompts.mkdir()
    (prompts / "control.txt").write_text("fixed control prompt")
    request = {
        "model": "fixed",
        "messages": [
            {"role": "system", "content": "fixed control prompt"},
            {
                "role": "user",
                "content": json.dumps({"ontology_tbox": tbox, "prefix_evidence": packet}),
            },
        ],
    }
    path = root / "arms" / "control" / "001-at-003" / "decisions-request.json"
    save(path, request)
    assert not validate_artifact(assemble_experiment(root, baseline))
    payload = json.loads(request["messages"][1]["content"])
    payload["historical_target"] = {"future": "leak"}
    request["messages"][1]["content"] = json.dumps(payload)
    save(path, request)
    with pytest.raises(ValueError, match="frozen prefix and Tboxes"):
        assemble_experiment(root, baseline)


def test_citation_catalog_requires_exact_source_offsets():
    catalog = {
        "sources": [{"origin": "prefix", "id": "001:L5", "text": "Repair approved."}],
        "spans": [
            {
                "id": "s1",
                "origin": "prefix",
                "source_id": "001:L5",
                "start": 0,
                "end": 6,
                "expression": "Repair",
                "occurrence": 1,
            }
        ],
    }
    assert not validate_citation_catalog(catalog)
    catalog["spans"][0]["expression"] = "Replacement"
    assert "Citation catalog expression differs from source slice" in validate_citation_catalog(
        catalog
    )


def test_judge_materialization_preserves_selection_and_support_origin():
    span = {
        "id": "s1",
        "origin": "prefix",
        "source_id": "001:L5",
        "start": 0,
        "end": 6,
        "expression": "Repair",
        "occurrence": 1,
        "path": "001:L5",
    }
    citation = {key: span[key] for key in ("origin", "source_id", "expression", "occurrence")}
    files = {
        "judge-selections.json": {"support_citations": [{"span_id": "s1"}]},
        "judge.json": {"support_citations": [citation]},
        "judge-spans.json": [{"judgment_path": "/support_citations/0", **span}],
    }
    assert not validate_materialization(files, {"spans": [span]})
    files["judge.json"]["support_citations"][0]["expression"] = "Replacement"
    assert (
        "Visible judgment differs from selected-span materialization"
        in validate_materialization(files, {"spans": [span]})
    )
    span["origin"] = "target"
    assert "Evidence support citation uses a non-prefix source" in validate_materialization(
        files, {"spans": [span]}
    )


def test_contextual_baseline_keeps_contract_separate_from_evidence(tmp_path):
    root, baseline, packet = create_inputs(tmp_path)
    save(root / "experiment.json", {"mode": "contextual_baseline", "arms": ["control"]})
    tbox = {"evidence": {}, "result": {}}
    save(root / "tbox.json", tbox)
    context = {"case_id": "001", "landlord_addressable_by_request": True}
    save(
        root / "benchmark-context.json",
        {"version": "property-benchmark-context-v1", "cases": {"001-at-003": context}},
    )
    prompts = root / "prompts"
    prompts.mkdir()
    (prompts / "control.txt").write_text("fixed prompt")
    payload = {"ontology_tbox": tbox, "prefix_evidence": packet, "benchmark_context": context}
    request = {
        "messages": [
            {"role": "system", "content": "fixed prompt"},
            {"role": "user", "content": json.dumps(payload)},
        ]
    }
    path = root / "arms" / "control" / "001-at-003" / "decisions-request.json"
    save(path, request)
    document = assemble_experiment(root, baseline)
    assert not validate_artifact(document)
    assert document["benchmark_context"]["artifact_ref"]
    assert (
        "benchmark_context"
        not in resolve_artifacts(document, document["checkpoints"][0])["evidence-packet.json"]
    )
    payload["benchmark_context"] = {"invented": "different contract"}
    request["messages"][1]["content"] = json.dumps(payload)
    save(path, request)
    with pytest.raises(ValueError, match="Decision input differs"):
        assemble_experiment(root, baseline)


def test_fresh_role_extraction_preserves_prefix_and_separates_contrast(tmp_path):
    root, baseline, packet = create_inputs(tmp_path)
    save(root / "experiment.json", {"mode": "role_extraction", "arms": ["control"]})
    fresh = {**packet, "records": [{"type": "role", "role": "landlord"}]}
    save(root / "evidence" / "001-at-003.json", fresh)
    save(root / "arms" / "control" / "001-at-003" / "records.json", {"records": fresh["records"]})
    save(root / "contrast" / "012-at-021" / "mentions-request.json", {"model": "fixed"})
    save(root / "contrast" / "012-at-021" / "mentions-response.json", {"usage": {"cost": 0.1}})
    document = assemble_experiment(root, baseline)
    assert document["completion"]["expected_checkpoints"] == 1
    assert len(document["contrasts"]) == 1
    assert document["accounting_by_scope"]["contrast"]["returned_cost_usd"] == 0.1
    checkpoint = document["checkpoints"][0]
    assert resolve_artifacts(document, checkpoint)["evidence-packet.json"] == fresh
    assert not validate_artifact(document)
    fresh["sources"] = [{"id": "future", "text": "not in prefix"}]
    save(root / "evidence" / "001-at-003.json", fresh)
    with pytest.raises(ValueError, match="changed frozen prefix/source"):
        assemble_experiment(root, baseline)
