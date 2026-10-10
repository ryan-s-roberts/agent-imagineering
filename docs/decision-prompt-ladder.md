# Evidence-to-choice prompt ladder

The primary intervention after baseline is the prompt mapping a fixed evidence packet into
the result ontology. Extraction and decision generation are separate experiments.

## Baseline freeze

Retain each checkpoint's exact prefix/evidence packet, extraction diagnostics and content hash.
Retain the exact decision prompt, result JSON schema, provider model and decoding settings,
raw request/response, usage, latency and validation results. Targets belong in a separate
evaluation artifact and never in the request. Cases041–050 are excluded from development.

Development includes all forty selected checkpoints. Pure syntax/interface failures are
pipeline defects to fix before accepting the baseline, not meaningful task failures to score.
Derive redundant metadata, align source text with an audit trail and perform bounded interface repair.
Parsed evidence with semantic support gaps must be explicitly marked diagnostic input rather
than silently relabelled validated state. Preserve raw model output and every repair.

## Later rungs

Change only the decision prompt. Reuse identical serialized evidence packets, response schema,
model/settings and scoring definitions. Do not change ontology, examples, extraction, selection
or token budget in the same claimed prompt comparison. Freeze each hypothesis and stop rule
before running. Label iterative development results as such; use an untouched evaluation
round for a generalization claim.

Candidate interventions after baseline review include explicit evidence-to-action mapping,
attention to uncertain identity and permission, or structured comparison of permitted choices.
These are hypotheses, not a prescribed winner. Do not paste development target actions or
near-duplicate examples into the prompt and call that general improvement.

## Outputs to inspect

Each decision has a typed action, citations and a concise explicit rationale: evidence relied
upon, relevant uncertainty, assumptions and why this choice follows. This is a user-facing
justification, not access to hidden reasoning. It may be wrong, contradicted or poorly supported.

Keep separate measures for schema/reference validity, grounded citations, observed-action
correspondence, unsupported assumptions, human-escalation causes and semantic decision quality.
Only the first measures can currently be mechanically established. Human/assistant-reviewed
labels should show who reviewed them and which cases remain unreviewed; no LLM judge is implied.

An observed action is not automatically a gold normative answer. A grounded escalation can
differ from an unsafe or under-evidenced historical action. Conversely, a historical match with
invented authority must not receive full correctness credit. Multiple defensible alternatives
need explicit annotations rather than fuzzy scoring invented after seeing a model answer.
