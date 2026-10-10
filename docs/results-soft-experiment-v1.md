# Soft-target prompt experiment v1: completed development comparison

## What ran

Both frozen arms completed all40 cases: **80 decisions and80 model-assisted judgments**,
with **zero interface repairs or failed jobs**. New returned-response cost was
**$0.66147757**, covering4,533,215 prompt tokens and268,728 completion tokens. The original
extraction cost is recorded separately and was not incurred again. Model: `openai/gpt-6-luna`;
concurrency24; seed42; fixed provider-default reasoning. No further arms were added.

The canonical artifact is `runs/decision-soft-v1/run.json`. Exact prompts, T-boxes, schemas,
requests, raw responses, evidence packets, targets, timings and checks are retained. The
assembler verified the decision payload contains exactly the shared ontology T-box and
prefix evidence; evaluation-only targets and judgments stay outside that boundary.

Both arms received actual evidence schemas, the result schema and common semantics for
identity, provenance, modalities, negation, open-world uncertainty, approval scope and
human intervention. The prior run already had the result JSON schema but lacked the full
evidence T-box and shared interpretation text. Comparisons against that old run are
interface-confounded. The comparison below changes one workflow-progress paragraph only.

## Results, with separate meanings

| Observation | Control | Progress paragraph |
| --- | ---: | ---: |
| Completed decisions / judgments | 40 /40 | 40 /40 |
| Judge: historical match | 2 | 2 |
| Judge: partial correspondence | 13 | 14 |
| Judge: materially different | 24 | 23 |
| Judge: unassessable | 1 | 1 |
| Judge: prediction supported | 15 | 13 |
| Judge: prediction partly supported | 25 | 27 |
| Decision reference/compatibility checks pass | 28 | 29 |
| Clarification actions | 28 | 23 |
| Approval-request actions | 4 | 13 |
| Escalation actions | 7 | 4 |
| Returned cost | $0.32880441 | $0.33267316 |

These are development observations, not an accuracy score. Action counts can exceed case
counts because a response can propose several actions. Historical correspondence and
prefix-supportedness remain independent: reproducing history can require unavailable
information, and a different action may be warranted.

The intervention changed the action mix toward approval requests and away from escalation.
It **did not demonstrate a reliable semantic improvement**. Historical exact matches stayed
at two; the single net movement from different to partial is small, and fully-supported
judgments fell from15 to13. No arm is selected as a validated winner.

## Paired review exposes judge limits

Three cases moved `different → partial`; two moved `partial → different`. Inspection of all
five changed labels shows that several changes concern nearly equivalent proposed acts:

- **016:** both arms ask for the approval contact/scope; judge labels shift partial→different.
- **023:** both ask the agency for provider/category/approval-recipient details; labels shift
  different→partial despite little material change in the proposed next step.
- **026:** both escalate to a property manager to resolve the approval route; labels shift
  different→partial.
- **025:** a material change from property-manager escalation to agency clarification;
  both still differ from the historical direct landlord approval request.
- **028:** clarification becomes no proposed action because request identity is absent;
  the judge calls it historically different but supported. Supported abstention is not
  equivalent to useful workflow progress.

This assistant source review is qualitative and exploratory; it does not replace the saved
judge labels. It shows why a one-judgment categorical difference should not be treated as
proof of a prompt gain. The same model judged its own model family's outputs, creating
additional shared-bias risk even though arm labels and decision prompts were hidden.

Target predictability changed between arms in **five cases**, although target and prefix
were identical. Those changes indicate judgment instability, not changes in information
availability. Exact judge-citation checks found **31 invalid expressions in15 judgments**
(19 expressions/9 control judgments;12 expressions/6 progress judgments). Many concern
JSON whitespace/order in prediction quotations, but there are also misattributed sources
and nonliteral target quotations. All raw judgments and failures remain visible; no labels
were repaired or excluded to improve results. Quote alignment alone would not prove entailment.

The judge also raised target-encoding concerns in33/80 assessments. Examples include
normalizing a generic contractor-attendance question to the narrower `inspect` scope, and
compressing a message with several intents into its primary act. These are advisory concerns
for annotation review, not retroactive changes to frozen targets or automatic proof that the
annotations are wrong. They further limit interpretation of small correspondence changes.

Case **010** is a useful positive check of the separation: both arms ask what the vague June
notes refer to. The historical message asks for solar-panel readings, absent from the prefix.
Both judges classify correspondence as different, predictability as unobservable, and the
clarification as supported. A coarse action-type match would have concealed that distinction.

## Annotation review and remaining scope

Targets were hand-authored as partial projections of result action types, with unknown
request identity and prefix actor mappings left null. An independent agent reviewed seven
cases before generation. This removed an invented notify action from035, separated038's
replacement approval from its removal-cost question, and preserved012's checks-before-engineer
condition. The other33 targets have single-author source review, not independent adjudication.
No target claims independently verified safety, authority, liability or completed work.

The40 selected prefixes precede the first reviewable outbound agency communication. They
are not comprehensive decision-point coverage and were already exposed during development.
No held-out performance or deterministic semantic-truth claim follows from this run.

## What this gives the next iteration

1. **A usable prompt comparison boundary:** freeze both T-boxes and evidence, vary only the
   decision prompt, and retain all predicted choices plus independent correspondence/support
   dimensions. The current paragraph is a candidate behavior change, not a proven winner.
2. **A measurable representational bottleneck:** some actions demand a resolved request or
   recipient ID even when the source establishes only a role or partial case context. Both
   arms often clarify bookkeeping before making the historical workflow choice. A future
   result-ontology experiment should represent unresolved role/request references explicitly
   for proposals; this must be a separate interface experiment, not hidden prompt tuning.
3. **A judge-quality task:** use source-addressed field citations and independently reviewed
   calibration examples, then assess repeated or independently judged agreement. Current
   free-form prediction JSON quotations and category boundaries are too brittle to support
   small headline gains. Keep unavailable historical specifics outside predictive penalties.

Validation:38 local tests passed after implementation, including both-T-box input boundaries,
target unknown identity, citation checks and canonical experiment artifact checks. No new
dependencies, commits or pushes were introduced.
