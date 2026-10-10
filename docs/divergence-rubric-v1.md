# Divergence review and proposed scoring revision

This exploratory review uses development predictions only. Existing scores and
the running continuity experiment retain their frozen rubric. Review labels are
model-assisted, overlapping diagnoses, not deterministic truth or revised scores.

## Separate the questions

1. **Choice quality:** does the proposal make useful progress from the prefix,
   respect authority and dependencies, or justify waiting?
2. **Evidence warrant:** which claims and prerequisites are actually supported?
3. **Historical correspondence:** which recorded effects are reproduced?
4. **Reference integrity:** do IDs and citations resolve? A failed reference does
   not erase a meaningful proposal or imply that its intent is wrong.

Assess the full action set with many-to-many correspondence. An explicit justified
no-action decision is assessable. Missing generation remains unavailable, not a pass.

## Classify historical action importance by meaning

| Class | Evaluation treatment |
|---|---|
| Operational | Work, booking, approval, document handling or another substantive effect |
| Workflow bookkeeping | Persisted hold, status or stage; score separately from the underlying business objective |
| Communication | An update, confirmation or request with an operational consequence |
| Courtesy | Acknowledgement without a material operational consequence |
| Uncertain | Insufficient source detail to assign importance |

Do not map every `notify` to auxiliary. Do not assume every recorded status update
was required or predictable. `await_response` and setting a CRM hold share an
intention but have different persisted effects; expose both levels of coverage.

## Divergence categories

- Material omission, workflow omission, communication omission.
- Partial scope or a consequential dependency/order difference.
- Extraction-induced blocker; unnecessary clarification; unnecessary escalation.
- Reasonable alternative; equivalent effect through different action decomposition.
- Historical target not warranted by the prefix.
- Boundary/annotation issue or ontology representation limit.
- No material divergence.

Every diagnosis identifies affected target/proposal IDs, explains the difference,
and cites prefix evidence where available. Absent evidence is not fabricated into
a quote. Later target text demonstrates observed behavior, not prior knowledge.

## Stronger progress criterion

“Not contradicted” is weaker than “useful next action.” For a clarification or
blocking escalation, identify the missing fact or competing source interpretations,
the decision they affect, and whether other actions can proceed. Separate genuine
source conflicts from differences introduced by extraction IDs. Penalize redundant
questions and unnecessary blockers separately from unsupported factual claims.

Review each historical action's prefix warrant: required now, reasonable now,
not yet warranted, not inferable, or uncertain. Do not treat every historical
omission as an agent error. Report required, reasonable and unassessable coverage
separately; freeze any subsequent scoring formula before rescoring.

## Review cautions before adopting revised scores

The initial classifier can itself overstate requirements. Unknown business policy
must remain unknown: do not assume independent inspection or an invoice is always
required to record reported completion or propose closure. Preserve reported versus
verified evidence without inventing a universal verification gate. A proposed
closure is also distinct from an executed closure.

If the prefix already establishes a hold or another target effect, a repeated
historical update does not necessarily create new work for the prediction. Review
already-satisfied state separately from missing action. Where the log cannot establish
whether updates share a workflow state, mark the comparison uncertain.

Categories such as `target_not_prefix_warranted` are audit candidates, not proof
that the historical agent was wrong. Before revised headline scores, review
policy-sensitive labels and split already-satisfied state from genuinely premature
actions. Keep the original model labels visible.

## Artifacts and execution

`python -m property_eval.divergence_review --run RUN --env-file ENV` reviews every
development checkpoint at 24 concurrent calls. It uses compact complete prefix
text, literal proposals, included historical actions, extracted entity labels,
record/request associations and gaps. It omits bulky derived extraction trace
metadata and existing judge opinions; omitted trace fields are not silently treated
as contradictory evidence. This is a diagnostic review, not a re-extraction.

Each checkpoint saves `divergence-review.json`, resolved source offsets, requests,
responses, validation repairs, usage and timing. The root summary retains failures
in the denominator and counts categories once per checkpoint. Category totals can
exceed checkpoint count. No holdout case informs this rubric revision.
