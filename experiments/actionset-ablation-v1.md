# Action-set prompting ablation v1

Frozen before generating any arm output. Exploratory development only.

## Hypothesis and factors

Incomplete action sets may be caused by weak completeness instructions, by
treating uncertainty as a global blocker, or both. The experiment changes only
the decision system prompt in a 2x2 factorial design.

| Arm | Complete supported action set | Action-local uncertainty |
|---|---|---|
| control | off | off |
| coverage | on | off |
| uncertainty | off | on |
| combined | on | on |

Each factor replaces one sentence block in the versioned current prompt. All
other bytes remain identical. The arms are whole frozen prompts; no case facts,
historical targets, counts or answer examples are added.

## Fixed inputs and settings

- Cases 001–040 only, exactly the full-eval-v1 development prefixes and saved
  evidence packets, including their extraction failures and gaps.
- No extraction or entity-linking calls. No new holdout predictions or tuning.
  The previous full-eval holdout has now been observed and cannot serve as a
  fresh confirmatory split for these changes.
- Model openai/gpt-6-luna; decision request settings/schema and user payload
  copied from the baseline canonical request. Seed 42, max output 8000.
- Current response/evidence T-boxes unchanged. Compact model IDs unchanged.
- Same episode-judge-v1 prompt/schema/settings, development annotations and
  immutable citation selection. Judge receives no arm label or decision prompt.
- 40 checkpoints x 4 arms = 160 fresh decisions and up to 160 judgments.
- 24 global in-flight requests across decisions and judges. Job order shuffled
  using seed 42 to interleave arms. Interface repairs remain bounded at one.

## Metrics and success interpretation

Primary: full operational episode coverage count and material/workflow effect
coverage (covered, partial, missing), with the same existing denominators.
Secondary: mean action count, action-type mix, auxiliary coverage, structural
validity, unsupported/partly supported additions, cost and latency.

An increase in action count alone is not success. A useful signal is higher
material/workflow coverage without increased unsupported proposals or reduced
structural validity. Report tradeoffs rather than select a flattering metric.
Judge labels are advisory; historical agreement is not normative correctness.

Report paired per-checkpoint deltas, both single-factor contrasts, and the
combined interaction. Rerun control as a contemporaneous comparator and compare
it descriptively with the earlier frozen control to expose sampling variation.
One sample per cell cannot establish statistical certainty or unseen-case gains.

## Stop rule

Run the four declared arms once. Retain all failed/unassessable cells in the
denominator. No prompt or rubric edits after inspecting results; no semantic
retries. Document transport/interface repairs and packaging fixes separately.
No deployment or default prompt promotion follows automatically.

## Contamination checks

No holdout/gold examples in prompts; no case-shaped scaffolding; no ontology,
model or judge change; all arms declared; no post-hoc exclusions or new score.
