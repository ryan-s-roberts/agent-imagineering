from types import SimpleNamespace

from property_eval.late_checkpoints import episodes


def event(number, minute, sender="Agency / system", channel="Email"):
    return SimpleNamespace(
        id=f"{number:03}",
        timestamp=f"2025-01-01 {minute // 60:02}:{minute % 60:02}:00 UTC",
        sender=sender,
        channel=channel,
    )


def test_external_observation_and_time_gap_end_episode():
    events = [
        event(1, 0),
        event(2, 1, channel="Hold"),
        event(3, 2, sender="Tenant"),
        event(4, 3),
        event(5, 90),
    ]
    assert [[e.id for e in block] for block in episodes(events)] == [
        ["001", "002"],
        ["004"],
        ["005"],
    ]


def test_notes_alone_are_not_action_episode():
    assert episodes([event(1, 0, channel="Note")]) == []
    assert len(episodes([event(1, 0, channel="Note"), event(2, 1, channel="Update")])) == 1
