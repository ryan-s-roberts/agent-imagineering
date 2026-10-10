# Decision cardinality audit

The frozen baseline already says “Choose one or more reasonable next actions”. The response
schema has an action list and `depends_on_action_ids`; the validator requires dependencies to
refer to earlier actions. The defect was not a singular-action schema. The opening sentence
uses singular “next ... action”, and the teaching does not define the full current-knowledge
agency episode or distinguish completeness from gratuitous extra actions.

The first historical target annotation selected one outbound event, often an auxiliary notice,
while the corresponding decision episode contains other instructions and workflow writes.
The single-event judge inherited that target-unit bias. Correcting targets and rescoring frozen
predictions comes before attributing any improvement to decision prompts.

Frozen output cardinalities:

- Control:36 single-action responses,2 double,1 triple,1 empty;43 actions and1 dependency.
- Progress:35 single-action responses,1 double,1 five-action,3 empty;42 actions and0 dependencies.

`experiments/prompts/decision-actionset-candidate-v1.txt` is a separately authored, **unexecuted**
domain-general candidate. It defines the present knowledge boundary, distinct supported effects,
communications plus administrative actions, parallel independence, necessary dependencies,
conditional later work and valid wait/conclusion. It avoids requiring a large action count or
introducing case-specific examples. No frozen prompt or prediction was changed.

A later comparison must freeze evidence, both T-boxes, schema, model/settings and the episode
judge. It must also state whether it uses the older evidence with known role-extraction defects
or freshly extracted evidence; changing both is not a pure decision-prompt comparison.
