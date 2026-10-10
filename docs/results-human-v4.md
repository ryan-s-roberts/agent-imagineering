# v4 human-intervention development diagnostic

One pass using `openai/gpt-6-luna`, with three previously inspected prefixes and no
few-shot examples. The new schema and target-event reference probes were authored
before the run. No post-result prompt repair or paid repeat was performed. This is a
development diagnostic, not an ablation, pristine holdout or decision-accuracy result.

| Prefix | Extraction outcome | Target-event probes | Latency | Cost USD |
| --- | --- | --- | --- | --- |
| 038 at 008 | Mention grounding rejected; no assertions | Not scored | 22.785s | 0.0017463 |
| 003 at 006 | Assertions parsed; packet rejected | 7/7 | 93.259s | 0.008094025 |
| 012 at 030 | Assertions parsed; packet rejected | 3/3 | 167.370s | 0.018684650 |

Total reported cost: **$0.028524975**. Zero accepted decision packets. Target-event
probe scores on rejected extractions are diagnostic and must not be presented as
deployable state coverage. Missing assertions are not counted as passing negative probes.

## Reviewed semantic outcomes

**003 event 006:** The model extracted a human intervention with `status=required`,
`requested_intervention=review_case`, unknown responsible role/person, and the actual
instruction to check whether a provider response is needed. It kept the conditional
return to auto mode in the intervention detail. The trigger was explicitly requested
review, with no fabricated deeper rationale. The priority failure was a separate
`workflow_failure`; it was not asserted as the review's cause. No sent reply, sent
escalation, resolved review or released blocker was inferred.

**012 event 030:** The priority-decrease rejection was preserved as a workflow failure.
No human intervention was fabricated from that event. An earlier event 010 was separately
represented as review requested, with unknown role/person and no sent response. This
earlier status exposes an inconsistency: the guide distinguishes a required check from
a drafted request, but the model used `requested` for wording similar to 003's `required`.
That earlier event was outside the selected target-event probes, so its error is reported
manually rather than hidden by the 3/3 score.

**038 event 008:** The assertion stage did not run. Two asset mentions lowercased
`Washing machine` to `washing machine`. Current alignment permits only explicitly
reported apostrophe changes, so those expressions failed exact grounding. No conclusion
about human-review extraction on this prefix follows from the run. The reviewed source
still establishes manual review required and an adjacent, causally unlinked validation
failure; that annotation is in `annotations/human-v4-references.json`.

## Remaining contract failures

003 produced 14 record-validation issues: omitted populated-field evidence and field
sources missing from the redundant provenance list. Its human record omitted the outer
`causes` field evidence despite providing the nested cause evidence, and omitted evidence
for the unknown blocker effect. It was therefore correctly kept out of decision state.

012 produced 17 issues: seven provenance source omissions, five missing field-evidence
entries and five unmatched expressions. Examples include citing `Hold` from the explanatory
body instead of the metadata line, capitalizing a source phrase, and combining a wrapped
invoice sentence into one quote attached to a single line. Source attribution remained
structurally imperfect even where the extracted value was useful.

The results support the usefulness of a first-class human-intervention representation,
not end-to-end extraction reliability. Next work should reduce model-generated redundant
metadata by deriving source lists from field/cause spans, evaluate event-spanning evidence
without fabricated quotes, and add direct probes for required-versus-requested distinctions.
Such changes need an explicit new round; these retained outputs were not repaired silently.

## Artifacts and checks

- `runs/human-v4/`: full inputs, requests, raw responses, parsed records, errors and scores.
- `annotations/human-v4-references.json`: reviewed boundaries for the three target events.
- `annotations/human-v4-examples.json`: six independently authored annotation examples.
- `docs/human-intervention-v4.md`: lifecycle, cause, actor and blocker semantics.
- `experiments/snapshots/round3/`: preserved historical implementation and reference artifacts.

`uv run pytest -q` passed **17 tests**. Focused Ruff checks passed. No dependencies,
commits or remote repositories were changed. Semantic completeness and sufficient support
for every response choice remain unproven.
