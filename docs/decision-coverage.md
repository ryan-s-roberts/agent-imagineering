# Can the response ontology reproduce recorded choices?

## Result

Not faithfully across the inspected property histories. This independent review compares
the current response contract with recorded agency/system actions, without using extraction
outputs or a decision model. It therefore isolates **representational coverage**.

Reviewed previously exposed cases 003, 012, 020 and 038. The machine-readable annotations
are in `annotations/decision-coverage.json`, pinned to source commit and response.py hash.
These are exploratory development diagnostics, not a held-out benchmark or accuracy estimate.
Round3 evaluation case 041 was not opened for this audit.

## Method

Each annotation identifies original event IDs, a grouped choice family, the closest response
type and whether it fits, only partially fits, or is missing. The prefix cutoff is immediately
before the first listed event. Repeated emails/SMS or duplicate holds can be grouped; the
denominator is these authored choice families, not all event rows or independent decisions.

`type_fit` means the intent has a dedicated representation. It does not mean the required
arguments can be recovered, the prefix warrants it, or the observed choice was sensible.
`partial` means required meaning is lost or the schema imposes an unsupported precondition.
`missing` means a new semantic action is needed. Stuffing an instruction into a question or
an escalation handover does not establish coverage.

Agency/system attribution does not prove a human chose the action. Logs include automated
notifications and workflow effects. Case038 event002 explicitly records AI intake. Case038
event010 is labelled From Tenant but includes both agency and tenant speech; classify spans,
not just envelope sender. Reported earlier actions (012 event012) have uncertain decision times.

## Concrete gaps

| Observed choice | Source examples | Response limitation |
| --- | --- | --- |
| Troubleshooting guidance | 012:005–006 | Clarification has a question, not procedural instructions. |
| Provider assignment | 003:002; 012:013 | Assignment differs from instructing an already selected provider. |
| Confirmation, notification and reminder | 012:014,018–020; 020:013–014 | No informational communication action. |
| Document delivery/registration | 003:020; 020:017–018 | No invoice/report delivery or document registration action. |
| Workflow changes and waivers | 012:025–030 | No review transition, document waiver, mode change or recorded key confirmation. |
| Completion without repair/payment | 038:013 | Closure validator requires positive actual repaired/working work reports. |
| Reschedule plus cancel plus notify | 020:007–012 | Replacement booking partially fits; cancellation and notifications are separate effects. |
| Approval with ownership/cost conditions | 038:004–005 | Approval fields lack typed payer, ownership terms and proposed price ranges. |

The omission of action families is independent of extraction quality. Better entity extraction
cannot make an absent response type expressible.

## Full case012 event accounting

- Input/context or reports: 001,004,008,011,012,016,021,024. Some also contain recording or
  reported agency actions, which are separately annotated. Contractor scheduling/arrival and
  tenant troubleshooting results are environment behavior for an agency decision agent.
- System prompts/requirements, not evidence of an executed action: 002,010,022,023,028.
  In particular, “need confirmation” is not a sent confirmation request.
- Observable outgoing agency communications: 005,006,014,015,018,019,020.
- Workflow/record changes: 003,007,009,013,017,025,026,027,029,030,031.
  Event030 includes an attempted priority change validation response as well as key confirmation.

This accounting intentionally overlaps report and action categories for mixed events. It is
not a simplistic sender-based labeler. The history is insufficient to distinguish every human
choice from automated consequences.

## Independent evaluation layers

1. **Ontology coverage:** hand-encode observed action intent. Unsupported actions count as
   coverage failures, not extraction errors. This audit implements this layer.
2. **Oracle-evidence decisions:** supply reviewed prefix evidence to a decision model; score
   against accepted actions and forbidden constraints. This isolates decision behavior.
3. **Extracted-evidence decisions:** run the same model and scoring with extracted evidence.
   The delta measures extraction-induced decision error. Neither layer 2 nor 3 has run yet.

Historical action matching should be reported separately from justified-choice scoring. Case012
closes after a landlord-confirmation requirement without a visible confirming reply. Case003
records approval after the instruction. Do not leak those later events into prefix evidence or
force the model to reproduce an unjustified choice to earn a correctness score.

## Required next contract revision

Separate **choice representation** from **admissibility checks**. A historically observed
instruction without visible authorization must be representable, and separately flagged as
unsupported. Do not require a model to fabricate an authorization record to describe it.

Add dedicated domain actions for guidance, assignment, notifications, document operations,
workflow transitions and requirement waivers; give completion an explicit reason such as
resolved, tenant-managed, cancelled or duplicate. Couple every action field to its evidence
requirements, including execution actor, recipient, scope, conditions and timing.

Freeze that revised contract before an independent unseen-case evaluation. This audit does
not change the response ontology during the subagent's frozen extraction comparison.

## Human escalation and its cause

User requirement: human intervention is a first-class decision, with its cause preserved.
The existing `escalate` type has recipient, coarse reason and handover text; that is insufficient
for deterministic cause-sensitive evaluation. A generic handover must not receive full credit.

The next contract must represent:

- Trigger: sourced event/field spans and the unmet obligation, conflict, authority boundary,
  validation failure, or explicit manual-review instruction that caused intervention.
- Requested intervention: the specific human decision or action, such as resolve identity,
  approve expenditure, adjudicate conflicting evidence, or handle a blocked workflow transition.
- Human responsibility: role and known recipient, with unresolved identity retained explicitly.
- Blocking effect: which proposed action cannot proceed and why; escalation may also be advisory.
- Handover evidence: relevant assertions, attempted actions and their observed failure responses.
- Lifecycle: review required, escalation requested/sent, acknowledged, resolved or declined.
  Record the human response and its effect on the blocking condition separately.

Extract an observed escalation only when the source supports it. A detected uncertainty may
justify a future escalation proposal; it does not establish that a historical escalation happened.
Do not invent escalation thresholds, deadlines or authority policies absent task instructions.

Corpus examples: case038:008 explicitly asks for manual review after a message arrives and also
reports a priority validation failure. Those are two observations; the log does not establish
that the failure caused the review instruction. Case012:030 confirms returned keys and reports
a rejected priority reduction; it does not show an escalation was sent. Case003:006 asks for
response review and possible return to auto mode, without identifying a specific human recipient.

Evaluate escalation detection, cause classification, evidence support, recipient role,
requested intervention, blocking effect and lifecycle separately. Include both missed required
human interventions and unnecessary escalations in the reviewed decision references.
