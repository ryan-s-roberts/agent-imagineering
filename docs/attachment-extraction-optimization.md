# Attachment extraction: bounded output and reusable prefixes

## Measured problem

The first case-020 record request consumed 172,088 input tokens and reached its
16,000-token output limit. Its saved schema occupied 133,607 JSON characters;
the user payload occupied 318,611. Long content-addressed source/entity identifiers
were repeated through metadata, identifier enums, assertions and citations. The
repair returned successfully, but this is avoidable transport and generation work.

## Representation changes

- A deterministic per-prefix view assigns short source, mention, entity and record
  aliases. Only typed identifier fields are translated. Quoted text, descriptions
  and rationale remain literal. Saved alias maps reconstruct canonical references.
- Source text remains complete. Repeated file/page/event metadata is factored into
  shared source groups for model input. The artifact retains full hashes, offsets,
  availability links and parser provenance.
- Record-level provenance source IDs are mechanically derived from the emitted
  field/cause evidence spans. The model does not repeat the same source union.
  This does not create evidence or certify semantic support.
- Primary extraction work is partitioned into batches of at most 4,000 source-text
  characters where source-unit boundaries permit. Oversize individual units are
  explicit. Admission is bounded to 64 batches; exceeding the bound fails rather
  than truncating evidence. Every source has exactly one primary batch.
- Batches retain the complete shared context and one globally linked entity table.
  Their outputs receive batch-local record/gap namespaces. No semantic identity
  merge or assertion deduplication is invented during combination. Different
  reports may remain separate assertions about the same subject.
- Calls share a global concurrency cap of 24. Source ownership diagnostics remain
  visible; completing the pipeline is distinct from clean extraction.

## Prefix caching

Static instructions and the shared case payload precede a separate trailing
message containing batch ownership. Shared response enums and source aliases stay
identical across batches. A stable case/context routing key is saved in the request.

OpenRouter documents automatic OpenAI prompt caching, session-based provider
stickiness, and the `cached_tokens` and `cache_write_tokens` usage fields. Cache
writes can incur cost. We retain those provider counters and actual returned cost;
missing counters are unknown. Concurrent cold requests are not guaranteed cache
hits, and no synthetic warm-up calls are added. See
[OpenRouter prompt caching](https://openrouter.ai/docs/guides/best-practices/prompt-caching).

## Comparison contract

`attachment-extraction-v2` reuses the two source prefixes and PDF bytes from v1,
but adds ontology-v7 observations and the representation/batching changes together.
This is a combined engineering diagnostic, not a controlled prompt-only ablation.
Report actual latency, input/output tokens, cache reads/writes, cost, repairs and
semantic coverage. Compare identical saved payloads through the compact projection
separately to quantify representation reduction without confusing it with ontology
or model-output changes. Reviewed expectations remain evaluation-only.

Old runs and their predictions remain immutable. New canonical requests,
compact wire requests, raw model responses, expanded results and alias maps remain
inspectable together. Generated ANSWER files render only saved decisions,
citations and model-authored rationale.

## Length-triggered subdivision

The first v2 round still exhausted its output budget on one dense inspection
batch (2,935 primary source characters). Its already-started interface repair
completed; that truncation and repair remain part of the frozen run and accounting.

The follow-up implementation bisects a length-exhausted batch at existing source
boundaries, balancing primary text volume. Children keep the complete shared
context and global aliases. IDs encode parentage (`b003.1`, `b003.2`), and only
successful leaves contribute records. Completed sibling batches are retained;
truncated parent attempts remain in the audit trail. No partially emitted record
is accepted. A single indivisible source or a subdivision-depth limit produces
an explicit failure, never silent omission. This policy does not establish a
universal character-to-output-token bound.

The subdivision helper has deterministic coverage, ordering, lineage and bound
tests. Live v2 results predate this follow-up and must not be reported as a live
validation of adaptive subdivision. Record-level relationships spanning batches
still require a separate reconciliation design; shared context alone does not
create those links.
