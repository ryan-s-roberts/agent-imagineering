# Decision rationale and evidence

Case 030; checkpoint `030-at-015`; prefix ends at event `15`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The objective is to establish what work the landlord reports completing and whether the smoke-alarm and socket issues are now addressed. The latest emails add a general completion claim and specific reports of work on two sockets, but do not establish the smoke-alarm work or whether all reported loose sockets were covered. Seek the relevant details from both landlord and tenant, communicate progress, and place the affected requests into completion review. The reports remain attributed reports, not independently verified facts.

## Assumptions

- The generic completion claim and the earlier smoke-alarm request are treated as likely part of the same continuing conversation, not as confirmed identical work.
- The landlord's socket follow-up and the earlier report of several loose sockets are treated as the same ongoing socket issue based on the conversation's chronology.

## Uncertainties

- The landlord's report does not specify which work the 31 August completion claim refers to, or its year.
- The landlord reports work on two sockets, but the prefix does not establish whether these are all the sockets in the tenant's report or their current condition.
- The alarm was reported removed; the latest messages do not say whether it has since been restored.

## Alternatives considered

- Closure is premature because the completion claim does not identify its scope and the alarm's reported removal remains unaccounted for.
- No new approval or provider instruction is proposed: the landlord said he would do the work himself, and the current need is to clarify reported outcomes rather than authorize agency work.

## Cited prefix evidence

```json
{
  "source_id": "012:L5",
  "expression": "Reports that the job was completed on 31 August",
  "occurrence": 1
}
```
Event `012`, source `012:L5`, event character range [120, 257).

> Reports that the job was completed on 31 August and says the smoke alarm has a ten-year life. Asks for the property record to be updated.

```json
{
  "source_id": "012:L5",
  "expression": "the smoke alarm has a ten-year life",
  "occurrence": 1
}
```
Event `012`, source `012:L5`, event character range [120, 257).

> Reports that the job was completed on 31 August and says the smoke alarm has a ten-year life. Asks for the property record to be updated.

```json
{
  "source_id": "014:L5",
  "expression": "he tightened screws on one back-bedroom socket",
  "occurrence": 1
}
```
Event `014`, source `014:L5`, event character range [120, 430).

> Adds that he tightened screws on one back-bedroom socket; that on 5 August he secured a kitchen socket he says had come away after boiler work in February 2025; and that on 6 August he provided the tenant with a portable dehumidifier to place in the bathroom. He says the tenant is aware and will use it there.

```json
{
  "source_id": "014:L5",
  "expression": "on 5 August he secured a kitchen socket",
  "occurrence": 1
}
```
Event `014`, source `014:L5`, event character range [120, 430).

> Adds that he tightened screws on one back-bedroom socket; that on 5 August he secured a kitchen socket he says had come away after boiler work in February 2025; and that on 6 August he provided the tenant with a portable dehumidifier to place in the bathroom. He says the tenant is aware and will use it there.

```json
{
  "source_id": "005:L5",
  "expression": "several plug sockets coming away from the wall",
  "occurrence": 1
}
```
Event `005`, source `005:L5`, event character range [120, 258).

> Adds that the tenant had also reported several plug sockets coming away from the wall, and asks whether these should be looked at as well.

```json
{
  "source_id": "001:L5",
  "expression": "She removed the alarm",
  "occurrence": 1
}
```
Event `001`, source `001:L5`, event character range [119, 313).

> Reports that the upstairs landing smoke alarm kept beeping despite attempts to stop it. She removed the alarm, leaving a small opening in the ceiling. Says she knows of no immediate safety risk.

```json
{
  "source_id": "008:L5",
  "expression": "for confirmation when it is complete",
  "occurrence": 1
}
```
Event `008`, source `008:L5`, event character range [120, 264).

> Acknowledges the landlord's intention to carry out the work and asks when he expects it to be finished and for confirmation when it is complete.

```json
{
  "source_id": "015:L5",
  "expression": "The landlord's email was added to the property record.",
  "occurrence": 1
}
```
Event `015`, source `015:L5`, event character range [149, 203).

> The landlord's email was added to the property record.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r1",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:001:34:45",
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
              "expression": "upstairs landing smoke alarm kept beeping",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "upstairs landing smoke alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports that the upstairs landing smoke alarm kept beeping despite attempts to stop it. She removed the alarm, leaving a small opening in the ceiling. Says she knows of no immediate safety risk.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "despite attempts to stop it",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "Reports that the upstairs landing smoke alarm kept beeping",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "kept beeping",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "kept beeping",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Nessa Quill",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-030:001:136:177",
      "asset_id": "entity:property-030:001:136:164",
      "property_id": null,
      "description": "Tenant reports the alarm kept beeping despite attempts to stop it, says she removed it and left a small ceiling opening, and says she knows of no immediate safety risk.",
      "troubleshooting": "reported_failed"
    },
    {
      "id": "b001:r2",
      "provenance": {
        "source_ids": [
          "005:L2",
          "005:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:001:65:76",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "several plug sockets coming away from the wall",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "plug sockets",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "the tenant had also reported several plug sockets coming away from the wall",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "reported",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "Adds that the tenant had also reported",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "had also reported",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "coming away from the wall",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "005:L2",
              "expression": "Ivo Merrick",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-030:005:159:205",
      "asset_id": "entity:property-030:005:167:179",
      "property_id": null,
      "description": "Property manager relays the tenant's report that several plug sockets were coming away from the wall.",
      "troubleshooting": "not_established"
    },
    {
      "id": "b001:r4",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:001:34:45",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "removed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "removed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "removed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "She removed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "She removed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "She removed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "removed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "removed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Nessa Quill",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-030:001:136:164",
      "location_text": "upstairs landing",
      "observation_kind": "presence",
      "attribute": "smoke alarm installed",
      "value": {
        "kind": "boolean",
        "value": false
      },
      "quoted_expression": "She removed the alarm",
      "epistemic_status": "asserted",
      "observed_at_text": null
    },
    {
      "id": "b001:r5",
      "provenance": {
        "source_ids": [
          "001:L2",
          "001:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:001:34:45",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "opening in the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "leaving a small opening in the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "opening in the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "small opening",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "leaving a small opening in the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "leaving a small opening in the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "leaving a small opening in the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "leaving",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "001:L5",
              "expression": "opening in the ceiling",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "001:L2",
              "expression": "Nessa Quill",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-030:001:246:268",
      "location_text": "ceiling",
      "observation_kind": "physical_condition",
      "attribute": "opening",
      "value": {
        "kind": "text",
        "value": "small opening"
      },
      "quoted_expression": "leaving a small opening in the ceiling",
      "epistemic_status": "asserted",
      "observed_at_text": null
    },
    {
      "id": "b001:r11",
      "provenance": {
        "source_ids": [
          "005:L2",
          "005:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:001:65:76",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "plug sockets coming away from the wall",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "landlord",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "whether these should be looked at as well",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "should be looked at",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "asks whether these should be looked at as well",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "asks whether these should be looked at as well",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "asks whether",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "005:L5",
              "expression": "should be looked at",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "005:L2",
              "expression": "Ivo Merrick",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-030:005:159:205",
      "grantor_id": "entity:property-030:003:187:197",
      "grantee_id": "entity:property-030:001:96:116",
      "scope": [
        "inspect"
      ],
      "decision": "requested",
      "amount_minor": null,
      "currency": null,
      "conditions": []
    },
    {
      "id": "b001:r12",
      "provenance": {
        "source_ids": [
          "010:L2",
          "010:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:003:187:197",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "sockets",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "he will complete the work himself",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "no external action is required",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "no external action is required",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "no external action is required",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "he will complete the work himself",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "repeats that he will complete the work himself",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "will complete the work himself",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "no external action is required",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "010:L2",
              "expression": "Tavian Rusk",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-030:005:159:205",
      "grantor_id": "entity:property-030:003:187:197",
      "grantee_id": "entity:property-030:001:96:116",
      "scope": [
        "repair"
      ],
      "decision": "denied",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "Landlord says he will complete the work himself."
      ]
    },
    {
      "id": "b001:r14",
      "provenance": {
        "source_ids": [
          "008:L2",
          "008:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:001:65:76",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "the work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "landlord's intention",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "for confirmation when it is complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "asks when he expects it to be finished and for confirmation when it is complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "when it is complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "asks ... for confirmation",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "asks",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "008:L5",
              "expression": "for confirmation when it is complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "008:L2",
              "expression": "Ivo Merrick",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "obligation",
      "request_id": "entity:property-030:001:136:177",
      "responsible_party_id": "entity:property-030:003:187:197",
      "requirement": "confirmation",
      "status": "requested",
      "conditions": [
        "Confirm when the landlord's work is complete."
      ]
    },
    {
      "id": "b001:r15",
      "provenance": {
        "source_ids": [
          "012:L2",
          "012:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:003:187:197",
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
              "expression": "the job was completed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "smoke alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "property record",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "the job was completed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "Reports that the job was completed on 31 August and says the smoke alarm has a ten-year life.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "Reports that the job was completed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "was completed on 31 August",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "012:L5",
              "expression": "job was completed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "012:L2",
              "expression": "Tavian Rusk",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-030:001:136:177",
      "asset_id": "entity:property-030:001:136:164",
      "document_id": "entity:property-030:012:227:242",
      "outcome": "unknown",
      "description": "Landlord reports the job was completed on 31 August; the message does not specify which reported work the job covered."
    },
    {
      "id": "b001:r17",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:003:187:197",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "one back-bedroom socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "back-bedroom socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "property record",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "tightened screws on one back-bedroom socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "he tightened screws on one back-bedroom socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Adds that he tightened screws",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "tightened screws",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "tightened screws",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Tavian Rusk",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-030:005:159:205",
      "asset_id": "entity:property-030:014:157:176",
      "document_id": null,
      "outcome": "repaired",
      "description": "Landlord reports tightening screws on one back-bedroom socket; no date is stated for this work."
    },
    {
      "id": "b001:r18",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-030:003:187:197",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "kitchen socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "kitchen socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "on 5 August he secured a kitchen socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "on 5 August he secured a kitchen socket he says had come away after boiler work in February 2025",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "he secured a kitchen socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "on 5 August he secured",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "secured a kitchen socket",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Tavian Rusk",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-030:005:159:205",
      "asset_id": "entity:property-030:014:208:222",
      "document_id": null,
      "outcome": "repaired",
      "description": "Landlord reports securing the kitchen socket on 5 August. He says it had come away after boiler work in February 2025."
    }
  ],
  "gaps": [
    {
      "id": "b001:g1",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-030:001:136:177",
        "entity:property-030:005:159:205"
      ],
      "source_ids": [
        "007:L5",
        "011:L5",
        "012:L5"
      ],
      "description": "The landlord initially gave no expected completion date or work description. The later statement that “the job was completed on 31 August” does not identify which reported work it covers; the year for 31 August is not stated."
    }
  ]
}
```
