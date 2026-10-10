# Evidence must support the choice ontology

This is a design requirement, not a property established by passing JSON validation.
The extraction ontology and response ontology form one contract. Every proposed choice needs
evidence arguments, and every missing prerequisite needs an explicit unknown or conflict.
Do not discard a fact because it is inconvenient to the entity schema if it can change a choice.

## Backward coverage from choices

| Choice | Evidence needed | Current representation | Outstanding limitation |
| --- | --- | --- | --- |
| request_clarification | Request, specific ambiguity, parties implicated and source of ambiguity | gaps, issue/identity records, contextual roles | A detected gap is supported; undetected missing information is not measured. |
| request_approval | Scope being proposed, asset/request, relevant grantor, existing approval and restrictions, proposed cost if any | authorization, issue, roles, gaps | No dedicated proposed-work/quote-price record; proposed amount can lack typed support. |
| instruct_provider | Correct provider/request, exact permission scope, grantor/grantee, spending cap, conditions and evidence that applicable conditions hold | assignment, authorization, roles, issue | Conditions are prose; satisfaction and authority policy are not mechanically established. |
| propose_booking | Request/provider, access party, existing booking, time window, availability and access constraints | appointment, assignment, roles | No typed availability/access/keyholder constraints; time remains text. |
| request_work_report | Assigned provider, relevant appointment, expected report, existing completion evidence | assignment, appointment, obligation, work_report | Absence from extraction cannot prove absence from the prefix. |
| propose_closure | Completion report, required confirmations, remaining obligations, key-return/invoice evidence, unresolved conflicts | work_report, obligation, request_status, gaps | No comprehensive policy prerequisites or typed obligation dependency graph. |
| escalate | Request, conflict or unresolved prerequisite, parties and prior attempts | gaps, identity, obligation, source lines | Contact-attempt chronology and escalation thresholds are not structured. |
| await_response | Outstanding request to a responsible party, what is awaited, whether reply arrived and any deadline | obligation, appointment, roles | No typed response-to links, deadlines or full satisfaction tracking. |

**Conclusion:** v2 provides a useful evidence vocabulary but does not yet satisfy the entire
choice contract. The decision agent must not be declared ready on these records alone.
Raw sources remain in the packet, but requiring it to re-extract omitted decision variables
would defeat the intended boundary. Review and fill these gaps before a decision benchmark.

## Required ontology extension, before freezing

Introduce sourced proposed-work and quote-line records (activity, asset, amount/currency,
issuer, validity and conditions); access/availability constraints; communication requests and
response links; and typed prerequisite/condition clauses with satisfied, contradicted or
unknown evidence. Connect obligations to the action or request they constrain. Preserve
literal condition text alongside typed clauses. Unsupported clause types remain unknown.

Represent observation time separately from referenced event time. Never convert a missing
timestamp or uncertain speaker into a fabricated value. Include authority rules only when
provided by the task/environment or explicitly sourced; they cannot be inferred universally
from these histories.

## Acceptance criteria

For every choice type, build reviewed prefix examples where changing one evidence fact changes
the admissible choice, including scope, amount, identity, conditionality and timing. Extract
the required fact and its provenance without a decision model. Score these fields directly.

Distinguish **present**, **explicitly denied**, **not observed**, **conflicting**, and
**unrepresentable**. A decision may ask for clarification when a prerequisite is unknown;
unknown must not silently become permission or a hard factual denial.

Run two evaluations: decisions on reviewed evidence, and decisions on extracted evidence.
Their difference measures extraction-induced decision error. A structurally valid proposal
and a citation to a real line are necessary checks, not proof that the choice is warranted.
Do not use an LLM judge to bridge missing ontology or missing reference annotations.
