"""Reviewed development annotations; never imported by decision prompt construction."""

import json
from pathlib import Path
from typing import get_args

from .cli import write_json
from .soft_eval import HistoricalTarget, ObservedAction

# Each tuple is an explicit annotation of agency speech, not inferred completed work.
# Whole-event context remains available to detect errors in these partial annotations.
ANNOTATIONS = {
    1: (
        "request_clarification",
        "Can you confirm how you'd like us to respond.",
        {
            "topic": "other",
            "question": "How should the agency respond to the garden maintenance report?",
        },
    ),
    2: (
        "instruct_provider",
        "Toilet need to be removed to clear blockage.",
        {"scope": ["repair"], "conditions": []},
    ),
    3: (
        "notify",
        "Please check your email",
        {"purpose": "reminder", "message": "Please check your email regarding the property."},
    ),
    4: (
        "notify",
        "Please check your email",
        {"purpose": "reminder", "message": "Please check your email regarding the property."},
    ),
    5: (
        "handle_document",
        "please provide an estimate",
        {"operation": "request", "document_kind": "quote"},
    ),
    6: (
        "notify",
        "They will contact you soon to arrange a suitable time to quote for the job.",
        {
            "purpose": "progress",
            "message": "Provider will arrange a quotation visit; landlord approval and instruction follow the quote.",
        },
    ),
    7: (
        "notify",
        "Please check your email",
        {"purpose": "reminder", "message": "Please check your email regarding the property."},
    ),
    8: (
        "handle_document",
        "please provide an estimate",
        {"operation": "request", "document_kind": "quote"},
    ),
    9: (
        "request_clarification",
        "If you can please provide some photos to confirm this is done.",
        {
            "topic": "work_outcome",
            "question": "Has front garden maintenance been completed? Please provide confirming photos.",
        },
    ),
    10: (
        "request_clarification",
        "Please could you send us a clear photo of your solar panel readings?",
        {"topic": "other", "question": "Please send a clear photo of solar panel readings."},
    ),
    11: (
        "request_approval",
        "Would you be happy for me to get a contractor out to have a look at this for you.",
        {"scope": ["inspect"]},
    ),
    12: (
        "provide_guidance",
        "Before we arrange an engineer, please could you run through the quick checks below",
        {
            "steps": [
                "Switch off at socket",
                "Check racks, spray arms, cutlery basket, seal and caps",
                "Test door empty gently without force",
            ],
            "requested_feedback": "Report if the door still will not close after checks.",
        },
    ),
    13: (
        "notify",
        "I will proceed and send an appliance engineer to see if this can be repaired.",
        {
            "purpose": "progress",
            "message": "Dishwasher failure reported; agency plans to send an appliance engineer.",
        },
    ),
    14: (
        "request_approval",
        "Please let me know if we can get someone out to have a look at this.",
        {"scope": ["inspect"]},
    ),
    15: (
        "request_approval",
        "Please confirm if you would like us to instruct a contractor to attend.",
        {"scope": ["inspect"]},
    ),
    16: (
        "request_approval",
        "resolve where possible (or quote if significant)",
        {"scope": ["inspect", "repair", "quote"]},
    ),
    17: (
        "notify",
        "I will contact the landlord to see what we can do to get someone to come and see to it.",
        {
            "purpose": "acknowledgement",
            "message": "Extractor fan request acknowledged; agency plans to contact landlord.",
        },
    ),
    18: (
        "notify",
        "The gardener is on annual leave and will be booked in at the earliest convinience upon his return.",
        {
            "purpose": "progress",
            "message": "Maintenance is being addressed; gardener booking awaits return from leave.",
        },
    ),
    19: (
        "request_clarification",
        "please let me know your plans and how you wish for me to respond.",
        {
            "topic": "other",
            "question": "What are the landlord's plans for the garden and how should the agency respond?",
        },
    ),
    20: (
        "notify",
        "has been scheduled for 13/02/2024 between 8:00AM and 12:00PM.",
        {
            "purpose": "confirmation",
            "message": "Inspection booked13/02/2024 08:00–12:00; photos for landlord; management-key access if tenant absent.",
        },
    ),
    21: (
        "request_approval",
        "Please confirm if you would like me to organise for a contractor to visit and carry out the necessary works?",
        {"scope": ["repair"]},
    ),
    22: (
        "notify",
        "Miles confirmed the arrangement with the customer.",
        {
            "purpose": "confirmation",
            "message": "Contractor visit for door lock agreed around half past two.",
        },
    ),
    23: (
        "request_approval",
        "Please kindly let me know if you are happy for us to send someone to attend to this?",
        {"scope": ["inspect"]},
    ),
    24: (
        "provide_guidance",
        "I suggest turn the left dial 3 turns and turn the heat to 200.",
        {
            "steps": ["Turn left dial three turns and heat to200, as advised in the message"],
            "requested_feedback": None,
        },
    ),
    25: (
        "request_approval",
        "Can you please advise if you wish for me to instruct a contractor to attend or if you want to arrange your own contractor?",
        {"scope": ["inspect"]},
    ),
    26: (
        "request_approval",
        "can i send out Keystone Compliance who check all our appliances please",
        {"scope": ["inspect"]},
    ),
    27: (
        "provide_guidance",
        "We kindly recommend that you try using a strong drain cleaner and a plunger",
        {
            "steps": [
                "Try drain cleaner and plunger as suggested by agency",
                "If unresolved, choose own plumber or agency contractor; agency asserts conditional tenant charges",
            ],
            "requested_feedback": "Let agency know how to proceed.",
        },
    ),
    28: (
        "request_approval",
        "Can you please advise if you wish for me to instruct a contractor to attend or if you want to arrange your own contractor?",
        {"scope": ["inspect"]},
    ),
    29: (
        "notify",
        "They will contact you soon to arrange a suitable time to quote for the job.",
        {
            "purpose": "progress",
            "message": "Provider will arrange quotation visit; landlord approval and instruction follow quote.",
        },
    ),
    30: (
        "notify",
        "I have raised a job for Riverside Works to sort.",
        {
            "purpose": "progress",
            "message": "Agency reports having raised a plumbing job with Riverside Works.",
        },
    ),
    31: (
        "notify",
        "They will contact you soon to arrange a mutually convenient time to visit and triage the problem or prepare the quote if needed.",
        {
            "purpose": "progress",
            "message": "Provider will arrange visit to triage plumbing issue or quote if needed.",
        },
    ),
    32: (
        "request_approval",
        "resolve where possible (or quote if significant)",
        {"scope": ["inspect", "repair", "quote"]},
    ),
    33: (
        "request_approval",
        "Can you please advise if you wish for me to instruct a contractor to attend or if you want to arrange your own contractor?",
        {"scope": ["inspect"]},
    ),
    34: (
        "notify",
        "They will contact you soon to arrange a mutually convenient time to visit and triage the problem or prepare the quote if needed.",
        {
            "purpose": "progress",
            "message": "Provider will arrange shower triage visit or quote if needed.",
        },
    ),
    35: (
        "notify",
        "The call discusses maintenance issues at the flat",
        {
            "purpose": "progress",
            "message": "Discussion of shower hose, water damage, repairs and letting tasks; precise agency intent unresolved.",
        },
    ),
    36: (
        "request_approval",
        "Please let me know if you are happy for me to send a contractor out to mend it if possible.",
        {"scope": ["repair"]},
    ),
    37: (
        "request_approval",
        "please let us know if you would like to arrange the repair directly, or if you would prefer for us to organise this on your behalf.",
        {"scope": ["repair"]},
    ),
    38: (
        "request_approval",
        "Seeks Henry Ingram's approval for tenants to replace the washing machine and to confirm who will cover the £24.37 removal cost.",
        {"scope": ["replace"]},
    ),
    39: (
        "request_clarification",
        "Can I just double check that there is nothing inside the machine hitting the sides that could be causing this noise while it is spinning?",
        {
            "topic": "issue",
            "question": "Is anything inside the washing machine hitting the sides during spinning?",
        },
    ),
    40: (
        "request_approval",
        "if you're happy for us to send someone out to look at this for you.",
        {"scope": ["inspect"]},
    ),
}


def build_targets(root=Path(".")):
    original = json.loads((root / "annotations/decision-dev-v1-targets.json").read_text())[
        "targets"
    ]
    models = {get_args(m.model_fields["type"].annotation)[0]: m for m in get_args(ObservedAction)}
    targets = []
    for row in original:
        case = int(row["case"])
        kind, quote, slots = ANNOTATIONS[case]
        event = row["events"][0]
        source_id = f"target:{row['case']}:{event['id']}"
        assert event["text"].count(quote) == 1, (case, quote)
        cite = {"source_id": source_id, "expression": quote, "occurrence": 1}
        actor_id = f"target:{row['case']}:recipient"
        role = {"Contractor": "provider", "Landlord": "landlord", "Tenant": "tenant"}.get(
            event["recipient"], "unknown"
        )
        actor_cite = {
            "source_id": source_id,
            "expression": f"- **To:** {event['recipient']}",
            "occurrence": 1,
        }
        payload = {"type": kind, "id": f"target:{row['case']}:action", **slots}
        for field in ("recipient_id", "provider_id"):
            if field in models[kind].model_fields:
                payload[field] = actor_id
        action = models[kind].model_validate(payload).model_dump()
        # Source context is cited for normalized slots; this is transparent annotation,
        # not a claim that a single phrase entails every field independently.
        contextual = {"source_id": source_id, "expression": event["text"], "occurrence": 1}
        target = HistoricalTarget.model_validate(
            {
                "version": "historical-target-v1",
                "id": row["id"],
                "case_id": "property-" + row["case"],
                "visibility": "evaluation_only",
                "observation": "mixed_speaker_call_summary"
                if event["channel"] == "Call"
                else "recorded_communication",
                "intent_assessability": "unassessable"
                if case == 35
                else "partially_assessable"
                if case in {2, 22}
                else "assessable",
                "actors": [
                    {
                        "id": actor_id,
                        "role": role,
                        "surface": event["recipient"],
                        "evidence": [actor_cite],
                        "prefix_entity_id": None,
                    }
                ],
                "actions": [
                    {
                        "action": action,
                        "evidence": [cite],
                        "slot_evidence": {
                            k: [actor_cite if k.endswith("_id") and v == actor_id else contextual]
                            for k, v in action.items()
                            if v is not None and k not in {"id", "type"}
                        },
                        "unknown_slots": [k for k, v in action.items() if v is None],
                        "alternative_action_types": [
                            k for k in row["candidate_action_types"] if k != kind
                        ],
                        "interpretation": "Observed agency communication; work described or proposed is not independently proven executed.",
                    }
                ],
                "source": {
                    "id": source_id,
                    "text": event["text"],
                    "event": event,
                    "anchor_start": event["text"].index(quote),
                    "anchor_end": event["text"].index(quote) + len(quote),
                },
                "review_status": "single_author_source_review; independent_review_pending",
                "limits": [
                    "Unknown prefix identity mappings remain null; target-local actors must never enter decision input.",
                    "Historical choice is soft observational target, not proof of authority, safety, optimality or prefix predictability.",
                ],
            }
        )
        data = target.model_dump()
        if case == 35:
            data["actions"] = []
            data["limits"].append(
                "Discussion is observed; no particular agency action intent can be established from the mixed-speaker summary."
            )
        if case == 12:
            data["actions"][0]["interpretation"] += (
                " Checks are requested before arranging an engineer; tenant should report continued door failure after checks."
            )
        if case == 38:
            data["actions"][0]["interpretation"] += (
                " Replacement permission is distinct from the question of who pays the removal cost; no combined expenditure approval amount is stated."
            )
            extra = (
                models["request_clarification"]
                .model_validate(
                    {
                        "type": "request_clarification",
                        "id": "target:038:cost-question",
                        "recipient_id": actor_id,
                        "topic": "authorization",
                        "question": "Who will cover the £24.37 removal cost?",
                    }
                )
                .model_dump()
            )
            data["actions"].append(
                {
                    "action": extra,
                    "evidence": [cite],
                    "slot_evidence": {
                        "question": [cite],
                        "recipient_id": [actor_cite],
                        "topic": [cite],
                    },
                    "unknown_slots": [k for k, v in extra.items() if v is None],
                    "alternative_action_types": [],
                    "interpretation": "Removal-cost responsibility is requested, not established; amount applies to removal only.",
                }
            )
        if case in {1, 10, 12, 22, 27, 35, 38}:
            data["review_status"] = (
                "single_author_source_review; independent_agent_sample_review_applied"
            )
        else:
            data["review_status"] = "single_author_source_review; not_independently_adjudicated"
        targets.append(HistoricalTarget.model_validate(data).model_dump())
    write_json(
        root / "annotations/historical-targets-v1.json",
        {"version": "historical-target-v1", "targets": targets},
    )
    write_json(
        root / "annotations/historical-targets-v1.schema.json", HistoricalTarget.model_json_schema()
    )


if __name__ == "__main__":
    build_targets()
