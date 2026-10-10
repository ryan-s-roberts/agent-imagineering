# Full evaluation v1 — 10 October 2026

Single frozen baseline: 50 property prefixes, current evidence/response ontologies,
`openai/gpt-6-luna`, `decision-role-v1` prompt, up to 24 simultaneous model calls.
[Protocol](../experiments/full-eval-v1.md) and
[manifest](../experiments/full-eval-v1.json). No prompt tuning or semantic replay
followed holdout inspection. Case 041 was previously exposed and is separate.

## Completion and validity

All 50 extraction/decision pipelines and all 50 historical judgments completed.

| Measure | Development 001–040 | Holdout 042–050 | Previously exposed 041 |
|---|---:|---:|---:|
| Checkpoints | 40 | 9 | 1 |
| Decisions passing all deterministic checks | 32 | 8 | 1 |
| Record packets without validation issues | 30 | 5 | 0 |
| Mention extraction without reported grounding issues | 34 | 8 | 1 |
| Proposed actions | 42 | 10 | 1 |
| Full historical correspondence | 0 | 0 | 0 |
| Partial historical correspondence | 25 | 8 | 1 |
| Different historical correspondence | 13 | 1 | 0 |
| Unassessable historical correspondence | 2 | 0 | 0 |

Nine decisions fail deterministic checks: cross-request evidence in 006, 008,
019, 040 and 042; missing actions in 010, 013 and 020; invalid request reference
in 027. There were no generation/JSON failures in these 50 predictions. Those
domain-reference/action failures remain failures, despite successful parsing.

The existing `evidence_compatible` flag is true for all 50. Its implemented checks
cover authorization/completion/human-resolution evidence; it **does not establish
general evidence compatibility**. Cross-request evidence is classified under
structural validity by the frozen validator. Do not use the flag as an accuracy
or complete grounding score.

## Historical action coverage

The same episode judge and many-to-many rubric used in development were applied
to the [reviewed development annotations](../annotations/decision-episodes-v1.json)
and [new source-reviewed holdout annotations](../annotations/holdout-episodes-v1.json).
Holdout targets were authored before reading predictions, using the existing
boundary/materiality rules. They were never included in decision inputs.

| Historical effects | Development: covered / partial / missing | Holdout: covered / partial / missing | Exposed 041 |
|---|---|---|---|
| Material | 1 / 20 / 21 | 0 / 7 / 2 | 0 / 1 / 0 |
| Workflow | 0 / 1 / 33 | 0 / 2 / 5 | 0 / 0 / 1 |
| Auxiliary notifications | 0 / 0 / 25 | 0 / 0 / 4 | none |

No checkpoint has full operational coverage. The 53 proposed actions comprise
29 clarification requests, 13 approval requests, six waits, three document
actions and two escalations. The judge labels 48 actions supported and five
partly supported. A reasonable supported proposal can nevertheless omit or
differ from the historical episode; historical actions themselves are not gold
operational truth.

Case 043 has an uncertain follow-up boundary. Case 041's recorded contractor
wait conflicts with its landlord addressee; the annotation preserves that
inconsistency. Existing uncertain development boundaries remain explicit.

## Cost, latency and caching

- Extraction and decisions: **238.47 seconds**, **$0.54453735** reported cost;
  250 returned calls, peak **24** simultaneous requests.
- Historical judging: **70.49 seconds**, **$0.29742721** reported cost;
  56 returned calls, including six bounded interface repairs.
- Total reported cost: **$0.84196456**, 306 saved responses and no saved request
  lacking a response. Unrecorded transport retries cannot be ruled out by these receipts.
- Tokens: **4,498,894 input**, **617,183 output**.
- Provider-reported cached input: **247,191 tokens**, all in judging. This run
  reported no cache reads for extraction or decisions. Cache-friendly layout
  does not guarantee a cache hit.

Phase durations exclude the time between phases. These early prefixes contain
**no loaded attachments**; the round does not replace the separate PDF diagnostic.
The older attachment probe results remain documented separately.

## Artifacts and reproducibility

`runs/full-eval-v1/run.json` contains all phases, original inputs/outputs,
evaluation-only targets, selected judge citations, costs, and split summaries.
Adjacent `index.html` renders it, and `ANSWERS/<case>/ANSWER.md` plus `REASONING.md`
contain only the recorded proposals and rationale, without target/judge leakage.
Runs are Git-ignored and must be distributed separately if required.

An initial packaging check rejected all decision inputs because its T-box-aware
branch recognized only the old two-case run-mode label. The validator was updated
to recognize the new `prefix_evaluation` mode while retaining exact payload
comparison. Predictions and model inputs were not changed or rerun.

78 implementation tests and Ruff passed. The HTML index's JavaScript passed a
syntax check. This remains an exploratory prefix-prediction experiment with a
static ontology, not demonstrated generalization or a simulated operational benchmark.
