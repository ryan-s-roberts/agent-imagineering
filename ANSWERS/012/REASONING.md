# Decision rationale and evidence

Case 012; checkpoint `012-at-025`; prefix ends at event `25`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The current objective is to review the reported lock-work completion without treating a contractor’s statement as verified completion. Most recently, Edrin again said the work was complete, but the file still lacks visit details or attendance evidence; an invoice remains promised. Request work details, put the case into completion review, and wait for the promised invoice. Keep the tenant and landlord informed without claiming the work is verified.

## Assumptions

- Edrin Moss (e50) and Keypath Repairs are the provider associated with the continuing lock-work request, based on the sequence of provider-change and follow-up communications.

## Uncertainties

- The provider’s completion report lacks visit details and attendance evidence; the tenant’s earlier possible appointment time was not confirmed.
- The earlier report of three unsuccessful visits and not having collected management keys is not reconciled with the later completion claim. The supplied material does not establish that these statements are contradictory.
- The packet reports the invoice promise as outstanding; it does not establish whether the promised invoice arrived after the latest call.

## Alternatives considered

- Do not close the request: the provider reported completion, but the record does not yet establish the visit or work outcome.
- Do not seek completion approval or authorize additional work: neither is supported by the latest events.

## Cited prefix evidence

```json
{
  "source_id": "025:L5",
  "expression": "Edrin says the work is complete",
  "occurrence": 1
}
```
Event `025`, source `025:L5`, event character range [136, 364).

> Ilyra follows up about the invoice. Edrin says the work is complete and promises to send the invoice later today. At the time of the call, no invoice, confirmed appointment, visit notes, or other attendance evidence is recorded.

```json
{
  "source_id": "025:L5",
  "expression": "no invoice, confirmed appointment, visit notes, or other attendance evidence is recorded",
  "occurrence": 1
}
```
Event `025`, source `025:L5`, event character range [136, 364).

> Ilyra follows up about the invoice. Edrin says the work is complete and promises to send the invoice later today. At the time of the call, no invoice, confirmed appointment, visit notes, or other attendance evidence is recorded.

```json
{
  "source_id": "025:L5",
  "expression": "promises to send the invoice later today",
  "occurrence": 1
}
```
Event `025`, source `025:L5`, event character range [136, 364).

> Ilyra follows up about the invoice. Edrin says the work is complete and promises to send the invoice later today. At the time of the call, no invoice, confirmed appointment, visit notes, or other attendance evidence is recorded.

```json
{
  "source_id": "022:L5",
  "expression": "have not collected management keys",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [136, 450).

> Edrin says they have tried the property three times but have not found Perrin in. Edrin says they have not collected management keys and cannot give a definite date for doing so. No dates or times for the attempts are provided. Perrin’s messages say they are likely to be at work and request management-key access.

```json
{
  "source_id": "023:L5",
  "expression": "the work was completed on Friday, 19 September",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [136, 448).

> Asked about availability, Edrin says the work was completed on Friday, 19 September, and that invoices are produced on Fridays. Ilyra says no invoice is visible. Edrin says they will check and send it on Friday, 26 September. No visit details, work description, or completion record are provided during the call.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r8",
      "provenance": {
        "source_ids": [
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-012:018:107:117",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the work was completed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the work was completed on Friday, 19 September",
              "occurrence": 1
            },
            {
              "source_id": "023:L5",
              "expression": "No visit details, work description, or completion record are provided during the call",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Edrin says",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the work was completed on Friday, 19 September",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the work was completed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Edrin says",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-012:002:213:217",
      "asset_id": null,
      "document_id": null,
      "outcome": "unknown",
      "description": "Edrin says the work was completed on Friday, 19 September; no visit details, work description, or completion record are provided during the call."
    },
    {
      "id": "b002:r10",
      "provenance": {
        "source_ids": [
          "025:L5"
        ],
        "asserted_by_entity_id": "entity:property-012:018:107:117",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "the work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "the work is complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "Edrin says the work is complete",
              "occurrence": 1
            },
            {
              "source_id": "025:L5",
              "expression": "no invoice, confirmed appointment, visit notes, or other attendance evidence is recorded",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "Edrin says",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "the work is complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "the work is complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "Edrin",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-012:002:213:217",
      "asset_id": null,
      "document_id": null,
      "outcome": "unknown",
      "description": "Edrin says the work is complete; no visit details or attendance evidence are recorded."
    },
    {
      "id": "b002:r11",
      "provenance": {
        "source_ids": [
          "025:L2",
          "025:L3",
          "025:L5"
        ],
        "asserted_by_entity_id": "entity:property-012:001:87:97",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "the invoice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "025:L2",
              "expression": "Ilyra Venn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "025:L3",
              "expression": "Edrin Moss",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "follows up about the invoice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "Edrin says",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "Ilyra follows up",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "promises to send the invoice later today",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "no invoice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "025:L2",
              "expression": "Ilyra Venn",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-012:002:213:217",
      "sender_id": "entity:property-012:001:87:97",
      "recipient_id": "entity:property-012:018:107:117",
      "purpose": "other",
      "status": "answered",
      "responds_to_record_id": null,
      "deadline_text": "later today"
    },
    {
      "id": "b002:r12",
      "provenance": {
        "source_ids": [
          "023:L5",
          "025:L5"
        ],
        "asserted_by_entity_id": "entity:property-012:018:107:117",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "send it on Friday, 26 September",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Edrin says they will check and send it",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "send it on Friday, 26 September",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "they will check and send it",
              "occurrence": 1
            },
            {
              "source_id": "025:L5",
              "expression": "promises to send the invoice later today",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "send it on Friday, 26 September",
              "occurrence": 1
            },
            {
              "source_id": "025:L5",
              "expression": "send the invoice later today",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Edrin says",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "they will check and send it on Friday, 26 September",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "they will check and send it",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Edrin says",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-012:002:213:217",
      "responsible_party_id": "entity:property-012:018:107:117",
      "requirement": "invoice",
      "status": "pending",
      "conditions": [
        "Edrin said they would check and send the invoice on Friday, 26 September; later promised to send it later that day."
      ]
    }
  ],
  "gaps": [
    {
      "id": "b002:g2",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-012:023:230:237",
        "entity:property-012:023:230:238",
        "entity:property-012:024:288:299",
        "entity:property-012:024:301:318",
        "entity:property-012:025:297:308",
        "entity:property-012:025:310:321",
        "entity:property-012:025:332:351"
      ],
      "source_ids": [
        "023:L5",
        "024:L5",
        "025:L5"
      ],
      "description": "The file is reported to lack an invoice, confirmed appointment, attendance record or evidence, and visit notes despite reports that the work was completed and an invoice would be sent."
    },
    {
      "id": "b002:g3",
      "kind": "timing",
      "entity_ids": [
        "entity:property-012:020:213:223",
        "entity:property-012:021:164:174",
        "entity:property-012:022:253:268",
        "entity:property-012:022:428:449"
      ],
      "source_ids": [
        "021:L5",
        "022:L5"
      ],
      "description": "No firm visit time was recorded; Edrin reported not having collected management keys and could not give a definite collection date. The three reported attempts have no dates or times."
    }
  ]
}
```
