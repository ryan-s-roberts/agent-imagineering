# Development decision replay and prompt ladder

## Scope

The initial pass selects **one checkpoint per case 001–040**. Cases 041–050 are excluded.
The target is the first reviewable agency outbound communication after at least one
preceding event. This deterministic early-choice scope is deliberately narrow: it contains
many notifications and approval requests and does not represent every decision point,
later escalation, dispute, closure or alternative branch in those cases.

`experiments/decision-dev-v1.json` freezes the checkpoints. The separate
`annotations/decision-dev-v1-targets.json` retains the later observed message and coarse
candidate response types. Candidate labels had single-author excerpt review before the run;
they are not independently adjudicated gold decisions. System-labelled outbound messages
do not prove a human author. Calls may contain agency and environment speech. Quoted
reports and proposed work inside a message are not additional completed agency actions.

## Leakage boundary

Extraction reads history only through the cutoff. The decision request contains only a
versioned prompt, static response schema, and an explicit development evidence packet.
The packet is constructed from a whitelist of prefix fields and extraction outputs.
Target events, target labels, index summaries and future outcomes are never supplied.
Each target remains in `observed-later.json` for reviewer comparison after generation.

Later message details may not be knowable from the prefix. For example, an observed
booking notification may contain a time and person absent from the earlier state. Matching
that specificity is not required and invention must not be rewarded. A different next
action can be reasonable; a historical action can itself be poorly supported.

## Flexible evidence and results

Extraction uses mention detection, explicit identity linking and typed assertion extraction.
The host canonicalizes unambiguous case/apostrophe/whitespace differences, exact references
misplaced within the same event, and wrapped source quotations while retaining original
offsets and a trace. It derives redundant provenance source lists and cause-container
evidence. These are interface corrections, not semantic repairs. Raw and canonicalized
artifacts are stored separately.

Remaining missing field evidence, unresolved identity and unsupported references stay
visible in the packet's diagnostics. Resolved mentions and parsed records can support a
development decision even when the strict production packet gate would reject them.
The envelope always says `development_diagnostic=true` and
`validated_decision_state=false`. It is never promoted to trusted CRM state.

Response v3 allows empty or wrong action bases to be generated and inspected. Every
response includes a concise review rationale: why selected, literal citations, uncertainties,
assumptions and alternatives. This is an explicit justification, not a private reasoning
transcript. Raw schema-invalid outputs are retained too. A single bounded interface repair
is allowed for JSON/schema failure; requests, responses and errors from both attempts are saved.

## What is checked

1. **Schema parsing:** can the typed response be read? Generation is not blocked by empty basis IDs.
2. **Reference and citation consistency:** do references exist, do source expressions align,
   and are parties/request ranges consistent?
3. **Evidence compatibility:** simple approval scope, completion and lifecycle constraints.
4. **Observed-action correspondence:** intersection of predicted action types with annotated
   historical candidate types. This is not correctness, semantic equivalence or a reward for
   matching an unsupported historical action.
5. **Semantic support review:** human/assistant source review of evidence, assumptions,
   reasoning and actual choice quality. Unreviewed entries remain explicitly unreviewed.

No LLM judge fills missing labels or evaluates the rationale. Corpus indexing retains all
40 cases, including any failures, rather than selecting successful or convenient outputs.
The objective is to eliminate avoidable interface failures before interpreting behavior;
remaining semantic uncertainty is an inspectable model result.

## Frozen prompt ladder

The decision prompt is `experiments/prompts/decision-baseline-v1.txt`. The baseline snapshots
that exact text, response schema, model/settings, implementation source hashes and code,
raw/canonical extractions, exact evidence packet, request hashes and later target separately.

After the baseline, decision-prompt experiments replay those exact cached evidence packets.
Extraction changes belong to a separate ladder. The `--evidence-root` mode verifies the
response schema, model/token settings, selected prefix digest and original packet hash.
It performs no extraction calls. An arm with different schema/model/settings is rejected
as a purported prompt-only comparison.

```sh
uv run python -m property_eval.decision_replay \
  --source /Users/ryan/code/HackatonPublicCases \
  --manifest experiments/decision-dev-v1.json \
  --targets annotations/decision-dev-v1-targets.json \
  --prompt experiments/prompts/decision-baseline-v1.txt \
  --output runs/decision-dev-v1 \
  --env-file /Users/ryan/code/plasm/.env \
  --model openai/gpt-6-luna --concurrency 24 --max-tokens 16000 --timeout 360
```

For a future prompt arm add `--evidence-root runs/decision-dev-v1`, select a new prompt
file and a fresh output directory; keep the other settings fixed. Do not tune the baseline
prompt after seeing outputs and then label the rerun confirmatory. These are development
cases; a later held-out assessment needs a separately locked design and annotation protocol.

## Interruption and continuation

`--resume` continues the same output directory after its original process has stopped.
It verifies the model, token budget, prompt, response schema and manifest, skips completed
checkpoints, and reuses saved provider responses only when their exact request hash matches.
Unfinished original directories are retained under `interrupted-attempts/`; continuation
keeps their raw responses and regenerates deterministic projections. Do not run two
schedulers against the same directory. This initial resume implementation supports one
interruption per unfinished checkpoint; it deliberately refuses to overwrite an existing
archived attempt.

The baseline began at concurrency 3. At the user's explicit request, after 25 completed
checkpoints the original process was interrupted and the remaining 15 admitted with a
concurrency limit of 24. `concurrency-amendment.json` records three unanswered provider
requests (025 decision, 026 records, 028 records). Their billed usage is unknown. Reported
cost sums returned provider usage; it is a lower bound on total billing, not a zero-cost
claim for interrupted requests. Prompt, model, schema and checkpoint selection stayed fixed.
Latency comparisons across this scheduling amendment are not controlled comparisons.

After completion, run `python -m property_eval.decision_alignment runs/decision-dev-v1`
once to apply audited deterministic citation alignment. Original parsed decisions remain
in `decisions-raw-parsed.json`, and the original provider responses are always retained.
This postprocessing changes citations only, never action choices or rationale assertions.

## Viewer artifacts

`corpus-index.json` contains every checkpoint with a root-relative `path` and status.
Each checkpoint has prefix `input.json`/`sources.json`, raw and canonical extraction files,
`evidence-packet.json`, `decisions-request.json`, `decisions-response.json`, parsed
`decisions.json` when available, `decisions-validation.json`, `decision-review.json` and
review-only `observed-later.json`. Citation/rationale failures are displayed as results;
they are not hidden by filtering the index.
