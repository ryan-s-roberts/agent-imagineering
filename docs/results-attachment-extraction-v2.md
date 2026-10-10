# Attachment extraction v2 results

Both probes completed. PDFs now produce typed observations in the same case-local graph
as event evidence, and that graph was passed with both ontologies to the decision model.
This round combines evidence v7, compact IDs/source metadata, derived provenance and bounded
record batches. It is a development engineering validation, not a controlled model-quality gain.

| Probe | Entities | Records | Physical observations | Proposed actions |
|---|---:|---:|---:|---:|
| 010 at 013 | 15 | 7 | 5 | 0 |
| 020 at 017 | 41 | 44 | 36 | 1 |

010 preserves the apparent reading 16845 without inventing a unit, the isolator setting,
label/presence facts, and the separate 1000 imp/kWh meter rating. However, the model concludes
without an action because it did not extract a request entity. Passing structural validation
does not resolve that workflow limitation. 020 preserves room-scoped conditions and reported
negative findings; see the independent review for semantic details and remaining gaps.

The independent manual review recovered 15 of 16 selected attachment claims. The one-defect
count remains absent as a typed count. These selected claims are not exhaustive recall or
an estimate of decision accuracy.

## Cost and performance

| Measure | v1 | v2 |
|---|---:|---:|
| Returned model calls | 11 | 15 |
| Input tokens | 1,050,670 | 594,224 |
| Output tokens | 67,616 | 81,529 |
| Cached input tokens | 181,393 | 63,344 |
| Reported cost | $0.14428073 | $0.107756815 |
| Measured round time | 303.542 s | 280.823 s |

Input fell 43.44% and cost 25.31%; output rose 20.58% as the new ontology captured many more
assertions. Cache-hit volume did not improve. V2 reported 530,835 cache-write tokens. Six
requests overlapped at peak, under the global cap of 24; all independent available batches
were admitted together. Parallel cold requests were not serialized merely to warm cache.
These combined-run changes do not isolate which intervention caused latency or quality effects.

The fair offline representation comparison transforms the exact original v1 requests,
keeping their ontology and payload facts unchanged. Request-byte savings range from 22.2%
to 86.8%; case020 record input shrinks 74.9%. Bytes are not a tokenizer or runtime measure.

## Remaining failures and corrections

- A dense report batch still exhausted 14,000 output tokens. Its retained full-size repair
  completed at 12,052 tokens. The live run therefore does **not** prove truncation eliminated.
- Subsequent generic execution code subdivides only a length-limited batch, preserves
  completed siblings and one shared graph, and rejects unsplittable sources/depth overflow.
  Stubbed tests verify no repeated full-size request and complete source ownership. This
  adaptive correction has not been exercised in a paid model run.
- Frozen ModelView v1 omitted two record-reference aliases in the 020 decision input.
  Canonical strings remained present but no longer matched compact record-row IDs. Their
  effect on the choice is unmeasured; the output references themselves pass validation.
  ModelView v2 fixes the full reference inventory for future calls.
- Raw-page revalidation proves three flagged quotes were contiguous line-wrapped text.
  Two further quote spans remain incomplete (one drops a clause, one the final period).
  The Utility Room location cites the wrong line, and one blocking_effect field lacks evidence.
  The frozen evidence packets, decisions and their original diagnostics are unchanged.
- The first cache-key transport attempt was rejected for exceeding the provider's 64-character
  limit. It is preserved separately. No generation response or usage receipt was returned;
  its cost is unknown, not asserted zero. The successful run uses a 64-character context hash.

Review: `docs/attachment-probe-review-v2.md`. Canonical artifact, HTML and self-contained
per-case answers are under `runs/attachment-extraction-v2/`. Source hashes, original page
text, field spans, actual compact calls, alias maps, separate revalidation and repair history
remain inspectable. No future attachment or evaluation-only annotation entered model input.
