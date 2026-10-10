# Agent-only late checkpoints

`property_eval.agent_action_checkpoints` supersedes the unreviewed last-activity
selection for scoring. Review each case backwards until three assessable agency
episodes are found, or all eligible episodes are exhausted. A failed annotation
blocks that case from the final manifest; it is not silently skipped.

## Target contract

- Only explicit agency acts are accepted. Every target uses the existing result
  ontology's `ObservedAction` projection, preserving unknown fields as null.
- Exact target quotations must isolate the agent's act. Counterparty behavior,
  new information and inseparable mixed summaries are excluded.
- Accepted acts require exact supporting prefix quotations. An act requiring
  information first disclosed inside the episode is excluded. Even an apparent
  internal ordering cannot create a new event-level prefix.
- Workflow actions count when earlier evidence supports them. Intake descriptions,
  classification output and generic call-recording greetings do not qualify.
- Multiple agency acts can remain in one episode. Selecting an episode does not
  accept every act or every sentence in its source events.

Semantic separation is model-assisted annotation, not deterministic proof or
human gold. Python validates exact quotes, occurrences, event membership and
prefix/target partitioning. The original requests/responses, prompt, schema,
implementation, exclusions and usage remain available for audit.

A separate availability audit assesses every candidate action for explicit agency
attribution, required input availability before the episode, and independence from
new episode information. All three must pass. Rejected annotations remain in
`pre-audit-target-actions.json` and `availability-audit.json`; the selector continues
backwards to replace rejected episodes. This additional semantic judgment is still
fallible and is not described as deterministic validation.

The development-only audited round is `runs/agent-only-late-dev-v3`, using cached
annotations from v2 where the request is identical. It implements the general
availability distinction derived in [development causal review](development-causal-review-v1.md).
No holdout content is used for that audit or rubric derivation. V2 is retained as
an earlier, insufficiently audited annotation round, with its failures visible.

## Artifacts

The round's `manifest.json` contains only case/cutoff/split selection.
`agent-only-targets.json` contains accepted actions and their citations; raw mixed
events and the exclusion ledger are not scoring targets. `selection-review.json`
and `reviews/<checkpoint>/` preserve the broader annotation audit. None of these
evaluation-only target records belongs in the decision agent's context.

Cases 041–050 have already been exposed and are labelled accordingly. This pass
selects and annotates checkpoints; it does not regenerate decisions or report
prediction scores.

```sh
uv run python -m property_eval.agent_action_checkpoints \
  --input-dir /path/to/property-cases \
  --output runs/agent-only-late-v1 --env-file /path/to/.env
```
