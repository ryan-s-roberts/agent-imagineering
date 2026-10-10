# Decision rationale and evidence

Case 023; checkpoint `023-at-023`; prefix ends at event `23`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

The operational objective is to address the tenant-reported intermittent heating while resolving whether the actuator work was actually completed and how the overlapping invoices should be treated. The latest contractor response says the records are still being checked, and the manager has asked the landlord how to proceed and whether further work or expenditure is authorized; those responses remain outstanding. Wait for each party’s already-requested response, and update the tenant without implying that the disputed work is verified or authorized.

## Assumptions

- Treat the initial inspection request and the later diagnosis/actuator references as one continuing heating matter for these proposals: the sources concern the same property and heating issue, and identify the same provider and 5 February service date. This is a continuity inference, not proof that extracted request IDs are identical.

## Uncertainties

- The invoices report billed work, not independently verified completion. The contractor has not resolved whether the charges overlap or one invoice supersedes the other.
- Further remedial work or expenditure is not authorized; the diagnostic-only authority does not cover actuator replacement.

## Alternatives considered

- Did not request another work report or repeat the landlord approval request: the provider has said it is checking the records, and the manager’s latest email already asks the landlord to advise and state whether further work or expenditure is authorized.
- Did not instruct or book remedial work: the landlord’s supplied decision expressly withholds authorization for remedial work and further expenditure.

## Cited prefix evidence

```json
{
  "source_id": "022:L5",
  "expression": "could not yet confirm whether the invoice entries represented separate chargeable work or whether one record replaced the other",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [147, 405).

> Replied that she was checking the records and could not yet confirm whether the invoice entries represented separate chargeable work or whether one record replaced the other. She supplied no further completion evidence, revised invoice or parts confirmation.

```json
{
  "source_id": "022:L5",
  "expression": "She supplied no further completion evidence, revised invoice or parts confirmation.",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [147, 405).

> Replied that she was checking the records and could not yet confirm whether the invoice entries represented separate chargeable work or whether one record replaced the other. She supplied no further completion evidence, revised invoice or parts confirmation.

```json
{
  "source_id": "023:L5",
  "expression": "there is no recorded payment, confirmed supersession or authorization for actuator work",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [121, 447).

> The two invoice records remain on file; there is no recorded payment, confirmed supersession or authorization for actuator work. The tenant reports intermittent heating and has not confirmed replacement. Please advise how you wish to proceed on the unresolved records and whether any further work or expenditure is authorized.

```json
{
  "source_id": "023:L5",
  "expression": "Please advise how you wish to proceed on the unresolved records and whether any further work or expenditure is authorized.",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [121, 447).

> The two invoice records remain on file; there is no recorded payment, confirmed supersession or authorization for actuator work. The tenant reports intermittent heating and has not confirmed replacement. Please advise how you wish to proceed on the unresolved records and whether any further work or expenditure is authorized.

```json
{
  "source_id": "020:L5",
  "expression": "Heating was currently working intermittently",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [118, 365).

> Said she recalled the 5 February visit but did not know whether the actuator had been replaced. She had not seen a contractor at the property since that visit. Heating was currently working intermittently, with one radiator cooler than the others.

```json
{
  "source_id": "020:L5",
  "expression": "did not know whether the actuator had been replaced",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [118, 365).

> Said she recalled the 5 February visit but did not know whether the actuator had been replaced. She had not seen a contractor at the property since that visit. Heating was currently working intermittently, with one radiator cooler than the others.

```json
{
  "source_id": "005:L5",
  "expression": "Authorized diagnosis up to £180 including VAT only.",
  "occurrence": 1
}
```
Event `005`, source `005:L5`, event character range [121, 260).

> Authorized diagnosis up to £180 including VAT only. Asked to be consulted before any remedial work or additional expenditure is authorized.

```json
{
  "source_id": "012:L5",
  "expression": "Did not authorize remedial work or further expenditure.",
  "occurrence": 1
}
```
Event `012`, source `012:L5`, event character range [121, 316).

> Had not decided on the estimate. Asked whether the actuator could be repaired and whether the price included all parts, labour and testing. Did not authorize remedial work or further expenditure.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b003:r1",
      "provenance": {
        "source_ids": [
          "022:L1",
          "022:L2",
          "022:L3",
          "022:L5"
        ],
        "asserted_by_entity_id": "entity:property-023:006:109:119",
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
              "expression": "invoice entries",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "022:L2",
              "expression": "Petra Quill",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "022:L3",
              "expression": "Ivo Merrick",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "could not yet confirm whether the invoice entries represented separate chargeable work or whether one record replaced the other",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Replied",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "022:L2",
              "expression": "Petra Quill",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "022:L1",
              "expression": "Email",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Replied",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "She supplied no further completion evidence, revised invoice or parts confirmation.",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-023:001:261:285",
      "sender_id": "entity:property-023:006:109:119",
      "recipient_id": "entity:property-023:001:64:75",
      "purpose": "clarification",
      "status": "answered",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b003:r2",
      "provenance": {
        "source_ids": [
          "023:L1",
          "023:L2",
          "023:L3",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-023:001:64:75",
        "origin": "system_record",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "two invoice records",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Ivo Merrick",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "023:L3",
              "expression": "Soren Dallow",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "whether any further work or expenditure is authorized",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Please advise",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Ivo Merrick",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L1",
              "expression": "Email",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Please advise",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "Please advise how you wish to proceed on the unresolved records",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-023:001:261:285",
      "sender_id": "entity:property-023:001:64:75",
      "recipient_id": "entity:property-023:004:110:118",
      "purpose": "approval",
      "status": "requested",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b003:r3",
      "provenance": {
        "source_ids": [
          "023:L2",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-023:001:64:75",
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
              "expression": "The tenant reports intermittent heating",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "asset_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "intermittent heating",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "The tenant reports intermittent heating and has not confirmed replacement.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "troubleshooting",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "has not confirmed replacement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Ivo Merrick",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "The tenant reports intermittent heating",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "reports intermittent heating",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "The tenant reports intermittent heating",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "issue",
      "request_id": "entity:property-023:001:261:285",
      "asset_id": "entity:property-023:001:132:148",
      "property_id": null,
      "description": "The tenant reports intermittent heating and has not confirmed replacement.",
      "troubleshooting": "not_established"
    }
  ],
  "gaps": []
}
```
