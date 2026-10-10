# Decision rationale and evidence

Case 024; checkpoint `024-at-021`; prefix ends at event `21`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The operational objective is to verify the reported move-out work and resolve the still-open approval/review situation before treating the request as complete or telling the landlord the work is confirmed. The latest note reports that the clear-out and service were done, but also says to check that everything is finished; the latest workflow update says landlord quote approval remains open. The quotation describes cleaning tasks, while the checkout report makes item removal a prerequisite to the final service. I infer these refer to the same move-out job from the property and chronology; the extracted request labels differ, so I do not treat them as proof that removal was included in the quote.

## Assumptions

- The internal note's clear-out and property service concerns this continuing move-out request, based on the chronology and references to Sella; this is an inference, not a verified entity merge.

## Uncertainties

- The internal note is a report of work done, not provider confirmation or proof that all requested work was completed.
- The supplied sources do not establish whether the listed items were removed, whether that work was part of the quoted price, or whether the still-pending approval was resolved outside the recorded communications.

## Alternatives considered

- Did not propose closure or completion review: the reported work still needs the specifically requested check, and the workflow remains at landlord quote approval.
- Did not repeat the landlord approval request: it was already sent and reminded; its response remains outstanding.

## Cited prefix evidence

```json
{
  "source_id": "020:L5",
  "expression": "clear-out and property service was done today; check to make sure all finished then let Sella know",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [156, 324).

> Internal note reads: “clear-out and property service was done today; check to make sure all finished then let Sella know.” The landlord-approval workflow is still open.

```json
{
  "source_id": "021:L5",
  "expression": "The request remains at landlord quote approval.",
  "occurrence": 1
}
```
Event `021`, source `021:L5`, event character range [138, 235).

> The request remains at landlord quote approval. The internal note reporting work done is on file.

```json
{
  "source_id": "019:L5",
  "expression": "No landlord response is recorded in the communications history.",
  "occurrence": 1
}
```
Event `019`, source `019:L5`, event character range [149, 278).

> Sent a reminder requesting a decision on the £180 plus VAT quote. No landlord response is recorded in the communications history.

```json
{
  "source_id": "018:L5",
  "expression": "Requested approval or rejection of the £180 plus VAT quote.",
  "occurrence": 1
}
```
Event `018`, source `018:L5`, event character range [149, 336).

> Requested approval or rejection of the £180 plus VAT quote. The email presents the original request alongside the contractor's task list. It says arrangements will be made after approval.

```json
{
  "source_id": "attachment:024:212d0770884928e3b11e:64f64699dad7ebd692df242fd6ffdabf8f32450218c17047da22d7f0def7b58d:p1:L12",
  "expression": "after the listed items and waste have",
  "occurrence": 1
}
```
Document `024:212d0770884928e3b11e` (`attachments/checkout-report.pdf`), page 1, source `attachment:024:212d0770884928e3b11e:64f64699dad7ebd692df242fd6ffdabf8f32450218c17047da22d7f0def7b58d:p1:L12`, extracted page Unicode character range [395, 486); available at events 021.

> Carry out final end-of-occupancy property preparation after the listed items and waste have

```json
{
  "source_id": "attachment:024:212d0770884928e3b11e:64f64699dad7ebd692df242fd6ffdabf8f32450218c17047da22d7f0def7b58d:p1:L13",
  "expression": "been removed.",
  "occurrence": 1
}
```
Document `024:212d0770884928e3b11e` (`attachments/checkout-report.pdf`), page 1, source `attachment:024:212d0770884928e3b11e:64f64699dad7ebd692df242fd6ffdabf8f32450218c17047da22d7f0def7b58d:p1:L13`, extracted page Unicode character range [487, 500); available at events 021.

> been removed.

```json
{
  "source_id": "attachment:024:8edd7445739a5b841a96:412c425f35355d13fe8458ab4c2f80efa06806c737d09eec1a49e2901ac6f253:p1:L7",
  "expression": "Included service",
  "occurrence": 1
}
```
Document `024:8edd7445739a5b841a96` (`attachments/property-service-quotation.pdf`), page 1, source `attachment:024:8edd7445739a5b841a96:412c425f35355d13fe8458ab4c2f80efa06806c737d09eec1a49e2901ac6f253:p1:L7`, extracted page Unicode character range [217, 233); available at events 021.

> Included service

```json
{
  "source_id": "011:L5",
  "expression": "Said completion photographs would be sent.",
  "occurrence": 1
}
```
Event `011`, source `011:L5`, event character range [147, 439).

> Quoted £180 plus VAT for an end-of-occupancy service. Listed internal windows and frames, white goods, kitchen units, bathroom treatment, carpets vacuumed and deodorised, hard floors swept and mopped, light fittings, and freestanding air fresheners. Said completion photographs would be sent.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r3",
      "provenance": {
        "source_ids": [
          "017:L5"
        ],
        "asserted_by_entity_id": null,
        "origin": "system_record",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The request has moved to landlord quote approval.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The request has moved to landlord quote approval.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The request has moved to landlord quote approval.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The request has moved to landlord quote approval.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The request has moved to landlord quote approval.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "source_label",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "The request has moved to landlord quote approval.",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "request_status",
      "request_id": "entity:property-024:001:167:183",
      "status": "awaiting_approval",
      "source_label": "The request has moved to landlord quote approval."
    },
    {
      "id": "b002:r5",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L3",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-024:001:34:46",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Elowen Pryce",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Requested approval or rejection of the £180 plus VAT quote.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Requested approval or rejection of the £180 plus VAT quote.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Requested approval or rejection of the £180 plus VAT quote.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "the original request",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "018:L3",
              "expression": "Landlord",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "£180 plus VAT quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Requested approval or rejection",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "amount_minor",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "£180",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "currency",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "£180",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "It says arrangements will be made after approval.",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-024:001:167:183",
      "grantor_id": "entity:property-024:002:189:197",
      "grantee_id": null,
      "scope": [
        "quote"
      ],
      "decision": "requested",
      "amount_minor": 18000,
      "currency": "GBP",
      "conditions": [
        "Arrangements will be made after approval."
      ]
    },
    {
      "id": "b002:r7",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L3",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-024:001:34:46",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Elowen Pryce",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Sent a reminder requesting a decision on the £180 plus VAT quote.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Sent a reminder requesting a decision on the £180 plus VAT quote.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Sent a reminder requesting a decision on the £180 plus VAT quote.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "the £180 plus VAT quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Elowen Pryce",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "019:L3",
              "expression": "Sella Voss",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "requesting a decision",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "No landlord response is recorded in the communications history.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responds_to_record_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Sent a reminder",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-024:001:167:183",
      "sender_id": "entity:property-024:001:34:46",
      "recipient_id": "entity:property-024:002:189:197",
      "purpose": "approval",
      "status": "no_response_reported",
      "responds_to_record_id": "b002:r6",
      "deadline_text": null
    },
    {
      "id": "b002:r8",
      "provenance": {
        "source_ids": [
          "020:L2",
          "020:L5"
        ],
        "asserted_by_entity_id": "entity:property-024:001:34:46",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "020:L2",
              "expression": "Elowen Pryce",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "clear-out and property service was done today",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "clear-out and property service was done today",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "clear-out and property service was done today",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "clear-out and property service",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "check to make sure all finished",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "clear-out and property service was done today; check to make sure all finished then let Sella know",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-024:001:167:183",
      "asset_id": null,
      "document_id": null,
      "outcome": "unknown",
      "description": "Internal note reports that “clear-out and property service was done today” and says to check that all was finished, then let Sella know."
    }
  ],
  "gaps": []
}
```
