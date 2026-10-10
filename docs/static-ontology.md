# Static property evidence ontology

Executable authority: `src/property_eval/models.py`; version `property-evidence-v4`.
The implementing assistant authors the vocabulary. Runtime extraction instantiates it.

## Entities

Person, organization, unresolved party, property, asset, maintenance request, work order,
appointment, quote, invoice and document. Tenant/landlord/agent/contractor are contextual
roles, not person subclasses. Unknown initials can denote an unresolved party. A proposed
replacement asset is distinct from the existing asset; being mentioned does not imply existence.

## Assertion types

| Type | Main arguments and semantics |
| --- | --- |
| role | Party has a contextual role in a property/request/work order. |
| issue | Request concerns an asset/property; preserves description and troubleshooting report. |
| ownership | Party owns an asset, subject to recorded conditions. |
| assignment | Provider assigned to a request. Receiving an email is insufficient. |
| authorization | Grantor/grantee, request, scope, decision, explicit amount/currency and conditions. |
| appointment | Booking identity, parties, status, time expression and optional superseded assertion. |
| work_report | Request/asset, documentary source if present, reported outcome and description. |
| request_status | Recorded workflow status plus literal source label. |
| obligation | Requested/pending/satisfied/waived/uncertain requirement and responsible party. |
| identity | Explicit same/different/unresolved relation between entity instances. |
| work_proposal | Proposed activity, provider, asset, amount/currency, validity and conditions. |
| access_constraint | Availability/keyholder/notice/entry-permission restrictions. |
| communication | Requested/answered/reported-no-response, participants, reply link and deadline. |
| condition | Requirement linked to the assertion it constrains, with satisfied/contradicted/unknown state. |
| human_intervention | Observed human-review requirement/lifecycle, cause status/evidence, responsible party/role and blocker effects. |
| workflow_failure | Attempted operation and recorded failure; does not imply a human escalation. |

Each assertion carries source-unit IDs, optional attributed speaker, origin (system record,
attributed report, unresolved), modality (actual/planned/requested/conditional/unknown), and
polarity. Actual means the assertion concerns an actual occurrence; it does not independently
verify an attributed report. Recorder and reported speaker are not necessarily the same party.

Domain/range checks constrain party, request, asset, property, appointment and document fields.
Gaps retain identity, authorization, timing, missing-evidence, conflict and unclassified issues.
These categories express model-detected uncertainty; their completeness is not guaranteed.

## Evidence-state semantics

Open world: absence of a record does not imply a negative fact. Retain conflicting statements
and historical statuses. Closure does not entail repair success, landlord consent or returned
keys. Attendance permission does not entail replacement permission. Proposed actions do not
become completed events. Preserve temporal expressions without fabricating normalized dates.

Source lines have stable IDs within a prefix plus half-open Unicode character offsets into
the event text. Three stages separate mention detection, explicit identity linking and typed
assertion extraction. Every populated assertion field has source expressions and occurrence
selectors. Code resolves offsets; apostrophe-only alignment is explicit and retains original
text. Semantic entailment is reviewed, not mechanically proved. See the frozen
[annotation guide](annotation-guide-v3.md) for identity stability and normalization rules.
The v4 [human-intervention extension](human-intervention-v4.md) defines the new lifecycle and causal boundaries.

`decision_packet` emits only structurally valid extractions, with prefix hash, entities, typed
records, gaps, type index and original sources. It deliberately retains evidence rather than
manufacturing one authoritative CRM state. The downstream decision agent must receive those
qualifiers and provenance, not just a flattened entity table.

See [implementation review](implementation-review.md) for missing coverage and evaluation work.
