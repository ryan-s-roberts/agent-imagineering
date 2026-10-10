"""Authored development checkpoint selection; future targets stay outside model inputs."""

from .prefix import load_prefix

TARGET_EVENTS = [
    4,
    5,
    3,
    5,
    4,
    4,
    4,
    3,
    3,
    6,
    4,
    5,
    2,
    5,
    3,
    3,
    3,
    4,
    3,
    2,
    3,
    4,
    3,
    3,
    3,
    4,
    2,
    3,
    4,
    4,
    5,
    3,
    3,
    6,
    4,
    3,
    3,
    4,
    3,
    4,
]
CANDIDATES = [
    ["request_clarification", "request_approval"],
    ["instruct_provider", "notify"],
    ["notify"],
    ["notify"],
    ["handle_document", "instruct_provider"],
    ["notify"],
    ["notify"],
    ["handle_document", "instruct_provider"],
    ["request_clarification", "handle_document"],
    ["request_clarification", "handle_document"],
    ["request_approval"],
    ["provide_guidance"],
    ["notify"],
    ["request_approval"],
    ["request_approval"],
    ["request_approval"],
    ["notify"],
    ["notify"],
    ["request_approval", "request_clarification"],
    ["notify"],
    ["request_approval"],
    ["propose_booking", "notify"],
    ["request_approval"],
    ["provide_guidance"],
    ["request_approval"],
    ["request_approval"],
    ["provide_guidance"],
    ["request_approval"],
    ["notify"],
    ["notify"],
    ["notify"],
    ["request_approval"],
    ["request_approval"],
    ["notify"],
    ["notify", "request_clarification"],
    ["request_approval"],
    ["request_approval", "request_clarification"],
    ["request_approval", "request_clarification"],
    ["request_clarification", "provide_guidance"],
    ["request_approval"],
]


def authored_selection(source):
    jobs, targets = [], []
    for case_number, (target_number, choices) in enumerate(
        zip(TARGET_EVENTS, CANDIDATES, strict=True), 1
    ):
        case = f"{case_number:03}"
        cutoff = target_number - 1
        prefix = load_prefix(source, case, cutoff)
        target = load_prefix(source, case, target_number).events[-1]
        if target.sender not in {
            "Agency / system",
            "Northbridge Lettings",
        } or target.channel not in {"Email", "SMS", "Call"}:
            raise ValueError(f"Selection needs agency-action review: {case}")
        job_id = f"{case}-at-{cutoff:03}"
        jobs.append(
            {
                "id": job_id,
                "case": case,
                "cutoff": cutoff,
                "prefix_sha256": prefix.source_sha256,
                "target_event_id": target.id,
            }
        )
        targets.append(
            {
                "id": job_id,
                "case": case,
                "events": [target.model_dump()],
                "visibility": "review_only",
                "actor_class": "mixed_speaker_agency_call"
                if target.channel == "Call"
                else "agency_outbound_communication",
                "execution_class": "recorded_communication_not_proof_of_proposed_work_completion",
                "agency_actor_identity": "system_or_staff_unresolved"
                if target.sender == "Agency / system"
                else "named_agency_human_author_not_always_established",
                "candidate_action_types": choices,
                "review_status": "single_author_excerpt_review; detailed choice support not adjudicated",
                "caveat": "Candidates compare coarse historical action types, not unique correct choices; quoted environment reports and proposed work are not additional completed agency actions.",
            }
        )
    return {
        "manifest": {
            "version": "decision-dev-v1",
            "scope": "001-040 development only; 041-050 excluded",
            "selection": "First reviewable agency outbound communication after at least one event; full target separately stored; agency Call events may contain mixed speakers",
            "model": "openai/gpt-6-luna",
            "concurrency": 3,
            "max_tokens": 16000,
            "timeout_seconds": 360,
            "stop_rule": "One baseline decision per checkpoint; deterministic syntax canonicalization plus bounded interface repair; no semantic/prompt tuning after results",
            "jobs": jobs,
        },
        "targets": {"version": "decision-dev-v1", "targets": targets},
    }
