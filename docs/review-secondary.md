# Manual development review: four property prefixes

Reviewed saved `input.json`, `extraction.json`, `result.json`, and
`validation.json` under `runs/phase1-baseline` for jobs 003-at-010, 020-at-012,
038-at-013, and 045-at-010. Baseline model: `openai/gpt-4.1-mini` served by
OpenAI. This is qualitative agent inspection of source and outputs, with no
additional LLM judge calls and no semantic accuracy percentage. No full future
histories or attachments were consulted. Case 045 is now exposed for review;
these findings must not become silent tuning on a claimed pristine holdout.

All four baseline outputs were retained and correctly flagged `invalid_graph`.
Their semantic errors matter separately from those structural failures: fixing
IDs and quotes alone would leave important wrong relations intact.

## 003-at-010: estimate, contractor instruction, approval

Artifacts: [input](../runs/phase1-baseline/003-at-010/input.json),
[extraction](../runs/phase1-baseline/003-at-010/extraction.json),
[validation](../runs/phase1-baseline/003-at-010/validation.json).

Supported successes:

- Extracts the precise address, the combined cleaning/removal/carpet request,
  Bennett's signature, and Northbridge Lettings.
- Claim c3 preserves the recorded hold, and c4 notices the explicit event010
  approval. The general approval finding is supported even though its subject
  representation is too broad.

Problems:

- The property is typed `asset`, and Theo Quinn is typed `role` instead of
  `person`. A named human and their contextual role should be distinct.
- c2 claims the request is assigned to Bennett as `recorded`, citing only
  event002, “Maintenance provider assigned.” Bennett appears in event007 as a
  contractor correspondent. Identity inference is plausible but is not the
  recorded fact evidenced by event002 alone.
- c4 transfers “Estimate approved” onto the request as a generic approved
  status. There is no Quote entity, approval scope, or representation of the
  event009 “Received :) Please proceed” instruction.
- Event004 references a checkout report and another attachment, but no Document
  is extracted. Event007's ambiguous attachment reference also disappears.
- No unresolved item preserves the unnamed provider in event002 or the identity
  of the received estimate/attachment. `unresolved` is empty.
- Entity quotes for events004 and009 reuse “property at ...” wording from
  event003 although those events say “Address: ...”. The deterministic validator
  catches both. It also catches unresolved attribution labels used where IDs
  were required.

## 020-at-012: inspection rescheduling

Artifacts: [input](../runs/phase1-baseline/020-at-012/input.json),
[extraction](../runs/phase1-baseline/020-at-012/extraction.json),
[validation](../runs/phase1-baseline/020-at-012/validation.json).

Supported successes:

- Preserves the original 13 February morning window and the replacement
  15 February afternoon window, plus the exact recorded 11:00 and 14:00 times.
- Retains the tenant's rescheduling request as a request and relates both
  appointment representations to the correct address.
- Keeps Oakfield Services and Northbridge Lettings as distinct organizations.

Problems:

- c4 assigns the first appointment to Oakfield Services based only on the SMS
  signature; c8 assigns the replacement to Northbridge Lettings based on message
  metadata. Sending a notice does not establish inspection assignment.
- Creates two appointments without a supersession/rescheduling relationship or
  explicit unresolved identity. A downstream consumer can interpret both as
  active bookings. Separate versions are acceptable only if their relationship
  is retained; the history does not require two independent visits.
- Event006 says “Friday, 15th February”; 15 February 2024 was Thursday. The
  extraction preserves the phrase in evidence but reports no unresolved
  calendar inconsistency. Date normalization needs an explicit conflict policy.
- The announced time windows and internal exact times are both preserved but
  their different meanings are not represented. They are compatible, not proof
  of contradictory schedules.
- The property is again typed `asset`. The management-key access notice and the
  tenant's dog concern are omitted; these are operationally relevant conditions
  if the extraction is intended to support later scheduling decisions.
- All ten claim attribution values use display labels rather than entity IDs,
  which the validator catches. Quote alignment passing would not catch the
  unsupported `assigned_to` semantics.

## 038-at-013: tenant replacement of washing machine

Artifacts: [input](../runs/phase1-baseline/038-at-013/input.json),
[extraction](../runs/phase1-baseline/038-at-013/extraction.json),
[validation](../runs/phase1-baseline/038-at-013/validation.json).

Supported successes:

- Recognizes Ruben, Henry Ingram, Eliza Oakley, and the washing-machine issue.
- Preserves the tenant's intention to supply a replacement and take it on
  departure, and identifies that permission and disposal costs were discussed.
- Represents the power-failure diagnosis as reported rather than physically
  verified. It does not invent a contractor repair.

Material semantic errors:

- **c6 asserts ownership of the old broken machine by the tenant.** Its evidence
  is “if I replace it will be mine ...”. This concerns a future replacement,
  not the old machine. Old and proposed replacement assets must be separate;
  conditional future ownership must not become present ownership.
- c3 uses the landlord Person as subject of `authorizes`; c4 does the same. The
  implemented predicate expects an Approval subject, so the validator rejects
  both. Semantically c3 also cites only “Yes this is fine,” omitting the earlier
  proposal needed to establish what the assent covers.
- c4 expands removal-cost permission into an unqualified authorization. The
  prefix describes a possible charge and an agency request about covering it;
  event010 reports coverage if charged and the tenant offers free family
  disposal. That condition should remain explicit.
- c5 calls Ruben's commitment to have a brother dispose of the old machine a
  `requests` relation. It is a stated future arrangement, not a request for
  somebody else to organize disposal.
- c7 attributes an agency note directly to the tenant. The note may summarize
  tenant intent, but the immediate evidence source remains the agency.

Omissions and unresolved evidence:

- Event004 references Flat18/128 Meadow Row, whereas events005–006 reference
  Flat9/59 Alder Lane. Neither address nor the conflict appears.
- Event001 says LG in the original query but “Willow Maintenance washing
  machine” in the generated summary. The extraction adopts the summary label
  without preserving that discrepancy or the distinction between tenant text
  and generated intake text.
- Event010's channel metadata calls the sender Tenant while its body includes
  Eliza speaking for Riverside Solutions; the prefix elsewhere uses Northbridge
  Lettings. No identity/source discrepancy is retained.
- Event013 explicitly records completion without payment; there is no Request
  entity or claim carrying that workflow outcome. This observation must not be
  expanded into physical confirmation that a replacement has already arrived.
- `unresolved` is empty. The validator also catches a fabricated non-exact
  landlord mention quote in event009.

## 045-at-010: poorly specified window request

Artifacts: [input](../runs/phase1-baseline/045-at-010/input.json),
[extraction](../runs/phase1-baseline/045-at-010/extraction.json),
[validation](../runs/phase1-baseline/045-at-010/validation.json).

Supported successes:

- Correct Property type and address; captures Clara Harper, the organization,
  and the kitchen/patio-window request.
- Preserves the hold messages, tenant's denial that the landlord requested the
  work, and the agent's tentative “windows are blown?” question in quoted text.
- Does not explicitly assert landlord approval or completed repair.

Problems:

- **c3 turns the email recipient Tenant into the request's assignee.** `To:
  Tenant` is communication routing, not work assignment. This is unsupported
  even if its currently invalid quote were repaired.
- c1 represents a maintenance request as `requests` a property, rather than
  `concerns` that property. It confuses the operational issue with an actor
  making a request.
- c2, c5, c6, and c8 put instructions, denial of landlord initiation, and a
  tentative diagnosis question into `has_status` string values. The strings
  retain wording but lose relational semantics and uncertainty. The explicit
  hold messages are much better fits for recorded status.
- Tenant and Landlord are typed as people, yet the output omits contextual
  names Dawson and Theo visible in greetings. Generic roles should remain
  roles until linked to those mentions with evidence.
- Event007 explicitly says three referenced photos are unavailable. No Document
  records or availability gap are extracted.
- `unresolved` is empty despite event009 expressly saying insufficient
  information was supplied and asking whether the windows are blown. The
  precise defect is unresolved, not an established condition.
- The validator catches eight bad entity quotes, one bad claim quote, and
  attribution values that do not resolve to entities.

## Implications for the extraction contract

1. Require both relation endpoints to be supported by evidence; a valid quote
   containing only one endpoint is insufficient.
2. Represent correspondence role separately from work assignment.
3. Separate old assets from proposed replacements, and distinguish proposal,
   commitment, permission, report, and recorded outcome.
4. Preserve source conflicts, missing referenced documents, and under-specified
   requests as structured unresolved items.
5. Avoid allowing `has_status` to absorb arbitrary sentences. It hides ontology
   failures while appearing schema-valid.
6. Keep recorded appointment versions linked without inferring two active visits.

## Sonnet counterparts: qualitative comparison

The three development counterparts subsequently completed and were reviewed in
`runs/phase1-sonnet`. This comparison is qualitative, one sample per checkpoint,
not a model ranking or accuracy estimate. The bare-string `attributed_to` schema
also underspecifies the validator's ID requirement; attribution failures are
partly an interface-design issue and should not all be blamed on extraction.

### 003-at-010

[Sonnet extraction](../runs/phase1-sonnet/003-at-010/extraction.json) fixes Property
and Theo Quinn typing, introduces Quote and Approval entities, and connects the
approval to both event010 and the event009 proceed instruction. It explicitly
records Bennett's unresolved person-versus-company identity, missing estimate
content, the unknown attachment, and the priority warning. This is materially
more useful than baseline's empty uncertainty list.

Remaining problems: the contractor is nevertheless committed to Organization
type and recorded assignment; the warning does not undo that claim. A checkout
report is typed Inspection instead of separating report/document from activity.
`e-quote requires e-mr` is a poor relational representation of a quote requested
for a job. Attributions still use names rather than IDs.

### 020-at-012

[Sonnet extraction](../runs/phase1-sonnet/020-at-012/extraction.json) retains the
time windows and recorded exact times, captures the management key, correctly
represents cancellation as requested, and explicitly flags absence of an
explicit cancellation record. It no longer fabricates inspector assignment
from agency sender/signature; it says the inspector is unknown and flags the
two agency identities.

Remaining problems: it splits into two Inspection and two Appointment entities
without connecting each appointment to its inspection or linking versions. The
Friday/date conflict remains unflagged. c-009 makes the Inspection the subject
requesting a reschedule, rather than the tenant. Generic Tenant is typed Person,
and attribution values remain unresolved display labels. These are graph
semantics problems even where the quoted evidence is accurate.

### 038-at-013

[Sonnet extraction](../runs/phase1-sonnet/038-at-013/extraction.json) recognizes
both addresses and explicitly flags their conflict, preserves the LG tenant
description, introduces a scoped Approval, records task completion without
payment, and distinguishes that from physical replacement. It correctly keeps
removal-cost coverage conditional and attributes that report to Eliza. It
also flags the Northbridge/Riverside organization discrepancy.

Remaining material problems:

- c-013 asserts the old machine `owns` Henry Ingram: direction is reversed, and
  “this one was here when I moved in” does not establish landlord ownership in
  either direction. This replaces baseline's ownership error with another.
- c-011 uses `reports_completion` for a future plan to have the brother remove
  the machine. Future commitment is still not completed work.
- It records the machine at property B while separately saying the correct
  address is unresolved; the selected location should retain that uncertainty.
- c-006 infers Henry manages property B from a `To: Landlord` header, despite the
  property conflict and insufficient evidence for that management relationship.
- Its proposed gender ambiguity is unsupported: “Ruben” does not establish a
  person's gender. Explicit pronouns and a name are not contradictory evidence.
- Some quotes normalize curly apostrophes or remove Markdown header formatting,
  violating exact-span requirements. These mechanical failures are separate
  from the supported semantic improvements.

The stronger extraction is substantially better at exposing missing information,
but extra output also introduces extra unsupported claims. More entities and
uncertainty entries alone are not a quality measure.
