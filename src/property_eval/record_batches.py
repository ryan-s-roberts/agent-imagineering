"""Bound assertion work by primary evidence volume while sharing one entity graph.

All batches can inspect the complete compact source context. Ownership narrows
what they extract, not what they can know. Combining results never merges domain
entities or guesses semantic equivalence between assertions.
"""

from collections import OrderedDict
from copy import deepcopy


def plan_record_batches(units, max_primary_chars=4000, max_batches=64):
    if max_primary_chars < 1:
        raise ValueError("Record batch character limit must be positive")
    ids = [u["id"] for u in units]
    if len(ids) != len(set(ids)):
        raise ValueError("Source IDs must be unique")
    groups = OrderedDict()
    for unit in units:
        origin = unit.get("origin", "event")
        group = (origin, unit.get("anchor_namespace", unit["event_id"]))
        groups.setdefault(group, []).append(unit)
    batches, current, size, current_origin = [], [], 0, None

    def flush():
        nonlocal current, size
        if current:
            batches.append(
                {
                    "id": f"b{len(batches) + 1:03}",
                    "primary_source_ids": [u["id"] for u in current],
                    "primary_char_count": size,
                    "origin": current_origin,
                    "oversize_source_ids": [
                        u["id"] for u in current if len(u["text"]) > max_primary_chars
                    ],
                }
            )
            current, size = [], 0

    for (origin, _), group in groups.items():
        group_size = sum(len(u["text"]) for u in group)
        if current and (origin != current_origin or size + group_size > max_primary_chars):
            flush()
        current_origin = origin
        # Preserve a whole event/page where it fits. Oversize groups split only
        # at existing source boundaries; a single oversize source is explicit.
        for unit in group:
            unit_size = len(unit["text"])
            if current and size + unit_size > max_primary_chars:
                flush()
            current.append(unit)
            size += unit_size
        if size >= max_primary_chars:
            flush()
    flush()
    if len(batches) > max_batches:
        raise ValueError(f"Record extraction needs {len(batches)} batches; limit is {max_batches}")
    assigned = [source_id for b in batches for source_id in b["primary_source_ids"]]
    if len(assigned) != len(ids) or set(assigned) != set(ids):
        raise ValueError("Every source must have exactly one primary batch")
    return {
        "version": "record-batches-v1",
        "max_primary_chars": max_primary_chars,
        "max_batches": max_batches,
        "context_source_ids": ids,
        "batches": batches,
        "semantics": "Shared complete context and entity graph; disjoint primary extraction sources",
    }


BATCH_INSTRUCTION = """This is one bounded assertion-extraction batch within a shared case graph.
All supplied source text and entities are available as context. Extract records and gaps
supported by the primary_source_ids assigned to this batch. Every returned record must cite
at least one primary source in its field or cause evidence; the host derives the redundant
provenance source union from those spans. Every gap must cite at least one primary source
in source_ids. Other sources may support attribution, identity or context.
Do not reproduce facts supported solely by another batch's sources. Preserve independent
reports even when they discuss the same subject; do not claim repeated reports are independent
verification. Create only within-response record references; no other batch's record IDs
are available. Do not emit events, actions or guesses to fill an empty batch. Return empty
record/gap lists when these primary sources contain no representable assertions or gaps.
"""


def subdivide_record_batch(batch, units, max_depth=6):
    """Bisect primary sources by text volume without changing source identities.

    A source is indivisible: exhaustion at one source or at the depth bound is
    an explicit failure. The caller retains the parent's failed attempt and
    combines only successful leaves, alongside already completed siblings.
    """
    depth = batch.get("split_depth", 0)
    if max_depth < 1 or depth >= max_depth:
        raise ValueError(f"Record batch {batch['id']} reached subdivision depth {max_depth}")
    source_map = {unit["id"]: unit for unit in units}
    if len(source_map) != len(units):
        raise ValueError("Source IDs must be unique")
    ids = batch["primary_source_ids"]
    if len(set(ids)) != len(ids) or any(source_id not in source_map for source_id in ids):
        raise ValueError("Batch primary sources must be unique known sources")
    if len(ids) < 2:
        raise ValueError(f"Record batch {batch['id']} has no splittable source boundary")
    sizes = [len(source_map[source_id]["text"]) for source_id in ids]
    total, prefix, candidates = sum(sizes), 0, []
    for index, size in enumerate(sizes[:-1], 1):
        prefix += size
        candidates.append((abs(total - 2 * prefix), index))
    _, split = min(candidates)
    children = []
    for number, child_ids in enumerate((ids[:split], ids[split:]), 1):
        children.append(
            {
                "id": f"{batch['id']}.{number}",
                "parent_batch_id": batch["id"],
                "split_depth": depth + 1,
                "primary_source_ids": child_ids,
                "primary_char_count": sum(len(source_map[s]["text"]) for s in child_ids),
                "origin": batch["origin"],
                "oversize_source_ids": [
                    s for s in batch.get("oversize_source_ids", []) if s in child_ids
                ],
            }
        )
    return children


def validate_batch_ownership(output, batch, known_source_ids):
    """Structural source ownership only; not an entailment test."""
    primary, known = set(batch["primary_source_ids"]), set(known_source_ids)
    for category in ("records", "gaps"):
        seen = set()
        for item in output[category]:
            if item["id"] in seen:
                raise ValueError(f"Duplicate {category} ID in batch {batch['id']}")
            seen.add(item["id"])
            cited = set(
                item["provenance"]["source_ids"] if category == "records" else item["source_ids"]
            )
            if not cited <= known:
                raise ValueError(f"Unknown source in {batch['id']} {item['id']}")
            if not cited & primary:
                raise ValueError(f"No primary evidence cited by {batch['id']} {item['id']}")


def combine_record_batches(results):
    """Namespace each batch's local record/gap references, retaining every assertion."""
    combined = {"records": [], "gaps": []}
    lineage = []
    seen_batches = set()
    for batch_id, raw in results:
        if batch_id in seen_batches:
            raise ValueError("Duplicate record batch ID")
        seen_batches.add(batch_id)
        data = deepcopy(raw.model_dump() if hasattr(raw, "model_dump") else raw)
        record_map = {r["id"]: f"{batch_id}:{r['id']}" for r in data["records"]}
        gap_map = {g["id"]: f"{batch_id}:{g['id']}" for g in data["gaps"]}
        if len(record_map) != len(data["records"]) or len(gap_map) != len(data["gaps"]):
            raise ValueError("Duplicate record/gap IDs within batch")

        def rewrite(value, key="", record_map=record_map, gap_map=gap_map):
            if isinstance(value, dict):
                return {k: rewrite(v, k) for k, v in value.items()}
            if isinstance(value, list):
                return [rewrite(v, key) for v in value]
            if isinstance(value, str):
                if key.endswith(("_record_id", "_record_ids")) or key == "record_ids":
                    return record_map.get(value, value)
                if key.endswith(("_gap_id", "_gap_ids")) or key == "gap_ids":
                    return gap_map.get(value, value)
            return value

        for category, mapping in (("records", record_map), ("gaps", gap_map)):
            for original in data[category]:
                item = rewrite(original)
                item["id"] = mapping[original["id"]]
                combined[category].append(item)
                lineage.append(
                    {
                        "batch_id": batch_id,
                        "kind": category,
                        "local_id": original["id"],
                        "id": item["id"],
                    }
                )
    return combined, lineage
