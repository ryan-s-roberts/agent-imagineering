# Judge citations: immutable span selection

## Triage before changing the interface

All31 failures from `decision-soft-v1` were classified against the saved judge requests
before the new prompt was written. `annotations/judge-citation-triage-v1.json` preserves each
failed citation, claimed source text, classification and diagnosis.

| Failure cause | Count |
| --- | ---: |
| Prediction JSON spacing changed during quotation | 23 |
| Prediction JSON fields reordered/concatenated, not a contiguous quotation | 2 |
| Markdown markers stripped from prefix text | 2 |
| Target quotation lowercased | 1 |
| Annotation summary mistaken for a historical source quotation | 1 |
| Prediction citation mislabelled as prefix evidence | 1 |
| Nonexistent prediction field name | 1 |

None resulted from an omitted source. Existing prediction field values can legitimately
support comparison of a proposed action, but cannot establish external-world truth. A
summary's meaning may resemble source text without being a quotation. No fuzzy matching,
semantic relabelling or retrospective acceptance was used to erase these failures.

## New construction

The host builds a catalog from the frozen inputs:

- Prefix: exact source-unit spans.
- Historical target: exact nonempty source lines, retaining repeated occurrences.
- Prediction: literal scalar or empty-container spans of canonical JSON, with JSON-pointer
  paths identifying the generated fields. Serializer positions handle escaping and Unicode.

Each immutable entry has an ID, namespace, source ID, exact expression, occurrence and
start/end positions. Positions are Python Unicode-code-point offsets into the identified
source text. Per-request JSON Schema enums restrict the judge to that request's span IDs.
The judge returns **only a span ID** for a citation; it cannot supply or rewrite its quote,
namespace, occurrence or offsets. Host materialization supplies those fields and checks the
original text slice. Unknown IDs fail validation. Factual-support citation enums allow only
prefix spans; prediction and target spans remain available for correspondence dimensions.

Reference validity is thus checked by construction. Semantic relevance is separate: the
judge can still select a real but irrelevant span, misinterpret it or make a poor judgment.
Empty citation lists remain visible instead of fabricating support. This change fixes the
reference interface; it does not make semantic judgments deterministic truth. Many-shot
examples were unnecessary because the host can own this bookkeeping.

## Controlled rerun

`runs/decision-soft-judge-v2` copies all80 existing predictions byte-for-byte, their original
decision requests/receipts,40 frozen evidence packets, target annotations and both T-boxes.
It performs **judge calls only**, using the same model/settings and shared rubric with the
citation paragraph replaced. Original results remain in `decision-soft-v1`.

The new contextual landlord/tenant assumption was introduced by the user during this work.
It is deliberately **absent from this frozen rerun**. Applying that assumption requires a
new decision ontology/context baseline; old predictions are not retrospectively changed.

Artifacts include `citation-catalog.json`, raw `judge-response.json`, `judge-selections.json`,
materialized `judge.json`, selected offset records in `judge-spans.json`, and independent
literal checks. The canonical artifact separates inherited decision costs from new judging
costs, verifies input identity and checks every selected-ID-to-materialized-quote mapping.

```sh
uv run python -m property_eval.citation_triage
uv run python -m property_eval.rejudge_spans prepare --output runs/decision-soft-judge-v2
uv run python -m property_eval.rejudge_spans run --output runs/decision-soft-judge-v2
```

Interpret changes in judgment labels as measurement sensitivity under a revised judge
interface, never a change in the frozen decision agent's performance. Predictability
agreement across the two predictions for a case remains a separate judge-consistency check.

## Completed result

All80 judge-only calls completed with zero interface repairs or failures. The host
materialized **1,546 citations, all valid**, and no judgment had an empty overall citation
set. All80 prediction files remain byte-identical to the prior run. New returned-response
cost was **$0.38813534** (2,571,662 prompt tokens;137,538 completion tokens); inherited
decision and extraction costs are reported separately in the canonical artifact.

This fixes reference validity, not semantic judgment stability. Three cases still received
different target-predictability labels across arms despite identical prefix/target data:
004,007 and013. Relative to the old judge, eight correspondence labels,22 support labels
and eight predictability labels changed on unchanged predictions. These are measurement
changes under the revised judge interface, not improvements in the decision agent.

Both arms still have two **model-judged matches**; these are provisional semantic labels,
not deterministic exact matches. Reference validity and semantic relevance remain separate.
The original31 failures and original judgment outputs are preserved for comparison.
