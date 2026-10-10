# Full evaluation v1: frozen protocol

- Objective: measure the current extraction-to-decision pipeline across all 50
  public property cases. This is a single-arm baseline, not a causal ablation.
- Development: 001–040, using the existing decision-dev-v1 prefix cutoffs.
- Holdout-labelled: 041–050. Case 041 was exposed in an earlier extraction round;
  report it separately. No claim that the entire split is pristine.
- Holdout selection: first agency Email/SMS/Call after at least one event, using
  the existing agency sender labels. Cut immediately before that event. If no
  event meets the rule, fail selection explicitly rather than inventing a cutoff.
- Fixed model: openai/gpt-6-luna; decision-role-v1 source prompt, current evidence
  and response schemas, compact representation, attachment extraction, 24 global
  in-flight calls, bounded interface repair and adaptive record subdivision.
- One prediction per checkpoint. No semantic retry, prompt tuning or exclusion
  based on observed performance. Failed checkpoints remain in denominators.
- Deterministic metrics: phase completion, mention/record grounding diagnostics,
  decision reference/evidence compatibility, action count, tokens, reported cost,
  missing usage, cache reads/writes and latency, split by development/holdout.
- Historical correspondence: reuse the existing episode rubric and development
  annotations. Author holdout episode annotations from later source events under
  that same boundary/materiality rule; these never enter extraction or decision
  input. Keep model-judged correspondence, prefix support and predictability
  separate. Annotation uncertainty is reported, not guessed away.
- Success criterion: deliver a complete accounting for all 50 checkpoints and
  transparent validity/correspondence denominators. No accuracy threshold or
  generalization claim is asserted for this exploratory baseline.
- Stop: one round, including the pre-existing bounded syntax/transport handling.
  Any required harness repair is logged separately; no model-specific semantic
  patching after seeing holdout results.
