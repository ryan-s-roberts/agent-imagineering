# Decision rationale and evidence

Case 016; checkpoint `016-at-017`; prefix ends at event `17`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The operational objective remains to resolve the reported smoke-alarm work without treating it as complete: the tenant reported the work unfinished and an alarm fitter's visit unsuccessful (r23), and the latest report describes an unannounced, unidentified visitor whom the tenant did not admit. Ask the landlord to establish whether that visitor and any future visit are connected to his electrician, and escalate the access/identity concern for human review. A brief acknowledgement can address the tenant's concern while respecting the recorded request to limit contact. The request is already recorded as pending review; that does not establish resolution or justify closure.

## Assumptions

- The alarm-work references in the later reports concern NBL-016, consistent with the request reference and chronological continuity.

## Uncertainties

- The visitor's identity, authority, and connection to the alarm work are unverified; the tenant reports that the visitor was not admitted.
- The tenant's reported plan to arrange the unfinished work and the landlord's earlier electrician plan do not establish who will arrange the next visit.
- The source packet supports continuity of the alarm reports with NBL-016, but does not establish a confirmed future appointment.

## Alternatives considered

- Do not assign or instruct a provider: no specific provider or verified visitor is established, and no confirmed appointment or authority for expanded work is supplied.
- Do not propose closure: the latest work account is unresolved and the status is only pending review.

## Cited prefix evidence

```json
{
  "source_id": "010:L5",
  "expression": "could not refit the alarm",
  "occurrence": 1
}
```
Event `010`, source `010:L5`, event character range [115, 379).

> Tenant said a fitter, not the landlord, had attended, removed the bracket, and could not refit the alarm because the box had no bracket in it. The alarm remained unmounted. Tenant thought the fitter might return the following day, but no appointment was confirmed.

```json
{
  "source_id": "013:L5",
  "expression": "asked the agency to leave them alone for the moment",
  "occurrence": 1
}
```
Event `013`, source `013:L5`, event character range [116, 409).

> Said the fitter had still not completed the alarm and that they had just been discharged from hospital. Tenant said they would arrange it and report when complete, and asked the agency to leave them alone for the moment because repeated calls and emails while they were ill had been upsetting.

```json
{
  "source_id": "014:L5",
  "expression": "Recorded a pause in tenant contact",
  "occurrence": 1
}
```
Event `014`, source `014:L5`, event character range [158, 323).

> Recorded a pause in tenant contact in response to the tenant's request while they recovered. There was no evidence on file that the alarm had been mounted or tested.

```json
{
  "source_id": "015:L5",
  "expression": "Tenant was unsure whether the visitor was connected to the alarm work.",
  "occurrence": 1
}
```
Event `015`, source `015:L5`, event character range [115, 417).

> Reported an unannounced person knocking at the property on Saturday morning and saying they were there to check something. Tenant did not let the person in because they could not verify who they were and thought it might be a scam. Tenant was unsure whether the visitor was connected to the alarm work.

```json
{
  "source_id": "016:L5",
  "expression": "The visitor's identity, organization, purpose, and authority have not been verified in this case.",
  "occurrence": 1
}
```
Event `016`, source `016:L5`, event character range [158, 429).

> Recorded the tenant's account that they had previously raised the unexpected knock with another agency contact, who said it had been passed to a building-management contact. The visitor's identity, organization, purpose, and authority have not been verified in this case.

```json
{
  "source_id": "017:L5",
  "expression": "NBL-016 is pending review.",
  "occurrence": 1
}
```
Event `017`, source `017:L5`, event character range [160, 186).

> NBL-016 is pending review.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b001:r9",
      "provenance": {
        "source_ids": [
          "010:L2",
          "010:L5"
        ],
        "asserted_by_entity_id": "entity:property-016:001:34:45",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "Tenant said",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "document_id",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "fitter, not the landlord, had attended",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "outcome",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "could not refit the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "a fitter, not the landlord, had attended, removed the bracket, and could not refit the alarm because the box had no bracket in it. The alarm remained unmounted.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "010:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "Tenant said",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "had attended",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "010:L5",
              "expression": "could not refit the alarm",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "work_report",
      "request_id": "entity:property-016:001:182:198",
      "asset_id": "entity:property-016:001:135:146",
      "document_id": null,
      "outcome": "unresolved",
      "description": "Tenant reported that a fitter (not the landlord) attended, removed the bracket, could not refit the alarm because the box had no bracket in it, and left the alarm unmounted."
    },
    {
      "id": "b001:r16",
      "provenance": {
        "source_ids": [
          "007:L2",
          "007:L3",
          "007:L5"
        ],
        "asserted_by_entity_id": "entity:property-016:002:210:218",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "the electrician would contact the tenant and complete the work by the following weekend at the latest",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "007:L2",
              "expression": "Ronan Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "007:L3",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "electrician would contact the tenant and complete the work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "would contact the tenant",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "deadline_text",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "by the following weekend at the latest",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "007:L2",
              "expression": "Ronan Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "Said the electrician would contact the tenant",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "would complete the work by the following weekend at the latest",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "007:L5",
              "expression": "would complete the work",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-016:001:182:198",
      "sender_id": "entity:property-016:002:210:218",
      "recipient_id": "entity:property-016:001:65:74",
      "purpose": "appointment",
      "status": "answered",
      "responds_to_record_id": "b001:r14",
      "deadline_text": "by the following weekend at the latest"
    },
    {
      "id": "b001:r21",
      "provenance": {
        "source_ids": [
          "013:L2",
          "013:L3",
          "013:L5"
        ],
        "asserted_by_entity_id": "entity:property-016:001:34:45",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "Tenant said they would arrange it and report when complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Elise Rowan",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "013:L3",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "asked the agency to leave them alone for the moment",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "Said the fitter had still not completed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "013:L2",
              "expression": "Elise Rowan",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "Said the fitter had still not completed the alarm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "they would arrange it and report when complete",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "013:L5",
              "expression": "asked the agency to leave them alone for the moment",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-016:001:182:198",
      "sender_id": "entity:property-016:001:34:45",
      "recipient_id": "entity:property-016:001:65:74",
      "purpose": "other",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": "for the moment"
    },
    {
      "id": "b002:r4",
      "provenance": {
        "source_ids": [
          "015:L1",
          "015:L2",
          "015:L3",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-016:001:34:45",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "alarm work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Elise Rowan",
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
              "expression": "Reported an unannounced person knocking at the property on Saturday morning",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant did not let the person in because they could not verify who they were and thought it might be a scam.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L1",
              "expression": "- **Channel:** Call",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Reported an unannounced person knocking at the property on Saturday morning",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Reported an unannounced person knocking at the property on Saturday morning",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Elise Rowan",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-016:001:182:198",
      "sender_id": "entity:property-016:001:34:45",
      "recipient_id": "entity:property-016:001:65:74",
      "purpose": "other",
      "status": "answered",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r6",
      "provenance": {
        "source_ids": [
          "015:L2",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-016:001:34:45",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "alarm work",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "visitor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant did not let the person in",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant did not let the person in because they could not verify who they were",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Saturday morning",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant did not let the person in because they could not verify who they were and thought it might be a scam.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Reported an unannounced person knocking at the property on Saturday morning",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant did not let the person in",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant did not let the person in",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Elise Rowan",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-016:001:182:198",
      "party_id": "entity:property-016:015:139:145",
      "constraint": "entry_permission",
      "status": "unavailable",
      "time_text": "Saturday morning",
      "description": "Tenant reported not letting the visitor in because they could not verify who they were and thought it might be a scam."
    },
    {
      "id": "b002:r7",
      "provenance": {
        "source_ids": [
          "017:L2",
          "017:L5"
        ],
        "asserted_by_entity_id": "entity:property-016:001:65:74",
        "origin": "system_record",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "NBL-016",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "pending review",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "source_label",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "NBL-016 is pending review.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "NBL-016 is pending review.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "NBL-016 is pending review.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "017:L5",
              "expression": "pending review",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "017:L2",
              "expression": "Maya Chen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "request_status",
      "request_id": "entity:property-016:001:182:198",
      "status": "other",
      "source_label": "pending review"
    }
  ],
  "gaps": [
    {
      "id": "b002:g1",
      "kind": "identity",
      "entity_ids": [
        "entity:property-016:015:139:145",
        "entity:property-016:001:182:198"
      ],
      "source_ids": [
        "015:L5",
        "016:L5"
      ],
      "description": "The visitor's identity, organization, purpose, and authority were not verified; it is also uncertain whether the visitor was connected to the alarm work."
    }
  ]
}
```
