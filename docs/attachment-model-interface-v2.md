# Attachment model interface v2

This engineering round combines evidence ontology v7, compact model-facing references,
source metadata grouping, mechanically derived record provenance, and bounded assertion
batches. It is not a one-factor semantic quality or latency experiment.

The canonical graph retains exact source IDs, file hashes, pages and offsets. ModelView
assigns global source/mention/entity/record aliases per prefix. All record batches use the
same maps; the host decodes typed references before validation. Prose and quoted expressions
are never rewritten. Actual compact requests/responses, canonical requests/responses and
alias maps are saved per stage.

Record output omits only redundant provenance.source_ids. Code derives their union from
field evidence and explicit cause evidence, preserving every field value and quote. Empty
evidence does not become invented provenance. Each batch owns at most 4,000 primary text
characters, splitting on source boundaries; all compact sources and one shared entity graph
remain visible for context. Records must cite an owned source. Violations are retained as
visible diagnostics. Batch-local record IDs are namespaced mechanically; no semantic merge
or deduplication hides disagreeing or repeated source reports.

## Cache and concurrency

OpenRouter/OpenAI automatic caching is used with stable `session_id` and `prompt_cache_key`
set to the 64-character SHA256 of ontology version plus full source context. The initial
85-character key was rejected before generation; that transport attempt is retained in a
separate sibling run. Shared system instructions, full case payload, schema and maps are
identical across a case's record batches. Only the final ownership message changes.

Independent calls share a request semaphore capped at 24. There is no serialized cache
warmup or extra warmup model call. Cold parallel batches may miss cache. Actual response
usage retains cached_tokens, cache_write_tokens and cost; per-stage timing includes queue
wait and request duration including transport retries. Cached local responses are not
measured as fresh HTTP calls.

The frozen v1 requests are also transformed offline without changing their ontology or
contents. `representation-comparison.json` measures serialized request bytes, not token
estimates or throughput; this isolates representation size from the combined live round.

Provider caching behavior: [OpenRouter prompt caching documentation](https://openrouter.ai/docs/guides/best-practices/prompt-caching).
