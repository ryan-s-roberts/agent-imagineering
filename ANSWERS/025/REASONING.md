# Decision rationale and evidence

Case 025; checkpoint `025-at-022`; prefix ends at event `22`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The latest event supplies a corrected invoice: it reports the tap was supplied and installed and says the property postcode was amended. The invoice had been described as awaiting operator review, so register it and route the reported tap work for review rather than treating the report as independently verified or closing the request. Separately, the tenant’s cloudy-water concern and drawer report are not addressed by the invoice and need distinct follow-up.

## Assumptions

- The corrected invoice's tap installation belongs to the original dripping-tap request, based on chronological continuity and the same contractor; the new tap is the replacement, not a claim that it is the original tap asset.

## Uncertainties

- The invoice is a document report of supplied and installed work, not independent verification; operator review is still pending.
- The sources do not say whether the water remains cloudy after the reported tap installation.
- The drawer has no reported assessment, and no suitable repair provider or scope is established.

## Alternatives considered

- Did not propose closure: the source says operator review is pending, and the reported installation does not resolve the separate cloudy-water concern.
- Did not assign the plumber to the drawer: the evidence does not establish that this plumbing provider can assess or repair it.

## Cited prefix evidence

```json
{
  "source_id": "022:L5",
  "expression": "The corrected invoice shows the property's recorded postcode and describes a new mono kitchen sink tap supplied and installed.",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [149, 316).

> The corrected invoice shows the property's recorded postcode and describes a new mono kitchen sink tap supplied and installed. The invoice is awaiting operator review.

```json
{
  "source_id": "022:L5",
  "expression": "The invoice is awaiting operator review.",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [149, 316).

> The corrected invoice shows the property's recorded postcode and describes a new mono kitchen sink tap supplied and installed. The invoice is awaiting operator review.

```json
{
  "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7",
  "expression": "Supply and install one new mono kitchen sink tap.",
  "occurrence": 1
}
```
Document `025:c21543fa295cfeec1578` (`attachments/corrected-plumbing-invoice.pdf`), page 1, source `attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7`, extracted page Unicode character range [223, 272); available at events 022.

> Supply and install one new mono kitchen sink tap.

```json
{
  "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L8",
  "expression": "Correction note: Property postcode amended.",
  "occurrence": 1
}
```
Document `025:c21543fa295cfeec1578` (`attachments/corrected-plumbing-invoice.pdf`), page 1, source `attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L8`, extracted page Unicode character range [273, 316); available at events 022.

> Correction note: Property postcode amended.

```json
{
  "source_id": "001:L5",
  "expression": "cloudy-looking water",
  "occurrence": 1
}
```
Event `001`, source `001:L5`, event character range [117, 345).

> Reports a constantly dripping kitchen mixer tap and cloudy-looking water when filling a glass. Says limescale may be involved and asks whether a replacement tap could be considered. No urgency or access constraints are reported.

```json
{
  "source_id": "012:L5",
  "expression": "the top kitchen drawer is loose and its metal front brackets appear snapped",
  "occurrence": 1
}
```
Event `012`, source `012:L5`, event character range [116, 354).

> Says they are still waiting for contact about the leaking tap despite providing availability. Separately reports the top kitchen drawer is loose and its metal front brackets appear snapped; asks if it can be repaired when someone attends.

```json
{
  "source_id": "015:L5",
  "expression": "The message does not address the drawer or provide new information about the cloudy water.",
  "occurrence": 1
}
```
Event `015`, source `015:L5`, event character range [116, 323).

> Says they will be at work from 11:00 the next day and authorizes the plumber to attend using the agency's spare key. The message does not address the drawer or provide new information about the cloudy water.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r5",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-025:001:34:44",
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
              "expression": "Reports a constantly dripping kitchen mixer tap and cloudy-looking water",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "kitchen mixer tap",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a constantly dripping kitchen mixer tap and cloudy-looking water. Says limescale may be involved and asks whether a replacement tap could be considered.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a constantly dripping kitchen mixer tap",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Nia Calder (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a constantly dripping kitchen mixer tap and cloudy-looking water",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports a constantly dripping kitchen mixer tap and cloudy-looking water",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-025:001:117:189",
      "asset_id": "entity:property-025:001:147:164",
      "property_id": null,
      "description": "Tenant reports a constantly dripping kitchen mixer tap and cloudy-looking water, says limescale may be involved, and asks whether replacement could be considered; limescale is a suspicion, not a confirmed cause.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b001:r10",
      "provenance": {
        "source_ids": [
          "004:L2",
          "004:L3",
          "004:L5"
        ],
        "asserted_by_entity_id": "entity:property-025:001:64:74",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "004:L5",
              "expression": "Requests a quote or advice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "004:L3",
              "expression": "Ivo Fenlock",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "004:L5",
              "expression": "quote",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "004:L5",
              "expression": "Requests a quote or advice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "004:L5",
              "expression": "whether a site visit is needed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "004:L2",
              "expression": "Tessa Wren (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "004:L5",
              "expression": "Requests a quote or advice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "004:L5",
              "expression": "Requests a quote or advice",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "004:L2",
              "expression": "Tessa Wren",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-025:001:117:189",
      "responsible_party_id": "entity:property-025:004:108:118",
      "requirement": "quote",
      "status": "requested",
      "conditions": [
        "Quote or advice requested on whether a site visit is needed for the dripping mixer tap and cloudy-water report."
      ]
    },
    {
      "id": "b001:r16",
      "provenance": {
        "source_ids": [
          "012:L2",
          "012:L5"
        ],
        "asserted_by_entity_id": "entity:property-025:001:34:44",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "top kitchen drawer",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "the top kitchen drawer is loose and its metal front brackets appear snapped; asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "012:L2",
              "expression": "Nia Calder (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "the top kitchen drawer is loose",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "012:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-025:012:306:353",
      "asset_id": "entity:property-025:012:233:251",
      "property_id": null,
      "description": "Tenant separately reports the top kitchen drawer is loose and its metal front brackets appear snapped, and asks if it can be repaired when someone attends.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b001:r19",
      "provenance": {
        "source_ids": [
          "012:L2",
          "012:L3",
          "012:L5"
        ],
        "asserted_by_entity_id": "entity:property-025:001:64:74",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "012:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "012:L3",
              "expression": "Tessa Wren",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "012:L2",
              "expression": "Nia Calder (Tenant)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "asks if it can be repaired when someone attends",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "012:L2",
              "expression": "Nia Calder",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-025:012:306:353",
      "sender_id": "entity:property-025:001:34:44",
      "recipient_id": "entity:property-025:001:64:74",
      "purpose": "clarification",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:work-report-invoiced-tap",
      "provenance": {
        "source_ids": [
          "022:L5",
          "022:L7"
        ],
        "asserted_by_entity_id": null,
        "origin": "document_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "new mono kitchen sink tap supplied and installed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "new mono kitchen sink tap",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "022:L7",
              "expression": "corrected-plumbing-invoice.pdf",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "supplied and installed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "The corrected invoice shows the property's recorded postcode and describes a new mono kitchen sink tap supplied and installed.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "The corrected invoice shows",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "describes a new mono kitchen sink tap supplied and installed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "supplied and installed",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-025:001:117:189",
      "asset_id": "entity:property-025:019:172:197",
      "document_id": "entity:property-025:022:15:23",
      "outcome": "repaired",
      "description": "Corrected invoice describes a new mono kitchen sink tap supplied and installed."
    },
    {
      "id": "b002:invoice-review-obligation",
      "provenance": {
        "source_ids": [
          "022:L5"
        ],
        "asserted_by_entity_id": null,
        "origin": "document_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "The invoice is awaiting operator review",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "operator review",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "awaiting operator review",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "The invoice is awaiting operator review",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "is awaiting operator review",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "The invoice is awaiting operator review",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-025:001:117:189",
      "responsible_party_id": null,
      "requirement": "invoice",
      "status": "pending",
      "conditions": []
    },
    {
      "id": "b003:r1",
      "provenance": {
        "source_ids": [
          "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L1",
          "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L3",
          "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L4",
          "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L5",
          "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L6",
          "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7",
          "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L8"
        ],
        "asserted_by_entity_id": null,
        "origin": "document_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7",
              "expression": "Supply and install one new mono kitchen sink tap.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7",
              "expression": "one new mono kitchen sink tap",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L1",
              "expression": "B I L L I N G  D O C U M E N T",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L6",
              "expression": "Work invoiced",
              "occurrence": 1
            },
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7",
              "expression": "Supply and install one new mono kitchen sink tap.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L3",
              "expression": "Invoice reference: NBL-025-INV-15",
              "occurrence": 1
            },
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L4",
              "expression": "Corrected: 15 September 2025",
              "occurrence": 1
            },
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L5",
              "expression": "Property: 18 Thistlewick Row, Fenmere, ZZ1 1ZZ",
              "occurrence": 1
            },
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7",
              "expression": "Supply and install one new mono kitchen sink tap.",
              "occurrence": 1
            },
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L8",
              "expression": "Correction note: Property postcode amended.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L1",
              "expression": "B I L L I N G  D O C U M E N T",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L6",
              "expression": "Work invoiced",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "attachment:025:c21543fa295cfeec1578:119597caa26becac9762275ab8462adbb2e7e59cfc53ffdc4e088763eba1333c:p1:L7",
              "expression": "Supply and install one new mono kitchen sink tap.",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-025:001:117:189",
      "asset_id": "entity:property-025:019:172:197",
      "document_id": "entity:property-025:022:15:23",
      "outcome": "repaired",
      "description": "The corrected invoice (reference NBL-025-INV-15), dated 15 September 2025, identifies the property as 18 Thistlewick Row, Fenmere, ZZ1 1ZZ and invoices supply and installation of one new mono kitchen sink tap. It notes that the property postcode was amended."
    }
  ],
  "gaps": []
}
```
