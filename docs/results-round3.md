# Round 3: mention → linking → assertion extraction

## Protocol and limits

Two pre-registered arms, one run each, two three-event prefixes. Model:
`openai/gpt-6-luna`, verified in the OpenRouter model catalog. The sole arm difference
is the independently authored interpretation examples appended to all stage prompts.
Same model, source prefixes, ontology, schemas, maximum tokens, concurrency and timeout.
No corrective retries, prompt edits or reruns after viewing outputs. Transport failures
retain the existing bounded retry policy; none were observed in these outputs.

The model catalog omits temperature support. Before paid requests, both arms were
amended to omit temperature instead of passing unsupported zero. This transport-only
change is recorded in `experiments/round3-amendment.json`, alongside its new client hash.
The original freeze remains in `experiments/round3-freeze.json`. Generation is not
guaranteed deterministic. Scoring and span resolution are deterministic.

Development: previously inspected case 012 at event 003. Evaluation: case 041 at event
003, first opened for this iteration after ontology/prompt/scorer freeze. Prior corpus
survey exposure cannot be ruled out; this is **not a pristine unseen holdout**. References
were hand-authored and source-checked before either model arm ran. They have a single
author and no independent annotation adjudication.

## Results

| Arm | Prefix | Reviewed probes | Valid decision packet | Latency | Cost USD |
| --- | --- | --- | --- | --- | --- |
| Zero-shot | 012 development | 4/5 | Yes | 58.448s | 0.0048939 |
| Few-shot | 012 development | 5/5 | Yes | 48.241s | 0.0039209 |
| Zero-shot | 041 evaluation | 6/7 | No | 70.678s | 0.0060536 |
| Few-shot | 041 evaluation | 7/7 | No | 101.834s | 0.0092715 |

Total reported cost: **$0.024139975**. All twelve stage calls returned parsed structured
output. Mention grounding and linking validated on all four jobs; all 45 mention spans
matched exactly. Apostrophe alignment is covered by a unit test but was unnecessary here.
Both development packets validated. Both evaluation packets were rejected, correctly.

Zero-shot evaluation: seven field sources missing from the redundant provenance source
list, plus two populated condition lists without field evidence. Few-shot evaluation:
four missing provenance source references plus one authorization scope without evidence.
Neither evaluation extraction was supplied as an accepted decision state.

The pre-registered probe criterion improved descriptively with no validity regression,
but **this does not establish a semantic improvement**. The two missed zero-shot probes
already had the correct approval-request values; their evidence quotes were shorter than
the frozen reference coverage requirement. For example, `approve` versus the reference
`approve selection of provider and category`. Few-shot used longer spans and passed.
We retain the frozen scores rather than revising the judge after results. A future round
should separate controlled-value recall from evidence sufficiency and annotation breadth.

These are targeted probe-recall scores, not precision, F1, exhaustive extraction accuracy,
decision accuracy or SOTA evidence. Extra assertions were not exhaustively annotated.
Scores on rejected packets are diagnostic extraction scores, not deployable state coverage.

## Manual semantic review

- Both evaluation arms extracted the washing-machine failure as a report, the £65.00
  proposed amount as 6500 GBP, a landlord approval request, and source-supported identity
  between the original and quoted machine mention. Neither promoted the request to approval.
- Both retained minimum charge and additional VAT in condition prose. The amount probe
  does not measure floor/tax semantics. No typed price qualifier exists yet.
- Both proposed attendance with an empty activity scope. `attend` is absent from the
  controlled proposal vocabulary; equating it to repair would be wrong. This is a real
  ontology expressiveness limitation, not evidence of successful full choice support.
- Zero-shot anchored the maintenance-request entity on `doesn't spin/drain`, while
  few-shot used `washing machine isn't spinning`. Both are fault-description phrases
  within an explicit request description. Whether to annotate that request as its header
  or its descriptive content needs a clearer boundary convention. Our selected evaluation
  probes do not score this request mention; valid offsets cannot establish typing accuracy.
- Few-shot retained a conditional approval prerequisite as `unknown` and linked it to
  the proposed attendance. That is useful representational behavior; one example is not
  a general accuracy claim.
- Speaker attribution remains variable: agency, tenant and signature author appear in
  different layers. The schema stores one attributed actor, not a nested report chain.
  Distinguishing recorder, immediate speaker and original reporter needs explicit evaluation.

## Choice support and human escalation

The new proposal, access, communication and condition records close representational
gaps, but this small round does not cover all eight response choices. Only clarification,
approval/waiting, identity and a recorded hold are probed. No decision model was evaluated.
See the independent `docs/decision-coverage.md` audit for historical choice representability.

The user's human-escalation requirement arrived after this round's freeze. Current gaps
and communication records cannot faithfully encode all of: why human intervention is
required, the requested intervention, responsible human role, blocking uncertainty and
the lifecycle **required/requested → sent → human response → resolved**. A CRM instruction
to review manually must not be interpreted as a sent or completed escalation. This needs
a next-version typed assertion and matching response arguments; it was not silently
inserted into this frozen comparison. Full evidence-to-choice sufficiency remains unproven.

## Reproduction and artifacts

Runs: `runs/round3-zero/` and `runs/round3-few/`; each contains all requests, raw responses,
parsed stages, grounding reports, input digests and scores. The later v4 cutover preserves
round3 code under `experiments/snapshots/round3/`. To reproduce use
`PYTHONPATH=experiments/snapshots/round3/src uv run property-extract` with
`--manifest experiments/round3.json --model openai/gpt-6-luna --concurrency 2 --timeout 300`,
plus source/env/output paths; append `--few-shot` for the second arm. Existing output directories cannot be
overwritten. References: `annotations/round3-references.json`.

Checks: `uv run ruff check src tests` passed; `uv run pytest -q` passed **13 tests**.
They exercise grounding/alignment, reference alternatives, failure retention, bounded
concurrency, timeout behavior, field coverage and response scope checks. They do not
prove extraction entailment or decision readiness. No dependencies changed this round.
