# Phase-one results — 10 October 2026

## Outcome

The ontology is useful as an extraction vocabulary, but this first one-pass implementation is
not reliable enough to use as authoritative state or as input to an automatic correctness score.
The pipeline runs, retains failures, and exposes concrete defects. No LLM judge was used:
semantic findings below are qualitative inspection by the implementing assistants against source
events, not independent human annotation. The same development process designed the ontology.

## What was built

- Local repository `/Users/ryan/code/dwelly-property-eval`, no remote or commit created.
- Corpus-derived ontology evidence from 1,177 events across development histories 001–040.
- Pydantic extraction schema with 15 entity kinds, 15 claim predicates, attributed evidence,
  six epistemic statuses, and explicit unresolved issues.
- Prefix-only inputs; model sees neither index summaries nor events after the cutoff.
- Async HTTPX/OpenRouter strict JSON Schema, bounded concurrency/retries/timeouts, usage and cost.
- Exact source-quote alignment, graph reference checks, selected relation constraints.
- Locked uv environment; pytest and Ruff. Nine tests pass, including parallel isolation,
  concurrency bounds, error retention, timeouts, future/outcome exclusion, and a test demonstrating
  that syntactically grounded false claims can pass structural validation.

The implementation is a compact baseline: entities contain their source mentions, but there is
not yet a separate mention-resolution pass, exhaustive domain/range validation, typed approval
conditions, or a literal/time normalizer. Attachments are referenced but their contents are not read.

## Runs

The first manifest was frozen before the baseline. The second arm was explicitly registered as
post-hoc exploratory after inspecting baseline failures. Prompt/schema stayed unchanged.

| Measure | GPT-4.1-mini baseline | Claude Sonnet 4.6 comparison |
|---|---:|---:|
| Prefix jobs | 9 across 6 cases | 7 across 4 development cases |
| Parsed under Pydantic | 8/9 | 7/7 |
| Passed every graph check | 1/9 | 0/7 |
| Invalid graph | 7 | 7 |
| Schema/content validation failure | 1 | 0 |
| Parsed entity count* | 48 | 69 |
| Parsed claim count* | 52 | 68 |
| Parsed unresolved-issue count* | 0 | 33 |
| Median job latency | 6.040 s | 32.630 s |
| Prompt tokens | 22,768 | 27,289 |
| Completion tokens | 7,852 | 14,314 |
| Provider-reported cost | $0.0216704 | $0.2965770 |

*Counts cover parsed graphs, including invalid graphs; they are not counts of correct items
and do not guarantee that their quotes aligned.
Total returned cost: $0.3182474. No transport errors occurred in the returned job summaries.
Different arm case counts preclude a simple aggregate model comparison. Four jobs are nested
prefixes from case 012, not independent examples. None of these validity ratios is semantic accuracy.

| Mechanical issue occurrences | Baseline | Sonnet |
|---|---:|---:|
| Unknown entity references | 30 | 49 |
| Non-exact evidence quotes | 38 | 19 |
| Invalid checked relation domain | 4 | 0 |
| Invalid checked relation range | 1 | 0 |

Run artifacts, including every raw response:

- [Baseline summary](../runs/phase1-baseline/summary.json)
- [Sonnet summary](../runs/phase1-sonnet/summary.json)

These local run directories are ignored by Git. They are retained on disk, not automatically
published. Each job also contains `input.json`, `request.json`, `response.json`, `result.json`,
and, when parsing succeeds, `extraction.json` and `validation.json`.

## Semantic review: case 012

### Cutoff 004

The baseline is the only mechanically valid output in the baseline suite. It identifies the
request and Ruben but omits the unresolved sink-thread association and the unanswered
troubleshooting. Its c4 presents Ruben's door complaint as concerning this request without
retaining the explicitly uncertain link. Mechanical success is consequently not semantic success.

Sonnet explicitly retains the ambiguous sink-thread reference, missing earlier email and approval
gap. However, its unresolved item says no provider has been selected or approved: the source only
establishes that confirmation is absent from this prefix. It also uses source labels instead of
entity IDs in every attribution, which makes the graph invalid.

### Cutoff 011

Baseline successes: captures the persistent fault and failed checks. Failures: classifies Willowbank
(part of the address) as an organization; asserts that the property owns the dishwasher; treats
the staff's prior-approval report as recorded authorization by the agency; omits unresolved GS.

Sonnet improves the prior attendance-approval representation and explicitly preserves Ruben/Leo,
GS and scope uncertainty. It still types GS as an organization without knowing whether it denotes
a person or company. Its approval relation points to GS rather than the authorized work/request.
That falls outside the documented intended range, but the current validator does not check that
range. Some quoted punctuation and metadata are not exact.

### Cutoff 016

Baseline merges person and organisation in the label 'Grant from Cedar Utilities', reverses an
assignment edge, and turns the conditional quote-approval instruction into an authorization
claim. All its unresolved lists remain empty.

Sonnet preserves the conflicting contractor and tenant names in unresolved records and captures
the reported appointment window. It omits a separate Leo Kendall entity while describing that
identity conflict. It overgeneralizes conditional quote approval into a blanket requirement before
all work, and says no approval entity can be created despite the reported approval in event 008.
It also upgrades the manager's report of instruction to a recorded action.

### Cutoff 024

Baseline captures the repair diagnosis and successful test as reported, but invents an assignment
to the caller Noah from an arrival notice and omits overdue-result/identity uncertainty.

Sonnet separates an invoice entity and uses a reports_completion relation for its repair evidence.
It retains missing results and conflicting contractor/agency names. Problems remain: it says no
quote was submitted or approved rather than no such evidence is visible; it overstates the
conditional quote policy. Its appointment interval includes the correct end time but cites event
017 alone, which only provides the start; the supporting end time is in later available events
018/019. A quote can match exactly while supporting only part of a value.

## Other cases

Detailed baseline review: [secondary review](review-secondary.md).

- **003:010:** baseline types the property as an asset and associates an assignment with Bennett
  on generic assignment evidence alone. Sonnet correctly represents a property and records the
  missing estimate amount, but one quote changes a curly apostrophe and attribution IDs fail.
- **020:012:** baseline infers inspector assignment from sender/signature and misses the
  weekday/date mismatch. Sonnet preserves a requested cancellation rather than completed
  cancellation and flags the absent inspector identity. It nevertheless splits a rescheduled
  inspection into two inspection entities without an explicit continuity relation and also misses
  that 15 February 2024 is Thursday, although the request calls it Friday.
- **038:013:** baseline confuses the tenant's proposed ownership of a replacement with ownership
  of the existing broken machine. Sonnet distinguishes that proposal and preserves conflicting
  property addresses. However, its c13 reverses `owns` (appliance -> landlord) and infers ownership
  from presence at move-in; its c11 calls a future disposal plan reports_completion; and one
  unresolved item infers a gender conflict from the name Ruben, which is unsupported and irrelevant.
- **045:010:** baseline treats an email recipient as an assignee and expands approval for a
  contractor visit to authorization to fix the issue. See secondary review for source references.
- **049:014:** raw output captures tenant repair permission and the recorded completion, but its
  final reports_completion claim has neither object nor value and fails Pydantic. The failed raw
  response remains available. It also contains unresolved source-label attribution references.

## What the experiment teaches us

1. **Ontology feasibility: supported.** Recurring concepts span repairs, checkout cleaning,
   inspection scheduling and tenant-owned replacements. It is an evidence ontology, not CRM truth.
2. **One-pass extraction quality: insufficient.** A stronger model surfaced more useful ambiguity
   in inspected examples, but this is a qualitative exploratory result and does not establish a
   model ranking or semantic accuracy rate.
3. **The interface is partly at fault.** `attributed_to` is an unconstrained string in the JSON
   schema, while the validator expects a local entity ID. The field name and absence of a field
   description make that requirement too implicit. Both models repeatedly return source labels.
4. **Exact evidence validation is valuable.** It exposes collapsed newlines, Markdown-stripped
   metadata, apostrophe changes and ellipsized quotes. We did not silently normalize or repair them.
5. **Exact grounding is not entailment.** Wrong ownership, assignment, approval scope, reported
   versus recorded status, and plan-versus-completion errors survive many structural checks.

## Recommended next experiment (not implemented or run)

Change one factor at a time, using development cases only:

- First, make the attribution contract explicit (`attributed_to_id`, field description, or
  a dedicated typed source-reference representation). Do not auto-map output labels into IDs.
- Then compare a mention-first pass with claims referring to an enumerated mention/entity table.
  This allows dynamic enums for references and reduces identity invention. Preserve raw mentions
  before any merge, and enforce consistent domain/range for all predicates.
- Separate polarity, modality and source status rather than force them into one enum. Add explicit
  conditional authorization and supersession/continuity links for approvals and appointments.
- Annotate a small exhaustive development sample for mention/relation quality before reporting
  precision/recall. Keep the next unseen cases untouched until the revised contract is frozen.

We stop here as recorded in the experiment manifest: no schema repair, silent fallback, third
model arm, or retrospective conversion of invalid outputs into passes.
