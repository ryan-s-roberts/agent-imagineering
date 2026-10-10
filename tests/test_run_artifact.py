import json

import pytest

from property_eval.run_artifact import assemble_run, digest, validate_artifact
from property_eval.submission import export_answers


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value))


def fixture_run(tmp_path):
    job = {"id": "001-at-003", "case": "001", "cutoff": "003", "prefix_sha256": "prefix"}
    save(tmp_path / "manifest.json", {"jobs": [job]})
    directory = tmp_path / job["id"]
    packet = {"prefix_sha256": "prefix", "records": [], "sources": []}
    request = {"messages": [{"role": "user", "content": json.dumps(packet)}]}
    response = {
        "id": "provider1",
        "usage": {"cost": 0.1, "prompt_tokens": 10, "completion_tokens": 2},
    }
    save(directory / "evidence-packet.json", packet)
    save(directory / "decisions-request.json", request)
    save(directory / "decisions-response.json", response)
    save(
        directory / "decisions.json",
        {
            "disposition": "wait",
            "actions": [],
            "rationale": {"selected_because": "Pending response."},
        },
    )
    save(directory / "decision-review.json", {"status": "decision_generated", "latency_seconds": 2})
    save(directory / "observed-later.json", {"SECRET_FUTURE": "Never export this"})
    return directory, request, response


def test_resume_usage_deduplicated_unknown_billing_retained(tmp_path):
    directory, request, response = fixture_run(tmp_path)
    archive = tmp_path / "interrupted-attempts" / directory.name
    save(archive / "decisions-request.json", request)
    save(archive / "mentions-request.json", {"model": "example"})
    save(archive / "mentions-response.json", response)
    save(directory / "mentions-request.json", {"model": "example"})
    save(directory / "mentions-response.json", response)
    artifact = assemble_run(tmp_path)
    assert artifact["accounting"]["returned_cost_usd"] == 0.2
    assert artifact["accounting"]["requests_without_saved_response"] == 1
    assert artifact["accounting"]["total_cost_usd"] is None
    assert len(artifact["calls"]) == 3
    assert artifact["checkpoints"][0]["latency"]["scope"] == "continuation_only"
    assert not validate_artifact(artifact)
    assert artifact == assemble_run(tmp_path)


def test_manifest_denominator_and_integrity(tmp_path):
    fixture_run(tmp_path)
    artifact = assemble_run(tmp_path)
    artifact["accounting"]["returned_cost_usd"] = 999
    artifact["content_sha256"] = digest(
        {k: v for k, v in artifact.items() if k != "content_sha256"}
    )
    assert "Accounting mismatch" in validate_artifact(artifact)


def test_decision_boundary_rejects_future_payload(tmp_path):
    directory, _, _ = fixture_run(tmp_path)
    save(directory / "decisions-request.json", {"messages": [{"role": "user", "content": "{}"}]})
    with pytest.raises(ValueError, match="Decision input differs"):
        assemble_run(tmp_path)


def test_submission_has_numbered_case_and_no_future(tmp_path):
    fixture_run(tmp_path)
    document = assemble_run(tmp_path)
    output = tmp_path / "ANSWERS"
    export_answers(document, output)
    assert (output / "1" / "ANSWER.md").exists()
    reasoning = (output / "1" / "REASONING.md").read_text()
    assert "Pending response." in reasoning
    assert "SECRET_FUTURE" not in reasoning
    assert document["content_sha256"] in reasoning
