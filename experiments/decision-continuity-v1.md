# Extraction continuity prompt experiment — exploratory development round

Hypothesis: distinguishing source ambiguity from representation fragmentation
reduces unnecessary identity clarification without suppressing genuine conflicts.

- Factor: decision system prompt only, control versus continuity-v1.
- Fixed: saved late-development evidence, ontologies, model, request settings,
  schema, reference repair protocol and historical judge.
- Population: 102 checkpoints from development cases 001–040, as frozen by the
  late-agent-action selection. Cases without assessable checkpoints stay outside
  prediction and remain in the selection audit. No holdout calls or examples.
- Model: openai/gpt-6-luna; original seed 42, decoding and token limit retained.
- Controls: a fresh control using the unchanged saved system prompt; compare both
  arms before and after the same bounded reference repair.
- Metrics: identity clarification/escalation frequency (qualitative source review,
  not a keyword correctness score), action count/type, structural validity,
  historical operational correspondence, judge failures, cost and latency.
- Selection rule: fewer unsupported identity blockers is useful only if responses
  preserve genuinely consequential ambiguity and supported operational actions.
  Historical agreement alone cannot establish this. No automatic promotion from
  an increase in action count or a decrease in clarification count.
- Stop: one candidate and one control, one generation per checkpoint per arm,
  with the same bounded repair. No prompt iterations based on this round.
- Interpretation: exploratory, designed after inspecting development failures.
  No generalization claim; promotion requires separate review and an untouched
  future dataset. Model-assisted historical labels are not human gold.

The candidate rewrites the epistemic treatment of extraction ambiguity coherently;
it contains no case names, addresses, observed target actions or quoted case examples.
