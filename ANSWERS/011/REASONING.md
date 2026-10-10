# Decision rationale and evidence

Case 011; checkpoint `011-at-024`; prefix ends at event `24`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The operational objective remains resolving the recurring tap-related leak. The quoted plumbing repair has not been completed: the contractor left without opening the ceiling, the joint is still inaccessible, and the lining is unidentified. The landlord’s earlier authorization was limited to quoted plumbing work, and the latest manager update requests a decision on additional assessment or repair; no additional cost or appointment is agreed. Keep work paused, update the tenant, help the manager obtain the cost/timing information the landlord requested without committing to paid work, and await the landlord’s response.

## Assumptions

- The latest reported pipe repair and lining issue concern the continuing leak described in the earlier case history; this is chronological continuity, not a claim that extracted request IDs are identical.

## Uncertainties

- The lining’s composition and the assessment needed remain unknown; the contractor says he cannot specify either.
- The landlord’s response to the latest request for a decision is not present.
- The extraction represents the follow-up decision request as e60 separately from the original leak request e1; actions use the request IDs associated with their supporting records rather than silently merging them.

## Alternatives considered

- Did not authorize or book the quoted repair or a specialist assessment: the landlord limited authority to the quoted plumbing scope and has not authorized additional expenditure or an appointment.
- Did not repeat a work-report request to the contractor: the latest report already says he left, the joint remains inaccessible, and he cannot price or specify the assessment.
- Did not escalate as a human intervention: the record shows a request to the landlord and a pending authority decision, but no separate human-review event or need is established.

## Cited prefix evidence

```json
{
  "source_id": "023:L5",
  "expression": "he has left without opening the ceiling. The joint remains inaccessible through the hatch",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [145, 485).

> Confirms he has left without opening the ceiling. The joint remains inaccessible through the hatch, and he cannot price work involving the unidentified lining or specify what assessment would be required. He notes Iven's 11:27 report, relayed by Mara, of a tap-related drip that morning. No drilling, cutting, sampling, or removal occurred.

```json
{
  "source_id": "023:L5",
  "expression": "he cannot price work involving the unidentified lining or specify what assessment would be required",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [145, 485).

> Confirms he has left without opening the ceiling. The joint remains inaccessible through the hatch, and he cannot price work involving the unidentified lining or specify what assessment would be required. He notes Iven's 11:27 report, relayed by Mara, of a tap-related drip that morning. No drilling, cutting, sampling, or removal occurred.

```json
{
  "source_id": "022:L5",
  "expression": "her authorization covered the quoted plumbing work only, not a specialist material assessment or other work outside that scope",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [118, 370).

> Confirms she has no further records. Says her authorization covered the quoted plumbing work only, not a specialist material assessment or other work outside that scope. Requests the likely cost and timing before considering any additional expenditure.

```json
{
  "source_id": "022:L5",
  "expression": "Requests the likely cost and timing before considering any additional expenditure.",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [118, 370).

> Confirms she has no further records. Says her authorization covered the quoted plumbing work only, not a specialist material assessment or other work outside that scope. Requests the likely cost and timing before considering any additional expenditure.

```json
{
  "source_id": "024:L5",
  "expression": "Requests a decision on whether any further assessment or repair scope may be authorized",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [119, 536).

> Records that the underlying pipe repair remains necessary, the leak has recurred when the tap is used, and Iven has stopped using that tap. The ceiling has not been opened; the visible lining remains unidentified, no confirming survey is on file, and the contractor has stopped work. Requests a decision on whether any further assessment or repair scope may be authorized; no additional cost or appointment is agreed.

```json
{
  "source_id": "024:L5",
  "expression": "no additional cost or appointment is agreed",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [119, 536).

> Records that the underlying pipe repair remains necessary, the leak has recurred when the tap is used, and Iven has stopped using that tap. The ceiling has not been opened; the visible lining remains unidentified, no confirming survey is on file, and the contractor has stopped work. Requests a decision on whether any further assessment or repair scope may be authorized; no additional cost or appointment is agreed.

```json
{
  "source_id": "020:L5",
  "expression": "Reports a small drip when the kitchen tap was used that morning",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [115, 323).

> Acknowledges the instruction. Reports a small drip when the kitchen tap was used that morning and says they have stopped using that tap. The ceiling is not visibly sagging, and Iven has not touched the hatch.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r4",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-011:001:34:43",
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
              "expression": "Reports a brown damp patch above the kitchen sink",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a brown damp patch above the kitchen sink, roughly the size of a small plate, and a few drops overnight. No part of the ceiling has fallen or visibly sagged.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a brown damp patch above the kitchen sink",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a brown damp patch above the kitchen sink",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a brown damp patch above the kitchen sink",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a brown damp patch above the kitchen sink",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Iven Rell",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-011:001:125:164",
      "asset_id": "entity:property-011:001:243:250",
      "property_id": null,
      "description": "Tenant reports a brown damp patch above the kitchen sink, roughly the size of a small plate, with a few overnight drops; reports no part of the ceiling has fallen or visibly sagged.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b002:r8",
      "provenance": {
        "source_ids": [
          "017:L2",
          "017:L5"
        ],
        "asserted_by_entity_id": "entity:property-011:008:107:117",
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
              "expression": "Iven answers and admits him",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "a pale, fibrous-looking lining behind the painted ceiling board",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Calls from outside the flat at 10:40",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Iven answers and admits him. From the access hatch, Kellan can see a pale, fibrous-looking lining behind the painted ceiling board. He cannot identify it visually and has not touched or disturbed it. The planned opening would require drilling or cutting nearby; he has paused and is waiting for instructions.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Kellan can see",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Calls from outside the flat at 10:40",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "has paused and is waiting for instructions",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Kellan Orve",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-011:001:125:164",
      "asset_id": "entity:property-011:009:418:432",
      "document_id": null,
      "outcome": "attended",
      "description": "Contractor attended; saw unidentified lining through the hatch, did not touch or disturb it, and paused pending instructions."
    },
    {
      "id": "b002:r11",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L3",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-011:001:63:72",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "not to disturb the lining or proceed with drilling, cutting, sampling, or removal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Mara Voss",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "018:L3",
              "expression": "Kellan Orve",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "not to disturb the lining or proceed with drilling, cutting, sampling, or removal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "not to disturb the lining or proceed with drilling, cutting, sampling, or removal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "while the material is unidentified",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Instructs Kellan not to disturb the lining",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Instructs Kellan not to disturb",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "not to disturb the lining",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Mara Voss",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-011:001:125:164",
      "grantor_id": "entity:property-011:001:63:72",
      "grantee_id": "entity:property-011:008:107:117",
      "scope": [
        "unspecified"
      ],
      "decision": "denied",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "Do not disturb the lining or drill, cut, sample, or remove it while the material is unidentified"
      ]
    },
    {
      "id": "b002:r16",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-011:001:63:72",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Asks Iven not to access the hatch or disturb the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Iven",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "not to access the hatch or disturb the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Asks Iven not to access the hatch or disturb the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "not to access the hatch or disturb the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Explains",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Asks Iven not to access the hatch",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "not to access the hatch or disturb the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Mara Voss",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-011:001:125:164",
      "party_id": "entity:property-011:001:34:43",
      "constraint": "other",
      "status": "required",
      "time_text": null,
      "description": "Do not access the hatch or disturb the ceiling; report any renewed dripping."
    },
    {
      "id": "b003:r7",
      "provenance": {
        "source_ids": [
          "022:L2",
          "022:L5"
        ],
        "asserted_by_entity_id": "entity:property-011:012:107:115",
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
              "expression": "Requests the likely cost and timing before considering any additional expenditure.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Requests the likely cost and timing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "the likely cost and timing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Requests the likely cost and timing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "before considering any additional expenditure",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Requests the likely cost and timing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "before considering any additional expenditure",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Requests the likely cost and timing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "022:L2",
              "expression": "Ossa Fenlow (Landlord)",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-011:024:412:490",
      "responsible_party_id": "entity:property-011:001:63:72",
      "requirement": "quote",
      "status": "requested",
      "conditions": [
        "Likely cost and timing are requested before any additional expenditure is considered."
      ]
    },
    {
      "id": "b003:r8",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L3",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-011:001:63:72",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "a decision on whether any further assessment or repair scope may be authorized",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Mara Voss (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "024:L3",
              "expression": "Ossa Fenlow (Landlord)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision on whether any further assessment or repair scope may be authorized",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Mara Voss (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-011:024:412:490",
      "sender_id": "entity:property-011:001:63:72",
      "recipient_id": "entity:property-011:012:107:115",
      "purpose": "approval",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b003:r9",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-011:001:63:72",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "a decision on whether any further assessment or repair scope may be authorized",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision on whether any further assessment or repair scope may be authorized",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "no additional cost or appointment is agreed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Records that",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "no additional cost or appointment is agreed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Requests a decision",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Mara Voss (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-011:024:412:490",
      "responsible_party_id": "entity:property-011:012:107:115",
      "requirement": "approval",
      "status": "requested",
      "conditions": [
        "A decision is requested on any further assessment or repair scope; no additional cost or appointment is agreed."
      ]
    }
  ],
  "gaps": [
    {
      "id": "b003:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-011:009:418:432",
        "entity:property-011:024:412:490"
      ],
      "source_ids": [
        "022:L5",
        "023:L5"
      ],
      "description": "The lining remains unidentified, and the contractor cannot price work involving it or specify the assessment required. The landlord requests likely cost and timing before considering additional expenditure; those details are not available in these sources."
    }
  ]
}
```
