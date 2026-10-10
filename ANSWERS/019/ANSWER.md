# Proposed answer

Case 019; checkpoint `019-at-016`; prefix ends at event `16`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

## Execution status

This system has no external execution environment, so it did not carry out any proposed actions. Actions and outcomes recorded in the case history are evidence; the actions below are recommendations. The case evidence bundle contains the supplied history and extracted support.

Disposition: **act**.

## Proposed actions

### Request clarification

```json
{
  "id": "a1",
  "request_id": "entity:property-019:001:145:170",
  "basis_record_ids": [
    "b001:r10",
    "b001:r11",
    "b001:r12",
    "b002:r1",
    "b003:r1"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g2"
  ],
  "depends_on_action_ids": [],
  "type": "request_clarification",
  "recipient_id": "entity:property-019:008:106:116",
  "topic": "authorization",
  "question": "Please explain what instruction or authority you understood permitted work to start and how access was arranged. Please also provide a breakdown of the £174 invoice and identify which charges relate to the original six items versus any additions or variations. This is needed to assess the disputed authority and the amount sought."
}
```

### Request approval

```json
{
  "id": "a2",
  "request_id": "entity:property-019:001:145:170",
  "basis_record_ids": [
    "b001:r9",
    "b003:r1"
  ],
  "basis_gap_ids": [
    "b002:g1"
  ],
  "depends_on_action_ids": [],
  "type": "request_approval",
  "recipient_id": "entity:property-019:004:198:206",
  "scope": [
    "repair",
    "replace"
  ],
  "proposed_amount_minor": 17400,
  "currency": "GBP"
}
```

### Handle document

```json
{
  "id": "a3",
  "request_id": "entity:property-019:001:145:170",
  "basis_record_ids": [
    "b003:r1"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "handle_document",
  "operation": "register",
  "document_id": "entity:property-019:016:673:699",
  "recipient_id": null,
  "document_kind": "invoice"
}
```

### Record evidence

```json
{
  "id": "a4",
  "request_id": "entity:property-019:001:145:170",
  "basis_record_ids": [
    "b002:r1",
    "b003:r1"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [
    "a3"
  ],
  "type": "record_evidence",
  "record_ids": [
    "b002:r1",
    "b003:r1"
  ]
}
```

### Change workflow

```json
{
  "id": "a5",
  "request_id": "entity:property-019:001:145:170",
  "basis_record_ids": [
    "b002:r1",
    "b003:r1"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g2"
  ],
  "depends_on_action_ids": [
    "a4"
  ],
  "type": "change_workflow",
  "operation": "review_completion",
  "value": "completion_review",
  "reason": "The provider reported completing the work and an invoice describes work invoiced, but authorization, access, and scope/price remain unresolved. Review the reported completion without closing the request."
}
```

### Escalate

```json
{
  "id": "a6",
  "request_id": "entity:property-019:001:145:170",
  "basis_record_ids": [
    "b001:r10",
    "b001:r11",
    "b001:r12",
    "b001:r9",
    "b002:r1",
    "b003:r1"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g2"
  ],
  "depends_on_action_ids": [],
  "type": "escalate",
  "recipient_id": null,
  "responsible_role": "supervisor",
  "causes": [
    {
      "category": "authority_required",
      "explanation": "The provider reports completed work despite the recorded instruction not to begin before quote review and written authority; the landlord's earlier general approval had no stated price limit.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "008:L5",
          "expression": "The email expressly said not to carry out any work until Northbridge Lettings reviewed the price and issued written authority.",
          "occurrence": 1
        },
        {
          "source_id": "005:L5",
          "expression": "No price limit, item-by-item instructions, or other conditions were stated.",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b001:r10",
        "b001:r11",
        "b001:r9",
        "b002:r1",
        "b003:r1"
      ],
      "gap_ids": [
        "b002:g1"
      ]
    },
    {
      "category": "conflicting_evidence",
      "explanation": "The written instruction required quote review and written authority, while Rowan reported believing the instruction was to carry out the work.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "008:L5",
          "expression": "The email expressly said not to carry out any work until Northbridge Lettings reviewed the price and issued written authority.",
          "occurrence": 1
        },
        {
          "source_id": "013:L5",
          "expression": "Rowan said he had not realised a quote was needed and thought the instruction was to carry out the work",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b001:r12",
        "b002:r1"
      ],
      "gap_ids": [
        "b002:g1"
      ]
    }
  ],
  "requested_intervention": "adjudicate_evidence",
  "intervention_detail": "Review the conflicting account of authority, the completed-work report and invoice, and determine the appropriate handling of the retrospective £174 spend before an approval decision or closure.",
  "blocking": true,
  "blocked_action_ids": [
    "a2"
  ],
  "handover": "The invoice and provider completion report are part of the case evidence; a provider clarification is requested separately. No conclusion is proposed that the work was authorized or that the invoice is payable."
}
```

## Action dependencies

- `a4` depends on `a3`.
- `a5` depends on `a4`.

## Human interventions

```json
[]
```

Conclusion records: []

## Evidence and reasoning

The evidence identifies the maintenance request as e3, and the cited records and gaps belong to that request. The provider reported completing work, and the invoice reports remedial work invoiced at £174. The earlier written instruction said not to begin before quote review and written authority; the provider later reported understanding the instruction differently. Register and record the existing invoice and work evidence, seek the provider's account and breakdown, and place the matter in completion review without proposing closure. Escalate the authority and evidence conflict for human review. A retrospective request for the landlord's spend decision is retained, but it is explicitly blocked by the escalation; it does not depend on that escalation, avoiding a circular dependency.

## Assumptions

- The cited request, provider, and six-item work description refer to the same case-local job, as supported by their shared request and work descriptions.
- The proposed £174 approval request seeks a retrospective spend decision, not authority to start or expand work.

## Uncertainties

- The completion account is reported by the provider and the invoice describes invoiced work; neither independently verifies the work's condition or completion.
- The evidence does not establish how access was arranged, who authorized work to start, or whether every invoiced item was within the original scope.
- The landlord's general approval stated no price limit, while the written instruction required quote review and written authority before work. The authority basis and agreed amount for the completed work remain unresolved.

## Alternatives considered

- Closure is not proposed because reported completion does not resolve the authority, scope, and spend questions.
- A repeat invoice request is not proposed because the invoice was received and the invoice obligation is recorded as satisfied.
- The retrospective approval request is retained but blocked pending human review; it is not made dependent on the escalation action.

## Cited prefix evidence

```json
{
  "source_id": "008:L5",
  "expression": "The email expressly said not to carry out any work until Northbridge Lettings reviewed the price and issued written authority.",
  "occurrence": 1
}
```
Event `008`, source `008:L5`, event character range [142, 527).

> Sent the six-item description and requested a quotation only. The email expressly said not to carry out any work until Northbridge Lettings reviewed the price and issued written authority. It asked for two or three possible inspection windows and confirmation of access requirements, and said arrangements would be confirmed with the tenant despite his earlier notice that he had left.

```json
{
  "source_id": "013:L5",
  "expression": "Rowan said he had not realised a quote was needed and thought the instruction was to carry out the work; he said he had completed it the previous day.",
  "occurrence": 1
}
```
Event `013`, source `013:L5`, event character range [141, 544).

> Maya called about a quotation. Rowan said he had not realised a quote was needed and thought the instruction was to carry out the work; he said he had completed it the previous day. Maya asked him to send an invoice, and Rowan agreed to send it with paperwork that evening. The call did not establish when or how access had been arranged, who had authorised work to start, or the agreed scope and price.

```json
{
  "source_id": "016:L5",
  "expression": "No quotation, itemised prices, prior approval of variations, or payment terms are described in the accompanying message.",
  "occurrence": 1
}
```
Event `016`, source `016:L5`, event character range [145, 608).

> Invoice description lists replacing the broken lounge floorboard and reinstating carpet; removing the front lounge blind and supplying and installing a new Venetian blind; refixing the cupboard handle with new fixings; adjusting the kitchen blind mechanism; retightening the toilet seat; and reattaching the front-gate hinge with new fixings. No quotation, itemised prices, prior approval of variations, or payment terms are described in the accompanying message.

```json
{
  "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L15",
  "expression": "Remedial works £174.00",
  "occurrence": 1
}
```
Document `019:359da97468bcc9ca91bf` (`attachments/remedial-works-invoice.pdf`), page 1, source `attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L15`, extracted page Unicode character range [552, 574); available at events 016.

> Remedial works £174.00

```json
{
  "source_id": "005:L5",
  "expression": "Yes, I am happy for you to proceed with the remedial works.",
  "occurrence": 1
}
```
Event `005`, source `005:L5`, event character range [117, 263).

> Replied, “Yes, I am happy for you to proceed with the remedial works.” No price limit, item-by-item instructions, or other conditions were stated.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r9",
      "provenance": {
        "source_ids": [
          "005:L2",
          "005:L5"
        ],
        "asserted_by_entity_id": "entity:property-019:004:198:206",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "Yes, I am happy for you to proceed with the remedial works.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "005:L2",
              "expression": "Ivo Marlow",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "for you to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "remedial works",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "happy for you to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "Yes, I am happy for you to proceed with the remedial works.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "happy for you to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "Yes, I am happy",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "005:L2",
              "expression": "Ivo Marlow",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-019:001:145:170",
      "grantor_id": "entity:property-019:004:198:206",
      "grantee_id": "entity:property-019:001:122:142",
      "scope": [
        "repair"
      ],
      "decision": "approved",
      "amount_minor": null,
      "currency": null,
      "conditions": []
    },
    {
      "id": "b001:r10",
      "provenance": {
        "source_ids": [
          "007:L2",
          "007:L5"
        ],
        "asserted_by_entity_id": "entity:property-019:001:104:120",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "Selected Alder & Finch Repairs to provide a quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "Alder & Finch Repairs",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "provide a quotation",
              "occurrence": 1
            },
            {
              "source_id": "007:L5",
              "expression": "for an inspection",
              "occurrence": 1
            },
            {
              "source_id": "007:L5",
              "expression": "key-access requirements",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "no work was to begin until the quote had been reviewed and written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "Selected Alder & Finch Repairs to provide a quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "to provide a quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "no work was to begin until the quote had been reviewed and written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "007:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-019:001:145:170",
      "asset_id": null,
      "provider_id": "entity:property-019:004:307:315",
      "scope": [
        "quote",
        "inspect",
        "access"
      ],
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "No work was to begin until the quote had been reviewed and written authority issued."
      ],
      "valid_time_text": null
    },
    {
      "id": "b001:r11",
      "provenance": {
        "source_ids": [
          "007:L2",
          "007:L5"
        ],
        "asserted_by_entity_id": "entity:property-019:001:104:120",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "no work was to begin until the quote had been reviewed and written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constrains_record_id",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "no work was to begin until the quote had been reviewed and written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "until the quote had been reviewed and written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "no work was to begin until the quote had been reviewed and written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "The note records that no work was to begin until the quote had been reviewed and written authority issued.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "until the quote had been reviewed and written authority issued",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "no work was to begin",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "007:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "condition",
      "request_id": "entity:property-019:001:145:170",
      "constrains_record_id": "b001:r10",
      "requirement": "approval",
      "status": "unknown",
      "description": "Work was not to begin until the quote had been reviewed and written authority issued."
    },
    {
      "id": "b001:r12",
      "provenance": {
        "source_ids": [
          "008:L2",
          "008:L3",
          "008:L5"
        ],
        "asserted_by_entity_id": "entity:property-019:001:104:120",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "requested a quotation only",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "008:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "008:L3",
              "expression": "Rowan Pike",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "two or three possible inspection windows",
              "occurrence": 1
            },
            {
              "source_id": "008:L5",
              "expression": "confirmation of access requirements",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "requested a quotation only",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "requested a quotation only",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "requested a quotation only",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "The email expressly said not to carry out any work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "008:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-019:001:145:170",
      "sender_id": "entity:property-019:001:104:120",
      "recipient_id": "entity:property-019:008:106:116",
      "purpose": "appointment",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r1",
      "provenance": {
        "source_ids": [
          "013:L5",
          "016:L5",
          "016:L7"
        ],
        "asserted_by_entity_id": "entity:property-019:008:106:116",
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
              "expression": "Maya called about a quotation. Rowan said he had not realised a quote was needed and thought the instruction was to carry out the work; he said he had completed it the previous day.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "016:L7",
              "expression": "remedial-works-invoice.pdf",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "he had completed it the previous day",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "he had completed it the previous day",
              "occurrence": 1
            },
            {
              "source_id": "016:L5",
              "expression": "Invoice description lists replacing the broken lounge floorboard and reinstating carpet; removing the front lounge blind and supplying and installing a new Venetian blind; refixing the cupboard handle with new fixings; adjusting the kitchen blind mechanism; retightening the toilet seat; and reattaching the front-gate hinge with new fixings. No quotation, itemised prices, prior approval of variations, or payment terms are described in the accompanying message.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "Rowan said",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "he had completed it the previous day",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "he had completed it the previous day",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "Rowan said",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-019:001:145:170",
      "asset_id": null,
      "document_id": "entity:property-019:016:673:699",
      "outcome": "repaired",
      "description": "Rowan reported that he had completed the work the previous day. The invoice description lists replacing the broken lounge floorboard and reinstating carpet; removing the front lounge blind and supplying and installing a new Venetian blind; refixing the cupboard handle with new fixings; adjusting the kitchen blind mechanism; retightening the toilet seat; and reattaching the front-gate hinge with new fixings."
    },
    {
      "id": "b003:r1",
      "provenance": {
        "source_ids": [
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L1",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L10",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L11",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L12",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L13",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L15",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L4",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L5",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L6",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L7",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L8",
          "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L9"
        ],
        "asserted_by_entity_id": null,
        "origin": "document_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L1",
              "expression": "B I L L I N G  D O C U M E N T",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L8",
              "expression": "Replaced the broken lounge floorboard and reinstated carpet.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L9",
              "expression": "Removed the front lounge blind and supplied and installed a new Venetian blind.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L10",
              "expression": "Refixed the cupboard handle with new fixings.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L11",
              "expression": "Adjusted the kitchen blind mechanism.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L12",
              "expression": "Retightened the toilet seat.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L13",
              "expression": "Reattached the front-gate hinge with new fixings.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L7",
              "expression": "Work invoiced",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L6",
              "expression": "18 Brindle Row, Larkspur Vale, ZZ1 1ZZ",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L1",
              "expression": "B I L L I N G  D O C U M E N T",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L7",
              "expression": "Work invoiced",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L8",
              "expression": "Replaced the broken lounge floorboard and reinstated carpet.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L9",
              "expression": "Removed the front lounge blind and supplied and installed a new Venetian blind.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L10",
              "expression": "Refixed the cupboard handle with new fixings.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L11",
              "expression": "Adjusted the kitchen blind mechanism.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L12",
              "expression": "Retightened the toilet seat.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L13",
              "expression": "Reattached the front-gate hinge with new fixings.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L4",
              "expression": "NBL-019-INV-11",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L5",
              "expression": "11 September 2025",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L6",
              "expression": "18 Brindle Row, Larkspur Vale, ZZ1 1ZZ",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L8",
              "expression": "Replaced the broken lounge floorboard and reinstated carpet.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L9",
              "expression": "Removed the front lounge blind and supplied and installed a new Venetian blind.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L10",
              "expression": "Refixed the cupboard handle with new fixings.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L11",
              "expression": "Adjusted the kitchen blind mechanism.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L12",
              "expression": "Retightened the toilet seat.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L13",
              "expression": "Reattached the front-gate hinge with new fixings.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:019:359da97468bcc9ca91bf:2e51f90d258f4a13d227115b6f0cd2a993874f778a9b947dd2eb9ec8e15362a9:p1:L15",
              "expression": "Remedial works £174.00",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-019:001:145:170",
      "asset_id": null,
      "document_id": "entity:property-019:016:673:699",
      "outcome": "repaired",
      "description": "The invoice (reference NBL-019-INV-11, dated 11 September 2025) reports work invoiced at £174.00 for the property: replaced the broken lounge floorboard and reinstated carpet; removed the front lounge blind and supplied and installed a new Venetian blind; refixed the cupboard handle with new fixings; adjusted the kitchen blind mechanism; retightened the toilet seat; and reattached the front-gate hinge with new fixings."
    }
  ],
  "gaps": [
    {
      "id": "b002:g1",
      "kind": "authorization",
      "entity_ids": [
        "entity:property-019:001:104:120",
        "entity:property-019:001:145:170",
        "entity:property-019:008:106:116",
        "entity:property-019:012:273:280"
      ],
      "source_ids": [
        "013:L5",
        "016:L5"
      ],
      "description": "The call report does not establish when or how access was arranged, who authorized work to start, or the agreed scope and price. The invoice description reports no quotation, itemized prices, or prior approval of variations; its invoiced amount does not establish an agreed price or authority to proceed."
    },
    {
      "id": "b002:g2",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-019:001:145:170",
        "entity:property-019:007:274:284",
        "entity:property-019:008:106:116",
        "entity:property-019:011:166:182"
      ],
      "source_ids": [
        "013:L5",
        "015:L5"
      ],
      "description": "The call did not establish how access had been arranged. The case note reports no appointment details, visit narrative, or separate completion evidence."
    }
  ]
}
```
