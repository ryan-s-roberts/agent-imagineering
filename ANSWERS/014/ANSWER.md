# Proposed answer

Case 014; checkpoint `014-at-019`; prefix ends at event `19`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

## Execution status

This system has no external execution environment, so it did not carry out any proposed actions. Actions and outcomes recorded in the case history are evidence; the actions below are recommendations. The case evidence bundle contains the supplied history and extracted support.

Disposition: **act**.

## Proposed actions

### Request clarification

```json
{
  "id": "a1",
  "request_id": "entity:property-014:009:128:143",
  "basis_record_ids": [
    "b002:r19",
    "b002:r20",
    "b002:r21",
    "b002:r22",
    "b002:r4",
    "b002:r5"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "request_clarification",
  "recipient_id": "entity:property-014:001:34:43",
  "topic": "appointment",
  "question": "Please confirm directly whether you can admit the contractor on 15 January, 09:00–11:00, and can receive the required direct call and at least 30 minutes’ notice. This confirmation is needed to book the offered slot and arrange access."
}
```

### Propose booking

```json
{
  "id": "a2",
  "request_id": "entity:property-014:009:128:143",
  "basis_record_ids": [
    "b002:r19",
    "b002:r20",
    "b002:r21",
    "b002:r22"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [
    "a1"
  ],
  "type": "propose_booking",
  "provider_id": "entity:property-014:005:107:125",
  "tenant_id": "entity:property-014:001:34:43",
  "time_text": "15 January, 09:00–11:00; proposed subject to Leah’s direct access confirmation and the provider securing the slot before 17:30",
  "replaces_appointment_id": null
}
```

### Instruct provider

```json
{
  "id": "a3",
  "request_id": "entity:property-014:009:128:143",
  "basis_record_ids": [
    "b002:r20",
    "b002:r8",
    "b002:r9"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [
    "a2"
  ],
  "type": "instruct_provider",
  "provider_id": "entity:property-014:005:107:125",
  "scope": [
    "inspect"
  ],
  "authorization_record_ids": [
    "b002:r8",
    "b002:r9"
  ],
  "conditions": [
    "Diagnostic inspection only at the proposed appointment.",
    "Proceed under this authority only if the incident is treated as a qualifying urgent repair.",
    "The £250 limit applies to the incident total; do not undertake additional repair work or parts beyond applicable authority, and refer for further consent where required."
  ]
}
```

### Request clarification

```json
{
  "id": "a4",
  "request_id": "entity:property-014:009:128:143",
  "basis_record_ids": [
    "b002:r14",
    "b002:r18",
    "b002:r10",
    "b002:r11",
    "b002:r12"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "request_clarification",
  "recipient_id": "entity:property-014:001:34:43",
  "topic": "other",
  "question": "Is your niece’s spare room actually available tonight, and have you confirmed whether the entrance is step-free? If it is a feasible option, would you prefer help with transport, or would heater delivery be more useful? This determines which interim arrangement to explore."
}
```

### Escalate

```json
{
  "id": "a5",
  "request_id": "entity:property-014:009:128:143",
  "basis_record_ids": [
    "b002:r16",
    "b002:r17"
  ],
  "basis_gap_ids": [
    "b002:g1"
  ],
  "depends_on_action_ids": [],
  "type": "escalate",
  "recipient_id": "entity:property-014:007:376:384",
  "responsible_role": "landlord",
  "causes": [
    {
      "category": "authority_required",
      "explanation": "The standing urgent-repair authority does not cover temporary heating, transport, or accommodation, and the duty file records no separate spending limit. Human approval is needed before committing any such expenditure.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "017:L5",
          "expression": "The duty file records no separate spending limit for temporary equipment, transport or accommodation.",
          "occurrence": 1
        },
        {
          "source_id": "007:L5",
          "expression": "Temporary heaters, transport and accommodation are not covered by this repair authority.",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b002:r16",
        "b002:r17"
      ],
      "gap_ids": [
        "b002:g1"
      ]
    }
  ],
  "requested_intervention": "approve_spend",
  "intervention_detail": "Please provide separate spending authority, if appropriate, for a feasible temporary-heating delivery or transport arrangement once Leah’s need and the available option and cost are established. Do not treat this request as authority to incur expenditure.",
  "blocking": false,
  "blocked_action_ids": [],
  "handover": "This approval issue is separate from the proposed £168 diagnostic inspection under the conditional urgent-repair authority; the diagnostic appointment may proceed independently if its prerequisites are met."
}
```

### Provide guidance

```json
{
  "id": "a6",
  "request_id": "entity:property-014:009:128:143",
  "basis_record_ids": [
    "b002:r14",
    "b002:r16"
  ],
  "basis_gap_ids": [
    "b002:g1"
  ],
  "depends_on_action_ids": [],
  "type": "provide_guidance",
  "recipient_id": "entity:property-014:001:92:112",
  "steps": [
    "Check approved suppliers for availability and price of heater delivery, as the duty manager said the office could do.",
    "Do not order, promise payment, or otherwise commit spending without separate applicable authority."
  ],
  "requested_feedback": "Report feasible supplier options and their costs for consideration."
}
```

### Notify

```json
{
  "id": "a7",
  "request_id": "entity:property-014:009:128:143",
  "basis_record_ids": [
    "b002:r18",
    "b002:r19",
    "b002:r20",
    "b002:r21",
    "b002:r22"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "notify",
  "recipient_id": "entity:property-014:001:34:43",
  "purpose": "progress",
  "message": "We have received your update. The contractor has offered a 15 January, 09:00–11:00 diagnostic slot, but it is not booked and must be secured by 17:30. We are seeking your direct access confirmation, including the call and notice arrangements. No interim arrangement is yet confirmed.",
  "about_record_ids": [
    "b002:r18",
    "b002:r19",
    "b002:r20",
    "b002:r21",
    "b002:r22"
  ]
}
```

## Action dependencies

- `a2` depends on `a1`.
- `a3` depends on `a2`.

## Human interventions

```json
[]
```

Conclusion records: []

## Evidence and reasoning

The immediate objective is to secure the newly available 15 January diagnostic visit before its 17:30 booking deadline, while obtaining Leah’s required direct access confirmation. The latest report says the living room is now 10°C and no appointment or interim arrangement is confirmed. I propose the inspection under the landlord’s conditional urgent-repair authority, expressly preserving that it may be used only if the incident is treated as qualifying urgent repair. In parallel, clarify whether the niece’s room is actually usable, coordinate a no-commitment supplier check, and seek separate landlord spending approval for any interim provision.

## Assumptions

- The successive references to the heating failure and diagnostic visit concern the same ongoing case-local repair, based on the continuous chronology and parties; this does not resolve any extraction uncertainty.
- The proposed inspection is limited to the £168 diagnostic call-out. No repair, parts, temporary heater, transport, or accommodation spending is authorized by this proposal.

## Uncertainties

- Leah’s reported room temperature and the possibility of the niece’s room are participant reports, not independently verified conditions.
- The niece’s room availability and step-free access remain unconfirmed; the requested interim option and its cost are also not established.
- Urgent-repair classification is a supported operational inference from the worsening cold, lack of safe temporary heat, and delayed standard visit; the cited authority remains conditional on that classification.

## Alternatives considered

- The 17 January standard offer is not a suitable fallback to rely on because Leah cannot guarantee access then.
- No interim purchase or transport is proposed: the duty file establishes no separate spending limit, and the need, option, and cost are not yet confirmed.

## Cited prefix evidence

```json
{
  "source_id": "019:L5",
  "expression": "could be held only if booked by 17:30",
  "occurrence": 1
}
```
Event `019`, source `019:L5`, event character range [155, 496).

> Said a cancellation appointment for 15 January, 09:00–11:00, had become available and could be held only if booked by 17:30. It would be the same £168 diagnostic call-out; no repair work or parts were included. Leah's direct confirmation of access, including the required call and notice, would still be needed. The slot has not been booked.

```json
{
  "source_id": "019:L5",
  "expression": "The slot has not been booked.",
  "occurrence": 1
}
```
Event `019`, source `019:L5`, event character range [155, 496).

> Said a cancellation appointment for 15 January, 09:00–11:00, had become available and could be held only if booked by 17:30. It would be the same £168 diagnostic call-out; no repair work or parts were included. Leah's direct confirmation of access, including the required call and notice, would still be needed. The slot has not been booked.

```json
{
  "source_id": "019:L5",
  "expression": "Leah's direct confirmation of access, including the required call and notice, would still be needed",
  "occurrence": 1
}
```
Event `019`, source `019:L5`, event character range [155, 496).

> Said a cancellation appointment for 15 January, 09:00–11:00, had become available and could be held only if booked by 17:30. It would be the same £168 diagnostic call-out; no repair work or parts were included. Leah's direct confirmation of access, including the required call and notice, would still be needed. The slot has not been booked.

```json
{
  "source_id": "013:L5",
  "expression": "She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call.",
  "occurrence": 1
}
```
Event `013`, source `013:L5`, event character range [112, 363).

> Confirmed she would not use the suspect heater. She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call. She cannot guarantee access on 17 January because of a hospital appointment. No key is held by the agency.

```json
{
  "source_id": "013:L5",
  "expression": "She cannot guarantee access on 17 January because of a hospital appointment.",
  "occurrence": 1
}
```
Event `013`, source `013:L5`, event character range [112, 363).

> Confirmed she would not use the suspect heater. She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call. She cannot guarantee access on 17 January because of a hospital appointment. No key is held by the agency.

```json
{
  "source_id": "018:L5",
  "expression": "Reported the living-room temperature as 10°C at 16:25.",
  "occurrence": 1
}
```
Event `018`, source `018:L5`, event character range [115, 387).

> Reported the living-room temperature as 10°C at 16:25. Her niece's spare room might be available tonight, but Leah had not confirmed whether the entrance was step-free. Asked for an update before the office closed. No appointment or interim arrangement had been confirmed.

```json
{
  "source_id": "018:L5",
  "expression": "No appointment or interim arrangement had been confirmed.",
  "occurrence": 1
}
```
Event `018`, source `018:L5`, event character range [115, 387).

> Reported the living-room temperature as 10°C at 16:25. Her niece's spare room might be available tonight, but Leah had not confirmed whether the entrance was step-free. Asked for an update before the office closed. No appointment or interim arrangement had been confirmed.

```json
{
  "source_id": "014:L5",
  "expression": "If the incident is treated as an urgent repair, Maya may authorise the £168 diagnostic call-out without further consent",
  "occurrence": 1
}
```
Event `014`, source `014:L5`, event character range [116, 483).

> Clarified that his request for a quote before committing expenditure concerned non-emergency spending and did not withdraw the standing £250 urgent-repair authority. If the incident is treated as an urgent repair, Maya may authorise the £168 diagnostic call-out without further consent; any later work must remain within the incident limit or be referred for consent.

```json
{
  "source_id": "014:L5",
  "expression": "any later work must remain within the incident limit or be referred for consent",
  "occurrence": 1
}
```
Event `014`, source `014:L5`, event character range [116, 483).

> Clarified that his request for a quote before committing expenditure concerned non-emergency spending and did not withdraw the standing £250 urgent-repair authority. If the incident is treated as an urgent repair, Maya may authorise the £168 diagnostic call-out without further consent; any later work must remain within the incident limit or be referred for consent.

```json
{
  "source_id": "017:L5",
  "expression": "The duty file records no separate spending limit for temporary equipment, transport or accommodation.",
  "occurrence": 1
}
```
Event `017`, source `017:L5`, event character range [144, 349).

> Confirmed the office could contact the landlord again and check approved suppliers for heater delivery. The duty file records no separate spending limit for temporary equipment, transport or accommodation.

```json
{
  "source_id": "017:L5",
  "expression": "the office could contact the landlord again and check approved suppliers for heater delivery",
  "occurrence": 1
}
```
Event `017`, source `017:L5`, event character range [144, 349).

> Confirmed the office could contact the landlord again and check approved suppliers for heater delivery. The duty file records no separate spending limit for temporary equipment, transport or accommodation.

```json
{
  "source_id": "018:L5",
  "expression": "Her niece's spare room might be available tonight, but Leah had not confirmed whether the entrance was step-free.",
  "occurrence": 1
}
```
Event `018`, source `018:L5`, event character range [115, 387).

> Reported the living-room temperature as 10°C at 16:25. Her niece's spare room might be available tonight, but Leah had not confirmed whether the entrance was step-free. Asked for an update before the office closed. No appointment or interim arrangement had been confirmed.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r4",
      "provenance": {
        "source_ids": [
          "013:L2",
          "013:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:34:43",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "She can admit a contractor on 15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "admit a contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "She can admit a contractor on 15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "She can admit a contractor on 15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observed_at_text",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Leah Venn (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "She can admit a contractor on 15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "She can admit a contractor on 15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-014:001:34:43",
      "location_text": null,
      "observation_kind": "presence",
      "attribute": "ability to admit a contractor",
      "value": {
        "kind": "boolean",
        "value": true
      },
      "quoted_expression": "She can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call.",
      "epistemic_status": "asserted",
      "observed_at_text": "15 January"
    },
    {
      "id": "b002:r5",
      "provenance": {
        "source_ids": [
          "013:L2",
          "013:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:34:43",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "at least 30 minutes' notice and a direct call",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "She can admit a contractor on 15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "at least 30 minutes' notice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "at least 30 minutes' notice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "15 January",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "if given at least 30 minutes' notice and a direct call",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Leah Venn (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "if given at least 30 minutes' notice and a direct call",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "at least 30 minutes' notice and a direct call",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-014:009:128:143",
      "party_id": "entity:property-014:001:34:43",
      "constraint": "notice",
      "status": "required",
      "time_text": "15 January",
      "description": "Leah said she can admit a contractor on 15 January if given at least 30 minutes' notice and a direct call."
    },
    {
      "id": "b002:r8",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:007:376:384",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "If the incident is treated as an urgent repair, Maya may authorise the £168 diagnostic call-out without further consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "standing £250 urgent-repair authority",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Maya may authorise",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "£168 diagnostic call-out",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Maya may authorise the £168 diagnostic call-out without further consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "£168",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "£168",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "If the incident is treated as an urgent repair",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Owen Pike (Landlord)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "If the incident is treated as an urgent repair",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Maya may authorise the £168 diagnostic call-out without further consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Owen Pike",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-014:009:128:143",
      "grantor_id": "entity:property-014:007:376:384",
      "grantee_id": "entity:property-014:001:63:72",
      "scope": [
        "inspect"
      ],
      "decision": "approved",
      "amount_minor": 16800,
      "currency": "GBP",
      "conditions": [
        "Applies if the incident is treated as an urgent repair; any later work must remain within the incident limit or be referred for consent."
      ]
    },
    {
      "id": "b002:r9",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:007:376:384",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "standing £250 urgent-repair authority",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Owen Pike",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Maya",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "any later work must remain within the incident limit or be referred for consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "did not withdraw the standing £250 urgent-repair authority",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "£250",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "£250",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "any later work must remain within the incident limit or be referred for consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Owen Pike (Landlord)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "If the incident is treated as an urgent repair",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "did not withdraw the standing £250 urgent-repair authority",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Owen Pike",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-014:009:128:143",
      "grantor_id": "entity:property-014:007:376:384",
      "grantee_id": "entity:property-014:001:63:72",
      "scope": [
        "inspect",
        "repair"
      ],
      "decision": "approved",
      "amount_minor": 25000,
      "currency": "GBP",
      "conditions": [
        "Applies to the incident if treated as an urgent repair; later work must remain within the incident limit or be referred for consent."
      ]
    },
    {
      "id": "b002:r10",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:34:43",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "living-room temperature as 10°C at 16:25",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "location_text",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "living-room",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "temperature",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "10°C",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Reported the living-room temperature as 10°C at 16:25.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Reported the living-room temperature as 10°C at 16:25.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observed_at_text",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "16:25",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Reported the living-room temperature as 10°C at 16:25.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "10°C",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-014:008:123:134",
      "location_text": "living-room",
      "observation_kind": "measurement",
      "attribute": "temperature",
      "value": {
        "kind": "number",
        "value": 10.0,
        "unit": "°C"
      },
      "quoted_expression": "Reported the living-room temperature as 10°C at 16:25.",
      "epistemic_status": "asserted",
      "observed_at_text": "16:25"
    },
    {
      "id": "b002:r11",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:34:43",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "niece's spare room might be available tonight",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "niece's spare room",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "niece's spare room might be available tonight",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Her niece's spare room might be available tonight",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "might be available",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observed_at_text",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "tonight",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "might be available tonight",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "might be available tonight",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-014:018:174:192",
      "location_text": null,
      "observation_kind": "presence",
      "attribute": "availability of niece's spare room",
      "value": {
        "kind": "boolean",
        "value": true
      },
      "quoted_expression": "Her niece's spare room might be available tonight",
      "epistemic_status": "uncertain",
      "observed_at_text": "tonight"
    },
    {
      "id": "b002:r12",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:34:43",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "had not confirmed whether the entrance was step-free",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Leah had not confirmed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "whether the entrance was step-free",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "had not confirmed whether the entrance was step-free",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "tonight",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "had not confirmed whether the entrance was step-free",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "had not confirmed whether the entrance was step-free",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "had not confirmed whether the entrance was step-free",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-014:009:128:143",
      "party_id": "entity:property-014:001:34:43",
      "constraint": "other",
      "status": "unknown",
      "time_text": "tonight",
      "description": "Leah had not confirmed whether the entrance to her niece's spare room was step-free."
    },
    {
      "id": "b002:r14",
      "provenance": {
        "source_ids": [
          "015:L2",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:63:72",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "She asked whether delivery of a heater or transport to her niece's home could be arranged.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "She asked whether delivery of a heater or transport to her niece's home could be arranged.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "delivery of a heater or transport to her niece's home",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "could be arranged",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "She still needed to check whether the niece's entrance was step-free.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Maya Chen (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "She asked whether delivery of a heater or transport to her niece's home could be arranged.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "could be arranged",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-014:009:128:143",
      "responsible_party_id": "entity:property-014:001:63:72",
      "requirement": "other",
      "status": "requested",
      "conditions": [
        "Leah still needed to check whether her niece's entrance was step-free."
      ]
    },
    {
      "id": "b002:r16",
      "provenance": {
        "source_ids": [
          "016:L5",
          "017:L2",
          "017:L3",
          "017:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:016:106:118",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The duty file records no separate spending limit for temporary equipment, transport or accommodation.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Priya Noll",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "017:L3",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "no separate spending limit for temporary equipment, transport or accommodation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The duty file records",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responds_to_record_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Asked what cover or separate spending authority applied",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Priya Noll (Duty Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The duty file records no separate spending limit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "no separate spending limit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Priya Noll",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-014:009:128:143",
      "sender_id": "entity:property-014:016:106:118",
      "recipient_id": "entity:property-014:001:63:72",
      "purpose": "clarification",
      "status": "answered",
      "responds_to_record_id": "b002:r15",
      "deadline_text": null
    },
    {
      "id": "b002:r17",
      "provenance": {
        "source_ids": [
          "002:L2",
          "002:L5",
          "016:L5",
          "017:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:63:72",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Asked what cover or separate spending authority applied to temporary heating, transport or accommodation.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "no separate spending limit for temporary equipment, transport or accommodation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "temporary heating, transport or accommodation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "temporary equipment, transport or accommodation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "no separate spending limit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The duty file records no separate spending limit for temporary equipment, transport or accommodation.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Asked what cover or separate spending authority applied",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Asked what cover or separate spending authority applied",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "no separate spending limit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "002:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-014:009:128:143",
      "grantor_id": null,
      "grantee_id": "entity:property-014:001:63:72",
      "scope": [
        "unspecified"
      ],
      "decision": "uncertain",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "The duty file records no separate spending limit for temporary equipment, transport or accommodation."
      ]
    },
    {
      "id": "b002:r18",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L3",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:001:34:43",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "No appointment or interim arrangement had been confirmed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "018:L3",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Asked for an update before the office closed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "No appointment or interim arrangement had been confirmed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "deadline_text",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "before the office closed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Asked for an update before the office closed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "No appointment or interim arrangement had been confirmed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Leah Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-014:009:128:143",
      "sender_id": "entity:property-014:001:34:43",
      "recipient_id": "entity:property-014:001:63:72",
      "purpose": "clarification",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": "before the office closed"
    },
    {
      "id": "b002:r19",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:005:107:125",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "appointment_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "cancellation appointment for 15 January, 09:00–11:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "cancellation appointment",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "could be held only if booked by 17:30",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "15 January, 09:00–11:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart (Heating Contractor, Brackenridge Heat Services)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "could be held only if booked by 17:30",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "appointment",
      "appointment_id": "entity:property-014:012:204:221",
      "request_id": "entity:property-014:009:128:143",
      "provider_id": "entity:property-014:005:107:125",
      "tenant_id": "entity:property-014:001:34:43",
      "status": "proposed",
      "time_text": "15 January, 09:00–11:00; could be held only if booked by 17:30; the slot has not been booked",
      "supersedes_record_id": null
    },
    {
      "id": "b002:r20",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:005:107:125",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "It would be the same £168 diagnostic call-out",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "£168 diagnostic call-out",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "£168",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "£168",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "valid_time_text",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "could be held only if booked by 17:30",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart (Heating Contractor, Brackenridge Heat Services)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "could be held only if booked by 17:30",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-014:009:128:143",
      "asset_id": null,
      "provider_id": "entity:property-014:005:107:125",
      "scope": [
        "inspect"
      ],
      "amount_minor": 16800,
      "currency": "GBP",
      "conditions": [
        "No repair work or parts are included.",
        "Leah's direct confirmation of access, including the required call and notice, is still needed.",
        "The slot has not been booked."
      ],
      "valid_time_text": "The slot could be held only if booked by 17:30."
    },
    {
      "id": "b002:r21",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:005:107:125",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Leah's direct confirmation of access, including the required call and notice, would still be needed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Leah's direct confirmation of access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "direct confirmation of access, including the required call and notice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "would still be needed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "15 January, 09:00–11:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Leah's direct confirmation of access, including the required call and notice, would still be needed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart (Heating Contractor, Brackenridge Heat Services)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "would still be needed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "would still be needed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-014:009:128:143",
      "party_id": "entity:property-014:001:34:43",
      "constraint": "entry_permission",
      "status": "required",
      "time_text": "15 January, 09:00–11:00",
      "description": "Leah's direct confirmation of access, including the required call and notice, is still needed."
    },
    {
      "id": "b002:r22",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-014:005:107:125",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attempted_operation",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "error_text",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart (Heating Contractor, Brackenridge Heat Services)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "The slot has not been booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Daniel Hart",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "workflow_failure",
      "request_id": "entity:property-014:009:128:143",
      "attempted_operation": "Booking the cancellation appointment",
      "error_text": "The slot has not been booked; it could be held only if booked by 17:30.",
      "outcome": "unknown"
    }
  ],
  "gaps": [
    {
      "id": "b002:g1",
      "kind": "authorization",
      "entity_ids": [
        "entity:property-014:009:128:143",
        "entity:property-014:016:328:345",
        "entity:property-014:015:287:307",
        "entity:property-014:015:311:340"
      ],
      "source_ids": [
        "016:L5",
        "017:L5"
      ],
      "description": "The duty file records no separate spending limit for temporary equipment, transport or accommodation; the applicable spending authority and cover for the requested interim arrangements are not established."
    }
  ]
}
```
