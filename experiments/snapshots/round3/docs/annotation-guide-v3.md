# Frozen annotation guide — property-evidence-v3 / round 3

This is an authored static ontology. The extractor instantiates its classes; it does
not discover new classes at runtime. `models.py`, `prompt.py`, `grounding.py`,
`validation.py`, `scoring.py`, this guide and the experiment manifest are frozen by
SHA-256 in `experiments/round3-freeze.json` before evaluation annotation is opened.
Changes after that point require a new round and must not be silently rescored.

## Three stages and identity

1. Detect mentions with class, literal expression, source line and mandatory one-based
   occurrence. Code resolves event-relative Unicode codepoint offsets.
2. Predict explicit same/different/unresolved mention links with source evidence.
   Only same links union entities; no implicit name similarity or string-equality merge.
3. Extract typed assertions using that fixed entity table and field-level evidence.

Mention IDs are `case:event:start:end` and stay stable if their exact span remains
present. Entity IDs use the lexicographically smallest mention anchor in an equivalence
class. They are case-local and prefix-local: a changed partition or newly detected
earlier anchor may change them. Consumers compare explicit mention membership across
prefixes, never assume an entity ID is a stable external CRM identifier. There is no
cross-case identity or persisted incremental merge mechanism in this round.

Same-link evidence must establish reference continuity: explicit aliases, repeated full
identifiers in the same continuing role, or unambiguous anaphora. Similar names, initials,
roles and recipients alone are insufficient. Record uncertain links without merging.
Entity labels are display text, never the matching key. Proposed and current assets differ.

## Assertions and evidence

Each populated scalar/list field receives its own evidence entry; lists may require
multiple spans. Null/empty fields mean not established. Ground provenance origin,
modality and polarity separately. For attribution, distinguish recorder from reported
speaker; unknown speaker stays null. System transactions and quoted reports differ.

Evidence retains submitted expression, original source expression, event-relative
start/end, source ID, occurrence and alignment mode. Exact matching is preferred.
The sole permitted alignment transforms U+2018/U+2019 apostrophes to ASCII apostrophe
for matching, preserving character counts. Both strings are retained and flagged.
No other Unicode normalization, fuzzy matching, paraphrase search or quote repair occurs.
Structural grounding proves location, not entailment or completeness.

Use controlled roles, issue, ownership, assignment, authorization, appointment, work
report, status, obligation and identity records. Additional choice-supporting types:

| Type | Decision variables |
| --- | --- |
| work_proposal | Proposed activity/asset/provider, quoted amount/currency, validity, conditions |
| access_constraint | Availability, keyholder, notice or entry permission, time and restriction |
| communication | Sender/recipient, purpose, requested/answered/reported nonresponse, response-to and deadline |
| condition | Requirement constraining a record, satisfied/contradicted/unknown, original clause |

Positive approval is limited to its stated activity, amount and conditions. Proposed
price is not authorized spend. Missing evidence is not a negative fact. Planned work is
not completed work. A closure transaction does not prove all prerequisites. Referenced
times remain text; recording timestamps remain in source units. No universal authority,
legal or closure policy is inferred from these histories.

## Reviewed reference protocol

The author reads ONLY the selected prefix and annotates targeted mention/assertion/link
probes before either model arm runs. This is a single-author review, not independent
adjudication. Store source digest and exact evidence expressions. List genuinely acceptable
alternatives explicitly; never choose a unique entity identity solely to make scoring easy.
Avoid free-text descriptions as exact semantic targets. Score controlled values and evidence.

This small round uses targeted probes, not exhaustive annotation of all facts. Report
reviewed probe recall and structural validity separately. Extra predictions are unjudged;
do not label the result precision, F1, global extraction accuracy or decision readiness.
Each assertion probe names choices it could support. That maps evidence coverage, not
the correctness or admissibility of any proposed action. Full choice coverage needs more
reviewed examples, including changed-fact counterexamples, after this bounded round.

The evaluation case is untouched by this round's prompt/ontology tuning, but the earlier
corpus survey and incomplete exposure log prevent calling it a pristine unseen holdout.
Do not modify prompts, annotation rules, metrics or alternatives after viewing model output.
