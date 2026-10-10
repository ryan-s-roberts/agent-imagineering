import pytest

from property_eval.canonicalization import align_references
from property_eval.grounding import resolve_mentions
from property_eval.models import MentionExtraction


def test_attachment_mentions_have_page_specific_anchors():
    units = [
        {
            "id": f"doc:p{page}:L1",
            "event_id": "004",
            "anchor_namespace": f"attachment:sha:p{page}",
            "text": "Mara",
            "start": 0,
            "document_id": "doc",
            "page_number": page,
        }
        for page in (1, 2)
    ]
    candidates = MentionExtraction.model_validate(
        {
            "mentions": [
                {"source_id": u["id"], "expression": "Mara", "occurrence": 1, "kind": "person"}
                for u in units
            ]
        }
    )
    result = resolve_mentions(candidates, units, "case")
    assert result["valid"]
    assert len({m["id"] for m in result["mentions"]}) == 2
    assert [m["page_number"] for m in result["mentions"]] == [1, 2]


def test_alignment_cannot_move_evidence_between_attachment_pages():
    units = [
        {
            "id": "doc:p1:L1",
            "event_id": "004",
            "anchor_namespace": "sha:p1",
            "text": "Mara",
            "start": 0,
        },
        {
            "id": "doc:p2:L1",
            "event_id": "004",
            "anchor_namespace": "sha:p2",
            "text": "approved repair",
            "start": 0,
        },
    ]
    with pytest.raises(ValueError):
        align_references(
            {"source_id": "doc:p1:L1", "expression": "approved repair", "occurrence": 1}, units
        )
