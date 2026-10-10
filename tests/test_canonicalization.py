import pytest

from property_eval.canonicalization import align_reference, align_references, canonicalize_mentions


def unit(source_id, text, start=0):
    return {
        "id": source_id,
        "event_id": source_id.split(":")[0],
        "text": text,
        "start": start,
        "end": start + len(text),
    }


def test_typography_keeps_source_coordinates():
    source = unit("001:L1", "The Washing machine isn’t working.", 20)
    result, audit = align_reference(
        {"source_id": source["id"], "expression": "washing machine isn't working", "occurrence": 1},
        [source],
    )
    assert result["expression"] == "Washing machine isn’t working"
    assert audit["event_start"] == 24
    assert audit["event_end"] == 53


def test_ambiguous_normalization_is_not_guessed():
    with pytest.raises(ValueError, match="ambiguous"):
        align_reference(
            {"source_id": "001:L1", "expression": "ALICE", "occurrence": 1},
            [unit("001:L1", "Alice met alice")],
        )


def test_wrapped_quote_splits_into_original_lines():
    sources = [
        unit("001:L1", "the lock engaged so", 4),
        unit("001:L2", "the door stayed closed", 24),
    ]
    spans, audit = align_references(
        {"source_id": "001:L1", "expression": "lock engaged so the door stayed", "occurrence": 1},
        sources,
    )
    assert [s["expression"] for s in spans] == ["lock engaged so", "the door stayed"]
    assert audit["operation"] == "split_wrapped_source_quote"


def test_wrong_line_can_align_only_within_event():
    span = {"source_id": "001:L2", "expression": "Hold", "occurrence": 1}
    sources = [unit("001:L1", "Channel: Hold"), unit("001:L2", "Review workload")]
    assert align_references(span, sources)[0][0]["source_id"] == "001:L1"
    with pytest.raises(ValueError):
        align_references(span, [sources[1], unit("002:L1", "Hold")])


def test_identical_mentions_are_deduplicated():
    mention = {"kind": "person", "source_id": "001:L1", "expression": "Alice", "occurrence": 1}
    result = canonicalize_mentions(
        {"mentions": [mention, mention]}, [unit("001:L1", "Alice")], "case"
    )
    assert result["valid"]
    assert len(result["mentions"]) == 1
