# Decision ontology v2

Executable authority: `src/property_eval/response.py`. Full cutover to
`property-response-v2`; historical v1 coverage audit remains pinned to its original hash.
The frozen extraction comparison remains unchanged. No decision-model accuracy is claimed.

## What happened, what should happen, and why

`actions` describes proposed choices. `human_interventions` describes sourced observations
of human-review lifecycle. Neither is an execution tool. An escalation proposal is not a
sent escalation; a manual-review instruction is not a human response.

Every proposed action identifies its request, supporting records/gaps and action dependencies.
The response disposition is act, clarify, wait, escalate or conclude. Conclusions cite records.

| Choice | Purpose |
| --- | --- |
| request_clarification | Ask a party to resolve a specific ambiguity. |
| request_approval | Seek permission for a scope and optional proposed cost. |
| instruct_provider | Instruct work, preserving authorization references and conditions. |
| propose_booking / cancel_booking | Propose or cancel an appointment. |
| request_work_report | Seek attendance, diagnosis, repair, test or invoice evidence. |
| propose_closure | Close as resolved, tenant-managed, cancelled, duplicate or no-work-required. |
| escalate | Request a human intervention with cause and blocking effect. |
| await_response | Wait for a specified kind of response from a responsible party. |
| provide_guidance | Give ordered steps and specify requested feedback. |
| assign_provider | Select a provider for a scope. |
| notify | Send confirmation, reminder, progress, approval outcome or acknowledgement. |
| handle_document | Request, send or register a specified document kind. |
| change_workflow | Hold, resume, review completion, change mode or revise description. |
| resolve_requirement | Record satisfaction or waiver of an existing obligation. |
| record_evidence | Record assertions already represented in the evidence packet. |

## Human intervention

An escalation includes recipient (nullable), responsible human role, one or more causes,
requested intervention, detailed request, whether it blocks progress, affected action IDs
and handover. Each cause includes category, explanation, original source expressions with
occurrence selectors, plus referenced assertions/gaps. Cause categories cover identity,
authority, conflicts, missing evidence, workflow failures, explicit review, safety and policy.

An observed intervention separately includes status (required, sent, acknowledged, resolved,
declined), source evidence, causes, requested intervention and response record references.
Its blocking effect is blocked, released, unchanged or unknown. Resolved/declined observations
without response evidence are flagged. A nearby validation error does not prove causal linkage.

## Validation boundary

Pydantic validates representation. `validate_response` returns combined `valid`, plus separate
`structurally_valid` and `evidence_compatible` flags. References, entity kinds, ordering of
dependencies and source expressions are checked deterministically. Authorization/closure
compatibility is reported separately. Missing authorization can therefore be represented and
flagged rather than fabricated. Full policy permission, semantic entailment, condition
satisfaction and completeness are not established by these checks.

Unresolved recipients remain unresolved. Source offsets are resolved through the same auditable
grounding code as extraction; normalized apostrophes do not replace original source text.

## Remaining work

The extraction ontology still needs a first-class human-review observation matching this
contract; the frozen extraction round did not include it. In the meantime the decision input
retains original sources. Do not claim that extracted records alone cover all new action
fields. Typed payer/price ranges, authority rules, notification content support and conditional
workflow semantics still need reference annotations and stronger checks. Extending a vocabulary
is not evidence that a model will select these choices correctly.
