# Model mention coverage pass: selected development check

Completed seven prefixes in **169.7seconds**, with all seven independent pipelines
observed outstanding concurrently (configured cap24). Forty-two calls cost
**$0.131641235**. The new stage is a model review of the initial mention inventory
against every prefix source unit, before entity linking. It returns the complete
corrected inventory. The host does not invent entities or repair omitted roles.

Initial extraction again found the landlord in six of seven prefixes and omitted
it in026. The coverage model added the literal role in026; final inventories and
linked entities contain the landlord in **7/7**. No decision blocks on missing
personal names or imaginary CRM IDs. Case026 now addresses a clarification directly
to the extracted landlord instead of escalating for a missing recipient.

| Case | Saved actions |
|---|---|
| 011 | Request inspection/quote approval |
| 016 | Request inspection approval |
| 025 | Request approval |
| 026 | Clarify authorization with landlord |
| 028 | Clarify authorization with landlord |
| 035 | Request approval; two clarifications |
| 038 | Clarify; request replacement approval |

This fixes the observed role recall omission through the model. It does not establish
generalized recall or decision quality: these are seven selected, exposed development
prefixes, fresh stochastic calls across stages, and a single pass. The decision/schema
teaching remains as in rolev1; the extraction pipeline adds the generic coverage review.
No target events enter extraction or decision inputs. Independent examples concern
caretakers, occupiers and suppliers rather than historical case answers.

Six decisions pass reference checks.035 retains an ungrounded source expression and
a cross-request evidence check. Four missing field-evidence diagnostics remain across
011/026/035. All126 **judge** citations resolve exactly; this does not certify the
separate decision model's citations or semantic reasoning.

The advisory single-event judge returned six partial correspondences and one
unassessable; three supported and four partly supported predictions. **Do not treat
these as choice-quality scores:** independent review identified that the historical
annotation unit often omits multiple actions in the same agency decision episode.
Episode-level target annotation and action-set alignment must precede further prompt
optimization. This role experiment demonstrates role recall/addressability only.

Frozen design/code: `runs/role-identity-v2/experiment.json` and
`implementation-snapshot.json`. Saved inspection: `role-review.json`.
Canonical artifact and HTML are assembled separately from these completed calls.
No further decision prompt tuning or model calls were launched after this round.
