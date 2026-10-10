"""Select late agency episodes mechanically; preserve boundary uncertainty for review."""

import argparse
import json
from datetime import datetime
from pathlib import Path

from .prefix import HEADER, load_prefix

AGENCY_SENDERS = {"Agency / system", "Northbridge Lettings", "Northbridge Lettings system"}
ACTION_CHANNELS = {"Email", "SMS", "Call", "Hold", "Update"}


def timestamp(event):
    return datetime.strptime(event.timestamp, "%Y-%m-%d %H:%M:%S UTC")


def episodes(events, gap_minutes=60):
    """Contiguous agency activity, bounded by external events and elapsed time.

    The gap is a reproducible session heuristic, not evidence of a timer firing.
    Notes attach to a block but cannot alone qualify it as an action episode.
    """
    blocks, current = [], []
    for event in events:
        agency = event.sender in AGENCY_SENDERS
        gap = (
            current
            and (timestamp(event) - timestamp(current[-1])).total_seconds() > gap_minutes * 60
        )
        if not agency or gap:
            if current:
                blocks.append(current)
            current = []
        if agency:
            current.append(event)
    if current:
        blocks.append(current)
    return [block for block in blocks if any(e.channel in ACTION_CHANNELS for e in block)]


def select(source, count=3, gap_minutes=60):
    jobs, review = [], []
    for path in sorted((source).glob("*/history.md")):
        case = path.parent.name
        events = load_prefix(source, case, len(list(HEADER.finditer(path.read_text())))).events
        candidates = [block for block in episodes(events, gap_minutes) if int(block[0].id) > 1]
        for block in candidates[-count:]:
            cutoff = int(block[0].id) - 1
            checkpoint = f"{case}-at-{cutoff:03}"
            jobs.append(
                {
                    "case": case,
                    "cutoff": cutoff,
                    "split": "development" if int(case) <= 40 else "previously_exposed",
                }
            )
            review.append(
                {
                    "checkpoint_id": checkpoint,
                    "total_case_events": len(events),
                    "target_event_ids": [e.id for e in block],
                    "review_status": "candidate_boundary_not_semantically_reviewed",
                    "boundary_rule": "External sender, agency inactivity gap, or end of history",
                    "mixed_turn_risk": any(e.channel == "Call" for e in block),
                    "workflow_only": all(e.channel in {"Hold", "Update", "Note"} for e in block),
                    "evaluation_only_events": [e.model_dump() for e in block],
                }
            )
    return {
        "version": "late-episodes-v1",
        "selection": f"Last {count} agency activity blocks per case; external-event boundaries; {gap_minutes}-minute inactivity threshold. Candidate boundaries require semantic review before scoring.",
        "jobs": jobs,
    }, {"version": "late-episode-boundary-review-v1", "model_input": False, "checkpoints": review}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", dest="source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest, review = select(args.source)
    args.output.mkdir(parents=True, exist_ok=False)
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (args.output / "boundary-review.json").write_text(json.dumps(review, indent=2) + "\n")
    print(
        json.dumps(
            {
                "checkpoints": len(manifest["jobs"]),
                "cases": len({j["case"] for j in manifest["jobs"]}),
                "output": str(args.output),
            }
        )
    )


if __name__ == "__main__":
    main()
