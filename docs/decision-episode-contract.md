# Decision episodes: one prefix, one or more agency actions

## Correction to the earlier evaluation

The earlier **2/40** is a model-judged correspondence result against first-message targets. It is **not a valid score for complete decision episodes**. A single decision can generate several communications and administrative effects. The original targets and predictions remain unchanged for audit; `annotations/decision-episodes-v1.json` is a separately authored replacement target unit.

All40 development prefixes are unchanged. Cases041–050 were not read. This annotation is an implementing-assistant source review, not an LLM judge output. Historical actions are observations of what staff did, not uniquely correct or normatively required actions.

## Boundary rule

Include agency actions available for the same decision until an external reply, new observation or newly recorded decision-relevant evidence changes what is known. Start a new episode for a new timeout/follow-up trigger. A display prompt such as “review response” belongs to its incoming-message boundary cluster; it is not independent world evidence. Time equality alone neither joins nor separates actions.

Distinguish an agency mutation from new evidence: provider assignment can be an effect inside a bundle; recording an otherwise unseen approval may introduce unavailable authority. In cases018/030 that distinction cannot be resolved from the log, so the conservative target stops there and records a possible continuation separately. Those continuation IDs are not additional mandatory actions.

For mixed calls, split only where speaker attribution supports it. Case022 records initial agency contact, tenant agreement, and agency confirmation in one prose summary. Only initial contact/proposal can be attributed to the prefix; exact proposal slots and subsequent confirmation cannot. Case035 has no reliable attribution of agency requests versus landlord responses. Its action is `unknown`, not a guessed approval request. Post-call consequences are outside the initial target.

## Representation and source integrity

Each episode records the unchanged checkpoint, included event IDs, decomposed actions, boundary with exact citations, a review-only source tail, ambiguity, and any possible continuation. Every action citation carries the original full body or a precisely delimited excerpt, raw-file one-based line positions and zero-based Unicode character offsets with exclusive end.

`earliest_knowledge.cutoff: null` means the earliest factual availability cannot be established. `prediction_cutoff` states the actual input boundary. Do not infer knowledge at that cutoff merely because an action precedes the next logged reply. Administrative effects instead carry their input cutoff and explicitly describe themselves as effects. `observed_at_event` establishes when the action appears in this log, not when every fact or instruction became known. Missing historical context and unavailable attachments remain missing.

Action cardinality is1+ when identifiable; unknown mixed calls remain explicit. One email can contain multiple acts, while several channels can express one act. Communications that repeat the same effect share one action and retain every citation. SMS cues remain auxiliary; duplicate substantive emails009/012 and repeated waiting state033 are collapsed. Case002's short scope email plus fuller provider instruction are a single progressive instruction effect. Case038's repeated approval request retains its contradictory property-address labels.

Materiality separates:

- **material:** operational request, instruction, guidance or substantive arrangement;
- **auxiliary:** acknowledgment, status notification or channel cue;
- **workflow:** recorded administrative effect;
- **unassessable:** source does not identify an agency act.

These are observational annotations. There is deliberately no normative required-action list. Missing a historical auxiliary notification must not become the same metric as omitting a substantive contractor instruction. A repair request, conditional instruction or promise does not prove repair execution, booking confirmation, or granted approval. Full source text retains conditional clauses; descriptive action summaries do not supersede it.

Partial-order edges are included only for recorded requests preceding a waiting state for that recipient. They do not impose ordering on simultaneous messages, require identical communication sequencing, or assert that timestamps prove causal necessity. Multiple independent actions may align without a total order. Recipient-ambiguous waiting records supply no edge.

## Audited examples

| Case | Initial bundle | Boundary and consequence |
|---|---|---|
|003, prefix2|SMS003 cue; quote request004 with checkout attachment; wait005|Review prompt006 accompanies provider reply007. Old SMS-only target omitted the operational request.|
|006, prefix3|Tenant notice004; contractor access/quotation instruction005|Next-day reminder006 is a fresh inferred timer trigger. Do not include repeated reminders in initial decision.|
|012, prefix4|Guidance005/006 deduplicated; task-description mutation007|Note008 records landlord approval not visible at prefix4. Approval may predate its record, but cannot be backfilled.|
|017, prefix2|Tenant acknowledgment003; landlord contractor-choice request004; wait005|Tenant acknowledgment007 is an external reply, signalled by006.|
|029, prefix3|Tenant notice004; provider instruction005; SMS006; damage clarification007; mode008; wait009|Tenant response010 is new evidence. Instruction and clarification coexist in the same episode.|
|037, prefix2|Landlord repair-choice request003; tenant photo request004; wait005|Landlord response007, signalled by006. Parallel recipient-specific acts.|
|038, prefix3|Call004/email005 approval request combined; tenant status006; wait007|Landlord approval009, signalled by008. Conflicting property labels remain a target limitation.|

## Counts and limits

The40 checkpoints contain102 annotated effects:35 have more than one source event. Four cases contain more than one material act (015,027,029,037); many other cases combine material acts with notifications and workflow effects. This is decomposition-dependent, not a success score. Six boundaries are explicitly uncertain:005,012,018,022,030,035. Cases022/035 are incomplete mixed-call targets. The other timer boundaries may be probable rather than explicitly logged timers.

Grouping cannot recover missing attachment content, unseen policies, unlogged authority, contractor availability or a fabricated CRM. Landlord, tenant and agency roles are usable identities under the benchmark assumption. Genuine conflicting references remain uncertainty.

## Rescoring contract

Reuse the frozen predictions. Compare action sets with many-to-many alignments so one composite prediction may cover several historical effects, or multiple predictions jointly cover one effect. Report material coverage, auxiliary coverage, workflow correspondence, unsupported additions, conditional-scope differences and evidenced ordering separately. An extra reasonable action is not automatically unsupported; an observed historical act is not automatically predictable from the prefix. Distinguish historical correspondence, prefix support and target predictability. Exclude or mark unassessable post-response slots at uncertain call boundaries. Preserve uncertainty and evidence citations in each judgment.

Do not use first-message counts, exact response-schema type equality, number of messages, or a single all-or-nothing accuracy label as substitutes for this review. Updated judge metrics must retain denominators and mark uncertain targets; these annotations themselves do not provide new scored results.

Reproduce annotations with `uv run python scripts/author_decision_episodes.py`. The script contains the manually reviewed segmentation and act descriptions, attaches source spans deterministically, and makes no model calls.
