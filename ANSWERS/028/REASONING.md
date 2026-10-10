# Decision rationale and evidence

Case 028; checkpoint `028-at-025`; prefix ends at event `25`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The landlord reported the work complete, and the request was marked completed; the outstanding operational issue is the unanswered request for an itemised cost breakdown and her view on former-tenant responsibility. The workflow task was dismissed and no active task remained, so a reminder and a renewed follow-up task are useful. I do not reopen maintenance work or propose another completion update.

## Assumptions

- e17 is the same move-out work bundle opened as NBL-028 (e3), based on the matching three work areas and chronological continuity.

## Uncertainties

- The completion statement is the landlord's report, not independent verification. No further verification is required for the administrative follow-up proposed here.
- Extracted request identifiers differ across records. The source chronology and matching work bundle support treating e17 as the continuing job for these actions; this is a continuity assumption, not a claim that the identifiers were reconciled.

## Alternatives considered

- Reopening maintenance work was not selected: the landlord reported completion and the request had already been marked completed.
- A new clarification request was not selected because the cost and responsibility questions were already asked; a reminder is more proportionate.

## Cited prefix evidence

```json
{
  "source_id": "021:L5",
  "expression": "The work has been completed at the property.",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [135, 284).

> Wrote: “The work has been completed at the property.” No completion date, photographs, invoice, or other contractor evidence accompanied the message.

```json
{
  "source_id": "022:L5",
  "expression": "The maintenance request was marked completed based on the landlord's email confirmation.",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [155, 243).

> The maintenance request was marked completed based on the landlord's email confirmation.

```json
{
  "source_id": "023:L5",
  "expression": "Asked for an itemised breakdown of costs incurred and whether the landlord considered any specific repairs to be the former tenant's responsibility",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [135, 325).

> Asked for an itemised breakdown of costs incurred and whether the landlord considered any specific repairs to be the former tenant's responsibility, so the tenancy account could be reviewed.

```json
{
  "source_id": "024:L5",
  "expression": "The pending workflow task was dismissed because the maintenance request was already completed.",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [155, 310).

> The pending workflow task was dismissed because the maintenance request was already completed. No further action was expected unless a new message arrived.

```json
{
  "source_id": "025:L5",
  "expression": "No reply to the request for the cost breakdown or responsibility allocation is recorded.",
  "occurrence": 1
}
```
Event `025`, source `025:L5`, event character range [153, 298).

> No reply to the request for the cost breakdown or responsibility allocation is recorded. The workflow has no active task following the dismissal.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r10",
      "provenance": {
        "source_ids": [
          "023:L2",
          "023:L3",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-028:001:32:42",
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
              "expression": "specific repairs",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Talia Wren",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "023:L3",
              "expression": "Elowen Quill",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Asked for an itemised breakdown of costs incurred and whether the landlord considered any specific repairs to be the former tenant's responsibility",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Asked for an itemised breakdown of costs incurred",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Asked for an itemised breakdown of costs incurred",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Asked for an itemised breakdown of costs incurred",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Asked for an itemised breakdown of costs incurred",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Talia Wren",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-028:002:188:203",
      "sender_id": "entity:property-028:001:32:42",
      "recipient_id": "entity:property-028:001:411:419",
      "purpose": "clarification",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r13",
      "provenance": {
        "source_ids": [
          "023:L5",
          "025:L2",
          "025:L3",
          "025:L5"
        ],
        "asserted_by_entity_id": "entity:property-028:001:32:42",
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
              "expression": "request for the cost breakdown or responsibility allocation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "025:L2",
              "expression": "Talia Wren",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "025:L3",
              "expression": "Oren Pell",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "No reply to the request for the cost breakdown or responsibility allocation is recorded.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "No reply to the request for the cost breakdown or responsibility allocation is recorded.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responds_to_record_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "request for the cost breakdown or responsibility allocation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "No reply to the request for the cost breakdown or responsibility allocation is recorded.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "No reply to the request for the cost breakdown or responsibility allocation is recorded.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "025:L5",
              "expression": "No reply to the request for the cost breakdown or responsibility allocation is recorded.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "025:L2",
              "expression": "Talia Wren",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-028:002:188:203",
      "sender_id": "entity:property-028:001:32:42",
      "recipient_id": "entity:property-028:001:411:419",
      "purpose": "clarification",
      "status": "no_response_reported",
      "responds_to_record_id": "b002:r10",
      "deadline_text": null
    }
  ],
  "gaps": [
    {
      "id": "b002:g2",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-028:002:188:203",
        "entity:property-028:001:411:419",
        "entity:property-028:023:252:265"
      ],
      "source_ids": [
        "023:L5",
        "025:L5"
      ],
      "description": "No reply is recorded to the request for an itemised cost breakdown or the landlord's view on whether particular repairs were the former tenant's responsibility; the workflow has no active task following dismissal."
    }
  ]
}
```
