# Evidence → response rubric v1

## Two separate questions

1. Was the proposed action warranted by what the decision agent received?
2. Did it correspond to an assessable historical **agent** action?

Evaluate the first without historical targets. Evaluate the second separately,
using only the accepted agent-action annotations. Neither historical occurrence
nor a valid source quotation proves a sound decision. Do not combine these into
one accuracy percentage. Freeze this rubric before evaluating the new late-prefix
population; do not reinterpret the completed early-prefix ablation with it.

## Unit and information boundary

The response is a set of zero or more actions, with explicit dependencies and
model-authored rationale. Score each action and then set-level progress. There is
no reward for cardinality itself. Distinct recipients, material effects and necessary
workflow changes can justify multiple actions; paraphrases do not create new work.

The evidence judge receives the exact evidence packet, evidence/result T-boxes and
generated response. It receives no historical target, excluded turn, later outcome
or summary. It must distinguish source claims, reported claims, extracted assertions,
unresolved identity, model assumptions and verified facts according to the ontology.
An extracted claim is not true merely because it has an assertion ID.

## Per-action assessment

| Dimension | Assess | Do not infer |
|---|---|---|
| References | Action/request/entity/record IDs exist; cited spans resolve exactly; dependencies reference this response and are acyclic | Semantic support from reference validity |
| Evidence availability | Required reports, documents, replies and authorizations are available at the cutoff | Waiting for a report means the report has arrived; a future attachment was available earlier |
| Evidence warrant | Cited assertions entail the action's premise, request scope, recipient role, amount and timing; preserve polarity, attribution and conditions | Tenant report → verified repair; proposed appointment → confirmed booking |
| Authority and preconditions | The **proposed effect** respects explicit approval/access/verification gates | Requesting approval means approval exists; missing policy means prohibition |
| Epistemic calibration | Reported, inferred, conditional and unknown information remain qualified | Unknown name means unknown role identity; missing evidence means evidence of absence |
| Necessary dependencies | Required gates precede dependent actions; independent supported actions can proceed | Every timestamp ordering is a causal dependency |
| Rationale fidelity | Saved rationale accurately identifies the evidence and explains this choice without adding facts | A coherent explanation repairs unsupported action slots; invented private reasoning |
| Relevance and progress | Action advances an evidenced request or removes a material blocker | Unnecessary clarification, circular escalation or a redundant wait is progress |

Each semantic dimension is `supported`, `partly_supported`, `unsupported` or
`unassessable`, with prefix-only citations and a short explanation. For missing
evidence, explicitly describe the inspected slot/requirement; do not fabricate a
quotation proving absence. `unassessable` is visible and never counted as a pass.
Structural checks remain deterministic and are reported independently.

### Proposal semantics

A request for approval can be supported without approval existing. An unconditional
instruction to perform work cannot satisfy an explicit approval gate by mentioning
approval in the rationale. A dependent future proposal can be supported when its
dependency and condition are represented by the response ontology. If the ontology
cannot express a required condition, report a representational limitation rather
than silently crediting prose as an executable gate. No proposed action is execution.

## Set-level assessment

Identify material obligations from **prefix evidence only**, citing each one. These
are advisory interpretations, not a second hidden gold action sequence. Map proposals
many-to-many to obligations; report covered, partly covered, unmet or unassessable.
Credit reasonable alternatives that satisfy the same obligation. Group duplicates
and waits attached to an existing request so they cannot inflate coverage. Preserve
unresolved blockers locally: one unresolved issue need not block unrelated supported
work. Score an empty response against the explicit situation; neither automatic
failure nor vacuous success is allowed.

Report counts for all proposed actions, unsupported actions, unassessable actions,
duplicates, unmet material obligations and violated explicit gates. Show each
dimension's denominator and uncertainty. No arbitrary weighted composite is defined.

## Error attribution

First assess the decision against the packet it actually received. Separately audit
the packet against available source events and attachments. A missing or distorted
source fact is an extraction error; a response that ignores or overstates a correctly
represented fact is a decision error. An ontology unable to represent a necessary
fact/condition is a representation error. More than one cause can apply. Never use
later evidence to retroactively blame the decision agent for unavailable information.

## Historical comparison

Match accepted agent actions by intent/effect, role, scope, conditions and necessary
dependencies. Permit 1:N and N:1 correspondence. Missing historical behavior and
unsupported predicted behavior are different findings. Supported alternatives remain
valid even when historical correspondence is low. Counterparty acts and inseparable
information-dependent acts have no target rows and cannot enter recall denominators.

The agent-only late selection intentionally excludes unassessable target actions;
report how many episodes/actions were screened out. Its correspondence scores are
conditional on this selection and must not be described as coverage of all case work.

## Implementation status

Development-source rationale and counterexamples are documented in
[development causal review](development-causal-review-v1.md). Cases and quotations
in that review are audit material, not decision-prompt examples. No holdout cases
were used to derive the rules.

`evidence_response_judge.py` defines the separate assessment schema, exact per-action
coverage validator and target-free payload boundary. Its prompt is versioned under
`experiments/prompts/evidence-response-v1.txt`. This is a new evaluation contract;
no evidence-response-v1 scores have yet been produced. Existing episode-judge-v1
scores retain their narrower historical/support interpretation.
