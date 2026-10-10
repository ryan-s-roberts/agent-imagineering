import json

import pytest

from property_eval.scoring import score_reference


def test_probe_alternatives_and_missing_output(tmp_path):
    (tmp_path / "sources.json").write_text(
        json.dumps({"sources": [{"id": "001:L1", "event_id": "001", "start": 0, "text": "Pump"}]})
    )
    (tmp_path / "input.json").write_text(json.dumps({"source_sha256": "abc"}))
    reference = {
        "id": "case",
        "split": "development",
        "prefix_sha256": "abc",
        "probes": [
            {
                "id": "asset",
                "kind": "mention",
                "alternatives": [
                    {"source_id": "001:L1", "expression": "Pump", "occurrence": 1, "kind": "asset"}
                ],
            }
        ],
    }
    assert score_reference(reference, tmp_path)["matched"] == 0
    (tmp_path / "mentions.json").write_text(
        json.dumps({"mentions": [{"event_id": "001", "start": 0, "end": 4, "kind": "asset"}]})
    )
    assert score_reference(reference, tmp_path)["matched"] == 1
    reference["prefix_sha256"] = "wrong"
    with pytest.raises(ValueError, match="digest mismatch"):
        score_reference(reference, tmp_path)
