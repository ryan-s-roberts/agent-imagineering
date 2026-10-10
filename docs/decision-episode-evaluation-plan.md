# Decision episode evaluation correction

## Status and scope

This is an exploratory correction to the evaluation unit on development cases
001–040. Earlier scores compared predictions with a single selected agency
communication. They do not measure reproduction of an entire decision episode.
No claim about unseen-case or final-outcome performance follows from this round.

The first corrected run reuses all 80 saved control/progress predictions and their
original evidence. It changes target construction and judging, not those model
decisions. The role-identity experiments remain separate interventions.

## Frozen-run contract

- Preserve the original prefix, evidence packet, prediction and their hashes.
- Annotate the subsequent agency action set until new decision-relevant evidence,
  an external response, or a timer trigger changes the decision context.
- Record uncertain boundaries and mixed-speaker events explicitly. Temporal
  proximity alone does not establish a shared decision context.
- Retain original event and text provenance for every historical action.
- Separate material operational actions from supporting notifications. Deduplicate
  equivalent communications without discarding their source references.
- Record necessary dependencies separately from observed chronological order.
- Keep future targets exclusively in the evaluation lane.

## Scoring dimensions

The judge must allow many-to-many correspondence. A prediction can implement
several historical acts, and several predictions can implement one historical act.
Different action counts are not themselves a failure.

Report historical material-action coverage, partial matches, participant and scope
differences, unmatched predictions and their prefix support, and violations of
annotated necessary dependencies separately. Supporting notifications must not
silently dominate the material-action denominator. The recorded actions are
observations, not a normative or uniquely correct policy.

Target predictability and prediction support use only the frozen prefix for their
evidential basis. Missing/private information and uncertain episode membership
must remain visible. Failed judgments stay in the expected denominator.

Constrain judge citations to supplied immutable span IDs. Deterministic validation
checks source slices, IDs, mapping completeness and counts; semantic alignment and
entailment remain model-assisted judgments.

## Execution and stop rule

Use the existing OpenRouter model and saved prediction settings. Run independent
judgments with a global concurrency limit of 24. Save exact rubric, schema,
requests, responses, cost and observed latency. Complete one correction round;
do not iteratively alter the rubric to improve its resulting scores.

Audit the decision prompt separately: it already permits one or more actions and
the response schema already carries action dependencies. Any revised instruction
for complete current-context action sets must be evaluated in a separately labeled
run, with evidence and judge held fixed. Never attribute a scoring-unit correction
to improved model decisions.

## Presentation

Publish one self-contained `run.json` with adjacent `index.html` rendered from it.
The UI presents episode boundaries, historical and predicted action sets,
many-to-many alignment, missing/extra actions, dependencies and citations. Preserve
the distinction between correspondence, evidence support and predictability.
