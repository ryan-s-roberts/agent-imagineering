# Decision rationale and evidence

Case 027; checkpoint `027-at-017`; prefix ends at event `17`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The operational objective is to decide whether to proceed with the quoted move-out works, but the workflow records that landlord approval is required before proceeding. The latest call added no approval or rejection, so the decision remains pending. Remind the landlord to respond, and independently request the quote detail missing from its single total so the decision can be better informed. Do not instruct work or change the existing awaiting-approval status.

## Assumptions

- The quotation, approval request, and latest call concern the same move-out works, based on the chronological continuity and references to the specific quotation.

## Uncertainties

- The call transcript reports that no substantive approval or rejection was captured; it does not establish whether the landlord responded through another channel.
- The quote provides a total but no task-level cost allocation or stated exclusions.

## Alternatives considered

- No provider instruction is proposed: the provider said scheduling would only be checked after approval, and approval remains outstanding.
- No workflow status change is proposed because the supplied status is already awaiting approval.

## Cited prefix evidence

```json
{
  "source_id": "015:L5",
  "expression": "landlord approval is required before proceeding",
  "occurrence": 1
}
```
Event `015`, source `015:L5`, event character range [135, 292).

> Quote received; the stated total is £3,865.68 and is above the approval threshold. The workflow records that landlord approval is required before proceeding.

```json
{
  "source_id": "016:L5",
  "expression": "Waiting for the landlord to respond to the request to approve or reject the specific quotation.",
  "occurrence": 1
}
```
Event `016`, source `016:L5`, event character range [133, 228).

> Waiting for the landlord to respond to the request to approve or reject the specific quotation.

```json
{
  "source_id": "017:L5",
  "expression": "No substantive discussion, approval or rejection was captured.",
  "occurrence": 1
}
```
Event `017`, source `017:L5`, event character range [115, 263).

> Call transcript contains an automated recording notice and a brief unclear utterance. No substantive discussion, approval or rejection was captured.

```json
{
  "source_id": "attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:L21",
  "expression": "Labour & Materials £3,865.68",
  "occurrence": 1
}
```
Document `027:f506cda19e3e397c5e5c` (`attachments/move-out-works-quotation.pdf`), page 1, source `attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:L21`, extracted page Unicode character range [604, 632); available at events 017.

> Labour & Materials £3,865.68

```json
{
  "source_id": "013:L5",
  "expression": "without task-by-task prices or stated exclusions",
  "occurrence": 1
}
```
Event `013`, source `013:L5`, event character range [144, 810).

> Sent a quotation for the property and invited questions. The listed tasks are: repair damaged newel post; address screw damage to a door frame; fill holes in uPVC window frames; make good wall damage; fit a new door threshold; fit a toilet-roll holder; renew smoke detector; rehang kitchen radiator; renew an extractor fan; renew en-suite radiator; renew an extractor fan; stain-block water-damaged ceilings; and reinstate decoration. The quotation text then gives a single “Labour & Materials” heading, without task-by-task prices or stated exclusions. Iris said she could not provide an attendance date at this stage and would only check scheduling after approval.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r1",
      "provenance": {
        "source_ids": [
          "013:L2",
          "013:L5"
        ],
        "asserted_by_entity_id": "entity:property-027:004:137:154",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "quotation for the property",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "for the property",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Iris Bell",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "repair damaged newel post",
              "occurrence": 1
            },
            {
              "source_id": "013:L5",
              "expression": "renew smoke detector",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "would only check scheduling after approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "Sent a quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "would only check scheduling after approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "repair damaged newel post",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Iris Bell",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-027:004:220:234",
      "asset_id": null,
      "provider_id": "entity:property-027:004:137:154",
      "scope": [
        "repair",
        "replace"
      ],
      "amount_minor": 386568,
      "currency": "GBP",
      "conditions": [
        "Provider would check scheduling only after approval"
      ],
      "valid_time_text": null
    },
    {
      "id": "b002:r2",
      "provenance": {
        "source_ids": [
          "013:L5",
          "014:L2",
          "014:L3",
          "014:L5",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-027:001:32:41",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "asked whether the landlord was happy to proceed at that cost",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "014:L3",
              "expression": "Owen Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "Iris said",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "repair damaged newel post",
              "occurrence": 1
            },
            {
              "source_id": "013:L5",
              "expression": "renew smoke detector",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "asked whether the landlord was happy to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "£3,865.68",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "£3,865.68",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "landlord approval is required before proceeding",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Forwarded the quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "asked whether the landlord was happy to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "asked whether the landlord was happy to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-027:004:220:234",
      "grantor_id": "entity:property-027:002:154:162",
      "grantee_id": "entity:property-027:004:137:154",
      "scope": [
        "repair",
        "replace"
      ],
      "decision": "requested",
      "amount_minor": 386568,
      "currency": "GBP",
      "conditions": [
        "Landlord approval is required before proceeding"
      ]
    },
    {
      "id": "b002:r4",
      "provenance": {
        "source_ids": [
          "016:L2",
          "016:L5"
        ],
        "asserted_by_entity_id": "entity:property-027:001:32:41",
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
              "expression": "request to approve or reject the specific quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "landlord",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "respond to the request to approve or reject",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Waiting for the landlord to respond",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "specific quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Waiting for the landlord to respond",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Waiting for the landlord to respond",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Waiting for the landlord to respond",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "016:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-027:004:220:234",
      "responsible_party_id": "entity:property-027:002:154:162",
      "requirement": "approval",
      "status": "pending",
      "conditions": [
        "Approval or rejection of the specific quotation is outstanding"
      ]
    },
    {
      "id": "b002:r5",
      "provenance": {
        "source_ids": [
          "017:L2",
          "017:L3",
          "017:L5"
        ],
        "asserted_by_entity_id": "entity:property-027:001:32:41",
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
              "expression": "No substantive discussion, approval or rejection was captured",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "017:L3",
              "expression": "Owen Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "approval or rejection",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "No substantive discussion, approval or rejection was captured",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Call transcript",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "No substantive discussion, approval or rejection was captured",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "No substantive discussion, approval or rejection was captured",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-027:004:220:234",
      "sender_id": "entity:property-027:001:32:41",
      "recipient_id": "entity:property-027:002:154:162",
      "purpose": "approval",
      "status": "no_response_reported",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r6",
      "provenance": {
        "source_ids": [
          "015:L2",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-027:001:32:41",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "landlord approval is required before proceeding",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "landlord approval is required before proceeding",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "source_label",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Quote received; the stated total is £3,865.68 and is above the approval threshold. The workflow records that landlord approval is required before proceeding.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "The workflow records",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Quote received",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "landlord approval is required before proceeding",
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
      "type": "request_status",
      "request_id": "entity:property-027:004:220:234",
      "status": "awaiting_approval",
      "source_label": "Workflow records landlord approval is required before proceeding"
    }
  ],
  "gaps": [
    {
      "id": "b002:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-027:004:181:186"
      ],
      "source_ids": [
        "013:L5"
      ],
      "description": "The quotation gives a single “Labour & Materials” heading without task-by-task prices or stated exclusions, so itemized costs and exclusions are not established."
    },
    {
      "id": "b003:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-027:004:181:186",
        "entity:property-027:attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:217:235",
        "entity:property-027:attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:585:603",
        "entity:property-027:attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:604:632"
      ],
      "source_ids": [
        "attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:L20",
        "attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:L21",
        "attachment:027:f506cda19e3e397c5e5c:c408d8e0693db6be73d204d0a419119e782ef944d25e46643554f9e4f8222511:p1:L7"
      ],
      "description": "The quotation gives a single Labour & Materials total (£3,865.68) but does not provide task-by-task prices; task-level cost allocation is not established."
    }
  ]
}
```
