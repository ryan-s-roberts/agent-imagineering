# Proposed answer

Case 008; checkpoint `008-at-024`; prefix ends at event `24`. Run `challenges-property-v1-run`, artifact SHA-256 `2501c378f571add7db016efb8bc1d5c695a52bb10ee73c993aec7c6b8020cfa2`.

[Case evidence bundle](evidence/README.md).

## Execution status

This system has no external execution environment, so it did not carry out any proposed actions. Actions and outcomes recorded in the case history are evidence; the actions below are recommendations. The case evidence bundle contains the supplied history and extracted support.

Disposition: **act**.

## Proposed actions

### Notify

```json
{
  "id": "a1",
  "request_id": "entity:property-008:014:156:194",
  "basis_record_ids": [
    "b002:r2",
    "b003:r3"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "notify",
  "recipient_id": "entity:property-008:014:105:115",
  "purpose": "progress",
  "message": "Please take account of the latest report of continued dripping and an apparently larger ceiling bulge beside the wet fitting in Flat 2. The stated attendance window is 12:30–13:15; please update the property manager on attendance and the on-site assessment. This is an update for the already arranged assessment, not authorization to expand work.",
  "about_record_ids": [
    "b002:r2",
    "b003:r3"
  ]
}
```

### Provide guidance

```json
{
  "id": "a2",
  "request_id": "entity:property-008:014:156:194",
  "basis_record_ids": [
    "b002:r10",
    "b002:r2",
    "b003:r4",
    "b003:r5"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "provide_guidance",
  "recipient_id": "entity:property-008:002:107:113",
  "steps": [
    "Continue to keep the bedroom clear and keep people away from the wet fitting and ceiling; do not touch them or try an unfamiliar breaker.",
    "If sparks, smoke, falling material, or immediate danger occurs, contact emergency services as previously advised and follow their direction."
  ],
  "requested_feedback": null
}
```

### Request work report

```json
{
  "id": "a3",
  "request_id": "entity:property-008:014:156:194",
  "basis_record_ids": [
    "b002:r2",
    "b002:r10"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "request_work_report",
  "provider_id": "entity:property-008:014:105:115",
  "requested_fields": [
    "attendance",
    "diagnosis",
    "test_result"
  ]
}
```

### Await response

```json
{
  "id": "a4",
  "request_id": "entity:property-008:014:156:194",
  "basis_record_ids": [
    "b002:r2",
    "b002:r4"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "await_response",
  "responsible_party_id": "entity:property-008:014:105:115",
  "awaited": "appointment"
}
```

### Handle document

```json
{
  "id": "a5",
  "request_id": "entity:property-008:001:248:296",
  "basis_record_ids": [
    "b002:r7",
    "b003:r9"
  ],
  "basis_gap_ids": [],
  "depends_on_action_ids": [],
  "type": "handle_document",
  "operation": "request",
  "document_id": null,
  "recipient_id": "entity:property-008:006:106:114",
  "document_kind": "other"
}
```

### Escalate

```json
{
  "id": "a6",
  "request_id": "entity:property-008:001:248:296",
  "basis_record_ids": [
    "b002:r7",
    "b003:r6",
    "b003:r7",
    "b003:r9"
  ],
  "basis_gap_ids": [
    "b003:g1"
  ],
  "depends_on_action_ids": [
    "a5"
  ],
  "type": "escalate",
  "recipient_id": "entity:property-008:022:539:554",
  "responsible_role": "supervisor",
  "causes": [
    {
      "category": "authority_required",
      "explanation": "A decision is needed on whether the full agreement permits Flat 3 entry despite Yara's continuing refusal; the record says Niko has not authorized entry and no entry authority was confirmed.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "024:L5",
          "expression": "Yara continues to withhold consent to Flat 3 entry until she returns",
          "occurrence": 1
        },
        {
          "source_id": "024:L5",
          "expression": "Niko has not authorized entry",
          "occurrence": 1
        },
        {
          "source_id": "022:L5",
          "expression": "No entry authority was confirmed.",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b002:r7",
        "b003:r6",
        "b003:r7",
        "b003:r9"
      ],
      "gap_ids": [
        "b003:g1"
      ]
    },
    {
      "category": "missing_evidence",
      "explanation": "The complete agreement had not been checked; the recorded route is to obtain it and seek an agency-director decision.",
      "causal_status": "asserted",
      "evidence": [
        {
          "source_id": "022:L5",
          "expression": "the complete tenancy wording had not been checked",
          "occurrence": 1
        },
        {
          "source_id": "022:L5",
          "expression": "The agency escalation route was to obtain the full agreement and a decision from the agency director;",
          "occurrence": 1
        }
      ],
      "record_ids": [
        "b003:r9"
      ],
      "gap_ids": [
        "b003:g1"
      ]
    }
  ],
  "requested_intervention": "review_case",
  "intervention_detail": "Review the complete agreement when available and decide whether, and within what limits, Flat 3 entry may be authorized despite the tenant's refusal. This request is not authority to enter. Source-flat access remains unresolved; the separately arranged Flat 2 electrical attendance should proceed only within its existing scope and access arrangements.",
  "blocking": false,
  "blocked_action_ids": [],
  "handover": "The latest report describes continued dripping and an apparently larger ceiling bulge in Flat 2. The plumber's Flat 2/common-riser visit did not identify the source or a usable isolation point. No Flat 3 entry is proposed pending an explicit authority decision."
}
```

## Action dependencies

- `a6` depends on `a5`.

## Human interventions

```json
[]
```

Conclusion records: []

## Evidence and reasoning

The current record supports continuing the already arranged electrical response in Flat 2 while keeping the unresolved Flat 3 access issue separate. Bevin reports continued dripping and an apparently larger ceiling bulge, can meet the electrician, and reports no sparks, smoke, or fallen material. The electrical attendance window is stated to remain 12:30–13:15, but the supplied evidence does not establish that the electrician has attended or assessed the fitting. The plumber's Flat 2 and common-riser attendance did not identify the source or a usable isolation point. Yara continues to withhold consent to Flat 3 entry, Niko has not authorized entry, and no entry authority was confirmed. Accordingly, the proposed actions request an update and work report, provide safety guidance, seek the full agreement and a responsible review, and do not authorize Flat 3 entry or expanded work.

## Assumptions

- The latest Flat 2 reports concern the same ongoing incident and wet fitting as the stated electrical attendance, based on their continuity and context.

## Uncertainties

- The condition and apparent enlargement are reported observations, not independently verified findings.
- The supplied evidence does not establish whether the electrician has attended or completed an assessment, or whether the full agreement has been obtained and reviewed by the agency director.
- The source of the leak and any safe isolation point remain unidentified.

## Alternatives considered

- No emergency-services contact is proposed because the latest report says Bevin has not seen sparks or smoke and no material has fallen; the prior safety instructions identify those signs or immediate danger as reasons to contact emergency services.
- No entry into Flat 3, or provider instruction to enter, is proposed because consent remains withheld and entry authority is unconfirmed.
- No completed electrical assessment or resolved leak is assumed; requesting a work report preserves that distinction.

## Cited prefix evidence

```json
{
  "source_id": "023:L5",
  "expression": "The drip continues and the ceiling bulge appears larger.",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [123, 301).

> The drip continues and the ceiling bulge appears larger. I am still outside the bedroom and can meet the electrician. I have not seen sparks or smoke, and no material has fallen.

```json
{
  "source_id": "023:L5",
  "expression": "I am still outside the bedroom and can meet the electrician.",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [123, 301).

> The drip continues and the ceiling bulge appears larger. I am still outside the bedroom and can meet the electrician. I have not seen sparks or smoke, and no material has fallen.

```json
{
  "source_id": "023:L5",
  "expression": "I have not seen sparks or smoke, and no material has fallen.",
  "occurrence": 1
}
```
Event `023`, source `023:L5`, event character range [123, 301).

> The drip continues and the ceiling bulge appears larger. I am still outside the bedroom and can meet the electrician. I have not seen sparks or smoke, and no material has fallen.

```json
{
  "source_id": "024:L5",
  "expression": "Vellum Electrical is due within its stated window.",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [146, 752).

> Current record: active dripping and a reportedly enlarging ceiling bulge in Flat 2 beside a wet light fitting; the room is being kept clear, but electrical safety has not been established. Vellum Electrical is due within its stated window. Brindle Flow Plumbing and Selka Venn attended Flat 2 and the common riser, with no source or confirmed isolation point found. Yara continues to withhold consent to Flat 3 entry until she returns; Niko has not authorized entry, and the agency has not verified an applicable emergency-entry authority. The source-flat access and any source isolation remain unresolved.

```json
{
  "source_id": "016:L5",
  "expression": "Daro had access to Flat 2 and the common riser. He saw water at the bedroom ceiling but could not locate the source.",
  "occurrence": 1
}
```
Event `016`, source `016:L5`, event character range [141, 412).

> Daro and Selka had met as arranged. Daro had access to Flat 2 and the common riser. He saw water at the bedroom ceiling but could not locate the source. The riser labels did not identify a confirmed Flat 3 branch; no valve had been operated. Flat 3 remained inaccessible.

```json
{
  "source_id": "024:L5",
  "expression": "The source-flat access and any source isolation remain unresolved.",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [146, 752).

> Current record: active dripping and a reportedly enlarging ceiling bulge in Flat 2 beside a wet light fitting; the room is being kept clear, but electrical safety has not been established. Vellum Electrical is due within its stated window. Brindle Flow Plumbing and Selka Venn attended Flat 2 and the common riser, with no source or confirmed isolation point found. Yara continues to withhold consent to Flat 3 entry until she returns; Niko has not authorized entry, and the agency has not verified an applicable emergency-entry authority. The source-flat access and any source isolation remain unresolved.

```json
{
  "source_id": "024:L5",
  "expression": "Yara continues to withhold consent to Flat 3 entry until she returns",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [146, 752).

> Current record: active dripping and a reportedly enlarging ceiling bulge in Flat 2 beside a wet light fitting; the room is being kept clear, but electrical safety has not been established. Vellum Electrical is due within its stated window. Brindle Flow Plumbing and Selka Venn attended Flat 2 and the common riser, with no source or confirmed isolation point found. Yara continues to withhold consent to Flat 3 entry until she returns; Niko has not authorized entry, and the agency has not verified an applicable emergency-entry authority. The source-flat access and any source isolation remain unresolved.

```json
{
  "source_id": "024:L5",
  "expression": "Niko has not authorized entry",
  "occurrence": 1
}
```
Event `024`, source `024:L5`, event character range [146, 752).

> Current record: active dripping and a reportedly enlarging ceiling bulge in Flat 2 beside a wet light fitting; the room is being kept clear, but electrical safety has not been established. Vellum Electrical is due within its stated window. Brindle Flow Plumbing and Selka Venn attended Flat 2 and the common riser, with no source or confirmed isolation point found. Yara continues to withhold consent to Flat 3 entry until she returns; Niko has not authorized entry, and the agency has not verified an applicable emergency-entry authority. The source-flat access and any source isolation remain unresolved.

```json
{
  "source_id": "022:L5",
  "expression": "No entry authority was confirmed.",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [144, 720).

> Arlen asked who could authorize emergency access after the occupant refused consent. Devra reviewed the available agency record and found no documented delegated authority for staff to override that refusal; the complete tenancy wording had not been checked. Devra recorded that Niko had not authorized entry. The agency escalation route was to obtain the full agreement and a decision from the agency director; if there were an immediate danger to life or property, contact emergency services and follow the responding authority's direction. No entry authority was confirmed.

```json
{
  "source_id": "022:L5",
  "expression": "The agency escalation route was to obtain the full agreement and a decision from the agency director;",
  "occurrence": 1
}
```
Event `022`, source `022:L5`, event character range [144, 720).

> Arlen asked who could authorize emergency access after the occupant refused consent. Devra reviewed the available agency record and found no documented delegated authority for staff to override that refusal; the complete tenancy wording had not been checked. Devra recorded that Niko had not authorized entry. The agency escalation route was to obtain the full agreement and a decision from the agency director; if there were an immediate danger to life or property, contact emergency services and follow the responding authority's direction. No entry authority was confirmed.

## Action evidence records and gaps

```json
{
  "records": [
    {
      "id": "b002:r2",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:001:73:84",
        "origin": "attributed_report",
        "modality": "planned",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "appointment_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "attendance window of 12:30–13:15",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "urgent qualified electrical attendance",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provider_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Runa confirmed electrical qualifications",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Runa confirmed the attendance window remained 12:30–13:15",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "12:30–13:15",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Runa confirmed electrical qualifications and offered an attendance window",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "offered an attendance window of 12:30–13:15",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "attendance window remained 12:30–13:15",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Arlen Quist",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "appointment",
      "appointment_id": "entity:property-008:014:290:322",
      "request_id": "entity:property-008:014:156:194",
      "provider_id": "entity:property-008:014:105:115",
      "tenant_id": null,
      "status": "confirmed",
      "time_text": "12:30–13:15",
      "supersedes_record_id": null
    },
    {
      "id": "b002:r4",
      "provenance": {
        "source_ids": [
          "014:L2",
          "014:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:001:73:84",
        "origin": "attributed_report",
        "modality": "conditional",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "attendance window of 12:30–13:15, subject to the tenant providing access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "the tenant providing access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "subject to the tenant providing access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "subject to the tenant providing access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "subject to the tenant providing access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "Runa confirmed electrical qualifications and offered an attendance window",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "subject to the tenant providing access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "014:L5",
              "expression": "subject to the tenant providing access",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "014:L2",
              "expression": "Arlen Quist",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-008:014:156:194",
      "party_id": "entity:property-008:002:107:113",
      "constraint": "entry_permission",
      "status": "required",
      "time_text": null,
      "description": "Electrical attendance is subject to the tenant providing access."
    },
    {
      "id": "b002:r7",
      "provenance": {
        "source_ids": [
          "019:L2",
          "019:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:006:106:114",
        "origin": "attributed_report",
        "modality": "unknown",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "He was uncertain whether the wording permitted entry after Yara's refusal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "grantor_id",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Niko",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "scope",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "whether the wording permitted entry after Yara's refusal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "decision",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "He was uncertain whether the wording permitted entry after Yara's refusal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "conditions",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "He did not authorize forced or unaccompanied entry.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "Niko had found a tenancy clause for access by arrangement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "He was uncertain whether the wording permitted entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "019:L5",
              "expression": "He did not authorize forced or unaccompanied entry.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "019:L2",
              "expression": "Niko Pell",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "authorization",
      "request_id": "entity:property-008:001:248:296",
      "grantor_id": "entity:property-008:006:106:114",
      "grantee_id": null,
      "scope": [
        "access"
      ],
      "decision": "uncertain",
      "amount_minor": null,
      "currency": null,
      "conditions": [
        "Niko did not authorize forced or unaccompanied entry."
      ]
    },
    {
      "id": "b002:r10",
      "provenance": {
        "source_ids": [
          "018:L2",
          "018:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:001:73:84",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "the fitting was not considered safe based on the wall switch position",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "the fitting was not considered safe based on the wall switch position",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "not considered safe based on the wall switch position",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "not considered safe based on the wall switch position",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "the fitting was not considered safe based on the wall switch position",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Runa confirmed ... the fitting was not considered safe based on the wall switch position.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "Runa confirmed ... the fitting was not considered safe based on the wall switch position.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "the fitting was not considered safe based on the wall switch position",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "018:L5",
              "expression": "the fitting was not considered safe based on the wall switch position",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "018:L2",
              "expression": "Arlen Quist",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-008:002:161:190",
      "location_text": null,
      "observation_kind": "physical_condition",
      "attribute": "electrical safety assessment",
      "value": {
        "kind": "text",
        "value": "not considered safe based on the wall switch position"
      },
      "quoted_expression": "the fitting was not considered safe based on the wall switch position",
      "epistemic_status": "asserted",
      "observed_at_text": null
    },
    {
      "id": "b003:r3",
      "provenance": {
        "source_ids": [
          "023:L2",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:002:107:113",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Bevin Orlo (Tenant, Flat 2)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the ceiling bulge appears larger",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the ceiling bulge appears larger",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the ceiling bulge appears larger",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "ceiling bulge",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the ceiling bulge appears larger",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the ceiling bulge appears larger",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the ceiling bulge appears larger",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "the ceiling bulge appears larger",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "appears larger",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-008:023:150:163",
      "location_text": null,
      "observation_kind": "physical_condition",
      "attribute": "apparent size",
      "value": {
        "kind": "text",
        "value": "larger"
      },
      "quoted_expression": "the ceiling bulge appears larger",
      "epistemic_status": "appears",
      "observed_at_text": null
    },
    {
      "id": "b003:r4",
      "provenance": {
        "source_ids": [
          "023:L2",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:002:107:113",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Bevin Orlo (Tenant, Flat 2)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "I have not seen sparks or smoke",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-008:001:189:195",
      "location_text": null,
      "observation_kind": "presence",
      "attribute": "sparks or smoke",
      "value": {
        "kind": "boolean",
        "value": false
      },
      "quoted_expression": "I have not seen sparks or smoke",
      "epistemic_status": "not_verified",
      "observed_at_text": null
    },
    {
      "id": "b003:r5",
      "provenance": {
        "source_ids": [
          "023:L2",
          "023:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:002:107:113",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "023:L2",
              "expression": "Bevin Orlo (Tenant, Flat 2)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "subject_id",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "observation_kind",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "attribute",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "value",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "quoted_expression",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "epistemic_status",
          "spans": [
            {
              "source_id": "023:L5",
              "expression": "no material has fallen",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "observation",
      "subject_id": "entity:property-008:001:189:195",
      "location_text": null,
      "observation_kind": "presence",
      "attribute": "fallen material",
      "value": {
        "kind": "boolean",
        "value": false
      },
      "quoted_expression": "no material has fallen",
      "epistemic_status": "asserted",
      "observed_at_text": null
    },
    {
      "id": "b003:r6",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:001:73:84",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Arlen Quist (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Yara continues to withhold consent to Flat 3 entry until she returns",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Yara continues to withhold consent to Flat 3 entry until she returns",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Yara continues to withhold consent to Flat 3 entry until she returns",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Flat 3 entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Yara continues to withhold consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "withhold consent to Flat 3 entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "continues to withhold consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "time_text",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "until she returns",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Yara continues to withhold consent to Flat 3 entry until she returns",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-008:001:248:296",
      "party_id": "entity:property-008:001:34:45",
      "constraint": "entry_permission",
      "status": "unavailable",
      "time_text": "until she returns",
      "description": "Yara continues to withhold consent to entry to Flat 3 until she returns."
    },
    {
      "id": "b003:r7",
      "provenance": {
        "source_ids": [
          "024:L2",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:001:73:84",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "negative"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "024:L2",
              "expression": "Arlen Quist (Property Manager, Northbridge Lettings)",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Niko has not authorized entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Niko has not authorized entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Niko has not authorized entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Niko has not authorized entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "party_id",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Niko",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "constraint",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "has not authorized entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "has not authorized entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "description",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Niko has not authorized entry",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "access_constraint",
      "request_id": "entity:property-008:001:248:296",
      "party_id": "entity:property-008:006:106:114",
      "constraint": "entry_permission",
      "status": "unavailable",
      "time_text": null,
      "description": "Niko has not authorized entry."
    },
    {
      "id": "b003:r9",
      "provenance": {
        "source_ids": [
          "022:L3",
          "022:L5",
          "024:L5"
        ],
        "asserted_by_entity_id": "entity:property-008:001:73:84",
        "origin": "attributed_report",
        "modality": "actual",
        "polarity": "positive"
      },
      "field_evidence": [
        {
          "field": "provenance.asserted_by_entity_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Arlen asked who could authorize emergency access after the occupant refused consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.origin",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Devra reviewed the available agency record and found no documented delegated authority for staff to override that refusal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.modality",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "No entry authority was confirmed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "provenance.polarity",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "No entry authority was confirmed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "request_id",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "emergency access after the occupant refused consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "status",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Devra reviewed the available agency record and found no documented delegated authority for staff to override that refusal",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_role",
          "spans": [
            {
              "source_id": "022:L3",
              "expression": "Duty Manager",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "responsible_party_id",
          "spans": [
            {
              "source_id": "022:L3",
              "expression": "Devra Senn",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "requested_intervention",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Arlen asked who could authorize emergency access after the occupant refused consent",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "intervention_detail",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Devra reviewed the available agency record and found no documented delegated authority for staff to override that refusal; the complete tenancy wording had not been checked.",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "causes",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "who could authorize emergency access after the occupant refused consent",
              "occurrence": 1
            },
            {
              "source_id": "022:L5",
              "expression": "the complete tenancy wording had not been checked",
              "occurrence": 1
            },
            {
              "source_id": "022:L5",
              "expression": "obtain the full agreement",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "blocking_context",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "No entry authority was confirmed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "blocked_record_ids",
          "spans": [
            {
              "source_id": "024:L5",
              "expression": "Yara continues to withhold consent to Flat 3 entry until she returns",
              "occurrence": 1
            },
            {
              "source_id": "024:L5",
              "expression": "Niko has not authorized entry",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "blocking_effect",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "No entry authority was confirmed",
              "occurrence": 1
            }
          ]
        },
        {
          "field": "response_record_ids",
          "spans": [
            {
              "source_id": "022:L5",
              "expression": "Devra reviewed the available agency record and found no documented delegated authority",
              "occurrence": 1
            }
          ]
        }
      ],
      "type": "human_intervention",
      "request_id": "entity:property-008:001:248:296",
      "status": "resolved",
      "responsible_role": "supervisor",
      "responsible_party_id": "entity:property-008:022:107:119",
      "requested_intervention": "review_case",
      "intervention_detail": "Review whether emergency access could be authorized after the occupant refused consent. The available agency record showed no documented delegated authority for staff to override the refusal; complete tenancy wording had not been checked. No entry authority was confirmed. The stated next route was to obtain the full agreement and a decision from the agency director; for immediate danger, contact emergency services and follow the responding authority's direction.",
      "causes": [
        {
          "category": "authority_required",
          "explanation": "The review was sought to identify who could authorize emergency access after the occupant refused consent.",
          "causal_status": "asserted",
          "evidence": [
            {
              "source_id": "022:L5",
              "expression": "who could authorize emergency access after the occupant refused consent",
              "occurrence": 1
            }
          ],
          "record_ids": []
        },
        {
          "category": "missing_evidence",
          "explanation": "The complete tenancy wording had not been checked, and the stated escalation route included obtaining the full agreement.",
          "causal_status": "asserted",
          "evidence": [
            {
              "source_id": "022:L5",
              "expression": "the complete tenancy wording had not been checked",
              "occurrence": 1
            },
            {
              "source_id": "022:L5",
              "expression": "obtain the full agreement",
              "occurrence": 1
            }
          ],
          "record_ids": []
        }
      ],
      "blocking_context": "No entry authority was confirmed; Yara continued to withhold consent and Niko had not authorized entry.",
      "blocked_record_ids": [
        "b003:r6",
        "b003:r7"
      ],
      "blocking_effect": "blocked",
      "response_record_ids": [
        "b003:r8"
      ],
      "previous_intervention_record_id": null
    }
  ],
  "gaps": [
    {
      "id": "b003:g1",
      "kind": "authorization",
      "entity_ids": [
        "entity:property-008:001:34:45",
        "entity:property-008:006:106:114",
        "entity:property-008:022:107:119",
        "entity:property-008:022:539:554"
      ],
      "source_ids": [
        "022:L5",
        "024:L5"
      ],
      "description": "Whether emergency access to Flat 3 can be authorized despite Yara's refusal remains unresolved: the complete tenancy wording had not been checked, no delegated authority for staff was documented, Niko had not authorized entry, and no entry authority was confirmed. The stated next step was to obtain the full agreement and a decision from the agency director."
    }
  ]
}
```
