# Development evidence → action review

Scope: development cases 001–040 only. This is exploratory rubric design, not a
new benchmark score or causal experiment. Log order supports operational dependency
inferences; it cannot establish that an action caused a later real-world outcome.
Cases below illustrate general rules and counterexamples, not templates for prompts.

| Development evidence | Observed agency act | Defensible inference | Limit / counterexample |
|---|---|---|---|
| 001, event 003: landlord approval is a prerequisite | Following agency approval request | An unmet authority gate supports requesting approval before dependent work | Does not justify issuing an unconditional work instruction |
| 001, event 038: waiting for provider confirmation | 039 requests an update; 040 holds the task | A known unresolved confirmation supports chasing and representing the waiting state | A hold is not confirmation, completion or two independent substantive effects |
| 008, cutoff 040: an existing provider wait | Subsequent hold mutation | Continuing a waiting state can correspond historically | Repeating the same state does not by itself demonstrate progress; do not reward action count |
| 020, event 013: rescheduled visit | Subsequent tenant reminders | An established appointment supports notification | The prior 14:00 time does not by itself establish the later 12:00–17:00 window; score timing specificity separately |
| 028, prefix before event 013: landlord says completion occurred | Completion note and status update | A reported completion can support recording the report and a workflow transition | Landlord report is not independent technical verification; any verification gate must be sourced |
| 035, cutoff 009: landlord will obtain parts and arrange fitting | Further landlord-wait hold | Responsibility and outstanding work support waiting on the appropriate role | No personal identity lookup is required merely because role references are used; repeatedly waiting may not advance work |
| 012, cutoff 023: work results still missing | Event 024 first presents an invoice work report | The missing result supports chasing or checking for the report | It does not establish possession of the invoice. The initial model annotation accepting `record_evidence` here is insufficiently justified |

Source of truth: `HackatonPublicCases/Property Management/<case>/history.md`.
The annotation artifacts retain exact event-relative quote positions and original
model responses under `runs/agent-only-late-v2/reviews/`. The reference to Case 012
is a discovered annotation limitation, not a per-case prompt patch.

## General consequences for the rubric

1. **Availability precedes use.** A needed input, an available input and a verified
   input are distinct states. Evaluate them separately for all action types.
2. **Support must cover the proposed effect.** Evidence for notification, requesting
   approval or chasing does not transfer automatically to work, payment or closure.
3. **State maintenance differs from progress.** Preserve historical holds in correspondence
   assessments, but deduplicate them when measuring satisfied obligations.
4. **Actor and epistemic status survive normalization.** A role can identify a party;
   a reported fact remains reported. Neither issue warrants invented CRM state.
5. **Detail support is granular.** The right broad action can still invent a time,
   cost, recipient or condition. Partial support must identify the unsupported slots.
6. **Missing observation can block evaluation.** If the logs omit receipt of evidence
   needed by an action, do not assume it existed simply because the later action occurred.

## Anti-overfitting controls

The general principles above belong in a versioned rubric; case numbers, dates,
names, quotes and observed action sequences do not enter the decision prompt.
The rubric and target selection are frozen before new prediction scores. Development
changes remain exploratory. All earlier arms and failures remain visible; the old
early-prefix scores are not relabelled. Previously exposed cases 041–050 provide
no rubric changes or teaching examples and cannot support fresh holdout claims.

Before reporting future gains, use a newly locked evaluation population and keep
model, extraction, response ontology and judge fixed while changing only the declared
decision-prompt factor. One changed output does not demonstrate causal improvement.
