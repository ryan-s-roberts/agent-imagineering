# Property ontology: evidence and proposed interpretation contract

## Scope and method

Derived from `Property Management/001/history.md` through `040/history.md` in
`/Users/ryan/code/HackatonPublicCases`, source commit
`9bcdca585955dfb930005ed742572606e68f5688`. Histories 041–050 were not read in this
extraction pass. They are reserved for subsequent extraction evaluation, but
earlier conversation exposure means they must not be advertised as a pristine
holdout. This document describes a candidate semantic contract, not a recovered
CRM schema or an authoritative reconstruction of the world.

The inventory parsed explicit `<a id="event-NNN">` boundaries and searched
complete event blocks, including channel/from/to metadata. There are **1,177
events in 40 histories**. Channels: Note 150, Update 349, Email 386, Hold 175,
Call 70, SMS 47. No attachments were interpreted in this ontology pass.

The following counts are lexical coverage, not entity counts or validated
instances. Case and event counts mean at least one regex match in a case/event.
Searches were case-insensitive with word boundaries; approval used `approv\w*`,
landlord included `LL`, provider included `contractor`, quote included
`quotation`, and keys included singular `key`.

| Search family | Cases / 40 | Events | Example case:event |
|---|---:|---:|---|
| address | 39 | 164 | 003:004 |
| tenant | 38 | 341 | 001:002 |
| landlord or LL | 38 | 319 | 002:002 |
| provider or contractor | 36 | 482 | 003:002 |
| appointment | 24 | 119 | 012:015 |
| quote or quotation | 28 | 103 | 004:016 |
| invoice | 22 | 51 | 012:024 |
| inspection | 10 | 24 | 003:004 |
| approval stem | 37 | 103 | 005:020 |
| key or keys | 15 | 44 | 012:030 |
| closed | 21 | 23 | 003:022 |
| Hold channel | 33 | 175 | 001:008 |

After stripping event headers and sender metadata, exact repeated body texts
occur 116 times after their first occurrence, across 29 cases. This is a textual
observation, not a claim that 116 real-world actions were duplicated. Repeated
status notices and templates are included. Case 012:005 and 012:006 are a clear
repeated troubleshooting message; count distinct evidence events but do not
automatically infer two distinct obligations or appliance faults.

## Entity backbone

Use stable case-local IDs assigned by the extractor. Keep source mentions and
exact evidence spans separate from canonical labels. Roles belong to a
relationship/context, not a permanent person type.

| Candidate type | Meaning | Evidence | Boundary |
|---|---|---|---|
| Person | Named human mention | 012:014 Leo Turner; 012:016 Leo Kendall and Grant | Similar role is insufficient to merge names |
| Organization | Agency, contractor, provider | 012:014 Riverside Compliance; 012:016 Cedar Utilities | Organization name alone does not establish provider assignment |
| Property | Addressed unit, building or premises | 003:004 address and job ID | Address string normalization must not merge separate flats |
| Asset | Appliance, fixture, or maintained physical feature | 012:001 dishwasher; 001:002 communal vegetation | A named service in a generated description need not be an appliance brand |
| Request | Operational issue or requested service | 003:001 checkout cleaning estimate; 012:001 door fault | One request may concern multiple assets/tasks |
| WorkOrder | Instruction to perform or quote for work | 002:008 provider instruction | An instruction can be conditional; do not infer completion |
| Approval | Scoped permission claim or recorded decision | 012:008 attendance permission; 004:016 quote approved but wait for other work | Scope, conditions and source matter independently |
| Quote | Proposed priced work | 002:017 referenced quote; 005:020 disputed quote status | A reference does not reveal unseen amount or terms |
| Appointment | Proposed or recorded attendance window | 012:016; 020:009 inspection reschedule | Proposal, agreement, recording and attendance are different claims |
| WorkReport | Statement about attendance, diagnosis or result | 012:024 repair report within invoice note | Reported success is not independent verification |
| Invoice | Billing record | 012:024 | Billing and work evidence can share a document |
| Document | Attachment or referenced artifact | 003:004 checkout report; 002:017 unavailable quote/photos/report | Track availability; no extraction of absent content |
| Inspection | Inspection activity or requested visit | 020:009 | Its report may exist separately from its appointment |

`Tenancy` is a useful optional extension, but a property/tenant association must
not invent a tenancy identifier, start/end date, contractual terms, or ownership.
The generic roles tenant, landlord, agency, and provider can be recorded from
message metadata without resolving a named Person or Organization. Likewise,
an unnamed reported Approval is representable without inventing an approval ID
from the source system.

## Claim backbone and domain/range

All relations below are **claims with evidence**, not automatically true database
edges. Candidate predicate names are implementation suggestions. A smaller first
implementation can collapse related predicates while preserving their arguments.

| Predicate | Subject domain | Object/range | Evidence or purpose |
|---|---|---|---|
| `located_at` | Asset, Request, Inspection | Property | 012:005 appliance request and address |
| `concerns` | Request, WorkOrder, Appointment, Document | Asset or Request as appropriate | 003:001 cleaning; 012:016 dishwasher inspection |
| `has_role` | Person, Organization, unresolved actor mention | Role + contextual Property/Request | Tenant/provider metadata and 012:014 |
| `assigned_to` | Request, WorkOrder | Person, Organization | 012:013–014 assignment and named notification |
| `instructed_for` | WorkOrder | Request | 002:008 instruction |
| `authorizes` | Approval | Activity scope + target Request/WorkOrder/Quote | 012:008 attendance, 004:016 quote approval |
| `granted_by` | Approval | Person, Organization, unresolved role | 012:008 reported landlord authority |
| `conditional_on` | Approval, WorkOrder, action proposal | Requirement | 004:016 wait for checkout work before clean |
| `quoted_for` | Quote | Request, WorkOrder | 002:017 |
| `scheduled_for` | Appointment | Time interval | 012:016; 020:009 |
| `participant` | Appointment, Inspection | Person, Organization, unresolved role | 012:016 |
| `reports_condition` | Person, Organization, WorkReport | Asset/Request + condition | 012:011 troubleshooting failed |
| `reports_result` | WorkReport | Request/WorkOrder + outcome | 012:024 repair and successful test |
| `references_document` | Event, Request, Quote, Invoice | Document | 003:004; 002:017 |
| `has_recorded_status` | Request, WorkOrder, Appointment, Quote | Status literal | 013:020 recorded visit state; preserve literal |
| `awaits` | Request, WorkOrder | Required response/report/decision + responsible actor if known | 012:022–023 missing result; 012:028 landlord confirmation |
| `identity_candidate` | Mention | Entity | Preserve possible alias matches, never merge automatically |

An event can support multiple claims. A note quoting an invoice should retain
both the note as evidence location and the invoice/contractor as the reported
source, where identifiable. Do not treat the note author as the repair performer.

Recommended claim fields: subject ID, predicate, typed object or literal,
evidence event IDs and exact spans, attributed actor, assertion mode,
polarity, modality, recorded timestamp, and optional asserted effective time.
Keep these dimensions orthogonal:

- Assertion mode: direct system record, attributed report, inference, unresolved.
- Polarity: positive or explicitly negative. Missing evidence is not negation.
- Modality: actual, proposed, requested, conditional, future/intended.
- Conflict: links to competing claims; it is not a confidence number.
- Availability: readable evidence versus referenced-but-unavailable artifact.

The statement “approval confirmed” may be a direct record of confirmation;
“LL already agreed” is a staff report of prior agreement. Both are positive
evidence with different provenance. “Confirmed” must never mean independently
verified by the extractor.

## Evidence-backed pitfalls

| Source | Observed issue | Extraction rule |
|---|---|---|
| 001:002 | Existing AI intake classification and confidence appear in the history | Attribute the classification to its source; it is not ontology ground truth |
| 002:017 | Referenced report, photos and quote explicitly unavailable | Extract references and missing-content status only |
| 003:001, 003:004 | Checkout clean/removal/carpet work plus inspection report | Preserve multiple work components; do not collapse all requests to appliance repair |
| 004:016 | Quote approved but cleaning must wait for other work | Authorization and readiness are distinct |
| 005:020 | Sender says quote should be approved while CRM appears to await a quote | Preserve contradiction between reported agreement and displayed workflow |
| 012:004 | Reply in unrelated sink thread; dishwasher reference unclear | Message-thread membership alone does not resolve the concerned asset |
| 012:005–006 | Same troubleshooting message repeated | Repeated evidence does not independently corroborate success |
| 012:008 | `GS` and `LL` abbreviations | Resolve LL as a role where supported; leave GS identity unresolved |
| 012:014, 012:016 | Riverside Compliance/Leo Turner versus Cedar Utilities/Leo Kendall | Keep separate mentions/candidate links unless additional evidence establishes identity |
| 012:022–023 | Repeated no-results prompts | Missing work report does not prove missed visit or failed repair |
| 012:024 | Repair diagnosis embedded in invoice note | Extract attributed diagnosis and test result, not independently verified repair |
| 012:028–031 | Confirmation requested, key return recorded with validation error, then closure | Preserve each observation; do not invent an unlogged landlord reply or transition semantics |
| 020:009 | Rescheduled inspection date/time | Maintain temporally qualified appointments; do not overwrite history silently |

## Prefix behavior for case 012

These are extraction expectations, not a unique next-action answer key.

| Cutoff | Supported extraction | Must remain absent/unresolved |
|---|---|---|
| 004 | Dishwasher door request; sink-thread ambiguity; prior unanswered troubleshooting reported | Troubleshooting outcome, named assigned provider, repair diagnosis |
| 008 | Corrected description; troubleshooting instructions; staff-reported landlord permission for GS attendance | GS identity, spending limit, unrestricted repair authority |
| 011 | Tenant reports all checks completed and door still fails to close | Mechanical cause, Riverside assignment, confirmed appointment |
| 023 | Recorded assignment/appointment evidence; conflicting names; overdue result prompts | Whether visit actually occurred or work succeeded |
| 024 | Invoice note reports prematurely engaged lock, repair, successful appliance test | Independent tenant verification; future final-check prompts or closure |

Event timestamps are record times. Relative appointment dates may be normalized
only with an explicit reference timestamp and documented locale/timezone rule.
For example, “this Wednesday” in 012:016 on 26 April 2026 resolves to 29 April
2026 under a stated next-Wednesday convention. Extracted calendar resolution
must not erase the original phrase or convert an uncertain identity into a
verified booking.

## Deterministic validation boundary

Mechanically check exact evidence spans, prefix membership, ID uniqueness and
references, permitted predicate domain/range, date/amount shapes, and explicit
claim modes. Reviewed fixtures can check known claim tuples and forbidden future
facts. None of these checks proves arbitrary unseen semantic extraction correct.

Do not score simply by counting extracted entities: over-extraction of template
roles, duplicated events, or imagined documents would be rewarded. Evaluate
entity mention grounding, relation precision/recall on reviewed assertions,
attribution, modality, temporal boundaries, and unresolved identity handling
separately. Freeze ontology and prompts before the reserved-case run; report
manual review findings and any subsequent revisions as development iterations.
