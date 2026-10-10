# Decision rationale and evidence

Case 015; checkpoint `015-at-021`; prefix ends at event `21`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The latest update keeps sanitation on hold until the separate major maintenance is completed, and reports no completion confirmation or booked date. The existing hold should remain; useful next steps are coordinating that prerequisite and resolving the outstanding ambiguity about the landlord’s approval before any later booking or work instruction.

## Assumptions

- The sanitation work in the latest update is the continuing post-tenancy sanitation request (e12), based on the chronological references to that work and the contractor.

## Uncertainties

- The landlord’s “approved quote” update does not identify the quote; the earlier approval was conditional on bond recovery. The supplied evidence does not establish that the condition has been met or that the later update approved the £665 preparation quotation.
- The separate maintenance completion and a sanitation appointment remain unconfirmed.

## Alternatives considered

- Did not resume the request, instruct the contractor, or propose a booking: the latest update expressly makes booking contingent on completion of separate major maintenance, and records no completion confirmation.
- Did not repeat the hold instruction to the contractor: the hold was already confirmed to the contractor (r24).

## Cited prefix evidence

```json
{
  "source_id": "021:L5",
  "expression": "wait three more working days",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [155, 407).

> Recorded the instruction to wait three more working days because the separate major maintenance work must be completed before the sanitation work can be booked. No date is booked, and no update confirming completion of the maintenance work is recorded.

```json
{
  "source_id": "021:L5",
  "expression": "the separate major maintenance work must be completed before the sanitation work can be booked",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [155, 407).

> Recorded the instruction to wait three more working days because the separate major maintenance work must be completed before the sanitation work can be booked. No date is booked, and no update confirming completion of the maintenance work is recorded.

```json
{
  "source_id": "021:L5",
  "expression": "no update confirming completion of the maintenance work is recorded",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [155, 407).

> Recorded the instruction to wait three more working days because the separate major maintenance work must be completed before the sanitation work can be booked. No date is booked, and no update confirming completion of the maintenance work is recorded.

```json
{
  "source_id": "020:L5",
  "expression": "The contractor had not provided a confirmed slot.",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [153, 302).

> Recorded that the post-tenancy work remained dependent on the separate maintenance being completed. The contractor had not provided a confirmed slot.

```json
{
  "source_id": "016:L5",
  "expression": "Sent the brief update “approved quote” without identifying which quote it referred to.",
  "occurrence": 1
}
```
Event `016`, source `016:L5`, event character range [135, 221).

> Sent the brief update “approved quote” without identifying which quote it referred to.

```json
{
  "source_id": "008:L5",
  "expression": "Happy to approve if they are recovered from the bond",
  "occurrence": 1
}
```
Event `008`, source `008:L5`, event character range [134, 257).

> Replied: “Happy to approve if they are recovered from the bond as there is no way it was in that state when they moved in.”

```json
{
  "source_id": "attachment:015:c613cfa2039ba14ce62b:001c56f26bed1109ac5b78c450f6ba38b76bf376a22cc0797ef3e675f7be74b0:p1:L8",
  "expression": "Degrease oven, hob and extractor.",
  "occurrence": 1
}
```
Document `015:c613cfa2039ba14ce62b` (`attachments/property-preparation-quotation.pdf`), page 1, source `attachment:015:c613cfa2039ba14ce62b:001c56f26bed1109ac5b78c450f6ba38b76bf376a22cc0797ef3e675f7be74b0:p1:L8`, extracted page Unicode character range [249, 282); available at events 021.

> Degrease oven, hob and extractor.

```json
{
  "source_id": "attachment:015:c613cfa2039ba14ce62b:001c56f26bed1109ac5b78c450f6ba38b76bf376a22cc0797ef3e675f7be74b0:p1:L9",
  "expression": "Shampoo carpets in Bedroom 1, stairs and landings.",
  "occurrence": 1
}
```
Document `015:c613cfa2039ba14ce62b` (`attachments/property-preparation-quotation.pdf`), page 1, source `attachment:015:c613cfa2039ba14ce62b:001c56f26bed1109ac5b78c450f6ba38b76bf376a22cc0797ef3e675f7be74b0:p1:L9`, extracted page Unicode character range [283, 333); available at events 021.

> Shampoo carpets in Bedroom 1, stairs and landings.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r9",
      "provenance": {
        "source_ids": [
          "008:L1",
          "008:L2",
          "008:L3",
          "008:L5"
        ],
        "asserted_by_entity_id": "entity:property-015:007:107:115",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "Happy to approve",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "008:L2",
              "expression": "Nessa Quill",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "008:L3",
              "expression": "Mira Venn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "Happy to approve",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "Happy to approve if they are recovered from the bond",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "if they are recovered from the bond",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "008:L1",
              "expression": "Channel: Email",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "if they are recovered from the bond",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "Happy to approve",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "008:L2",
              "expression": "Nessa Quill",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-015:002:202:225",
      "grantor_id": "entity:property-015:007:107:115",
      "grantee_id": "entity:property-015:001:32:41",
      "scope": [
        "unspecified"
      ],
      "decision": "approved",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "Approval depends on recovering the cost from the bond."
      ]
    },
    {
      "id": "b002:comm_ambiguous_approval",
      "provenance": {
        "source_ids": [
          "016:L2",
          "016:L3",
          "016:L5"
        ],
        "asserted_by_entity_id": "entity:property-015:007:107:115",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "approved quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "016:L2",
              "expression": "Nessa Quill",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "016:L3",
              "expression": "Mira Venn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "approved quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Sent the brief update “approved quote”",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Sent the brief update “approved quote” without identifying which quote it referred to.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Sent the brief update “approved quote” without identifying which quote it referred to.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "approved quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "016:L2",
              "expression": "Nessa Quill",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-015:002:202:225",
      "sender_id": "entity:property-015:007:107:115",
      "recipient_id": "entity:property-015:001:32:41",
      "purpose": "approval",
      "status": "answered",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:status_hold_6",
      "provenance": {
        "source_ids": [
          "021:L2",
          "021:L5"
        ],
        "asserted_by_entity_id": "entity:property-015:001:32:41",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "the sanitation work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "wait three more working days",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "source_label",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Recorded the instruction to wait three more working days because the separate major maintenance work must be completed before the sanitation work can be booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Recorded the instruction to wait three more working days because the separate major maintenance work must be completed before the sanitation work can be booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "the separate major maintenance work must be completed before the sanitation work can be booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "wait three more working days",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "021:L2",
              "expression": "Mira Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "request_status",
      "request_id": "entity:property-015:002:202:225",
      "status": "on_hold",
      "source_label": "Recorded the instruction to wait three more working days because the separate major maintenance work must be completed before the sanitation work can be booked."
    },
    {
      "id": "b002:obligation_appointment",
      "provenance": {
        "source_ids": [
          "017:L2",
          "017:L3",
          "017:L5",
          "021:L5"
        ],
        "asserted_by_entity_id": "entity:property-015:001:32:41",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "the post-tenancy work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "017:L3",
              "expression": "Elian Wren",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "propose a date and time",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Asked the contractor to propose a date and time",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "the separate major maintenance work must be completed before the sanitation work can be booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Asked the contractor to propose a date and time for the post-tenancy work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Asked the contractor to propose a date and time",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Asked the contractor to propose a date and time",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Mira Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-015:002:202:225",
      "responsible_party_id": "entity:property-015:002:106:116",
      "requirement": "appointment",
      "status": "requested",
      "conditions": [
        "No booking until the separate major maintenance work is completed."
      ]
    },
    {
      "id": "b002:condition_maintenance_first",
      "provenance": {
        "source_ids": [
          "021:L2",
          "021:L5"
        ],
        "asserted_by_entity_id": "entity:property-015:001:32:41",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "the sanitation work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constrains_record_id",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "the separate major maintenance work must be completed before the sanitation work can be booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "must be completed before the sanitation work can be booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "no update confirming completion of the maintenance work is recorded",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "the separate major maintenance work must be completed before the sanitation work can be booked. No date is booked, and no update confirming completion of the maintenance work is recorded.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Recorded the instruction to wait three more working days because the separate major maintenance work must be completed before the sanitation work can be booked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "must be completed before the sanitation work can be booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "must be completed before the sanitation work can be booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "021:L2",
              "expression": "Mira Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "condition",
      "request_id": "entity:property-015:002:202:225",
      "constrains_record_id": "b002:obligation_appointment",
      "requirement": "confirmation",
      "status": "unknown",
      "description": "Separate major maintenance must be completed before sanitation can be booked; no update confirming completion is recorded."
    }
  ],
  "gaps": [
    {
      "id": "b001:g1",
      "kind": "authorization",
      "entity_ids": [
        "entity:property-015:002:202:225",
        "entity:property-015:006:157:167",
        "entity:property-015:007:107:115"
      ],
      "source_ids": [
        "007:L5",
        "008:L5"
      ],
      "description": "The landlord's conditional approval was requested for work described generally as post-tenancy work according to inspection instructions, while the £665 quote included carpet shampooing and garden tasks not listed in that approval request. Whether the conditional approval covered the full quoted scope is unclear."
    },
    {
      "id": "b002:gap_quote_reference",
      "kind": "identity",
      "entity_ids": [
        "entity:property-015:002:202:225",
        "entity:property-015:015:199:225",
        "entity:property-015:015:335:365",
        "entity:property-015:016:158:172"
      ],
      "source_ids": [
        "016:L5"
      ],
      "description": "The landlord's update says “approved quote” but does not identify which quote, so its referent and applicable work scope are unresolved."
    },
    {
      "id": "b002:gap_visit_timing",
      "kind": "timing",
      "entity_ids": [
        "entity:property-015:002:202:225",
        "entity:property-015:001:437:449",
        "entity:property-015:002:106:116"
      ],
      "source_ids": [
        "017:L5",
        "018:L5",
        "019:L5",
        "020:L5",
        "021:L5"
      ],
      "description": "No visit was booked or confirmed; no firm date or confirmed contractor slot is recorded, and no maintenance completion date/update is recorded."
    }
  ]
}
```
