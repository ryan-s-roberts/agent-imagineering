# Contextual-party benchmark contract v1

The user explicitly supplies this assumption: **the landlord and tenant are known and
addressable through the case/property context**. Missing names or CRM IDs do not block
contacting those roles and must not, by themselves, cause clarification or human escalation.

This is benchmark context, not an extracted observation. `BenchmarkContext` records
`provenance=benchmark_assumption` and `authority=explicit_user_instruction`; it is supplied
separately from the immutable prefix evidence. Extraction continues to leave omitted names
and uncertain identity links unknown. No synthetic named person is added to the entity table.

Response ontology v4 party-reference fields accept either an observed entity ID or a typed
contextual reference: `{kind: contextual_role, role: landlord|tenant, case_id: ..., provenance:
benchmark_assumption}`. The latter must match a binding supplied for the same case. These
are distinct semantic reference forms. Provider IDs are not supplied by this assumption.
Request identity, approval, authority scope, attendance, completion and document contents
are not supplied by the assumption either.

Use the known contextual role when proposing a communication or approval request even if
names or delivery-system IDs are omitted. Genuine conflicting relationships, ambiguous
applicable properties or other material uncertainty still require appropriate handling.
The assumption does not turn reports into facts or authorize work. An approval request to
the known landlord is not approval granted.

The new contextual baseline uses the same40 prefix evidence packets and historical target
events with this explicit context and response v4. It is a deliberate benchmark/interface
amendment, not a pure prompt-effect comparison with earlier runs. Old predictions and
judge-only citation-v2 results remain under their original assumption. No historical score
is retrospectively rewritten.

The contextual judge knows the same contract and separately records whether it relied on
benchmark context. Its factual-support citations still select original prefix spans;
addressability is justified by the declared contract, not a fabricated source quote.
