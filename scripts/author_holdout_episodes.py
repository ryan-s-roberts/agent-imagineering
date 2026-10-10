"""Source-reviewed holdout episode annotations; never model input or prompt examples."""

import argparse
import json
from pathlib import Path

from property_eval.prefix import HEADER, load_prefix

# Same episode rule as development: stop before incoming evidence or a new timer.
# Reviewed before reading this round's predictions. No inferred normative policy.
SPECS = {
    "041": (
        2,
        4,
        [5],
        [
            (
                [3],
                "request_approval",
                "material",
                "Ask landlord to authorize appliance attendance at the stated minimum charge.",
            ),
            (
                [4],
                "change_workflow",
                "workflow",
                "Record waiting for contractor response, despite the preceding request being addressed to landlord.",
            ),
        ],
    ),
    "042": (
        3,
        6,
        [7, 8],
        [
            (
                [4],
                "request_approval",
                "material",
                "Ask landlord to authorize investigation of washing-machine heating fault.",
            ),
            (
                [5],
                "notify",
                "auxiliary",
                "Acknowledge tenant report, explain pending landlord instruction and invite reports of worsening or additional faults.",
            ),
            ([6], "change_workflow", "workflow", "Record waiting for landlord."),
        ],
    ),
    "043": (
        2,
        3,
        [4, 5, 6],
        [
            (
                [3],
                "request_approval",
                "material",
                "Ask landlord permission to send appliance contractor for washing-machine drainage fault.",
            )
        ],
    ),
    "044": (
        4,
        6,
        [7],
        [
            ([5], "request_clarification", "material", "Ask tenant which window is affected."),
            ([6], "change_workflow", "workflow", "Record that tenant has been emailed."),
        ],
    ),
    "045": (
        2,
        4,
        [5, 6],
        [
            (
                [3],
                "request_clarification",
                "material",
                "Ask tenant whether landlord requested the work.",
            ),
            ([4], "change_workflow", "workflow", "Record waiting for tenant."),
        ],
    ),
    "046": (
        2,
        5,
        [6, 7],
        [
            (
                [3],
                "request_approval",
                "material",
                "Ask landlord permission for contractor to fix bedroom window hinge/closure issue.",
            ),
            (
                [4],
                "notify",
                "auxiliary",
                "Tell tenant landlord authorization is pending and agency or contractor will arrange a visit.",
            ),
            ([5], "change_workflow", "workflow", "Record waiting for landlord."),
        ],
    ),
    "047": (
        2,
        4,
        [5, 6],
        [
            (
                [3],
                "notify",
                "auxiliary",
                "Acknowledge tenant and explain intended landlord contact for contractor quotation.",
            ),
            (
                [4],
                "request_approval",
                "material",
                "Ask landlord to choose agency or own contractor for toilet blockage and bedroom window issues.",
            ),
        ],
    ),
    "048": (
        2,
        4,
        [5, 6],
        [
            (
                [3],
                "request_approval",
                "material",
                "Ask landlord permission to fix bathroom window that does not open.",
            ),
            ([4], "change_workflow", "workflow", "Record waiting for landlord."),
        ],
    ),
    "049": (
        3,
        5,
        [6, 7],
        [
            (
                [4],
                "request_approval",
                "material",
                "Ask landlord whether tenant may fix sagging shed door or a contractor should attend.",
            ),
            (
                [5],
                "change_workflow",
                "workflow",
                "Record waiting for landlord/tenant response before provider selection.",
            ),
        ],
    ),
    "050": (
        3,
        7,
        [8, 9],
        [
            (
                [4, 6],
                "request_approval",
                "material",
                "Ask landlord permission for contractor to address bedroom window handle, with follow-up attachment reference.",
            ),
            (
                [5],
                "notify",
                "auxiliary",
                "Tell tenant landlord was contacted and further steps will follow.",
            ),
            ([7], "change_workflow", "workflow", "Record waiting for landlord."),
        ],
    ),
}


def author(source):
    episodes = []
    for case, (cutoff, end, boundary, acts) in SPECS.items():
        path = source / case / "history.md"
        raw = path.read_text()
        headers = list(HEADER.finditer(raw))
        events = load_prefix(source, case, len(headers)).events

        def citation(number, events=events, headers=headers, raw=raw, path=path):
            body = events[number - 1].text.split("\n\n", 1)[1]
            stop = headers[number].start() if number < len(headers) else len(raw)
            start = raw.index(body, headers[number - 1].end(), stop)
            return {
                "event_id": f"{number:03}",
                "source_path": str(path.relative_to(source)),
                "quote": body,
                "char_start": start,
                "char_end": start + len(body),
                "line_start": raw.count("\n", 0, start) + 1,
                "line_end": raw.count("\n", 0, start + len(body)) + 1,
                "offset_basis": "zero-based Unicode codepoints in complete history.md; end exclusive",
            }

        actions = []
        for numbers, intent, materiality, summary in acts:
            actions.append(
                {
                    "id": f"{case}-a{len(actions) + 1:02}",
                    "intent": intent,
                    "summary": summary,
                    "materiality": materiality,
                    "source_citations": [citation(n) for n in numbers],
                    "observed_at_event": f"{numbers[0]:03}",
                    "deduplication": "Same request and attachment follow-up."
                    if len(numbers) > 1
                    else None,
                    "earliest_knowledge": {
                        "cutoff": cutoff if materiality == "workflow" else None,
                        "prediction_cutoff": cutoff,
                        "status": "observed_effect"
                        if materiality == "workflow"
                        else "earliest_factual_availability_not_established",
                    },
                    "execution_semantics": "Observed communication or administrative effect; requested work is not executed work or granted authority.",
                }
            )
        order = []
        # Explicitly reviewed recipient-compatible wait dependencies only.
        if case in {"042", "045", "046", "048", "049", "050"}:
            order = [
                {
                    "before": actions[0]["id"],
                    "after": actions[-1]["id"],
                    "basis": "Recorded request precedes waiting for the requested response.",
                }
            ]
        timer = case in {"041", "043"}
        limits = []
        if case == "041":
            limits = [
                "Earlier round exposed this case; not pristine holdout.",
                "Recorded contractor wait conflicts with landlord addressee; preserve rather than correct history.",
            ]
        if case == "043":
            limits = [
                "Five-day-later task-manager updates accompany follow-up; exact trigger is not recorded. Conservative episode boundary."
            ]
        episodes.append(
            {
                "checkpoint_id": f"{case}-at-{cutoff:03}",
                "case_id": case,
                "cutoff": cutoff,
                "included_event_ids": [f"{n:03}" for n in range(cutoff + 1, end + 1)],
                "actions": actions,
                "partial_order": order,
                "boundary": {
                    "event_ids": [f"{n:03}" for n in boundary],
                    "kind": "timer_trigger" if timer else "external_reply",
                    "reason": "New nonresponse/follow-up episode."
                    if timer
                    else "Incoming reply changes available evidence; preceding review prompt belongs to that boundary.",
                    "confidence": "uncertain"
                    if case == "043"
                    else "probable"
                    if timer
                    else "clear",
                    "citations": [citation(n) for n in boundary],
                },
                "source_tail": [
                    {
                        "event_id": f"{n:03}",
                        "timestamp": events[n - 1].timestamp,
                        "channel": events[n - 1].channel,
                        "sender": events[n - 1].sender,
                        "recipient": events[n - 1].recipient,
                        "citation": citation(n),
                        "role": "episode" if n <= end else "boundary_or_later_review_only",
                    }
                    for n in range(cutoff + 1, max(boundary) + 1)
                ],
                "alternative_continuation_event_ids": [],
                "limits": limits,
                "target_completeness": "boundary_ambiguous" if case == "043" else "observed_bundle",
                "normative_required_actions": None,
            }
        )
    return {
        "version": "holdout-episodes-v1",
        "visibility": "evaluation_only",
        "author": "implementing assistant source review before reading predictions",
        "protocol": "docs/decision-episode-contract.md",
        "episodes": episodes,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", dest="source", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(author(args.source), ensure_ascii=False, indent=2))
