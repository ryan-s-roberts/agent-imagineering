# Decision rationale and evidence

Case 013; checkpoint `013-at-024`; prefix ends at event `24`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The latest document report describes supply and fitting one pane of kitchen glazing, but its amount is blank. It supports moving the glazing request into completion review, not treating completion or the amount as independently verified. Request a corrected invoice amount and report the progress without closing the request. Separately seek inspection authority for the cold-kitchen and damp concerns under their distinct supplied request IDs; the record says neither has a site assessment or diagnosis, and the glazing authorization does not establish authority for those inspections.

## Assumptions

- The invoice's kitchen-glazing description refers to the glazing work represented by request e1, consistent with the linked work report record r33 and the matching asset and work description.
- Inspection approval is sought separately for e4 and e5 because the supplied evidence ontology represents the cold-kitchen and damp concerns as distinct maintenance requests; this does not assert that they are separate physical causes or merge their request identities.

## Uncertainties

- The invoice is a document report, not independent confirmation that fitting occurred; the available evidence includes no appointment confirmation or visit report.
- The invoice amount is not established, so whether the reported work met the landlord's conditional £180-total term cannot be assessed.
- The cause and current condition of the reported cold-kitchen and damp concerns remain unestablished.

## Alternatives considered

- Do not close the glazing request: move it to completion review because the new evidence is a document report and the amount is missing.
- Request the specific missing invoice amount rather than treating the document report as proof that all work-outcome evidence is complete.
- Do not extend the glazing approval to inspection of the cold or damp concerns; seek authority separately under their supplied request IDs.

## Cited prefix evidence

```json
{
  "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7",
  "expression": "Supply and fit 1 pane of glass to the kitchen glazing.",
  "occurrence": 1
}
```
Document `013:e333c7f8dfc8890ab1ed` (`attachments/glazing-invoice.pdf`), page 1, source `attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7`, extracted page Unicode character range [221, 275); available at events 024.

> Supply and fit 1 pane of glass to the kitchen glazing.

```json
{
  "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L8",
  "expression": "Amount: —",
  "occurrence": 1
}
```
Document `013:e333c7f8dfc8890ab1ed` (`attachments/glazing-invoice.pdf`), page 1, source `attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L8`, extracted page Unicode character range [276, 285); available at events 024.

> Amount: —

```json
{
  "source_id": "010:L5",
  "expression": "if £180 was the total value of the quote",
  "occurrence": 1
}
```
Event `010`, source `010:L5`, event character range [119, 258).

> Said he had been away and was catching up on email. Wrote that he was happy to use the contractor if £180 was the total value of the quote.

```json
{
  "source_id": "022:L5",
  "expression": "Moved the case to awaiting post-visit documents",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [149, 310).

> Moved the case to awaiting post-visit documents without sending messages. The record available at that time contains no appointment confirmation or visit report.

```json
{
  "source_id": "022:L5",
  "expression": "no appointment confirmation or visit report",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [149, 310).

> Moved the case to awaiting post-visit documents without sending messages. The record available at that time contains no appointment confirmation or visit report.

```json
{
  "source_id": "005:L5",
  "expression": "No site assessment or diagnosis of the wider damp or cold concern is recorded",
  "occurrence": 1
}
```
Event `005`, source `005:L5`, event character range [149, 290).

> Recorded authorization to obtain a glazing contractor's price. No site assessment or diagnosis of the wider damp or cold concern is recorded.

```json
{
  "source_id": "001:L5",
  "expression": "a cold kitchen",
  "occurrence": 1
}
```
Event `001`, source `001:L5`, event character range [118, 335).

> Reported moisture between the kitchen glazing panes, water gathering around the frame, a cold kitchen and concern about damp, especially in winter. Confirmed the sash opens, closes and locks; pets are at the property.

```json
{
  "source_id": "001:L5",
  "expression": "concern about damp",
  "occurrence": 1
}
```
Event `001`, source `001:L5`, event character range [118, 335).

> Reported moisture between the kitchen glazing panes, water gathering around the frame, a cold kitchen and concern about damp, especially in winter. Confirmed the sash opens, closes and locks; pets are at the property.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r3",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-013:001:33:44",
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
              "expression": "a cold kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "a cold kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "a cold kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reported",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "a cold kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "a cold kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Elowen Marr (Tenant)",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-013:001:205:219",
      "asset_id": null,
      "property_id": null,
      "description": "Reported a cold kitchen.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b001:r4",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-013:001:33:44",
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
              "expression": "concern about damp",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "concern about damp, especially in winter",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "concern about damp",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reported",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "concern about damp",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "concern about damp",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Elowen Marr (Tenant)",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-013:001:224:242",
      "asset_id": null,
      "property_id": null,
      "description": "Concern about damp, especially in winter; this is a reported concern, not a confirmed diagnosis.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b001:r19",
      "provenance": {
        "source_ids": [
          "010:L2",
          "010:L3",
          "010:L5"
        ],
        "asserted_by_entity_id": "entity:property-013:003:108:116",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "happy to use the contractor if £180 was the total value of the quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "010:L2",
              "expression": "Orren Vale (Landlord)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "010:L3",
              "expression": "Tamsin Rook (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "use the contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "happy to use the contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "£180",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "£180",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "if £180 was the total value of the quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "Wrote that he was happy to use the contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "if £180 was the total value of the quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "happy to use the contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "010:L2",
              "expression": "Orren Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-013:001:127:169",
      "grantor_id": "entity:property-013:003:108:116",
      "grantee_id": "entity:property-013:001:64:75",
      "scope": [
        "unspecified"
      ],
      "decision": "approved",
      "amount_minor": 18000,
      "currency": "GBP",
      "conditions": [
        "Only if £180 was the total value of the quote."
      ]
    },
    {
      "id": "b002:r8",
      "provenance": {
        "source_ids": [
          "022:L2",
          "022:L5"
        ],
        "asserted_by_entity_id": "entity:property-013:001:64:75",
        "origin": "system_record",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "the case",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Moved the case to awaiting post-visit documents",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "source_label",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "awaiting post-visit documents",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Moved the case",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Moved the case to awaiting post-visit documents",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Moved the case to awaiting post-visit documents",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "022:L2",
              "expression": "Tamsin Rook",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "request_status",
      "request_id": "entity:property-013:001:127:169",
      "status": "awaiting_results",
      "source_label": "awaiting post-visit documents"
    },
    {
      "id": "b003:r1",
      "provenance": {
        "source_ids": [
          "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L1",
          "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7"
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
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L1",
              "expression": "B I L L I N G  D O C U M E N T",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7",
              "expression": "Supply and fit 1 pane of glass to the kitchen glazing.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7",
              "expression": "Supply and fit 1 pane of glass to the kitchen glazing.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7",
              "expression": "kitchen glazing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7",
              "expression": "kitchen glazing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L1",
              "expression": "Glazing Invoice Copy",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7",
              "expression": "Supply and fit 1 pane of glass to the kitchen glazing.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L7",
              "expression": "Supply and fit 1 pane of glass to the kitchen glazing.",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-013:001:127:169",
      "asset_id": "entity:property-013:001:148:163",
      "document_id": "entity:property-013:attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:111:125",
      "outcome": "repaired",
      "description": "Supply and fit 1 pane of glass to the kitchen glazing."
    }
  ],
  "gaps": [
    {
      "id": "b001:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-013:001:205:219",
        "entity:property-013:001:224:242"
      ],
      "source_ids": [
        "005:L5"
      ],
      "description": "The wider cold and damp concern has no recorded site assessment or diagnosis; its cause and condition remain unestablished."
    },
    {
      "id": "b002:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-013:001:127:169",
        "entity:property-013:022:269:293",
        "entity:property-013:022:297:309"
      ],
      "source_ids": [
        "022:L5"
      ],
      "description": "When the case was moved to awaiting post-visit documents, the available record contained no appointment confirmation or visit report."
    },
    {
      "id": "b003:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-013:attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:111:125"
      ],
      "source_ids": [
        "attachment:013:e333c7f8dfc8890ab1ed:a4382ed65e3f517101f0faa3d67c361a3133ed23289adf7df6604b3b15431348:p1:L8"
      ],
      "description": "The invoice copy gives no amount (\"Amount: —\"), so the invoiced amount is not established."
    }
  ]
}
```
