# Soft historical targets and the T-box prompt experiment

## Pre-registration

- Hypothesis: distinguishing blocking from nonblocking uncertainty reduces unnecessary
  clarification/escalation and improves historical workflow correspondence without reducing
  evidence support.
- Factor: one general workflow-progress paragraph. No per-case advice, examples or target
  specifics enter either decision prompt.
- Fixed: exact baseline evidence packets, both full ontology T-boxes, response schema,
  model `openai/gpt-6-luna`, seed42, token limits, judge prompt/schema, historical targets.
- Scope: 40 exposed development cases001–040. Cases041–050 excluded. This is exploratory
  development; neither arm can establish held-out generalization.
- Arms: control retains the earlier general decision instructions plus common T-box
  interpretation; progress adds the hypothesis paragraph. Both use the same common interface.
- Judge: blinded single-prediction model-assisted correspondence plus separate evidence
  support and target predictability. Literal checks are reported independently.
- Stop: two arms, one decision and one judge per case/arm, at most one interface repair for
  each response. No semantic retuning or additional arms after results.
- Interpretation: report paired categorical transitions and predictability strata. There is
  no composite correctness score or confirmatory threshold on this exposed set.

The original decision baseline already supplied the response JSON schema through structured
outputs. It lacked the explicit evidence T-box and common interpretation text. Comparing
that old run with either new arm therefore changes the interface as well as instructions;
only the two new arms form the controlled prompt comparison.

## Historical targets

`annotations/historical-targets-v1.json` contains source-reviewed, partial action annotations
derived from the same response action field types. Unknown slots are null and listed
explicitly. Recipient roles are target-local observations, never invented prefix entities.
No target request ID is manufactured. Main intent quotes have exact original character
positions; normalized slots retain source-context evidence. Actor evidence cites recipient
metadata. Source text remains available for disagreement with annotations.

Targets describe the recorded communication, not successful work execution. Proposed future
instructions, quoted tenant reports and descriptions of earlier work remain distinguished.
Case035's mixed-speaker summary is intent-unassessable;002 and022 are partially assessable.
The annotations chiefly encode the primary communication act; original context and candidate
alternative action types remain visible to judge omissions, composites or encoding gaps.
Historical guidance is recorded as speech without endorsement of its safety or correctness.

## Judgment boundaries

The judge receives prefix evidence, both T-boxes, the target's original later event and one
anonymous prediction. It never sees arm names, prompts or another arm's output. It returns
match/partial/different/unassessable independently for intent, roles, scope/conditions,
sequencing and omissions/extras. Overall correspondence concerns material next-action intent,
not an average of dimensions or a type-name match.

Target predictability asks which historical details were available before the cutoff.
Prediction supportedness asks whether the proposed choice follows from prefix evidence and
declared assumptions. Those judgments remain separate: an alternative choice can be better
supported than history, and matching history can require guessing unavailable specifics.
Literal source checks validate judge citations; they cannot certify entailment. Model bias,
same-model self-preference and one-sample variance remain limitations. This is an advisory
LLM judge, explicitly authorized for this development comparison, not deterministic truth.

## Artifacts and commands

```sh
uv run python -m property_eval.author_soft_targets
uv run python -m property_eval.soft_experiment prepare --output runs/decision-soft-v1
uv run python -m property_eval.soft_experiment run --output runs/decision-soft-v1
```

Preparation freezes target/evidence copies, exact prompts, schemas, T-box, implementation and
hashes before paid calls. `experiment.json` records hypothesis, stop rule and settings.
Decision payload keys are exactly `ontology_tbox` and `prefix_evidence`. Targets and judge
results never enter that payload. Shared evidence resides in `evidence/JOB.json`; targets in
`targets/JOB.json`; per-arm decisions, judgments, literal checks, usage and timings in
`arms/ARM/JOB/`. Raw requests/responses and any bounded interface repair remain available.
Completed calls can be reused by exact request hash on continuation; no semantic result is
rewritten to improve comparison.

Planned baseline is160 calls (80 decisions,80 judgments). Provider-reported cost and failed
or interrupted-call uncertainty must be reported separately. There is no hard provider
billing cap. No fresh extraction is performed during this ladder.
