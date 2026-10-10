import asyncio

from property_eval.decision_replay import (
    OutputLimitError,
    execute_record_subdivisions,
    structured_call,
)
from property_eval.models import RecordExtraction


def test_length_subdivides_only_failed_batch_and_retains_sibling():
    units = [{"id": f"s{i}", "text": "data"} for i in range(4)]
    failed = {
        "id": "b1",
        "primary_source_ids": ["s0", "s1"],
        "primary_char_count": 8,
        "origin": "event",
    }
    sibling = {
        "id": "b2",
        "primary_source_ids": ["s2", "s3"],
        "primary_char_count": 8,
        "origin": "event",
    }
    calls, splits = [], []

    async def leaf(batch):
        calls.append(batch["id"])
        if batch["id"] == "b1":
            raise OutputLimitError("retained raw output")
        return batch["primary_source_ids"]

    async def run():
        return await asyncio.gather(
            *[execute_record_subdivisions(b, units, leaf, splits.append) for b in [failed, sibling]]
        )

    result = asyncio.run(run())
    assert calls.count("b1") == calls.count("b2") == 1
    assert {x for group in result for _, owned in group for x in owned} == {"s0", "s1", "s2", "s3"}
    assert [s["parent"]["id"] for s in splits] == ["b1"]
    assert result[1] == [("b2", ["s2", "s3"])]


def test_length_does_not_retry_same_fullsize_request(monkeypatch, tmp_path):
    calls = []

    async def complete(client, key, body):
        calls.append(body)
        return {"choices": [{"finish_reason": "length", "message": {"content": "{"}}], "usage": {}}

    monkeypatch.setattr("property_eval.decision_replay.complete", complete)

    async def run():
        try:
            await structured_call(
                None,
                "unused",
                {"messages": []},
                RecordExtraction,
                tmp_path,
                "records-b1",
                {},
                subdivide_on_length=True,
            )
        except OutputLimitError:
            return
        raise AssertionError("length not surfaced")

    asyncio.run(run())
    assert len(calls) == 1
    assert (tmp_path / "records-b1-response.json").exists()
    assert not (tmp_path / "records-b1-repair-request.json").exists()
