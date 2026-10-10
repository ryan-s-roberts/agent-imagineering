# Decision development baseline v1

## Completed run

All **40/40** development checkpoints produced a parsed response with explicit rationale
and source citations. The model was `openai/gpt-6-luna`. Each checkpoint ran mention
detection, identity linking, typed assertion extraction, then one decision request.
There were **160 returned provider responses, zero schema repairs and zero final interface
failures**. Cases 041–050 were excluded.

The frozen prompt is `experiments/prompts/decision-baseline-v1.txt`; artifacts live in
`runs/decision-dev-v1/`. `audit-summary.json` holds the derived counts and integrity checks.
`corpus-index.json` retains every case. Targets remain review-only in `observed-later.json`.

| Observation | Result | Interpretation |
| --- | ---: | --- |
| Parsed decisions | 40/40 | Interface completion, not decision correctness |
| Rationale citations aligned to supplied source | 40/40 | Text grounding, not entailment of the choice |
| Citation normalization changes / unresolved citations | 0 / 0 | Decision citations already matched source |
| Cases passing current reference/compatibility checks | 26/40 | Limited deterministic checks, not semantic accuracy |
| Cases with retained reference/compatibility issues | 14/40 | Visible failures or unresolved evidence relationships |
| Coarse overlap with historical candidate action types | 8/40 | Descriptive correspondence only |
| Reported returned-response cost | $0.2699253 | Lower bound; three interrupted calls have unknown billing |
| Returned prompt / completion tokens | 1,125,809 / 304,444 | Provider-reported usage across completed stages |

The retained check occurrences are 22 `cross_request_evidence`, 10 `invalid_request`,
one `missing_actions`, and one `wrong_case`. These are occurrences, not distinct cases.
No record or response was silently repaired to make those semantic/reference checks pass.

## Behavior observed

The model selected 24 `clarify`, nine `escalate`, five `act`, and two `wait` dispositions.
Across their action lists it produced 27 clarification requests, nine escalations, four
approval requests, four waits and one document action. A response can contain several
actions. This is a strong tendency toward seeking information or human intervention in
these partial evidence packets; the run alone does not establish whether that tendency is
appropriate. It may reflect extraction gaps, request identity fragmentation, thin prefixes,
the prompt's uncertainty handling, or model behavior. Those causes require separate review.

The historical target types often describe notification or approval messages. The observed
type overlap must not be labelled an accuracy score: the next historical action may contain
information absent from the prefix, and alternative actions can be reasonable.

Case 010 illustrates the distinction. The prefix contains vague timing language about June;
the model asks what that refers to and retains uncertainty. The later agency action requests
a solar-panel photo, a topic not recoverable from that prefix. Both are classified broadly
as clarification, so the type overlap hides a substantial semantic difference. Inventing
the later photo request would not demonstrate grounded prediction. The model also uses the
case identifier where a request entity is required, which remains a reference failure.

## Integrity and execution amendments

All 40 evidence packet hashes match their saved decision review. All decision user payloads
are exactly those frozen packets. No target event, candidate label or suffix was supplied
to the decision request. The response schema, prompt, model, settings and implementation
are snapshotted in the run directory. Original parsed decisions and provider responses
remain available alongside deterministic checks.

At the user's request the initial concurrency of three was raised to 24 by stopping the
original scheduler after 25 completed checkpoints, then resuming the remaining 15. Completed
checkpoints were not rerun. Saved stage responses were reused only when their request hash
matched. The incomplete original directories are preserved in `interrupted-attempts/`.
Three unanswered calls—025 decision, 026 records and 028 records—have unknown billing;
`concurrency-amendment.json` records them. They are not counted as zero cost. Resumed job
latencies measure continuation only, so this run cannot support controlled latency claims.

Offline citation alignment was applied uniformly after all generation completed. It made
zero changes. That stage preserves original parsed responses and never alters choices,
rationale assertions or entity references.

## Limits and next comparison

These are first outbound agency choices, one per case, rather than exhaustive decision
points or a balanced sample of escalation, scheduling, closure and dispute resolution.
Targets have single-author excerpt review; they are not independently adjudicated gold.
The development diagnostic packets explicitly retain unsupported fields and unresolved
identity. They are not authoritative CRM state. Exact quotation does not establish that a
cited observation entails an action or that an escalation's stated cause is justified.

Future decision prompt arms should use `--evidence-root runs/decision-dev-v1` and a new
output directory, holding model/schema/checkpoints/evidence fixed. Extraction improvements
belong to a separate experiment. Semantic support and observed-action correspondence must
remain separate review dimensions; no LLM judge or automated rationale-correctness score
was used here.

Validation: `uv run pytest -q` passed **27 tests**, including cached response reuse without
network and refusal to reuse a response for a changed request. Focused Ruff checks passed.
