import pytest

from property_eval.record_batches import subdivide_record_batch


def fixtures():
    units = [{"id": f"s{i}", "text": "x" * size} for i, size in enumerate([2, 8, 3, 7])]
    batch = {"id": "b003", "primary_source_ids": [u["id"] for u in units], "origin": "attachment"}
    return batch, units


def test_subdivision_preserves_order_identity_and_balances_volume():
    batch, units = fixtures()
    children = subdivide_record_batch(batch, units)
    assert [c["id"] for c in children] == ["b003.1", "b003.2"]
    assert [c["primary_char_count"] for c in children] == [10, 10]
    assert [s for c in children for s in c["primary_source_ids"]] == batch["primary_source_ids"]
    assert all(c["parent_batch_id"] == "b003" and c["split_depth"] == 1 for c in children)
    assert "split_depth" not in batch


def test_recursive_subdivision_has_stable_lineage_and_explicit_bounds():
    batch, units = fixtures()
    child = subdivide_record_batch(batch, units)[0]
    with pytest.raises(ValueError, match="depth"):
        subdivide_record_batch(child, units, max_depth=1)
    leaf = subdivide_record_batch(child, units)[0]
    assert leaf["id"] == "b003.1.1"
    with pytest.raises(ValueError, match="no splittable"):
        subdivide_record_batch(leaf, units)


def test_invalid_source_assignments_are_rejected():
    batch, units = fixtures()
    batch["primary_source_ids"] = ["s0", "missing"]
    with pytest.raises(ValueError, match="unique known"):
        subdivide_record_batch(batch, units)
    batch["primary_source_ids"] = ["s0", "s0"]
    with pytest.raises(ValueError, match="unique known"):
        subdivide_record_batch(batch, units)
