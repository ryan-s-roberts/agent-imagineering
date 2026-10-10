# Proposed answer

Case 004; checkpoint `004-at-023`; prefix ends at event `23`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

## Execution status

This system has no external execution environment, so it did not carry out any proposed actions. Actions and outcomes recorded in the case history are evidence; the actions below are recommendations. The case evidence bundle contains the supplied history and extracted support.

Disposition: **act**.

## Proposed actions

### Request clarification

```json
{
  "id": "a1",
  "request_id": "entity:property-004:001:132:173",
  "basis_record_ids": [
    "b001.1:r16",
    "b002:r20",
    "b002:r21",
    "b002:r4"
  ],
  "basis_gap_ids": [
    "b002:g2"
  ],
  "depends_on_action_ids": [],
  "type": "request_clarification",
  "recipient_id": "entity:property-004:011:153:163",
  "topic": "work_outcome",
  "question": "Please confirm whether you attended the property as expected today and, if so, what work was completed and the lock's outcome. If you did not attend or the work remains incomplete, please confirm the next visit date and time."
}
```

### Await response

```json
{
  "id": "a2",
  "request_id": "entity:property-004:001:132:173",
  "basis_record_ids": [
    "b002:r20",
    "b002:r21"
  ],
  "basis_gap_ids": [
    "b002:g2"
  ],
  "depends_on_action_ids": [
    "a1"
  ],
  "type": "await_response",
  "responsible_party_id": "entity:property-004:011:153:163",
  "awaited": "clarification"
}
```

### Request clarification

```json
{
  "id": "a3",
  "request_id": "entity:property-004:001:132:173",
  "basis_record_ids": [
    "b001.1:r4",
    "b001.1:r9",
    "b002:r10"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "request_clarification",
  "recipient_id": "entity:property-004:001:34:44",
  "topic": "issue",
  "question": "Given your report that the lock is now worse than before, can you currently lock the front door securely and close it properly? Please tell us if either is no longer possible so we can assess the urgency of the outstanding lock work."
}
```

### Notify

```json
{
  "id": "a4",
  "request_id": "entity:property-004:001:132:173",
  "basis_record_ids": [
    "b002:r20",
    "b002:r21"
  ],
  "basis_gap_ids": [
    "b002:g2"
  ],
  "depends_on_action_ids": [
    "a1"
  ],
  "type": "notify",
  "recipient_id": "entity:property-004:001:34:44",
  "purpose": "progress",
  "message": "Thank you for the update. Your message says Dorian was expected after 10:00, but does not confirm that he attended or completed the lock work. We are contacting him directly to confirm the outcome and, if needed, a firm return time.",
  "about_record_ids": [
    "b002:r20",
    "b002:r21"
  ]
}
```

### Escalate

```json
{
  "id": "a5",
  "request_id": "entity:property-004:021:165:204",
  "basis_record_ids": [
    "b002:r14"
  ],
  "basis_gap_ids": [
    "b002:g1"
  ],
  "depends_on_action_ids": [],
  "type": "escalate",
  "recipient_id": "entity:property-004:001:64:72",
  "responsible_role": "property_manager",
  "causes": [
    {
      "category": "missing_evidence",
      "explanation": "The tenant reported the broken blind, while the agency could not confirm its status or ownership; review the available maintenance information and establish who is handling it and the next appropriate step.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "021:L5",
          "expression": "a broken bedroom blind that lets in light",
          "occurrence": 1
        },
        {
          "source_id": "021:L5",
          "expression": "The agency representative cannot confirm their status or ownership during the call.",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b002:r14"
      ],
      "gap_ids": [
        "b002:g1"
      ]
    }
  ],
  "requested_intervention": "review_case",
  "intervention_detail": "Review the reported bedroom-blind concern, identify its current handling and responsible party if established, and determine the appropriate next step.",
  "blocking": false,
  "blocked_action_ids": [],
  "handover": "The tenant asked who is handling this concern. Its status and ownership remain unconfirmed in the supplied prefix."
}
```

### Escalate

```json
{
  "id": "a6",
  "request_id": "entity:property-004:021:206:280",
  "basis_record_ids": [
    "b002:r15"
  ],
  "basis_gap_ids": [
    "b002:g1"
  ],
  "depends_on_action_ids": [],
  "type": "escalate",
  "recipient_id": "entity:property-004:001:64:72",
  "responsible_role": "property_manager",
  "causes": [
    {
      "category": "missing_evidence",
      "explanation": "The tenant reports glazing that the landlord had previously said would be addressed, but the agency could not confirm current status or ownership.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "021:L5",
          "expression": "glazing in a door that the landlord had previously said would be addressed",
          "occurrence": 1
        },
        {
          "source_id": "021:L5",
          "expression": "The agency representative cannot confirm their status or ownership during the call.",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b002:r15"
      ],
      "gap_ids": [
        "b002:g1"
      ]
    }
  ],
  "requested_intervention": "review_case",
  "intervention_detail": "Review the reported glazing concern and any available information about the landlord's earlier statement; establish current status, handling, and the appropriate next step.",
  "blocking": false,
  "blocked_action_ids": [],
  "handover": "The tenant reports an earlier landlord statement about addressing the glazing; the prefix does not establish whether it was acted on."
}
```

### Escalate

```json
{
  "id": "a7",
  "request_id": "entity:property-004:021:286:320",
  "basis_record_ids": [
    "b002:r16"
  ],
  "basis_gap_ids": [
    "b002:g1"
  ],
  "depends_on_action_ids": [],
  "type": "escalate",
  "recipient_id": "entity:property-004:001:64:72",
  "responsible_role": "property_manager",
  "causes": [
    {
      "category": "missing_evidence",
      "explanation": "The tenant reports that the hot water is too hot, and the agency could not confirm the concern's status or ownership.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "021:L5",
          "expression": "hot water that she says is too hot",
          "occurrence": 1
        },
        {
          "source_id": "021:L5",
          "expression": "The agency representative cannot confirm their status or ownership during the call.",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b002:r16"
      ],
      "gap_ids": [
        "b002:g1"
      ]
    }
  ],
  "requested_intervention": "review_case",
  "intervention_detail": "Review the reported hot-water concern, establish its current handling and responsible party if known, and assess the appropriate next step.",
  "blocking": false,
  "blocked_action_ids": [],
  "handover": "The tenant reports the hot water is too hot. No temperature, current handling, or ownership is established in the supplied prefix."
}
```

## Action dependencies

- `a2` depends on `a1`.
- `a4` depends on `a1`.

## Human interventions

```json
[]
```

Conclusion records: []

## Evidence and reasoning

The active objective is to complete the authorized front-door lock work. The latest tenant update says Dorian was expected that day after 10:00, but attendance and repair or replacement are unconfirmed. Contact Dorian directly for the actual outcome and any firm return appointment; meanwhile establish whether the worsening lock can still be secured. The tenant also raised three separate concerns whose handling and ownership the agency could not confirm, so request a property-manager review for each rather than assume they are already assigned.

## Assumptions

- Dorian Wren, the landlord's contractor, is the contractor referred to in the tenant's latest update; the chronology and earlier explicit identification support this continuity.

## Uncertainties

- The latest update does not establish whether Dorian attended, what work (if any) was done, or whether the lock is currently secure.
- The blind, glazing, and hot-water concerns have no established handling or ownership in the supplied prefix.

## Alternatives considered

- Do not book a visit yet: the contractor's latest expected attendance is not a confirmed appointment, and no firm return time is supplied.
- Do not instruct Peregrine Keyworks or another provider: the landlord directed the agency to wait for his contractor, and the agency stood down its selected provider.

## Cited prefix evidence

```json
{
  "source_id": "023:L5",
  "expression": "Says the contractor is meant to come that day sometime after 10:00",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [114, 367).

> Says the contractor is meant to come that day sometime after 10:00 but has not given a narrower time. The tenant says she will update the agency. At this point there is no confirmation that he has attended or that the lock has been repaired or replaced.

```json
{
  "source_id": "023:L5",
  "expression": "there is no confirmation that he has attended or that the lock has been repaired or replaced",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [114, 367).

> Says the contractor is meant to come that day sometime after 10:00 but has not given a narrower time. The tenant says she will update the agency. At this point there is no confirmation that he has attended or that the lock has been repaired or replaced.

```json
{
  "source_id": "020:L5",
  "expression": "the lock is now worse than before",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [113, 537).

> The tenant reports a later visit by Dorian Wren, separate from the earlier Saturday visit reported by the landlord. She says Dorian initially disputed that the lock was faulty. After a key he tried also failed, he said a new lock was needed. He left to obtain a lock and said he would return the following week, but did not give a date or time. The tenant says the lock is now worse than before; no replacement is confirmed.

```json
{
  "source_id": "016:L5",
  "expression": "Asks the agency to communicate directly with Dorian",
  "occurrence": 1
}
```
Event `016`, source `016:L5`, event character range [116, 313).

> Says his contractor, Dorian Wren, is away until 9 September. Asks the agency to communicate directly with Dorian, and says Dorian has told him he called and left a message asking for a return call.

```json
{
  "source_id": "006:L5",
  "expression": "approval to proceed with the lock repair or replacement",
  "occurrence": 1
}
```
Event `006`, source `006:L5`, event character range [140, 306).

> Records the landlord's approval to proceed with the lock repair or replacement and his separate agreement to the tenant's proposed paint touch-ups at her own expense.

```json
{
  "source_id": "021:L5",
  "expression": "The agency representative cannot confirm their status or ownership during the call.",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [113, 445).

> Raises other unresolved concerns during the call: a broken bedroom blind that lets in light, glazing in a door that the landlord had previously said would be addressed, and hot water that she says is too hot. She asks who is handling these matters. The agency representative cannot confirm their status or ownership during the call.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001.1:r4",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "front-door lock is loose and intermittent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "front-door lock",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "front-door lock is loose and intermittent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports that the front-door lock is loose and intermittent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports that the front-door lock is loose and intermittent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "front-door lock is loose and intermittent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Nessa Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-004:001:132:173",
      "asset_id": "entity:property-004:001:132:147",
      "property_id": null,
      "description": "The front-door lock is reported loose and intermittent; it can be manually locked at present.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b001.1:r9",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "front-door lock",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Says it can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Says it can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "can be manually locked at present",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Nessa Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-004:001:132:147",
      "location_text": null,
      "observation_kind": "physical_condition",
      "attribute": "manual locking possible",
      "value": {
        "kind": "boolean",
        "value": true
      },
      "quoted_expression": "can be manually locked at present",
      "epistemic_status": "asserted",
      "observed_at_text": null
    },
    {
      "id": "b001.1:r16",
      "provenance": {
        "source_ids": [
          "003:L5",
          "006:L2",
          "006:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:64:72",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "006:L5",
              "expression": "lock repair or replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "006:L5",
              "expression": "landlord's approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "003:L5",
              "expression": "Requests approval to arrange a locksmith visit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "006:L5",
              "expression": "lock repair or replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "006:L5",
              "expression": "Records the landlord's approval to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "006:L5",
              "expression": "Records the landlord's approval to proceed with the lock repair or replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "006:L5",
              "expression": "approval to proceed with the lock repair or replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "006:L5",
              "expression": "approval to proceed with the lock repair or replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "006:L2",
              "expression": "Mira Sol",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-004:001:132:173",
      "grantor_id": "entity:property-004:003:105:113",
      "grantee_id": "entity:property-004:001:92:112",
      "scope": [
        "repair",
        "replace"
      ],
      "decision": "approved",
      "amount_minor": null,
      "currency": null,
      "conditions": []
    },
    {
      "id": "b002:r4",
      "provenance": {
        "source_ids": [
          "016:L2",
          "016:L3",
          "016:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:003:105:113",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "016:L2",
              "expression": "Tomas Elde",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Says his contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Asks the agency to communicate directly with Dorian",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Asks the agency to communicate directly with Dorian",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "his contractor, Dorian Wren",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "016:L2",
              "expression": "Tomas Elde",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "016:L3",
              "expression": "Mira Sol",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Asks the agency to communicate directly with Dorian",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Says his contractor, Dorian Wren, is away until 9 September.",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-004:001:132:173",
      "sender_id": "entity:property-004:003:105:113",
      "recipient_id": "entity:property-004:001:64:72",
      "purpose": "appointment",
      "status": "answered",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r10",
      "provenance": {
        "source_ids": [
          "020:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "The tenant says",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "The tenant says the lock is now worse than before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "the lock is now worse than before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "the lock is now worse than before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "the lock",
              "occurrence": 2
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "the lock is now worse than before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "worse than before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "worse than before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "the lock is now worse than before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "The tenant says",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-004:001:132:147",
      "location_text": null,
      "observation_kind": "physical_condition",
      "attribute": "reported comparative condition",
      "value": {
        "kind": "text",
        "value": "worse than before"
      },
      "quoted_expression": "the lock is now worse than before",
      "epistemic_status": "asserted",
      "observed_at_text": null
    },
    {
      "id": "b002:r14",
      "provenance": {
        "source_ids": [
          "021:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "The tenant",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "a broken bedroom blind that lets in light",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Raises other unresolved concerns",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "broken bedroom blind",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "broken bedroom blind that lets in light",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "broken bedroom blind",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "a broken bedroom blind that lets in light",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "unresolved concerns",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-004:021:165:204",
      "asset_id": "entity:property-004:021:165:185",
      "property_id": null,
      "description": "Tenant raises an unresolved concern about the broken bedroom blind letting in light.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b002:r15",
      "provenance": {
        "source_ids": [
          "021:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "The tenant",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "glazing in a door that the landlord had previously said would be addressed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Raises other unresolved concerns",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "glazing in a door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "glazing in a door that the landlord had previously said would be addressed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "glazing in a door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "glazing in a door that the landlord had previously said would be addressed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "unresolved concerns",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-004:021:206:280",
      "asset_id": "entity:property-004:021:206:223",
      "property_id": null,
      "description": "Tenant raises an unresolved glazing concern and reports that the landlord had previously said it would be addressed.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b002:r16",
      "provenance": {
        "source_ids": [
          "021:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "The tenant",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "hot water that she says is too hot",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Raises other unresolved concerns",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "hot water that she says is too hot",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "hot water that she says is too hot",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "hot water",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "hot water that she says is too hot",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "unresolved concerns",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-004:021:286:320",
      "asset_id": "entity:property-004:021:286:295",
      "property_id": null,
      "description": "Tenant says the hot water is too hot and raises this as an unresolved concern.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b002:r20",
      "provenance": {
        "source_ids": [
          "023:L2",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "The tenant says",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Says the contractor is meant to come that day sometime after 10:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "is meant to come that day sometime after 10:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "is meant to come",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "appointment_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "that day sometime after 10:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the lock has been repaired or replaced",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "tenant_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Nessa Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "is meant to come",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "that day sometime after 10:00",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "appointment",
      "appointment_id": "entity:property-004:023:151:180",
      "request_id": "entity:property-004:001:132:173",
      "provider_id": "entity:property-004:011:153:163",
      "tenant_id": "entity:property-004:001:34:44",
      "status": "proposed",
      "time_text": "that day sometime after 10:00",
      "supersedes_record_id": null
    },
    {
      "id": "b002:r21",
      "provenance": {
        "source_ids": [
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-004:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "The tenant says",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "there is no confirmation that he has attended or that the lock has been repaired or replaced",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "there is no confirmation that he has attended",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no confirmation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the lock has been repaired or replaced",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the lock",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "there is no confirmation that he has attended or that the lock has been repaired or replaced",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no confirmation that the lock has been repaired or replaced",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-004:001:132:173",
      "asset_id": "entity:property-004:001:132:147",
      "property_id": null,
      "description": "Tenant reports the contractor is meant to come after 10:00, but there is no confirmation that he attended or that the lock was repaired or replaced.",
      "troubleshooting": "not_established"
    }
  ],
  "gaps": [
    {
      "id": "b002:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-004:021:165:204",
        "entity:property-004:021:206:280",
        "entity:property-004:021:286:320",
        "entity:property-004:021:366:387"
      ],
      "source_ids": [
        "021:L5"
      ],
      "description": "Tenant asks who is handling the blind, glazing, and hot-water concerns; the agency representative cannot confirm their status or ownership. Responsibility and status for these matters remain unestablished."
    },
    {
      "id": "b002:g2",
      "kind": "timing",
      "entity_ids": [
        "entity:property-004:001:132:173",
        "entity:property-004:011:153:163",
        "entity:property-004:019:222:238"
      ],
      "source_ids": [
        "018:L5",
        "019:L5",
        "020:L5"
      ],
      "description": "No date for Dorian Wren's visit is recorded in the maintenance note; the later reported visit included a promise to return the following week without a date or time. No confirmed appointment time or inspection outcome is recorded."
    }
  ]
}
```
