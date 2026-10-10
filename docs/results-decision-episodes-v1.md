# Episode action-set rescoring: frozen predictions

## Completed run

All80 judgments completed for40 development prefixes ×2 frozen prompt arms. The run used
**93 returned calls** (80 initial +13 bounded interface repairs), cost **$0.442347055**, and
took **87.2seconds** for judging/queues/retries/local serialization. Observed peak concurrency
was24. All80 prediction files and40 evidence packets are byte-identical to the preceding run.
No decisions or extractions were rerun. All**1,995** selected citations resolve exactly;
reference integrity is not semantic entailment.

The target now represents an agency decision episode, with102 annotated effects per arm:
42 substantive actions,34 workflow writes/transitions,25 auxiliary effects and1 unassessable
mixed-call action. The judge maps action sets many-to-many. Every target and predicted action
has one typed assessment; the host computes counts and deduplicates IDs. Excluded later raw
events and boundary quotes are omitted from judge input. Full audited annotations remain in
the canonical artifact, with hashes linking each projected target to its source annotation.

## Correspondence counts

These are deterministic counts **over model-assisted labels**, not correctness scores.
Historical actions are observations rather than mandatory or uniquely correct choices.

| Historical effects, per arm | Control covered / partial / missing | Progress covered / partial / missing |
|---|---:|---:|
| Substantive actions,42 |1 /22 /19|1 /20 /21|
| Workflow effects,34 |0 /3 /31|0 /2 /32|
| Combined operational effects,76 |1 /25 /50|1 /22 /53|
| Auxiliary effects,25 |0 /0 /25|0 /0 /25|

The single unassessable target remains unassessable in both arms. No episode has all its
operational effects covered. This shows incomplete **historical correspondence**; it does
not prove all omitted effects were justified or predictable from the prefix.

Support is a separate question. Control's43 proposed actions are judged40 supported and3
partly supported; progress's42 are35 supported and7 partly supported. The judge maps27
predicted actions in each arm to historical effects and calls the remaining16/15 supported
extras. There are no unsupported-extra labels in this pass. These judgments warrant review;
they are not deterministic factual guarantees, and the denominator differs from the previous
response-level support metric.

Necessary ordering is assessed separately from logged chronology. Of22 observed order edges
per arm, control marks18 not required and4 not represented; progress marks17 not required and5
not represented. The annotation's request-to-wait ordering is not automatically a hard gate.

## What changed in the measurement

The old single-event judge had2 model-judged matches per arm. Both of those become partial
episode correspondences. The new broad labels are28 partial,10 different and2 unassessable in
each arm. Neither shift is an agent improvement or regression: predictions are unchanged and
the target unit and rubric changed.

The free-form overall label can disagree with detailed coverage: progress022 is called partial
while its only target action is marked missing. Report per-action counts first; the broad
label is advisory. Do not synthesize a headline accuracy from it.

Source-reviewed examples:

- **003:** The old target was an SMS cue. Both predictions partly map to the substantive
  cleaning/removal/carpet quote request, while the auxiliary cue and workflow hold are absent.
  Quote scope and the checkout-report attachment are not fully represented in the proposals.
- **006:** The episode contains both a tenant notice and the contractor access/quotation
  instruction. Both predictions instead clarify assignment scope. Historical effects are
  missing; their prefix justification is a separate matter because extraction fragmented tasks.
- **012:** Duplicate guidance emails form one action, followed by a task-description mutation.
  The judge finds partial overlap between the predictions' clarification and the response
  request inside the guidance, but the substantive checks and workflow mutation are missing.
  That partial mapping is semantic judgment, not proof equivalent guidance was produced.

## Boundary and information limits

Six boundaries are uncertain:005/012/018/022/030/035. Excluding those yields34 checkpoints per
arm, including probable timer boundaries. Operational coverage becomes control1 covered,
24 partial,46 missing of71; progress1/21/49 of71. This sensitivity view does not silently
replace the full40 denominator.022 and035 mixed calls do not expose reliably separable
post-response actions or precise booking slots.

The extraction input is **history text only**; `prefix.py` does not load PDFs or images.
The40 frozen evidence packets contain no attachment content. In003 the PDF link first appears
in event004, after cutoff002, so that later attachment is unavailable to the decision agent.
A future checkpoint with an in-prefix attachment would need an explicit ingestion contract;
this run did not provide one or infer the file contents.

All cases are previously exposed development data. Nothing here measures unseen-case accuracy,
real CRM execution or environment interaction.

## Review and reusable outputs

- `runs/decision-episodes-v1/run.json`: canonical evidence, frozen predictions, episode targets,
  mapping judgments, raw calls, costs and integrity checks.
- `index.html`: action-set comparison and source review.
- `ANSWERS-control/<case>/ANSWER.md` and `ANSWERS-progress/<case>/ANSWER.md`: each arm's own saved
  actions, dependencies, cited prefix evidence and rationale; no future target/judge content.
- `episode-review.json`: deterministic aggregate counts and per-checkpoint metrics.
- `arms/<arm>/<checkpoint>/judge-selections.json`, `judge-spans.json`, `episode-metrics.json`:
  exact mapping/citation evidence and local counts.

The response schema already supports multiple actions and dependencies. The unexecuted
candidate in `experiments/prompts/decision-actionset-candidate-v1.txt` clarifies the present
knowledge boundary and complete supported action set. No further decision prompt was run.
