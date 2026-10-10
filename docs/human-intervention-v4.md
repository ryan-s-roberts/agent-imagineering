# Human intervention as extracted evidence — v4

`human_intervention` is a source-backed record of a human-review requirement or its
observed lifecycle. `escalate` in the response ontology is a proposed action. The former
can support the latter; neither is a receipt for an action that has not occurred.

## Contract

| Field | Meaning |
| --- | --- |
| status | required, requested, sent, acknowledged, resolved, declined |
| responsible_role / responsible_party_id | Explicit role and identified party; unknown/null otherwise |
| requested_intervention / intervention_detail | Typed intervention plus original operational detail |
| causes | Source-linked category, explanation and asserted/inferred/unresolved causal status |
| blocked_record_ids / blocking_context | Existing obligations/proposals or literal workflow context affected |
| blocking_effect | blocked, released, unchanged, unknown; never inferred solely from resolution |
| response_record_ids | Answered communication records supporting human receipt/response |
| previous_intervention_record_id | Explicitly linked earlier lifecycle observation |

Every populated field requires evidence. Each cause additionally retains its own spans.
`asserted` means the source connects the reason to the intervention; `inferred` means the
extractor proposes the relationship; `unresolved` means it is not established. Being on the
same CRM update is not an asserted causal connection. A review directive can itself be an
`explicit_human_review` trigger while the deeper reason remains unknown.

`workflow_failure` records attempted operation, exact error text and rejected/failed/unknown
outcome. It does not imply anyone was contacted. `Agency / system` identifies a recorder,
not proof of a human action or a specific responsible person.

## Lifecycle rules

- A system instruction to review manually is **required**.
- A drafted or expressly requested human review without transmission evidence is **requested**.
- An observed transmission is **sent**. A recipient acknowledging receipt is **acknowledged**.
- A substantive human disposition is **resolved** or **declined**, with an answered
  communication record. A resolution does not itself establish that blocked work was released.
- Preserve transitions separately, with explicit continuity links when available.

Code checks record references, same-request boundaries, source locations and field coverage.
Acknowledged/resolved/declined requires response evidence; sent and later states require
actual modality; released requires resolved. These compatibility checks cannot prove that
a cited sentence entails the predicted lifecycle or causal link. Reviewed references are
still needed for that semantic boundary.

## Independently authored annotation examples

These examples are explanatory fixtures, not copied case histories and not added to prompts.

1. `Supervisor review required because two inspection findings disagree.` → required;
   supervisor; adjudicate_evidence; conflicting_evidence/asserted; person unknown.
2. `Draft review request for supervisor. Not yet dispatched.` → requested, not sent;
   explicit_human_review/asserted. No acknowledgement or release.
3. `At 09:10 the review request was emailed to Mina. At 09:15 Mina acknowledged receipt.`
   → separate sent/acknowledged records, second linked to first and to an answered communication.
4. `Mina approved the exception. The blocked booking may now proceed.` → resolved with
   response evidence and explicit released effect on the booking; neither follows from an
   acknowledgement alone.
5. `Queue priority update rejected. Resident's address verified.` → workflow_failure;
   no human-intervention record is warranted solely by the error or adjacency.
6. `Please review the reply manually. Priority update rejected.` → required review plus
   workflow_failure; the failure is not an asserted cause without an explicit connection.

## Corpus review boundaries

- 038 event 008 explicitly requires manual review. Its adjacent priority validation
  failure is separately observed; it does not establish why review is required.
- 003 event 006 asks someone to decide whether a provider response is needed, with a
  conditional return to automatic mode. It does not establish a sent response or escalation.
- 012 event 030 confirms key return and records a priority validation failure. That event
  supplies no observed human-review request or escalation.

These are development diagnostics on already inspected cases. They are not holdout evidence.
Round 3 artifacts and frozen code are preserved under `experiments/snapshots/round3/`;
the v4 cutover is not a rerun or repair of the prior comparison.
