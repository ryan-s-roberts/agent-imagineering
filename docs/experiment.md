# Phase one: frozen exploratory extraction run

This is an extraction implementation experiment, not a scored benchmark of agent capability.

- Question: can a compact ontology and schema-constrained extraction preserve useful entities,
  relations, attribution and uncertainty from raw property history prefixes?
- Model: `openai/gpt-4.1-mini`, temperature 0; no examples, repair calls or model fallback.
- Input: history.md only, ending at the manifest cutoff. No index.md, summaries or future events.
- Attachment limitation: referenced attachment names/text are visible; binary attachment contents
  are not loaded in this phase. Missing document facts must not be inferred.
- Source: DwellyOrg/HackatonPublicCases commit `9bcdca585955dfb930005ed742572606e68f5688`.
- Schema and prompt: versioned Python files; the full request and its hash are stored per run.
- Manifest: experiments/phase1.json, nine prefixes; four from case 012, three other development
  cases and two transfer probes. These are not nine independent cases.
- Ontology source: cases 001-040. Cases 041-050 are excluded from this construction pass but have
  appeared earlier in the conversation; no pristine holdout or generalization claim is permitted.
- Execution: concurrency 3, max output 12,000 tokens, per-job timeout 180s. Up to three transport
  attempts for 429/5xx/network failures; no retries for invalid extraction. Temperature zero does
  not guarantee identical LLM outputs or deterministic provider routing.
- Stop: one baseline pass. Any revised prompt/schema or rerun is labelled separately and is
  exploratory. Do not silently discard invalid/error cases.

## Mechanical checks

Schema validity, exact event quote matching, references within the prefix, entity reference
integrity, duplicate IDs, and selected domain/range constraints. Report invalid cases and errors
in the denominator. A successful check does not prove a claim is entailed by its quote.

## Manual review checklist fixed before outputs

Review outputs against original events, including omissions and misattribution:

| Prefix | Evidence to inspect |
|---|---|
| 012:004 | Dishwasher vs unrelated sink thread; no confirmed troubleshooting outcome |
| 012:011 | Troubleshooting failed; reported prior attendance approval; unresolved GS; no future diagnosis |
| 012:016 | Assigned Riverside Compliance vs Cedar Utilities, Leo Turner vs Leo Kendall; appointment is reported |
| 012:024 | Invoice note is attributed repair evidence; does not prove tenant/landlord confirmation |
| 003:010 | Provider assignment and estimate approval are distinct records/claims |
| 020:012 | Original appointment vs rescheduled appointment; date/weekday conflicts preserved |
| 038:013 | Tenant-owned replacement and landlord-covered disposal proposal; no fabricated paid invoice |
| 045:010 | Review all entities, claims and source attribution without a pre-authored expected answer |
| 049:014 | Review all entities, claims and source attribution without a pre-authored expected answer |

This checklist is incomplete annotation, not a gold dataset. Do not report precision, recall,
or semantic accuracy percentages from it. Report supported observations, errors and gaps.

## Post-hoc exploratory model comparison

After observing baseline quote/reference/type failures, run a single additional arm using
`anthropic/claude-sonnet-4.6`. Keep the existing prompt, schema, temperature, token limit and
timeouts unchanged. Use the seven development jobs in experiments/model-comparison.json.
Do not rerun transfer probes or change the ontology on their account. Report both arms including
all failures. This is exploratory, not a preregistered claim about model superiority; model
identity includes provider/default decoding differences. Stop after this comparison.
