# Property ontology T-box semantics v1

The supplied JSON schemas define the classes, field ranges and union alternatives. This
document defines their interpretation. They are static domain vocabulary, not case examples.

## Evidence

An entity is a case-local referent: party, property, asset, request, work order, appointment
or document. Mention IDs anchor source occurrences. Identity links state same/different/
unresolved identity with source evidence. Similar names do not establish identity. IDs
are identifiers, not descriptive facts; unresolved aliases remain distinct until supported.

Records are typed assertions with provenance, not automatically true world state. Issue,
ownership, assignment, authorization, appointment, work, status, obligation, identity,
proposal, access, communication, condition, human intervention and workflow failure each
retain the epistemic and modal distinctions specified in their schema. An agency/system
source does not identify a human author. Source occurrence and field-level spans establish
where an assertion came from; they do not prove its truth or entailment.

Use an open-world interpretation. Missing evidence means unknown, not false. Negated,
conditional, hypothetical, proposed, requested, quoted and actual statements differ.
Approval covers only its stated scope, conditions and amount. Proposal is not permission;
permission is not instruction; instruction is not attendance, completion or satisfaction.
Temporal order and quoted speech do not independently establish causation. Attachments
whose contents are unavailable contribute only their explicitly reported existence/content.

Human intervention has a lifecycle: required/requested/sent/acknowledged/resolved/declined.
Its cause has asserted/inferred/unresolved status and source evidence. A workflow failure
does not imply escalation; a prompt to review does not imply the review was sent or done.
Resolution needs response evidence and a stated effect on blockers. Diagnostics expose
support gaps and extraction errors; they are not additional source facts or automatic policy.

## Result actions

The response describes proposed next actions, never execution receipts. `request_clarification`
asks for information; `request_approval` seeks authority for stated scope; `instruct_provider`
directs work subject to authority and conditions. `propose_booking` proposes an appointment;
`request_work_report` seeks attendance/diagnosis/work evidence; `propose_closure` proposes an
end state with completion evidence and outstanding gaps. `escalate` requests a responsible
human intervention with cause, requested remedy and blockers. `await_response` waits for an
already relevant response; waiting itself does not send a request.

`provide_guidance` gives actionable advice; `assign_provider` assigns responsibility;
`notify` communicates acknowledgement, progress, confirmation, reminder or approval outcome.
`handle_document` requests/sends/registers a document. `change_workflow` changes operational
handling. `resolve_requirement` proposes satisfying/waiving an obligation. `cancel_booking`
cancels a known appointment. `record_evidence` records referenced observations.

Action request/party IDs refer to supplied entities; basis IDs refer to supplied records or
gaps, and dependency IDs sequence proposed actions. Unknown references remain observable
errors, not new entities. An empty basis is representable and reviewable. Source-supported
roles may be clearer than resolved identity; state that distinction in the rationale.
Never manufacture IDs, authority or source facts to satisfy a schema field.

Rationale citations identify evidence used, while uncertainties, assumptions and alternatives
make the justification reviewable. They do not certify correctness. Historical actions are
soft observational targets: reasonable alternatives can differ, and later history can include
details unavailable at prediction time. The vocabulary itself is not a tenancy policy,
legal rule, authority grant or evidence that a particular action should be chosen.
