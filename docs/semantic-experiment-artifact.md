# Semantic comparison artifact

This experiment extends the canonical run contract to an explicitly controlled
comparison. The original `property-run-v1` baseline remains immutable. The new
document retains the exact baseline evidence and its source hash, historical
choices as **soft targets**, both ontology definitions (T-boxes), every decision
prompt arm, and the constrained semantic judge's saved inputs and outputs.

## Three questions, three answers

| Dimension | What it asks | What it does not establish |
|---|---|---|
| Historical agreement | Does the proposed choice correspond to the recorded later human/system choice? | That the historical choice was warranted or uniquely correct |
| Evidence support | Does the prefix evidence support the proposed action, rationale and escalation cause? | That agreement with later history follows |
| Target predictability | Could the historical choice reasonably have been inferred from this prefix? | That omitted/private information was available to the decision agent |

Unknown, ambiguous and unjudgeable cases remain explicit. An LLM judge is a
model-assisted assessment, not a deterministic proof or a human-reviewed gold
label. The artifact keeps its rubric, model, prompt, structured response, citations,
validation and cost alongside each assessment. Deterministic checks report only
the properties they actually check: schema, references, exact spans and fixed-input
boundaries. None can certify semantic entailment by itself.

## Information boundaries

The decision agent receives the shared prefix evidence packet and both fixed
T-boxes. Only the decision prompt differs between arms. Historical targets and
future observations belong to the evaluation lane. The semantic judge may receive
both lanes to compare them, but its input names them separately and it must assess
evidence support using only prefix evidence. A plausible explanation invented
after reading the later event is not a supported decision rationale.

The historical target is an annotation in the result ontology. It retains source
provenance, unknown fields, alternatives and its author/review status. It is not
silently upgraded to gold truth when a judge agrees with it. Target-generation
calls, if used, are a separate paid phase from decision and judge calls.

## Reproducibility

Compare arms only where evidence, ontologies, output schema, decision model,
generation settings, target annotations and judge rubric/settings are held fixed.
The container stores content hashes and exact payloads for these factors. Preserve
failed or missing assessments in the denominator. A winner must not be selected
by retrospectively changing the target or rubric after seeing the arm outputs.
Prompt development and evaluation remain restricted to the authorized development
split; this round does not establish performance on unseen holdout cases.

## Submission boundary

A multi-arm artifact requires an explicit selected arm when exporting
`ANSWERS/<case>/ANSWER.md` and `REASONING.md`. Export the saved decision and its
prefix citations from that arm. Never substitute the historical target, judge's
critique, judge-generated rationale or later observations into a submission.
The selected arm and source artifact hash belong in the export index and files.

## Container: property-run-v2

The content-addressed blob format and canonical hashing algorithm are unchanged
from [the base contract](run-artifact-format.md). `format_version` is now
`property-run-v2`. The following differences are intentional:

- `baseline` records the immutable source run ID, document hash and root artifact
  references. Shared extraction artifacts and original baseline outputs are
  embedded, so the new document is self-contained without following that path.
- `arm_ids` is the complete declared arm inventory, including missing outputs.
  It comes from `experiment.json`, never from whichever output folders exist.
- Each checkpoint's `artifacts` contains shared extraction/evidence only.
  `baseline_artifacts` preserves its original decision/evaluation outputs for
  provenance, without making those the decision of an experimental arm.
- `historical_target.artifact_ref` points to the soft annotation and is explicitly
  `evaluation_only`. Null means missing; it is not interpreted as no historical
  action. Author/review status and ambiguity are preserved in the target itself.
- `arms[arm_id]` contains `artifacts`, `call_ids`, `status`, availability flags and
  `evidence_ref`. Every arm must reference the identical shared evidence blob.
- `ontology.tbox_ref` references the combined evidence/result T-box definitions.
  `response_schema_ref` names the frozen result schema. The content-addressed IDs
  are hashes of the full definitions, not just version labels.
- `root_artifacts` embeds experiment configuration, judge prompt/schema, target
  review, summary and code snapshot whenever the producer has saved them.
  `prompt_artifacts` embeds each arm's exact prompt by arm ID.
- `calls` includes an explicit `accounting_scope`: `inherited_baseline` versus
  `experiment`, and an `arm_id` for new calls. `accounting_by_scope` separates prior
  spend from new decision/judge spend. Global `accounting` includes both and must
  not be described as the incremental experiment cost.
- `completion` counts expected checkpoints, expected arm results, decisions
  available and judge assessments available. Availability is not success or
  semantic validity. The denominator includes unfinished/failed arms.

Each arm's `latency` preserves measured total execution seconds and the producer's
`decision_seconds`/`judge_seconds` phase timers. These include structured parsing,
any bounded repair, and local processing around the model call. They are not
misrepresented as individual HTTP-call latencies. The latter remain null when
unmeasured; whole-run wall time is likewise unavailable unless explicitly recorded.

`resolve_artifacts(document, checkpoint, arm_id)` resolves shared files and overlays
the selected arm's files. Without `arm_id`, v2 returns shared evidence only.
Judge outputs use the saved schema's field names: `overall_correspondence` and its
dimensions for historical agreement, `prediction_supportedness` for evidence
support, and `target_predictability` for predictability. No synthetic combined
score is computed by the assembler. `mechanical.json` remains a separate literal
slot comparison. Judge validation reports do not turn the model score into proof.

The assembler verifies the exact decision user payload contains only
`ontology_tbox` and `prefix_evidence`, matching the shared blobs. The judge payload
must match those plus the saved historical target, prediction and serialized
prediction citation source. Declared system prompts must match. Non-message model
request settings/schema must remain identical across arms for each phase. These
are data-boundary checks, not a claim that a model followed the instructions.

## Assembly and exports

The producer layout is:

```text
decision-soft-v1/
  manifest.json, experiment.json, tbox.json, judge-prompt.txt, response-schema.json
  evidence/<checkpoint>.json
  targets/<checkpoint>.json
  arms/control/<checkpoint>/{decisions*,judge*,mechanical.json,result.json}
  arms/progress/<checkpoint>/{decisions*,judge*,mechanical.json,result.json}
```

```sh
uv run python -m property_eval.experiment_artifact runs/decision-soft-v1 \
  --baseline runs/decision-dev-v1/run.json
uv run python -m property_eval.submission runs/decision-soft-v1/run.json \
  --arm control --output runs/decision-soft-v1/ANSWERS-control
```

Assembly never overwrites the baseline. A changed shared evidence packet raises
an error. Sparse snapshots preserve missing targets, decisions and judges without
fabricating responses. Reassemble after the producer finishes and render the
adjacent HTML from that exact final JSON. The extraction/decision semantics are
not reinterpreted during assembly.

## Judge-only reruns and citation selection

An experiment with `mode: "judge_only"` preserves existing decisions and reruns
only evaluation. Original requests/responses remain embedded. Their calls are
classified `inherited_decisions`; new judge calls remain `experiment`. The separate
`inherited_baseline` scope still describes the original extraction baseline.
These sums cover the observations embedded in this document, not every historical
experiment ever run. Superseded judge costs are not silently attributed to the new
judge. `inherited-experiment.json`, when supplied, preserves the source experiment
configuration and lineage. Existing experiment artifacts remain unchanged.

For `judge_version: "soft-judge-v2"`, the judge chooses immutable catalog span IDs.
It does not author source quotation strings. Per arm/checkpoint:

- `citation-catalog.json` contains source texts and candidate spans with IDs,
  origins, source IDs, exact character offsets, expressions and occurrences.
- `judge-selections.json` retains the raw typed model selections.
- `judge-spans.json` records selected spans materialized with their positions.
- `judge.json` retains the semantic assessment with host-materialized citation
  fields, so readers can still inspect the same substantive judgment dimensions.
- The exact `judge-request.json` embeds the citation catalog, and its JSON Schema
  constrains choices to those IDs. The generic schema remains at the run root.

The assembler verifies every catalog expression equals its source slice and that
IDs are unique. Case-local enum values may differ, while other model settings and
schema structure remain fixed across arms. A mechanically valid citation proves
that the selected text exists; it does not prove that the cited text entails the
judge's explanation. Those are separate evaluation dimensions.

`decision-difference-review.json`, when included, is an independently authored
review of paired decision changes. Preserve its author/method and review status;
do not label it as an LLM-judge score or a deterministic semantic verdict.

## Benchmark assumptions are a separate input category

**Superseded design, not executed:** the proposed contextual-addressability round
below was replaced by model-extracted role identities. It records the earlier
artifact design; it is not authorization to inject role parties into current runs.
The current intervention contract is [model-extracted roles](#model-extracted-role-intervention).

Future rounds may include versioned `benchmark-context.json` through
`benchmark_context.artifact_ref`. This declares experiment assumptions separately
from source-derived evidence and the decision model's own assumptions. In
particular, a landlord or tenant may be addressable via a case/property/request
role without a person's name or CRM ID. Such a declaration does not establish a
new person entity or prove an extracted identity. It must be frozen with the
round and reflected explicitly in its input/T-box contract. Do not retrofit it
into an older frozen run or use it as evidence that a historical source said so.

`mode: "contextual_baseline"` is a fresh single-arm round, not a judge-only rerun
or a pure prompt comparison with the older round. The root context document has
`version: "property-benchmark-context-v1"` and `cases`, keyed by checkpoint ID.
For this mode, decision input is exactly `{ontology_tbox, prefix_evidence,
benchmark_context}`; each checkpoint receives only its own frozen context. Judge
input receives the same context in addition to the saved target, prediction and
citation catalog. The assembler verifies both against the separate context blob.

The contextual judge (`soft-judge-v3`) may mark `benchmark_context_used` to explain
that addressability follows from the benchmark contract. That is not a fabricated
prefix quotation. Citation namespaces remain prefix, target and prediction;
evidence-support quotations still select only prefix spans. Existing evidence
packets, historical annotations and prior experiment results remain unchanged.

## Model-extracted role intervention

`mode: "role_extraction"` is a fresh extraction experiment. It replaces the
planned contextual-addressability baseline: role identities must be detected and
linked by the extraction model, rather than injected by host assumptions. This
mode forbids a benchmark-context artifact and uses exactly one declared arm.

The manifest may intentionally contain a selected development subset. For every
primary checkpoint the original prefix hash and source units must match the
immutable baseline. Extracted mentions, identity links, role entities and typed
assertions may change under the new evidence ontology. Shared `artifacts` contains
these fresh outputs; `baseline_artifacts` retains the earlier results only as
provenance. Incomplete extraction never silently supplies the old evidence packet
as the new model's output. Decision input remains exactly `ontology_tbox` and
`prefix_evidence`.

Additional diagnostic jobs under `contrast/<checkpoint>/` are embedded in
`contrasts`, with `included_in_primary_denominator: false`. Their source prefix,
model calls and outputs are retained separately and their costs use accounting
scope `contrast`. They do not increase primary checkpoint/arm totals and are not
exported into `ANSWERS`. A contrast without a historical target or judge is not
described as a failed scored checkpoint. Do not combine its observations with
paired primary-case results without stating the different design.

## Episode-level historical targets

`judge_version: "episode-judge-v1"` re-evaluates the same frozen prediction sets
against an observed **episode**, rather than the first later message alone. An
episode can contain multiple material acts, supporting notifications and workflow
effects. Its reviewed stopping boundary identifies the next information change;
uncertain boundaries and excluded alternative continuations remain explicit.
The earlier first-message scores are superseded as episode-level measurements.
They remain historical artifacts, not interchangeable baselines for a new unit.

`episode-annotations.json` embeds the complete reviewed annotations and boundary
citations. Each `historical_target` contains the narrower judge projection: the
episode's included actions, necessary-order relations and included source text.
Excluded later tails and boundary quotes are review-only and must not become
correspondence evidence. The prediction still has only its original prefix.

The judge emits these independent dimensions:

- `target_assessments`: every observed action exactly once, its coverage,
  participants, scope, prefix predictability and zero or more prediction IDs.
  A prediction may recur across target rows; a target may map to several
  predictions. This preserves many-to-many coverage without flattening action sets.
- `prediction_assessments`: every proposed action exactly once, its evidence
  support and whether it is mapped, a supported/unsupported extra or a duplicate.
- `necessary_order_assessments`: only annotated causal/precondition dependencies,
  separately from observed timestamp order. Independent communications need not
  be serialized to match a recorded message sequence.
- Boundary concerns and cited explanation remain visible. Overall correspondence
  is a model-assisted summary, not a replacement for the set-level dimensions.

Case 035's ambiguous call is an **unassessable historical target**: known sender
and recipient do not identify who requested or approved what. It is not counted
as a missing material act, and absence of assessable targets cannot establish
full correspondence. Prediction support can still be judged against the prefix.

The per-request schema constrains target IDs, prediction IDs, ordering IDs and
citation span IDs; assessment-array lengths match the available sets. The artifact
validator checks these dynamic restrictions against the frozen generic schema and
the actual case data. Selected citations are host-materialized exactly as in the
span-selection contract. `episode-metrics.json` retains deterministic count
projections separately from semantic judgments.

The adjacent HTML exposes historical/proposed sets side by side, switches between
the two frozen prediction arms, and displays missing material acts, missing
workflow effects, omitted notifications, extra proposals and support separately.
Per-action and per-judgment evidence is expandable with original text and positions.

## Self-contained submission answers

Every exported `ANSWER.md` includes all recorded actions, their recorded dependency
relations, and the saved evidence/reasoning content. `REASONING.md` remains available
as a companion. Reasoning is copied literally from the run's decision rationale;
the exporter never synthesizes a new explanation, infers an action-specific motive
from an overall rationale, or invokes a model. Missing rationale is explicitly
unavailable. Cited prefix text is resolved from the frozen evidence packet.

For a two-arm run, export both `ANSWERS-control` and `ANSWERS-progress`, each with
40 numbered case folders and its explicit selected-arm/index metadata. This is
not winner selection. Historical targets, episode annotations and judge critiques
are excluded from both answer and reasoning files.
