# Phase-one extraction: contemporary techniques and design

Research date: 2026-10-10. Scope: event-to-entity, relation, and claim extraction from property-case prefixes. Recommendations below are design proposals, not measured results for this corpus.

## Recommendation

Use schema-constrained OpenRouter extraction with source-grounded mentions, explicit claims, and conservative entity resolution. Retain raw evidence and uncertainty. Validate structure deterministically and score semantic extraction against independently authored annotations. No agent framework, graph database, CRM simulator, or LLM judge is necessary for phase one.

The output is an evidence model, not recovered authoritative CRM state. An invoice reporting a repair establishes a reported repair; a reminder requesting results establishes a missing report. Neither warrants silently upgrading that information to physical-world truth.

## Techniques worth adopting

| Technique | Primary evidence | Application and limits |
|---|---|---|
| Schema-constrained generation | [OpenRouter Structured Outputs](https://openrouter.ai/docs/guides/features/structured-outputs) documents strict JSON Schema and provider parameter requirements. | Use `response_format.type=json_schema`, `json_schema.strict=true`, and `provider.require_parameters=true`. Validate again locally. This constrains representation, not factual accuracy. |
| Grounded span extraction | [Google LangExtract](https://github.com/google/langextract) uses extraction text aligned to source spans; unmatched extraction text has no character interval. | Request verbatim evidence quotes and locate them deterministically inside the referenced event. Preserve failed or ambiguous alignment as a validation error. Never treat a source match as proof that a relation is semantically entailed. |
| Explicit alignment policy | [LangExtract resolver source](https://github.com/google/langextract/blob/main/langextract/resolver.py) distinguishes exact, partial, fuzzy, and absent alignment. | Our first version should require exact matching, with all offsets measured against the immutable source string. Repeated quotes need an occurrence selector or disambiguating context. Do not silently accept approximate evidence. |
| Schema-driven extraction with small models | [GLiNER2, July 2025](https://arxiv.org/abs/2507.18546) combines NER, classification, and structured extraction behind a schema interface. | A credible later span-extraction baseline. It does not establish property-domain approval interpretation or cross-event resolution quality. Avoid its additional model/runtime dependencies until the OpenRouter baseline is measured. |
| Mention-first entity resolution | [Evaluation of named entity coreference](https://aclanthology.org/W19-2801/) treats named, nominal, and pronominal mentions as a distinct coreference problem. | Store every mention before grouping entities. Separate exact identity evidence, plausible links, and unresolved references. Different names with matching roles must not automatically collapse into one person. |
| Attribution and derivation | [W3C PROV-O](https://www.w3.org/TR/prov-o/) supplies explicit attribution and derivation relations. | Borrow the concepts: who asserted a claim, which source carries it, and how an extracted object derives from evidence. Full RDF/OWL machinery is unnecessary. |
| Temporal claim preservation | [Zep paper, January 2025](https://arxiv.org/abs/2501.13956) describes temporally aware integration of conversations and business data; [Graphiti](https://github.com/getzep/graphiti) implements temporal graph memory. | Keep recording time separate from the time a claim refers to. Preserve competing or superseded claims instead of overwriting them. These systems motivate the representation; their memory benchmarks do not validate property-case extraction. |

The selected literature establishes useful contemporary implementation patterns, not a leaderboard result on these cases. A newer publication date is not evidence of better suitability. Official repositories and API documentation were inspected live; pin versions and model/provider identifiers in actual run artifacts.

## Minimal extraction contract

1. **Source event:** stable case/event ID, original text, sender/channel/date metadata, content hash, prefix position. Preserve both the text and its boundaries.
2. **Mention:** event ID, verbatim text, exact span, entity type, local mention ID. Extract organisations and people separately from their contextual roles.
3. **Entity:** case-local ID, type, member mentions, unresolved candidate links. Tenant, landlord, property manager, and contractor are roles in a relationship, not necessarily exclusive entity types.
4. **Claim:** subject reference, typed relation, object reference or typed literal, evidence spans, attributed speaker, polarity, and status such as reported/proposed/requested/recorded/uncertain. Keep assertion status separate from model confidence.
5. **Time:** source timestamp plus optional referenced time/window. Relative-date normalization must retain the original expression and resolution basis; absent dates remain absent.
6. **Conflict/unknown:** references to competing claims or unresolved identity mentions. Unknown is different from false; missing evidence is different from an observed negative.

Use a small typed relation vocabulary with domain/range rules and a separate unclassified-evidence collection. Do not turn every novel phrase into a new ontology class. Approval claims need scope, actor, request, and conditions when explicitly present; they must not invent monetary limits. Factual extraction and next-action prediction should remain separate tasks so extraction defects remain visible.

## Minimal Python pipeline

`immutable prefix -> parsed events -> constrained extraction -> evidence alignment -> local schema/reference validation -> entity/claim artifact -> evaluation report`

Use Pydantic for typed contracts and schema generation, `httpx` for the OpenRouter HTTP client, and standard-library `asyncio`, `json`, `hashlib`, `pathlib`, and `argparse`. A semaphore bounds concurrent requests; each case/prefix gets isolated files. Keep network retries bounded and visible, recording attempts and failures rather than silently repairing model content. Explicitly select a currently supported model and fail if strict output is unsupported.

Run the baseline on one complete prefix per call, so earlier context is available without leaking later events. For longer prefixes, compare event batches that include only preceding context. Parallelize across independent prefixes; do not share mutable entity registries between cases. Quote alignment can generate offsets in code, avoiding fragile model arithmetic. Persist prompt/schema versions, source hashes, requested and returned model identifiers, raw outputs, timing, usage, and validation failures. Low temperature reduces variation but does not guarantee identical provider responses.

LangExtract is a useful design reference, but direct HTTP plus Pydantic keeps the initial dependency surface small. A graph database or multi-pass extraction should be justified by measured recall or consistency improvements.

## Evaluation without an LLM judge

Keep two reports separate:

**Mechanical validity, available for every output:** schema success, exact quote alignment, valid event references, cutoff compliance, unique IDs, valid relation endpoints, domain/range validity, and preserved raw response. An empty extraction may pass all these checks; therefore they are not accuracy metrics.

**Semantic quality, available on annotated examples:** mention span/type precision-recall-F1; typed relation precision-recall-F1; attribution, polarity and claim-status accuracy; temporal normalization accuracy; and erroneous entity merges/splits. Match semantic records by grounded spans and canonical tuples rather than arbitrary generated IDs. Count omissions as false negatives and unmatched predictions as false positives only where annotation coverage is declared exhaustive. Partial challenge assertions must be labelled coverage probes, never comprehensive precision or recall.

Author annotations before inspecting predictions. Mark genuinely ambiguous identities as unresolved, with explicit allowed alternatives where needed. Separate ontology-development cases from held-out cases before changing prompts or schema; freeze a version before the held-out run. Case 012 has already heavily informed design and cannot serve as independent validation. If phase-one inspection uses all public cases, report those results as development performance; the organiser's unseen cases remain the future generalisation test.

The assistant can inspect source and predictions to diagnose concrete failures, but that is qualitative review by the development agent, not independent human ground truth or a deployed LLM judge. If the same assistant authored expectations, disclose that dependency. No factual-accuracy claim should be based solely on a model validating its own extraction.

Useful stress checks include duplicate events, unresolved initials, inconsistent organisation names, reported versus approved work, requests versus completed actions, and missing reports versus failed work. Apply transformations only where they preserve the intended semantics. Prefix-extension changes can reflect legitimate newly available evidence and are not automatically inconsistency errors.

## Decision for phase one

Build and measure the smallest grounded extraction baseline. Treat schema validity, evidence validity, semantic extraction accuracy, latency, and cost as separate outputs. Retain exact failures for review. Expand extraction passes, ontology scope, or dependencies only in response to observed deficiencies, and keep unseen-case claims narrower than the evidence supports.
