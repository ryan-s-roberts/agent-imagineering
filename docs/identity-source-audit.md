# Identity confusion actually present in the property histories

## Answer

Agent, landlord and tenant can function as contextual identities. **There is no source evidence of competing landlord identities in any of the seven affected baseline prefixes** (011,016,025,026,028,035,038). Missing personal names or extracted IDs did not create a real ambiguity there; requiring an imagined CRM lookup was a benchmark/modeling mistake.

Actual data quality problems do exist later: unexplained party/provider label changes, inconsistent sender metadata, and references to different properties. Those deserve narrow source attribution checks when relevant, not universal identity-resolution prerequisites.

## Scope and cautious counts

- Screened identity-bearing lines in all40 histories001–040; read candidate events in context. Earlier decision review read all40 selected prefixes in full. No holdout041–050 contents or attachment contents were opened.
- Verified **nine discrepancy findings across eight cases**:008,012,020,025,026,030,034,038. This is a minimum supported set from a targeted screen, not an exhaustive corpus error rate.
- **Zero proven incompatible real-person identities** in those examples: the text does not rule out co-tenants, co-owners, representatives, subcontractors or aliases. Nevertheless, the differing labels and property references are observable and should not be silently unified.
- **Zero of seven affected initial prefixes provides competing landlord identities.** Later anomalies cannot retrospectively justify an earlier escalation.

The repository explicitly describes these as synthetic, made-up cases ([README](/Users/ryan/code/HackatonPublicCases/README.md:3)). Synthetic label drift is a possible explanation, not an established cause for each discrepancy.

## Verified source findings

### 012-party-labels

Tenant Leo Turner and provider Riverside Compliance in job emails become Leo Kendall / Cedar Utilities in a scheduling call, then revert. A later arrival call names Meadow Services. Earlier Ruben need not be the same tenant; no co-tenancy/subcontractor/alias relation is supplied.

**Effect on choice:** Do not silently merge specific named provider/tenant nodes. At later scheduling checkpoints preserve unresolved links while using case-level tenant/provider roles. None of these future names justifies missing-landlord blocking at cutoff4.

[012 event015 L200](</Users/ryan/code/HackatonPublicCases/Property Management/012/history.md:200>); [012 event015 L193](</Users/ryan/code/HackatonPublicCases/Property Management/012/history.md:193>); [012 event016 L214](</Users/ryan/code/HackatonPublicCases/Property Management/012/history.md:214>); [012 event018 L239](</Users/ryan/code/HackatonPublicCases/Property Management/012/history.md:239>); [012 event021 L277](</Users/ryan/code/HackatonPublicCases/Property Management/012/history.md:277>)

### 020-landlord-label

Inspection report addresses landlord Oliver Bennett; later landlord reply summary names Felix Clarke. There is no statement excluding co-owners or an agent/representative, so different names are not proven incompatible identities.

**Effect on choice:** At a later reply attribution checkpoint, retain source-specific name/role rather than assert same person. Known contextual landlord is sufficient for proposing a reply.

[020 event017 L156](</Users/ryan/code/HackatonPublicCases/Property Management/020/history.md:156>); [020 event020 L194](</Users/ryan/code/HackatonPublicCases/Property Management/020/history.md:194>); [020 event020 L197](</Users/ryan/code/HackatonPublicCases/Property Management/020/history.md:197>)

### 025-tenant-label

Job/tenant emails identify Leo Bennett; call summaries alternately address Oliver Ashford and Leo Bennett. Appointment dates also differ, which is a scheduling issue distinct from identity.

**Effect on choice:** Do not infer that an Oliver appointment confirms the Leo-labelled booking without a case relationship. This appears after the baseline cutoff2.

[025 event013 L145](</Users/ryan/code/HackatonPublicCases/Property Management/025/history.md:145>); [025 event053 L545](</Users/ryan/code/HackatonPublicCases/Property Management/025/history.md:545>); [025 event054 L554](</Users/ryan/code/HackatonPublicCases/Property Management/025/history.md:554>); [025 event058 L590](</Users/ryan/code/HackatonPublicCases/Property Management/025/history.md:590>)

### 026-many-labels

An email to Ruben Oakley embeds the original request signed Clara; appointment email lists Tenant Name Clara. A later caller is Grace Mercer, and closing call is with Leo. Provider/agency labels also change. Multiple occupants/representatives are possible, but mappings are unexplained.

**Effect on choice:** Maintain uncertain named-person links and check which appointment a later call concerns. The initial landlord identity is not in conflict: cutoff3 has a generic landlord prerequisite, not competing landlords.

[026 event013 L179](</Users/ryan/code/HackatonPublicCases/Property Management/026/history.md:179>); [026 event018 L283](</Users/ryan/code/HackatonPublicCases/Property Management/026/history.md:283>); [026 event021 L322](</Users/ryan/code/HackatonPublicCases/Property Management/026/history.md:322>); [026 event021 L322](</Users/ryan/code/HackatonPublicCases/Property Management/026/history.md:322>); [026 event029 L399](</Users/ryan/code/HackatonPublicCases/Property Management/026/history.md:399>); [026 event029 L399](</Users/ryan/code/HackatonPublicCases/Property Management/026/history.md:399>)

### 030-provider-label

Same-timestamp tenant notification names Willow Services while the job instruction addresses Riverside Works for the same plumbing request/property. Later reminder names Willow Services; later call names Beacon Works. This is an observable assignment-label inconsistency, although subcontracting or multiple providers could reconcile it.

**Effect on choice:** Specific provider routing needs an explicit link or confirmation at that later checkpoint; generic provider-assigned communication is not automatically impossible. No earlier landlord-identity conflict follows.

[030 event007 L101](</Users/ryan/code/HackatonPublicCases/Property Management/030/history.md:101>); [030 event008 L123](</Users/ryan/code/HackatonPublicCases/Property Management/030/history.md:123>); [030 event012 L179](</Users/ryan/code/HackatonPublicCases/Property Management/030/history.md:179>); [030 event021 L339](</Users/ryan/code/HackatonPublicCases/Property Management/030/history.md:339>)

### 038-address

Call places the washer at Flat18,128 Meadow Row,Cedarford; following emails use Flat9,59 Alder Lane,Eastmere. This is a different property reference, not proof of different landlords. Henry Ingram is consistent between the call and approval reply.

**Effect on choice:** Later permission/payment should not silently cross property references. This mismatch first appears after cutoff3; it cannot explain withholding the initial role-addressed approval proposal.

[038 event004 L58](</Users/ryan/code/HackatonPublicCases/Property Management/038/history.md:58>); [038 event005 L70](</Users/ryan/code/HackatonPublicCases/Property Management/038/history.md:70>); [038 event009 L117](</Users/ryan/code/HackatonPublicCases/Property Management/038/history.md:117>)

### 038-speaker

Call event010 is labelled From Tenant, but dialogue opens with Eliza addressing Ruben as agency representative. Eliza says Riverside Solutions, while earlier agency metadata says Northbridge Lettings. The conversation roles are explicit despite metadata/branding drift.

**Effect on choice:** Read speaker turns; do not attribute Eliza approval report to tenant solely because of event metadata. Do not invent a new authorized principal from the brand difference.

[038 event010 L123](</Users/ryan/code/HackatonPublicCases/Property Management/038/history.md:123>); [038 event010 L126](</Users/ryan/code/HackatonPublicCases/Property Management/038/history.md:126>); [038 event004 L55](</Users/ryan/code/HackatonPublicCases/Property Management/038/history.md:55>)

### 008-cross-property

Header property is Flat5,55 Lantern Quay while body discusses quotes for other properties and later invoice for Flat13,83 Harbour View. Those may be legitimate portfolio communications but cannot automatically be scoped to the header job. Langley is labelled Landlord in021/028 but Contractor in027.

**Effect on choice:** This is an actual document/job attribution problem for quote approval or invoice matching, not a need to look up an unnamed landlord in a simulated CRM.

[008 event021 L213](</Users/ryan/code/HackatonPublicCases/Property Management/008/history.md:213>); [008 event021 L215](</Users/ryan/code/HackatonPublicCases/Property Management/008/history.md:215>); [008 event027 L279](</Users/ryan/code/HackatonPublicCases/Property Management/008/history.md:279>); [008 event028 L291](</Users/ryan/code/HackatonPublicCases/Property Management/008/history.md:291>); [008 event045 L482](</Users/ryan/code/HackatonPublicCases/Property Management/008/history.md:482>)

### 034-cross-property

One email header gives Flat9,9 Willowmere Road,Bellmere while its body says the contractor attended Flat17,77 Harbour View,Northbridge.

**Effect on choice:** Relating work completion/invoice to a property needs source reconciliation at that later event. This is not actor identity ambiguity.

[034 event011 L141](</Users/ryan/code/HackatonPublicCases/Property Management/034/history.md:141>); [034 event011 L143](</Users/ryan/code/HackatonPublicCases/Property Management/034/history.md:143>)

## Things that are not actual actor conflicts

### 012-issue-link

The real prefix ambiguity is which issue the later door reply refers to. It explicitly arrived in a sink email; this is issue/thread linkage, not proof that Ruben has conflicting identities.

[012 event004 L39](</Users/ryan/code/HackatonPublicCases/Property Management/012/history.md:39>)

### 010-june

“waiting for mid june” is strong ordinary-language evidence of a calendar month. No person named June is introduced. Missing year/due date/purpose is real; person-versus-month identity ambiguity was overcautious and is not source-supported as a competing actor.

[010 event002 L21](</Users/ryan/code/HackatonPublicCases/Property Management/010/history.md:21>); [010 event004 L39](</Users/ryan/code/HackatonPublicCases/Property Management/010/history.md:39>)

### 006-different-roles

Oscar is addressed as landlord and Sawyer as contractor; quote and approval explicitly connect them. Different names are expected roles, not a contradiction.

[006 event013 L181](</Users/ryan/code/HackatonPublicCases/Property Management/006/history.md:181>); [006 event013 L183](</Users/ryan/code/HackatonPublicCases/Property Management/006/history.md:183>); [006 event016 L226](</Users/ryan/code/HackatonPublicCases/Property Management/006/history.md:226>)

### 035-different-roles

Isaac is landlord recipient and Palmer tenant recipient in consecutive messages. They are different role holders, not conflicting names for one actor.

[035 event005 L80](</Users/ryan/code/HackatonPublicCases/Property Management/035/history.md:80>); [035 event005 L84](</Users/ryan/code/HackatonPublicCases/Property Management/035/history.md:84>); [035 event006 L99](</Users/ryan/code/HackatonPublicCases/Property Management/035/history.md:99>); [035 event006 L103](</Users/ryan/code/HackatonPublicCases/Property Management/035/history.md:103>)

### 036-different-roles

Sawyer is the landlord; Oliver is contractor addressed for work/invoices. Different names here are not an identity discrepancy.

[036 event003 L28](</Users/ryan/code/HackatonPublicCases/Property Management/036/history.md:28>); [036 event003 L32](</Users/ryan/code/HackatonPublicCases/Property Management/036/history.md:32>); [036 event023 L281](</Users/ryan/code/HackatonPublicCases/Property Management/036/history.md:281>); [036 event023 L285](</Users/ryan/code/HackatonPublicCases/Property Management/036/history.md:285>)

## Modeling consequences

1. Use case/property contextual roles as valid identities for proposed communication: landlord, tenant and agent do not need invented personal names.
2. Preserve named mentions with source provenance. A different label is not enough to merge or split real people conclusively.
3. Only clarify a concrete relationship that changes the decision: which request a reply concerns, which provider a booking belongs to, or which property an invoice covers.
4. Separate issue/thread identity, property identity, actor identity, authorization scope and sender attribution. They are distinct uncertainties.
5. Do not ask the model to invent CRM lookup work in a prefix/prediction task. A proposal addressed to landlord remains meaningful; execution plumbing is outside this benchmark.

Source excerpts, line positions and hashes are recorded in [`annotations/identity-source-audit-v1.json`](../annotations/identity-source-audit-v1.json).
