# Decision rationale and evidence

Case 017; checkpoint `017-at-019`; prefix ends at event `19`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

Progress the quoted decorative-painting work toward a decision without treating the landlord’s affordability comment as approval or bypassing the building manager’s pending scope response. No work is booked. The quote is now available with a specific £186 price and explicit exclusions, so the landlord can be asked for a defined decision while the building response is awaited; the tenant can also be updated about what the quote does and does not establish.

## Assumptions

- The attachment quotation and the ongoing entrance-door request refer to the same job, as supported by the property, door, provider, and continuous discussion of the quoted scope.

## Uncertainties

- The building manager has not yet confirmed whether the quoted painting needs approval or specified materials or procedure.
- The quote does not assess whether painting would affect the door’s operation or fire performance.
- The landlord has not approved the £186 charge or the quoted work.

## Alternatives considered

- Booking or instructing the painter now was rejected: the landlord requested confirmation of scope and the building response before booking, and the quote is not authorization.

## Cited prefix evidence

```json
{
  "source_id": "019:L5",
  "expression": "Building manager's response to the scope query is pending. No work has been booked.",
  "occurrence": 1
}
```
Event `019`, source `019:L5`, event character range [133, 354).

> Quotation, tenant access preference, contractor's visual-only observations, and building manager's limited check information are on file. Building manager's response to the scope query is pending. No work has been booked.

```json
{
  "source_id": "017:L5",
  "expression": "Replied that the quotation appears affordable and asked whether it can be approved from the repair budget.",
  "occurrence": 1
}
```
Event `017`, source `017:L5`, event character range [134, 334).

> Replied that the quotation appears affordable and asked whether it can be approved from the repair budget. Asked for the proposed scope and any building response to be confirmed before work is booked.

```json
{
  "source_id": "017:L5",
  "expression": "Asked for the proposed scope and any building response to be confirmed before work is booked.",
  "occurrence": 1
}
```
Event `017`, source `017:L5`, event character range [134, 334).

> Replied that the quotation appears affordable and asked whether it can be approved from the repair budget. Asked for the proposed scope and any building response to be confirmed before work is booked.

```json
{
  "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L15",
  "expression": "Quotation total: £186.00, including materials and labour.",
  "occurrence": 1
}
```
Document `017:ac210e2489e972791b0d` (`attachments/fire-door-quotation.pdf`), page 1, source `attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L15`, extracted page Unicode character range [616, 673); available at events 019.

> Quotation total: £186.00, including materials and labour.

```json
{
  "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L19",
  "expression": "This quotation covers surface preparation and decorative painting only.",
  "occurrence": 1
}
```
Document `017:ac210e2489e972791b0d` (`attachments/fire-door-quotation.pdf`), page 1, source `attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L19`, extracted page Unicode character range [883, 966); available at events 019.

> This quotation covers surface preparation and decorative painting only. It excludes

```json
{
  "source_id": "015:L5",
  "expression": "Asked whether painting would affect the door and requested advance notice before any further access.",
  "occurrence": 1
}
```
Event `015`, source `015:L5`, event character range [132, 315).

> Said the door has latched on each use since the visit but still needs a firm pull. Asked whether painting would affect the door and requested advance notice before any further access.

```json
{
  "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L23",
  "expression": "No door-set inspection, fire-performance test, certification, compliance assessment, or fire-",
  "occurrence": 1
}
```
Document `017:ac210e2489e972791b0d` (`attachments/fire-door-quotation.pdf`), page 1, source `attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L23`, extracted page Unicode character range [1165, 1258); available at events 019.

> No door-set inspection, fire-performance test, certification, compliance assessment, or fire-

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r3",
      "provenance": {
        "source_ids": [
          "015:L2",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-017:001:34:43",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "but still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Said the door has latched on each use since the visit but still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Said the door has latched on each use since the visit but still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "still needs a firm pull",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Iona Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-017:001:184:197",
      "location_text": null,
      "observation_kind": "physical_condition",
      "attribute": "closing operation",
      "value": {
        "kind": "text",
        "value": "needs a firm pull"
      },
      "quoted_expression": "but still needs a firm pull",
      "epistemic_status": "asserted",
      "observed_at_text": "since the visit"
    },
    {
      "id": "b002:r5",
      "provenance": {
        "source_ids": [
          "017:L2",
          "017:L3",
          "017:L5"
        ],
        "asserted_by_entity_id": "entity:property-017:006:105:113",
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
              "expression": "the quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Elian Moss",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "017:L3",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "the quotation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "asked whether it can be approved from the repair budget",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Asked for the proposed scope and any building response to be confirmed before work is booked",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "Replied that the quotation appears affordable and asked whether it can be approved",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "asked whether it can be approved from the repair budget",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "asked whether it can be approved from the repair budget",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Elian Moss",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-017:001:141:243",
      "grantor_id": "entity:property-017:006:105:113",
      "grantee_id": "entity:property-017:001:80:89",
      "scope": [
        "repair"
      ],
      "decision": "requested",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "The proposed scope and any building response are to be confirmed before work is booked."
      ]
    },
    {
      "id": "b002:r6",
      "provenance": {
        "source_ids": [
          "015:L2",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-017:001:34:43",
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
              "expression": "requested advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Iona Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "requested advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "requested advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "requested advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "requested advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "requested advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Iona Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-017:001:141:243",
      "party_id": "entity:property-017:001:34:43",
      "constraint": "notice",
      "status": "required",
      "time_text": null,
      "description": "Tenant requested advance notice before any further access."
    },
    {
      "id": "b002:r9",
      "provenance": {
        "source_ids": [
          "015:L2",
          "015:L3",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-017:001:34:43",
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
              "expression": "Asked whether painting would affect the door and requested advance notice before any further access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Iona Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "015:L3",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Asked whether painting would affect the door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Asked whether painting would affect the door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Asked whether painting would affect the door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Asked whether painting would affect the door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Asked whether painting would affect the door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Iona Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-017:001:141:243",
      "sender_id": "entity:property-017:001:34:43",
      "recipient_id": "entity:property-017:001:80:89",
      "purpose": "clarification",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r10",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L3",
          "018:L5",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-017:001:80:89",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "asked whether surface preparation and painting of the flat-side face and top edge require building approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "018:L3",
              "expression": "Ravi Dast",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "asked whether the building has a current door schedule, inspection findings for this flat, or a preferred process",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Building manager's response to the scope query is pending",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Requested any inspection or door-record information relevant to the observed contact and slow closing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Asked whether surface preparation and painting ... require building approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Requested any inspection or door-record information",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-017:001:141:243",
      "sender_id": "entity:property-017:001:80:89",
      "recipient_id": "entity:property-017:004:104:120",
      "purpose": "clarification",
      "status": "no_response_reported",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r11",
      "provenance": {
        "source_ids": [
          "018:L5",
          "019:L2",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-017:001:80:89",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "asked whether surface preparation and painting of the flat-side face and top edge require building approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Building manager's response to the scope query is pending",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "require building approval or any specified materials or procedure",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "response to the scope query is pending",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "surface preparation and painting of the flat-side face and top edge",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Building manager's response to the scope query is pending",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Asked whether ... require building approval",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "response ... is pending",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-017:001:141:243",
      "responsible_party_id": "entity:property-017:004:104:120",
      "requirement": "confirmation",
      "status": "pending",
      "conditions": [
        "Confirm whether surface preparation and painting of the flat-side face and top edge require building approval or specified materials or procedure."
      ]
    },
    {
      "id": "b003:r1",
      "provenance": {
        "source_ids": [
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L1",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L10",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L11",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L12",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L13",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L14",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L15",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L17",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L18",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L19",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L20",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L21",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L22",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L23",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L24",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L25",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L26",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L3",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L6",
          "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L9"
        ],
        "asserted_by_entity_id": "entity:property-017:010:55:76",
        "origin": "document_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L1",
              "expression": "Flat Entrance Door Surface",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L1",
              "expression": "Flat Entrance Door",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L3",
              "expression": "Pale Finch Decorating",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L10",
              "expression": "Protect the immediate work area on the flat side of the entrance door.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L11",
              "expression": "Lightly sand loose coating on the flat-side face and visible top edge.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L12",
              "expression": "Spot-fill minor surface marks and apply one undercoat and two finish coats of water-",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L13",
              "expression": "based interior paint to those areas.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L14",
              "expression": "Remove work-area protection and leave the area tidy.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L19",
              "expression": "This quotation covers surface preparation and decorative painting only.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L15",
              "expression": "Quotation total: £186.00, including materials and labour.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L15",
              "expression": "£186.00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L17",
              "expression": "Price assumes access during one visit and a sound, dry surface beneath the loose coating.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L18",
              "expression": "Any additional substrate damage or preparation will be priced separately before proceeding.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L19",
              "expression": "This quotation covers surface preparation and decorative painting only. It excludes",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L20",
              "expression": "adjustment of the door, frame or hinges; removal or replacement of hardware; alterations to",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L21",
              "expression": "the door, frame, seals or threshold; and investigation of the door's construction or closing",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L22",
              "expression": "performance.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L23",
              "expression": "No door-set inspection, fire-performance test, certification, compliance assessment, or fire-",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L24",
              "expression": "safety opinion is included. No statement is made about the door's rating or suitability for any",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L25",
              "expression": "fire-safety purpose.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L26",
              "expression": "Work is subject to access being arranged by the client. No work has been scheduled.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "valid_time_text",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L6",
              "expression": "Valid until: 28 February 2025",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L1",
              "expression": "C O N T R A C T O R  Q U O TAT I O N",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L9",
              "expression": "Proposed work",
              "occurrence": 1
            },
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L26",
              "expression": "No work has been scheduled.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L15",
              "expression": "Quotation total: £186.00, including materials and labour.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "attachment:017:ac210e2489e972791b0d:14872b21608680524fccd59419d8c6a41db0e9a8180384ad6f3469e721f46f11:p1:L3",
              "expression": "Pale Finch Decorating",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_proposal",
      "request_id": "entity:property-017:001:141:243",
      "asset_id": "entity:property-017:001:184:197",
      "provider_id": "entity:property-017:010:55:76",
      "scope": [
        "repair"
      ],
      "amount_minor": 18600,
      "currency": "GBP",
      "conditions": [
        "Protect the immediate work area; sand loose coating on the flat-side face and visible top edge; spot-fill minor surface marks; apply one undercoat and two finish coats of water-based interior paint to those areas; remove protection and leave the area tidy.",
        "Price assumes access during one visit and a sound, dry surface beneath the loose coating.",
        "Any additional substrate damage or preparation will be priced separately before proceeding.",
        "Surface preparation and decorative painting only; excludes door/frame/hinge adjustment, hardware removal or replacement, alterations to the door/frame/seals/threshold, investigation of construction or closing performance, door-set inspection, fire-performance test, certification, compliance assessment, or fire-safety opinion. No statement is made about the door's rating or suitability for any fire-safety purpose.",
        "Work is subject to access being arranged by the client; no work has been scheduled."
      ],
      "valid_time_text": "28 February 2025"
    }
  ],
  "gaps": []
}
```
