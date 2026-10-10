# Late development evaluation v1 — frozen before predictions

- Population: all 102 checkpoints in `runs/agent-only-late-dev-v3/manifest.json`.
  Development cases only; some cases have fewer than three assessable episodes.
  Excluded/unassessable episodes remain in the annotation audit denominator.
- Selection: model-annotated agency-only actions, independently audited for required
  input availability before the episode. Mixed counterparty behavior is excluded.
- Prediction: existing extraction pipeline, evidence/result T-box, role decision
  prompt, `openai/gpt-6-luna`, existing settings; no new winning prompt selected.
- Concurrency: 24 global requests per active phase. No simultaneous independent
  pools claiming a single cap. Keep attachment extraction prefix-scoped.
- Assessment: episode-judge-v1 for historical correspondence, separately
  evidence-response-v1 for target-free evidence warrant and progress.
- Metrics: full denominator, phase failures, structural validity, proposal counts,
  per-action support dimensions, historical operational coverage, cost and latency.
  Checkpoint results and case-level rollups must be distinguished.
- Stop: one prediction and assessment round with bounded interface repair. No
  semantic retries, prompt changes or target changes based on these predictions.
- Interpretation: exploratory development evaluation. No untouched-holdout claim,
  no causal improvement comparison with the differently sampled early-prefix run.

Historical adapter: `notify` is auxiliary; `change_workflow`, `await_response` and
`record_evidence` are workflow effects; other selected action types are material.
These labels describe target categories, not normative action quality. No necessary
order edges were independently annotated for this round; dependency warrant is
assessed separately against the prefix. Only accepted agent quotations enter the
historical judge's source text.

## User-authorized reference-repair amendment

After observing structural reference failures during prediction, the user requested
a repair subloop. The original predictions remain frozen and separately reported.
Before judging, run at most two model reference-repair rounds using only the same
prefix evidence, ontologies and validator diagnostics. Each round retains the
existing single schema-repair allowance. Accept only structurally valid responses;
retain unresolved originals explicitly. No historical targets or judge scores enter
repair. Record all prompts, attempts, costs, timings and accepted-stage lineage.
This is an amended pipeline, not an unchanged first-pass baseline or a causal
prompt improvement experiment. See `docs/decision-reference-repair.md`.
