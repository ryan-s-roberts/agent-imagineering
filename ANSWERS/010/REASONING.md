# Decision rationale and evidence

Case 010; checkpoint `010-at-026`; prefix ends at event `26`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The current objective is to complete the landlord-requested comparison of two replacement estimates without authorizing replacement work. The contractor has now sent full-kitchen figures, but the cupboards-and-doors-only estimate is still outstanding and the commission/VAT calculation and payable total remain unresolved. Follow up on those independent gaps, obtain human direction on the unresolved commercial terms, and preserve the already-pending landlord response. The full-kitchen figures are reported estimates, not approval or a settled total.

## Assumptions

- The contractor's missing cupboards-and-doors-only estimate remains part of the landlord's requested comparison, and the contractor's submitted full-kitchen figures are on the same continuous maintenance matter.

## Uncertainties

- The source packet does not establish the applicable commission arrangement, any cap, or the total including VAT.
- No current appointment or dog-access arrangement is recorded; the former tenant-offered dates have passed. The packet does not establish that a visit is currently needed to complete either estimate.
- The landlord's response about the forwarded figures remains outstanding; the packet does not establish that this is approval.

## Alternatives considered

- Do not request replacement approval yet: one requested estimate and a reliable payable total are missing, and the prefix explicitly records no replacement approval.
- Do not propose a visit or repair booking: no current visit requirement, available time, or confirmed dog-access arrangement is supplied.

## Cited prefix evidence

```json
{
  "source_id": "016:L5",
  "expression": "Agreed to obtain up-to-date estimates for two alternatives",
  "occurrence": 1
}
```
Event `016`, source `016:L5`, event character range [118, 378).

> Agreed to obtain up-to-date estimates for two alternatives: a full new kitchen and replacement cupboards and doors only. Said the appliances, worktops, and flooring were in good condition. This requested estimates; it did not approve either replacement option.

```json
{
  "source_id": "024:L5",
  "expression": "No cupboards-and-doors-only estimate was included.",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [140, 582).

> Sent full-kitchen figures: supply £4,850 plus VAT; removal of the old kitchen and fitting of the new one, including tiled splashback, £3,800 plus VAT; waste removal £230 plus VAT. Electrical work was estimated at £380 plus VAT and would need checking if the quote were acceptable. The proposed kitchen includes an oven, hob, and chimney extractor; it excludes a microwave, washer, and dryer. No cupboards-and-doors-only estimate was included.

```json
{
  "source_id": "022:L5",
  "expression": "The applicable basis, any cap, VAT treatment for the resulting total, and the total payable were not settled in this discussion",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [139, 574).

> While discussing the delayed kitchen quote, the contractor cited a 15% commission as a concern and questioned whether the old or revised commission basis applied, whether a cap applied to a larger job, and how VAT affected the amount. The contractor said these uncertainties could change the quoted amount. The applicable basis, any cap, VAT treatment for the resulting total, and the total payable were not settled in this discussion.

```json
{
  "source_id": "023:L5",
  "expression": "did not establish the applicable commission calculation, any cap, or the resulting total",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [139, 398).

> Told the contractor to use the previous commission arrangement and classify the job as before. The conversation did not establish the applicable commission calculation, any cap, or the resulting total. The contractor said the quote would be sent that evening.

```json
{
  "source_id": "026:L5",
  "expression": "there is no recorded approval for a full kitchen or cupboards-and-doors replacement",
  "occurrence": 1
}
```
Event `026`, source `026:L5`, event character range [147, 416).

> Recorded that a response from the landlord about the quote was awaited. The original laminate-repair approval and the later requests for expanded replacement estimates remain distinct; there is no recorded approval for a full kitchen or cupboards-and-doors replacement.

```json
{
  "source_id": "025:L5",
  "expression": "No approval for replacement work",
  "occurrence": 1
}
```
Event `025`, source `025:L5`, event character range [118, 481).

> Forwarded the full-kitchen figures and noted that the electrical item was an estimate requiring confirmation. The requested cupboards-and-doors-only estimate had not arrived. The listed figures were plus VAT, while the commission basis, any cap, and resulting payable total remained unconfirmed. No approval for replacement work or access appointment is recorded.

```json
{
  "source_id": "021:L5",
  "expression": "no appointment or dog-access arrangement had been confirmed",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [147, 360).

> The silent wait expired without a new contractor response. No visit slot or updated estimates had arrived. The first tenant-offered date had passed, and no appointment or dog-access arrangement had been confirmed.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r13",
      "provenance": {
        "source_ids": [
          "023:L2",
          "023:L3",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:001:65:75",
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
              "expression": "Told the contractor to use the previous commission arrangement and classify the job as before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "023:L3",
              "expression": "Kellan Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "use the previous commission arrangement and classify the job as before",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Told the contractor to use the previous commission arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Told the contractor to use the previous commission arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Told the contractor to use the previous commission arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Told the contractor to use the previous commission arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-010:001:127:159",
      "sender_id": "entity:property-010:001:65:75",
      "recipient_id": "entity:property-010:007:109:119",
      "purpose": "clarification",
      "status": "answered",
      "responds_to_record_id": null,
      "deadline_text": "that evening"
    },
    {
      "id": "b002:r15",
      "provenance": {
        "source_ids": [
          "022:L5",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:007:109:119",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "these uncertainties could change the quoted amount",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "entity_ids",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "whether the old or revised commission basis applied, whether a cap applied to a larger job, and how VAT affected the amount",
              "occurrence": 1
            },
            {
              "source_id": "023:L5",
              "expression": "did not establish the applicable commission calculation, any cap, or the resulting total",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "source_ids",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "The applicable basis, any cap, VAT treatment for the resulting total, and the total payable were not settled in this discussion",
              "occurrence": 1
            },
            {
              "source_id": "023:L5",
              "expression": "did not establish the applicable commission calculation, any cap, or the resulting total",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "The applicable basis, any cap, VAT treatment for the resulting total, and the total payable were not settled in this discussion",
              "occurrence": 1
            },
            {
              "source_id": "023:L5",
              "expression": "did not establish the applicable commission calculation, any cap, or the resulting total",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "workflow_failure",
      "request_id": "entity:property-010:001:127:159",
      "attempted_operation": null,
      "error_text": "Commission calculation remains unresolved: the applicable old or revised basis, any cap, VAT treatment, and total payable were not established, despite the instruction to use the previous arrangement.",
      "outcome": "unknown"
    },
    {
      "id": "b003:p_full_kitchen_supply",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:007:109:119",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "full-kitchen figures",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "The proposed kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "full-kitchen figures",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£4,850 plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£4,850",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Kellan Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Sent full-kitchen figures",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "The proposed kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "supply £4,850 plus VAT",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-010:001:127:159",
      "asset_id": "entity:property-010:024:421:441",
      "provider_id": "entity:property-010:007:109:119",
      "scope": [
        "quote",
        "replace"
      ],
      "amount_minor": 485000,
      "currency": "GBP",
      "conditions": [
        "Supply estimate; plus VAT"
      ],
      "valid_time_text": null
    },
    {
      "id": "b003:p_full_kitchen_removal_fitting",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:007:109:119",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "full-kitchen figures",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "The proposed kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "removal of the old kitchen and fitting of the new one, including tiled splashback",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£3,800 plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£3,800",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Kellan Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Sent full-kitchen figures",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "fitting of the new one",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£3,800 plus VAT",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-010:001:127:159",
      "asset_id": "entity:property-010:024:421:441",
      "provider_id": "entity:property-010:007:109:119",
      "scope": [
        "quote",
        "replace"
      ],
      "amount_minor": 380000,
      "currency": "GBP",
      "conditions": [
        "Removal and fitting estimate, including tiled splashback; plus VAT"
      ],
      "valid_time_text": null
    },
    {
      "id": "b003:p_full_kitchen_waste_removal",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:007:109:119",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "full-kitchen figures",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "The proposed kitchen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "waste removal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£230 plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£230",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Kellan Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Sent full-kitchen figures",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "waste removal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£230 plus VAT",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-010:001:127:159",
      "asset_id": "entity:property-010:024:421:441",
      "provider_id": "entity:property-010:007:109:119",
      "scope": [
        "quote",
        "replace"
      ],
      "amount_minor": 23000,
      "currency": "GBP",
      "conditions": [
        "Waste-removal estimate; plus VAT"
      ],
      "valid_time_text": null
    },
    {
      "id": "b003:p_electrical_estimate",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:007:109:119",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Electrical work was estimated at £380 plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Electrical work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£380 plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "£380",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "would need checking if the quote were acceptable",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Kellan Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Electrical work was estimated at £380 plus VAT",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "would need checking if the quote were acceptable",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Electrical work was estimated at £380 plus VAT",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-010:001:127:159",
      "asset_id": null,
      "provider_id": "entity:property-010:007:109:119",
      "scope": [
        "quote"
      ],
      "amount_minor": 38000,
      "currency": "GBP",
      "conditions": [
        "Estimate; plus VAT; electrical work would need checking if the quote were acceptable"
      ],
      "valid_time_text": null
    },
    {
      "id": "b003:auth_replacement_not_recorded",
      "provenance": {
        "source_ids": [
          "025:L5",
          "026:L2",
          "026:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:001:65:75",
        "origin": "attributed_report",
        "modality": "unknown",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "there is no recorded approval for a full kitchen or cupboards-and-doors replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "a full kitchen or cupboards-and-doors replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "there is no recorded approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "a response from the landlord about the quote was awaited",
              "occurrence": 1
            },
            {
              "source_id": "025:L5",
              "expression": "No approval for replacement work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "026:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "Recorded that a response from the landlord about the quote was awaited",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "there is no recorded approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "there is no recorded approval",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-010:001:127:159",
      "grantor_id": "entity:property-010:003:107:115",
      "grantee_id": null,
      "scope": [
        "replace"
      ],
      "decision": "uncertain",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "No approval for a full kitchen or cupboards-and-doors replacement is recorded; a response from the landlord about the quote was awaited."
      ]
    },
    {
      "id": "b003:obligation_cupboards_doors_estimate",
      "provenance": {
        "source_ids": [
          "025:L2",
          "025:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:001:65:75",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "The requested cupboards-and-doors-only estimate had not arrived",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "The requested cupboards-and-doors-only estimate",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "cupboards-and-doors-only estimate",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "had not arrived",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "The requested cupboards-and-doors-only estimate had not arrived",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "025:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "The requested cupboards-and-doors-only estimate had not arrived",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "requested",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "had not arrived",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-010:001:127:159",
      "responsible_party_id": "entity:property-010:007:109:119",
      "requirement": "quote",
      "status": "pending",
      "conditions": [
        "Requested cupboards-and-doors-only estimate had not arrived."
      ]
    },
    {
      "id": "b003:obligation_landlord_quote_response",
      "provenance": {
        "source_ids": [
          "026:L2",
          "026:L5"
        ],
        "asserted_by_entity_id": "entity:property-010:001:65:75",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "a response from the landlord about the quote was awaited",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "the landlord",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "a response from the landlord about the quote was awaited",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "was awaited",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "about the quote",
              "occurrence": 1
            },
            {
              "source_id": "026:L5",
              "expression": "there is no recorded approval for a full kitchen or cupboards-and-doors replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "026:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "Recorded that a response from the landlord about the quote was awaited",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "was awaited",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "026:L5",
              "expression": "a response from the landlord about the quote was awaited",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-010:001:127:159",
      "responsible_party_id": "entity:property-010:003:107:115",
      "requirement": "other",
      "status": "pending",
      "conditions": [
        "Response about the quote awaited; this does not establish approval for either replacement option."
      ]
    }
  ],
  "gaps": [
    {
      "id": "b003:gap_cupboards_doors_estimate",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-010:025:228:275",
        "entity:property-010:016:201:237"
      ],
      "source_ids": [
        "024:L5",
        "025:L5"
      ],
      "description": "The requested cupboards-and-doors-only estimate was not included with the full-kitchen figures and had not arrived."
    },
    {
      "id": "b003:gap_commission_total",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-010:025:132:152"
      ],
      "source_ids": [
        "025:L5"
      ],
      "description": "The commission basis, any cap, and the resulting payable total remained unconfirmed; the listed figures were plus VAT."
    }
  ]
}
```
