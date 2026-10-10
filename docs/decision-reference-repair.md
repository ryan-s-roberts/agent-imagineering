# Decision reference repair

`property_eval.decision_repair` runs at most two model repair rounds when the
deterministic response validator rejects the structural reference contract.
Each round may additionally use the existing single JSON/schema repair.
The model receives the frozen evidence and both ontologies, the prior proposal,
validation errors, permitted request entities and action-to-record request mappings.
Request fields are constrained to supplied request/work-order IDs when available.
No historical target or judge feedback enters this process.
Compact identity aliases and a stable evidence message are reused across repair
rounds; changing diagnostics are appended last to preserve prefix-cache eligibility.
Only provider-reported cache usage counts as observed caching.

The model authors the replacement response and rationale. The host does not
merge identities, rewrite action semantics or invent citations. Citation alignment
continues to resolve source offsets separately. Acceptance requires structural
validity; evidence compatibility and semantic warrant remain separate checks.
An exhausted budget retains the original response as explicitly unresolved.

`decisions-before-reference-repair.json` preserves the original proposal.
Every round saves its request, provider response, parsed response, alignment,
validation and timings. `decisions-resolution.json` identifies the accepted stage
and before/after validation. `decisions.json` is the accepted model response.
The canonical report includes all attempts, usage and the original proposal.

For a finished run created before the repair hook was installed:

```sh
uv run python -m property_eval.decision_repair --run runs/late-dev-eval-v1 \
  --env-file /path/to/.env
```

The standalone phase uses 24 concurrent calls and writes a protocol amendment,
implementation snapshot and phase summary. Apply it before running judges.
Existing resolutions are preserved on resume. This amendment changes the evaluated
pipeline; repaired results must not be presented as original first-pass validity.
