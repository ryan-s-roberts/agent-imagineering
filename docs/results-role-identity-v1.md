# Model-extracted role identities: development diagnostic

All seven selected early prefixes and the separate case012/event021 contrast completed.
The run made 39 calls to `openai/gpt-6-luna`, costing **$0.14269695**. No interface repair
was needed. All127 selected judge citations resolve exactly. Primary calls cost$0.11405071;
the separate contrast cost$0.02864624. The earlier runs remain unchanged. Forty-seven focused/repository tests pass.

This intervention changes the evidence ontology to v5, extraction teaching, fresh model
extraction and decision role semantics together. It is **not** a pure prompt ablation or
an unseen-case performance claim. The seven prefixes were selected because previous
outputs exposed identity blockers. Historical targets were absent from extraction and
decision inputs. Eight pipelines ran concurrently; the contrast has no historical judge
and is excluded from the primary denominator.

## What the model did

| Prefix | New saved decision | Identity finding |
|---|---|---|
| 011/003 | Seek approval to inspect/quote | Landlord role extracted and addressed |
| 016/002 | Seek inspection approval | Landlord role extracted and addressed |
| 025/002 | Seek inspection approval | Landlord role extracted and addressed |
| 026/003 | Escalate for approval | Mention detector omitted the explicit landlord role |
| 028/002 | Seek inspection approval | Landlord role extracted and addressed |
| 035/003 | Seek inspection/repair approval; clarify access | Landlord role extracted; unanswered access/isolation remains |
| 038/003 | Seek replacement approval | Landlord role extracted and addressed |

Six of seven directly use the model-extracted landlord entity. The host neither creates
role entities nor substitutes decisions. Names and imaginary CRM IDs cease being blockers
in those six. All seven primary decision reference checks pass; this does not establish
that the actions or proposed scopes are correct. Extraction diagnostics remain:016 has two
missing party-field evidence spans,035 lacks a condition-field span, and038 includes an
unmatched property mention and condition expression. The diagnostic packet retains these
issues; decision reference validity does not erase extraction coverage/grounding defects.

Case026 is a real remaining extraction failure: event003 literally contains “landlord”,
but mention detection omitted it. The assertion stage describes an approval obligation
without an identified landlord entity; the decision then escalates for a missing recipient.
There is no competing landlord in the prefix. Fixing that needs extraction coverage rather
than declaring the downstream action correct or fabricating an entity after the fact.

The advisory judge labels six historical correspondences partial and one unassessable;
five decisions partly supported and two supported. All seven targets are partly observable.
These are model-assisted assessments, separate from identity coverage. Limited inspection
scope is often an explicitly declared assumption; removal of a name blocker does not prove
that scope is supported or historical specificity is predictable.

## Separate later012 contrast

The model preserves Riverside Compliance, Cedar Utilities and Meadow Services as distinct
labels with unexplained linkage. It also notices Turner/Kendall, while retaining an
addressable case-scoped tenant for clarification. This demonstrates that role usability
need not require resolving every personal-name discrepancy.

Residuals remain visible:

- Its description calls reports “incompatible” and the name discrepancy a “conflict”. The
  source establishes differing labels, not proof of distinct competing real-world actors.
- The proposed work-outcome question follows an announcement of arrival in about15 minutes;
  observed attendance/completion is absent, so past-tense follow-up may be premature.
- Two `cross_request_evidence` checks expose fragmented task/context linkage. These remain
  reported; the output is not promoted to a fully validated state.

The contrast has no scored historical target. Do not blend it into the seven-case result.

## Artifacts

`runs/role-identity-v1/experiment.json` freezes the design; `implementation-snapshot.json`
retains source and hashes. `role-review.json` records the independent assistant inspection.
`summary.json` retains all eight results and stage usage. The canonical `run.json` embeds
prefixes, fresh evidence, decisions, citations, targets, judges and the separate contrast;
`index.html` is its deterministic review projection.
