# Decision rationale and evidence

Case 001; checkpoint `001-at-023`; prefix ends at event `23`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The immediate objective is to resolve the landlord’s genuine uncertainty about which quotation he was asked to approve, while keeping repair work unauthorized until the provider clarifies material price and deposit details. The latest event identifies his confusion; the supplied quotation identifies a specific reference and scope, and the contractor has supplied a partial breakdown that does not reconcile the total.

## Assumptions

- The attached NBL-001-Q1 quotation is the Hearthline bathroom quotation already discussed in this request: its provider, scope and £2,844 total match the earlier correspondence. This continuity is inferred from the source content, not from extraction IDs.

## Uncertainties

- The provider’s breakdown does not establish a revised all-in total or the basis for the 50% deposit.
- The attachment’s property address is not independently linked by the extracted identity data, although its provider, proposed scope and price correspond to the earlier quotation in the case.

## Alternatives considered

- Seeking final approval now was rejected because the latest breakdown leaves the total and deposit basis unclear, and the landlord has not confirmed whether to proceed.
- Instructing repair work was rejected because the correspondence expressly says the quoted repair work was not authorized.

## Cited prefix evidence

```json
{
  "source_id": "023:L5",
  "expression": "Which quote do you mean?",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [118, 243).

> Orin replied: “Which quote do you mean? There are a couple.” He asked for clarification before confirming whether to proceed.

```json
{
  "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L4",
  "expression": "Quotation reference: NBL-001-Q1",
  "occurrence": 1
}
```
Document `001:437b7ee851765447a667` (`attachments/bathroom-works-quotation.pdf`), page 1, source `attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L4`, extracted page Unicode character range [118, 149); available at events 023.

> Quotation reference: NBL-001-Q1

```json
{
  "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L15",
  "expression": "Total £2,844.00",
  "occurrence": 1
}
```
Document `001:437b7ee851765447a667` (`attachments/bathroom-works-quotation.pdf`), page 1, source `attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L15`, extracted page Unicode character range [520, 535); available at events 023.

> Total £2,844.00

```json
{
  "source_id": "021:L5",
  "expression": "materials £1,270; labour £1,170 for two people, half a day each; VAT at 20%; Northbridge commission at 10%",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [148, 480).

> Ewan replied: materials £1,270; labour £1,170 for two people, half a day each; VAT at 20%; Northbridge commission at 10%. He said a 50% deposit would be required if the landlord wished to proceed. The message did not state a revised subtotal or total, clarify how the commission is applied, or specify the deposit calculation basis.

```json
{
  "source_id": "021:L5",
  "expression": "The message did not state a revised subtotal or total, clarify how the commission is applied, or specify the deposit calculation basis.",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [148, 480).

> Ewan replied: materials £1,270; labour £1,170 for two people, half a day each; VAT at 20%; Northbridge commission at 10%. He said a 50% deposit would be required if the landlord wished to proceed. The message did not state a revised subtotal or total, clarify how the commission is applied, or specify the deposit calculation basis.

```json
{
  "source_id": "005:L5",
  "expression": "His message did not authorize the quoted repair work.",
  "occurrence": 1
}
```
Event `005`, source `005:L5`, event character range [118, 242).

> Orin authorized arranging a plumbing inspection and obtaining a quote. His message did not authorize the quoted repair work.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r13",
      "provenance": {
        "source_ids": [
          "005:L1",
          "005:L2",
          "005:L3",
          "005:L5"
        ],
        "asserted_by_entity_id": "entity:property-001:003:107:115",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "His message did not authorize the quoted repair work.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "005:L2",
              "expression": "Orin Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "005:L3",
              "expression": "Mira Sallow",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "the quoted repair work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "did not authorize the quoted repair work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "005:L1",
              "expression": "Email",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "His message did not authorize the quoted repair work.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "did not authorize the quoted repair work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "005:L2",
              "expression": "Orin Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-001:001:118:162",
      "grantor_id": "entity:property-001:003:107:115",
      "grantee_id": "entity:property-001:001:64:75",
      "scope": [
        "repair"
      ],
      "decision": "denied",
      "amount_minor": null,
      "currency": null,
      "conditions": []
    },
    {
      "id": "b002:r1",
      "provenance": {
        "source_ids": [
          "016:L2",
          "016:L5",
          "021:L5"
        ],
        "asserted_by_entity_id": null,
        "origin": "document_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Quotation received after the bathroom inspection.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "016:L2",
              "expression": "Ewan Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Scope: remove the existing shower screen, taps, and shower valve; install a wall-and-riser cladding system with chrome trims; fit new bath taps and a new shower valve; refit the existing screen.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "total £2,844.00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "total £2,844.00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Scope: remove the existing shower screen, taps, and shower valve; install a wall-and-riser cladding system with chrome trims; fit new bath taps and a new shower valve; refit the existing screen.",
              "occurrence": 1
            },
            {
              "source_id": "016:L5",
              "expression": "It contains no separate materials or labour line items.",
              "occurrence": 1
            },
            {
              "source_id": "021:L5",
              "expression": "a 50% deposit would be required if the landlord wished to proceed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Quotation received after the bathroom inspection.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Scope: remove the existing shower screen, taps, and shower valve; install a wall-and-riser cladding system with chrome trims; fit new bath taps and a new shower valve; refit the existing screen.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Quotation received after the bathroom inspection.",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-001:001:118:162",
      "asset_id": null,
      "provider_id": "entity:property-001:006:107:117",
      "scope": [
        "replace"
      ],
      "amount_minor": 284400,
      "currency": "GBP",
      "conditions": [
        "Quoted work description: remove the existing shower screen, taps, and shower valve; install a wall-and-riser cladding system with chrome trims; fit new bath taps and a new shower valve; refit the existing screen.",
        "The quotation contains no separate materials or labour line items.",
        "A 50% deposit would be required if the landlord wished to proceed."
      ],
      "valid_time_text": null
    },
    {
      "id": "b002:r14",
      "provenance": {
        "source_ids": [
          "020:L5",
          "021:L2",
          "021:L3",
          "021:L5"
        ],
        "asserted_by_entity_id": "entity:property-001:006:107:117",
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
              "expression": "Ewan replied:",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "021:L2",
              "expression": "Ewan Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "021:L3",
              "expression": "Mira Sallow",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "materials £1,270; labour £1,170 for two people, half a day each; VAT at 20%; Northbridge commission at 10%",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Ewan replied:",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responds_to_record_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Mira asked Ewan for an itemized breakdown",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Ewan replied:",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Ewan replied:",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "021:L5",
              "expression": "Ewan replied:",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "021:L2",
              "expression": "Ewan Rook",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-001:001:118:162",
      "sender_id": "entity:property-001:006:107:117",
      "recipient_id": "entity:property-001:001:64:75",
      "purpose": "clarification",
      "status": "answered",
      "responds_to_record_id": "b002:r13",
      "deadline_text": null
    },
    {
      "id": "b002:r16",
      "provenance": {
        "source_ids": [
          "022:L5",
          "023:L2",
          "023:L3",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-001:003:107:115",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "He asked for clarification before confirming whether to proceed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Orin Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "023:L3",
              "expression": "Mira Sallow",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "asked for clarification before confirming whether to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "He asked for clarification",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responds_to_record_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Mira sent a brief follow-up asking whether they could go ahead with the quote for the property.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Orin replied:",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "before confirming whether to proceed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "He asked for clarification",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Orin Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-001:001:118:162",
      "sender_id": "entity:property-001:003:107:115",
      "recipient_id": "entity:property-001:001:64:75",
      "purpose": "clarification",
      "status": "answered",
      "responds_to_record_id": "b002:r15",
      "deadline_text": null
    },
    {
      "id": "b003:r1",
      "provenance": {
        "source_ids": [
          "016:L5",
          "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L10",
          "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L11",
          "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L15",
          "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L3",
          "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L7",
          "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L8",
          "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L9"
        ],
        "asserted_by_entity_id": null,
        "origin": "document_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "016:L5",
              "expression": "Quotation received after the bathroom inspection.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L3",
              "expression": "Hearthline Plumbing & Bath",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L8",
              "expression": "Remove the existing shower screen, bath taps and shower valve.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L9",
              "expression": "Install a wall-and-riser cladding system with chrome trims.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L10",
              "expression": "Fit new bath taps and a new shower valve.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L11",
              "expression": "Refit the existing shower screen.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L15",
              "expression": "Total £2,844.00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L15",
              "expression": "Total £2,844.00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L7",
              "expression": "Proposed scope",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L7",
              "expression": "Proposed scope",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "attachment:001:437b7ee851765447a667:ead9d12a916d0de1856b00c02639c81ed9a50ef76fe7991fa3c0fec873802ee3:p1:L7",
              "expression": "Proposed scope",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-001:001:118:162",
      "asset_id": null,
      "provider_id": "entity:property-001:006:119:145",
      "scope": [
        "replace"
      ],
      "amount_minor": 284400,
      "currency": "GBP",
      "conditions": [],
      "valid_time_text": null
    }
  ],
  "gaps": [
    {
      "id": "b002:g2",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-001:016:151:160",
        "entity:property-001:020:288:297",
        "entity:property-001:021:239:250",
        "entity:property-001:021:278:291"
      ],
      "source_ids": [
        "021:L5"
      ],
      "description": "The contractor's breakdown does not state a revised subtotal or total, explain how the 10% commission is applied, or specify the calculation basis for the 50% deposit."
    },
    {
      "id": "b002:g3",
      "kind": "identity",
      "entity_ids": [
        "entity:property-001:016:151:160",
        "entity:property-001:022:238:247",
        "entity:property-001:022:315:348",
        "entity:property-001:023:133:157",
        "entity:property-001:023:168:176"
      ],
      "source_ids": [
        "022:L5",
        "023:L5"
      ],
      "description": "The follow-up asking whether to proceed did not identify an amount or include the latest breakdown; the landlord asked which quote was meant and said there were a couple. The intended quote for that approval request is unclear."
    }
  ]
}
```
