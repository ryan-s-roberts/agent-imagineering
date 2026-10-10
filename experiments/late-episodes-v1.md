# Late decision checkpoints

**Superseded for scoring:** use the [agent-only late checkpoint procedure](../docs/agent-only-late-checkpoints.md).
The activity-block manifest below is retained only as the initial candidate audit.

The early-prefix run chiefly measured intake. This selection targets the last
three agency activity episodes per case. It currently yields 148 checkpoints
across 50 cases; cases 014 and 035 have two eligible episodes.

## Reproducible candidate selection

`property_eval.late_checkpoints` recognizes the three agency sender labels found
in this corpus. Email, SMS, Call, Hold and Update qualify an activity block;
adjacent agency notes are included. A non-agency event or an inactivity gap over
60 minutes ends the block. The time threshold is a session heuristic, not an
inferred timer event. Blocks starting at event 1 cannot supply a nonempty prefix.
Choose the last three remaining blocks. The prefix stops immediately before
the first event in each block. Every available earlier event and prefix-linked
attachment belongs to input. No summary, target or later attachment belongs to it.

Manifest: `late-episodes-v1/manifest.json`. Evaluation-only source blocks and
boundary flags: `late-episodes-v1/boundary-review.json`.

## Review still required before semantic scoring

These are candidate boundaries, not reviewed result-ontology annotations.
Nine contain calls which can mix agent behavior with newly received information.
Eighty-three contain workflow activity only. Preserve these strata. Inspect mixed
turns for unobservable information, and mark ambiguity rather than demanding that
the agent predict the other party's reply. Subsequent annotation must retain source
spans and 1+ action cardinality. No predictions or scores have been run on this set.

Case 001 now has cutoffs 37, 38 and 40, targeting events 38, 39–40 and 41–44.
The original cutoff-3 run is retained as a separate early-prefix baseline.
Cases 041–050 are previously exposed, not a fresh untouched holdout.

## Artifact layout

Multiple checkpoints remain separate. `ANSWERS/<case>/ANSWER.md` is a linked
checkpoint index; full answers live at
`ANSWERS/<case>/checkpoints/<checkpoint>/ANSWER.md`, with matching `REASONING.md`.
Every answer links to the complete canonical run JSON. One-checkpoint case exports
retain their existing direct `ANSWERS/<case>/ANSWER.md` layout.
