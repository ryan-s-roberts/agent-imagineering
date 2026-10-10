# Proposed answer

Case 029; checkpoint `029-at-020`; prefix ends at event `20`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

## Execution status

This system has no external execution environment, so it did not carry out any proposed actions. Actions and outcomes recorded in the case history are evidence; the actions below are recommendations. The case evidence bundle contains the supplied history and extracted support.

Disposition: **act**.

## Proposed actions

### Notify

```json
{
  "id": "a1",
  "request_id": "entity:property-029:002:142:172",
  "basis_record_ids": [
    "b002:r3",
    "b002:r5",
    "b002:r6",
    "b002:r9",
    "b002:r11",
    "b002:r13"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g3"
  ],
  "depends_on_action_ids": [],
  "type": "notify",
  "recipient_id": "entity:property-029:001:118:124",
  "purpose": "progress",
  "message": "The Saturday visit is not confirmed. The landlord has authorized a diagnostic visit only by a suitably identified heating contractor and has not agreed to entry while you are absent or to an external key arrangement. Please do not leave the key in the meter cabinet or treat Bram's message as an appointment confirmation. We are seeking confirmation of the contractor and arrangements; your possible 10:00–12:00 availability remains conditional on the visitor and purpose being confirmed in advance.",
  "about_record_ids": [
    "b002:r3",
    "b002:r5",
    "b002:r6",
    "b002:r9",
    "b002:r11"
  ]
}
```

### Provide guidance

```json
{
  "id": "a2",
  "request_id": "entity:property-029:002:142:172",
  "basis_record_ids": [
    "b002:r3",
    "b002:r4",
    "b002:r6",
    "b002:r11",
    "b002:r13"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g3"
  ],
  "depends_on_action_ids": [],
  "type": "provide_guidance",
  "recipient_id": "entity:property-029:001:172:190",
  "steps": [
    "Do not attend or seek access on the basis of the proposed Saturday period; no appointment is confirmed.",
    "Do not ask the tenant to leave a key in the external meter cabinet or to provide her mobile number directly.",
    "Send the property manager your current business identity/contact details, the diagnostic task you understand is authorized, and a specific available visit window. Wait for confirmation of the contractor and access arrangements through the manager before arranging attendance."
  ],
  "requested_feedback": "Please confirm the business identity/contact details and whether you can offer a specific visit window."
}
```

### Notify

```json
{
  "id": "a3",
  "request_id": "entity:property-029:002:142:172",
  "basis_record_ids": [
    "b002:r12",
    "b002:r3",
    "b002:r6",
    "b002:r11"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g3"
  ],
  "depends_on_action_ids": [],
  "type": "notify",
  "recipient_id": "entity:property-029:004:108:116",
  "purpose": "reminder",
  "message": "Following up on the outstanding request to confirm whether you intend to engage Bram Alder for this diagnostic visit and what access arrangements you authorize. Bram has now proposed Saturday and again asked for an external key drop, but no appointment window or such access authorization is established. Please confirm the intended contractor and authorized access arrangement; no absent entry or external key drop will be treated as approved meanwhile.",
  "about_record_ids": [
    "b002:r12",
    "b002:r3",
    "b002:r6",
    "b002:r11"
  ]
}
```

### Change workflow

```json
{
  "id": "a4",
  "request_id": "entity:property-029:002:142:172",
  "basis_record_ids": [
    "b002:r3",
    "b002:r4",
    "b002:r5",
    "b002:r6",
    "b002:r11"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g3"
  ],
  "depends_on_action_ids": [],
  "type": "change_workflow",
  "operation": "hold",
  "value": "Hold contractor attendance, appointment confirmation, and access arrangements pending contractor identification and authorized access confirmation.",
  "reason": "The landlord's diagnostic authorization is limited to a suitably identified contractor, while Bram's engagement remains unconfirmed and absent entry/external key access has not been agreed."
}
```

### Await response

```json
{
  "id": "a5",
  "request_id": "entity:property-029:002:142:172",
  "basis_record_ids": [
    "b002:r12",
    "b002:r3",
    "b002:r6"
  ],
  "basis_gap_ids": [
    "b002:g1",
    "b002:g3"
  ],
  "depends_on_action_ids": [
    "a3"
  ],
  "type": "await_response",
  "responsible_party_id": "entity:property-029:004:108:116",
  "awaited": "clarification"
}
```

## Action dependencies

- `a5` depends on `a3`.

## Human interventions

```json
[]
```

Conclusion records: []

## Evidence and reasoning

The objective remains a suitably identified contractor's diagnostic visit for intermittent boiler-pressure loss. The tenant now reports the heating is working but pressure has dropped intermittently, and Bram has renewed a Saturday visit/key request without a confirmed appointment window. The landlord authorized a diagnostic visit only for a suitably identified contractor and has not agreed absent entry or an external key arrangement. Keep the request open and hold attendance/entry arrangements while seeking the outstanding landlord response and preventing any assumption that the key request is authorized.

## Assumptions

- The Saturday messages and the earlier diagnostic-visit authorization concern the same open maintenance request, based on the continuing boiler-pressure issue and chronological continuity.

## Uncertainties

- Bram's current engagement/business identity for this visit remains unconfirmed; the landlord's clarification request has no recorded reply.
- No Saturday appointment window or approved access arrangement is established. The tenant's stated availability was conditional, not an appointment confirmation.
- The reported heating function and intermittent pressure loss are tenant reports, not independently verified findings.

## Alternatives considered

- Do not propose a booking or instruct diagnostic work to Bram now: the visit is unconfirmed and the landlord's suitably-identified-contractor condition is unresolved.
- Do not close the request: intermittent pressure loss is still reported and the diagnostic visit has not occurred.

## Cited prefix evidence

```json
{
  "source_id": "014:L5",
  "expression": "Landlord authorizes a diagnostic visit by a suitably identified heating contractor",
  "occurrence": 1
}
```
Event `014`, source `014:L5`, event character range [119, 414).

> Landlord authorizes a diagnostic visit by a suitably identified heating contractor to investigate intermittent pressure loss. He does not confirm that Bram Alder is currently engaged by Hearthline Boiler Service and has not agreed entry while the tenant is absent or an external key arrangement.

```json
{
  "source_id": "014:L5",
  "expression": "has not agreed entry while the tenant is absent or an external key arrangement",
  "occurrence": 1
}
```
Event `014`, source `014:L5`, event character range [119, 414).

> Landlord authorizes a diagnostic visit by a suitably identified heating contractor to investigate intermittent pressure loss. He does not confirm that Bram Alder is currently engaged by Hearthline Boiler Service and has not agreed entry while the tenant is absent or an external key arrangement.

```json
{
  "source_id": "015:L5",
  "expression": "Tenant reports the heating is currently working, although boiler pressure has dropped intermittently during the past month.",
  "occurrence": 1
}
```
Event `015`, source `015:L5`, event character range [118, 354).

> Tenant reports the heating is currently working, although boiler pressure has dropped intermittently during the past month. She could be home Saturday, May 17, between 10:00 and 12:00 if the visitor and purpose are confirmed in advance.

```json
{
  "source_id": "015:L5",
  "expression": "could be home Saturday, May 17, between 10:00 and 12:00 if the visitor and purpose are confirmed in advance",
  "occurrence": 1
}
```
Event `015`, source `015:L5`, event character range [118, 354).

> Tenant reports the heating is currently working, although boiler pressure has dropped intermittently during the past month. She could be home Saturday, May 17, between 10:00 and 12:00 if the visitor and purpose are confirmed in advance.

```json
{
  "source_id": "020:L5",
  "expression": "I can come Saturday sometime between 08:00 and 13:00. Can you confirm and leave the key in the meter cabinet if you won't be there?",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [113, 301).

> Message from 07700 900683: 'I can come Saturday sometime between 08:00 and 13:00. Can you confirm and leave the key in the meter cabinet if you won't be there?' The tenant has not replied.

```json
{
  "source_id": "020:L5",
  "expression": "The tenant has not replied",
  "occurrence": 1
}
```
Event `020`, source `020:L5`, event character range [113, 301).

> Message from 07700 900683: 'I can come Saturday sometime between 08:00 and 13:00. Can you confirm and leave the key in the meter cabinet if you won't be there?' The tenant has not replied.

```json
{
  "source_id": "019:L5",
  "expression": "No reply is yet recorded",
  "occurrence": 1
}
```
Event `019`, source `019:L5`, event character range [119, 290).

> Asked the landlord to clarify whether Bram Alder is the contractor he intends to engage and to confirm the access arrangements he is authorizing. No reply is yet recorded.

```json
{
  "source_id": "017:L5",
  "expression": "Consent field for disclosure to Bram Alder: EMPTY.",
  "occurrence": 1
}
```
Event `017`, source `017:L5`, event character range [135, 346).

> Tenancy record holds Elowen Vey's contact details. Consent field for disclosure to Bram Alder: EMPTY. Appointment correspondence logged: tenant message of 13 May at 11:41 and contractor email of 13 May at 12:26.

```json
{
  "source_id": "013:L5",
  "expression": "Maintenance enquiry NBL-029-01 remains open.",
  "occurrence": 1
}
```
Event `013`, source `013:L5`, event character range [135, 359).

> Maintenance enquiry NBL-029-01 remains open. Correspondence logged: landlord email of 12 May at 10:11 and contractor call of 13 May at 08:03. Work-order appointment entry: EMPTY. External key-drop authorisation field: EMPTY.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r3",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:004:108:116",
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
              "expression": "diagnostic visit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Landlord",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantee_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "suitably identified heating contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "diagnostic visit",
              "occurrence": 1
            },
            {
              "source_id": "014:L5",
              "expression": "investigate intermittent pressure loss",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "suitably identified heating contractor",
              "occurrence": 1
            },
            {
              "source_id": "014:L5",
              "expression": "does not confirm that Bram Alder is currently engaged by Hearthline Boiler Service",
              "occurrence": 1
            },
            {
              "source_id": "014:L5",
              "expression": "has not agreed entry while the tenant is absent or an external key arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Landlord authorizes",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "authorizes a diagnostic visit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "authorizes a diagnostic visit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Orren Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-029:002:142:172",
      "grantor_id": "entity:property-029:004:108:116",
      "grantee_id": "entity:property-029:014:163:201",
      "scope": [
        "inspect"
      ],
      "decision": "approved",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "Only a suitably identified heating contractor is authorized for the diagnostic visit; Bram Alder's current engagement by Hearthline Boiler Service is not confirmed.",
        "Entry while the tenant is absent and an external key arrangement are not agreed."
      ]
    },
    {
      "id": "b002:r4",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:004:108:116",
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
              "expression": "diagnostic visit",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constrains_record_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "suitably identified heating contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requirement",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "suitably identified heating contractor",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "does not confirm that Bram Alder is currently engaged by Hearthline Boiler Service",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "suitably identified heating contractor",
              "occurrence": 1
            },
            {
              "source_id": "014:L5",
              "expression": "does not confirm that Bram Alder is currently engaged by Hearthline Boiler Service",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Landlord authorizes",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "does not confirm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "does not confirm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Orren Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "condition",
      "request_id": "entity:property-029:002:142:172",
      "constrains_record_id": "b002:r3",
      "requirement": "other",
      "status": "unknown",
      "description": "The diagnostic visit requires a suitably identified heating contractor; Bram Alder's current engagement by Hearthline Boiler Service is not confirmed."
    },
    {
      "id": "b002:r5",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:004:108:116",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed entry while the tenant is absent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Landlord",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "entry while the tenant is absent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed entry while the tenant is absent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "while the tenant is absent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed entry while the tenant is absent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Landlord authorizes",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Orren Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-029:002:142:172",
      "party_id": "entity:property-029:004:108:116",
      "constraint": "entry_permission",
      "status": "unavailable",
      "time_text": "while the tenant is absent",
      "description": "The landlord has not agreed to entry while the tenant is absent."
    },
    {
      "id": "b002:r6",
      "provenance": {
        "source_ids": [
          "004:L2",
          "004:L3",
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:004:108:116",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "an external key arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "004:L3",
              "expression": "Orren Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "an external key arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed entry while the tenant is absent or an external key arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Landlord authorizes",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "has not agreed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Orren Vale",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-029:002:142:172",
      "party_id": "entity:property-029:004:108:116",
      "constraint": "keyholder",
      "status": "unavailable",
      "time_text": null,
      "description": "The landlord has not agreed to an external key arrangement."
    },
    {
      "id": "b002:r9",
      "provenance": {
        "source_ids": [
          "015:L2",
          "015:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:001:118:124",
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
              "expression": "could be home Saturday, May 17, between 10:00 and 12:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "could be home Saturday, May 17, between 10:00 and 12:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "could be home",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Saturday, May 17, between 10:00 and 12:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "if the visitor and purpose are confirmed in advance",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "Tenant reports",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "could be home",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "015:L5",
              "expression": "could be home",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "015:L2",
              "expression": "Elowen Vey",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-029:002:142:172",
      "party_id": "entity:property-029:001:118:124",
      "constraint": "availability",
      "status": "available",
      "time_text": "Saturday, May 17, between 10:00 and 12:00",
      "description": "Tenant could be home if the visitor and purpose are confirmed in advance."
    },
    {
      "id": "b002:r11",
      "provenance": {
        "source_ids": [
          "020:L2",
          "020:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:001:172:190",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "appointment_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Saturday sometime between 08:00 and 13:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "I can come Saturday sometime between 08:00 and 13:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "020:L2",
              "expression": "Bram Alder",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "tenant_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "The tenant",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Can you confirm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Saturday sometime between 08:00 and 13:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "I can come",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "I can come Saturday sometime between 08:00 and 13:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "I can come Saturday sometime between 08:00 and 13:00",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "020:L2",
              "expression": "Bram Alder",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "appointment",
      "appointment_id": "entity:property-029:016:158:166",
      "request_id": "entity:property-029:002:142:172",
      "provider_id": "entity:property-029:001:172:190",
      "tenant_id": "entity:property-029:001:118:124",
      "status": "proposed",
      "time_text": "Saturday sometime between 08:00 and 13:00",
      "supersedes_record_id": null
    },
    {
      "id": "b002:r12",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L3",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:001:64:75",
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
              "expression": "Asked the landlord to clarify",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Tamsin Rook",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "019:L3",
              "expression": "Orren Vale",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "clarify whether Bram Alder is the contractor he intends to engage and to confirm the access arrangements he is authorizing",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "No reply is yet recorded",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Asked the landlord",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Asked the landlord to clarify",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Asked the landlord to clarify",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Tamsin Rook",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-029:002:142:172",
      "sender_id": "entity:property-029:001:64:75",
      "recipient_id": "entity:property-029:004:108:116",
      "purpose": "clarification",
      "status": "no_response_reported",
      "responds_to_record_id": null,
      "deadline_text": null
    },
    {
      "id": "b002:r13",
      "provenance": {
        "source_ids": [
          "020:L2",
          "020:L3",
          "020:L5"
        ],
        "asserted_by_entity_id": "entity:property-029:001:172:190",
        "origin": "attributed_report",
        "modality": "requested",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Can you confirm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "sender_id",
          "spans": [
            {
              "source_id": "020:L2",
              "expression": "Bram Alder",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "recipient_id",
          "spans": [
            {
              "source_id": "020:L3",
              "expression": "Elowen Vey",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "purpose",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Can you confirm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "The tenant has not replied",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Message from 07700 900683",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Can you confirm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "020:L5",
              "expression": "Can you confirm",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "020:L2",
              "expression": "Bram Alder",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "communication",
      "request_id": "entity:property-029:002:142:172",
      "sender_id": "entity:property-029:001:172:190",
      "recipient_id": "entity:property-029:001:118:124",
      "purpose": "appointment",
      "status": "no_response_reported",
      "responds_to_record_id": null,
      "deadline_text": null
    }
  ],
  "gaps": [
    {
      "id": "b002:g1",
      "kind": "identity",
      "entity_ids": [
        "entity:property-029:001:172:190",
        "entity:property-029:008:120:145",
        "entity:property-029:004:108:116"
      ],
      "source_ids": [
        "014:L5",
        "019:L5"
      ],
      "description": "Whether Bram Alder is the contractor Orren Vale intends to engage, and whether Bram is currently engaged by Hearthline Boiler Service, remains unconfirmed."
    },
    {
      "id": "b002:g3",
      "kind": "missing_evidence",
      "entity_ids": [
        "entity:property-029:001:172:190",
        "entity:property-029:016:158:166",
        "entity:property-029:002:142:172"
      ],
      "source_ids": [
        "018:L5",
        "019:L5",
        "020:L5"
      ],
      "description": "No confirmed appointment window or landlord-confirmed access arrangement is established. The tenant has not replied to Bram's request to confirm the proposed Saturday visit and leave a key if absent."
    }
  ]
}
```
