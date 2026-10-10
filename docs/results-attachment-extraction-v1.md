# Attachment extraction diagnostic v1

Both development prefixes completed extraction and decision generation: 010 at event 013,
020 at event 017. Only explicitly linked files available by each cutoff were loaded.
The same mention detection, coverage, linking and assertion pipeline processed events and
PDF text, producing one case-local entity graph. No evaluation annotations entered prompts.

| Probe | PDF pages | Entities with attachment mentions / all | Attachment-supported records / all | Decision interface |
|---|---:|---:|---:|---|
| 010 at 013 | 1 | 11 / 19 | 0 / 2 | Invalid empty request reference |
| 020 at 017 | 5 | 21 / 39 | 3 / 9 | Structural/reference checks pass |

The 010 graph includes meter, isolator and document entities. The source's apparent meter
reading and switch state survive as an explicitly cited ontology gap: evidence v6 has no
measurement or physical-observation record. The decision cites that PDF text but asks for
clarification, using an empty request ID because the model did not extract a request entity.
This is an observable interface failure, not a valid executable answer.

The 020 decision cites the PDF's defect and tenant make-good statement alongside the email's
"No issues" summary, and proposes two clarifications. Two attachment mention expressions
failed exact grounding and remain visible diagnostics. Valid references do not establish
correct identity linking, causal interpretation, or whether either clarification is useful.
Independent semantic review is recorded separately in the attachment probe review.

## Execution

- Model: `openai/gpt-6-luna`.
- 11 returned calls, including one record-stage repair after 16,000-token truncation.
- Cost: **$0.14428073**; measured wall time **303.542 seconds**.
- Two independent case pipelines ran concurrently, under the configured cap of 24.
- Per-case elapsed: 139.701 seconds / 303.527 seconds.
- The repair succeeded at the original limit; no increased-budget retry was needed.
- 56 focused existing and attachment checks passed before this run.

Output repetition is excessive: the larger record request used 172,088 prompt tokens and
its decision request 183,564. Long source/entity IDs, redundant provenance and repeated
schema/context structures need transport optimization. Raising the output limit alone is
not an optimization. This diagnostic is complete; subsequent interface/ontology changes
belong to a new run. PDF text interpretation is not image inspection or verified world state.

Artifacts: `runs/attachment-extraction-v1/run.json`, adjacent `index.html`, and per-case
`ANSWERS/*/ANSWER.md` plus `REASONING.md`. Frozen v1 inputs and outputs remain unchanged.
