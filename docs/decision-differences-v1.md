# Why the decisions differ from the recorded history

## Scope and interpretation

All40 development checkpoints and both80 predictions were reviewed by the implementing assistant against the original prefix events and original later communication. This is an explicit assistant-authored semantic review, not a human-consensus annotation and not a fresh LLM API judge run. No dataset, frozen prediction, prompt, or historical target was changed. The machine-readable review is [`annotations/decision-difference-review-v1.json`](../annotations/decision-difference-review-v1.json). It records source quotations/positions, target anchors, prediction JSON pointers, action types, material differences, labels, and epistemic limits for every checkpoint/arm.

**The reported 2/40 is the soft judge’s `match` label in each arm. It is not deterministic exact match, task success, or accuracy.** The two corresponding cases014 and040 also match the material maintenance step in this review. That coincidence does not validate the judge’s remaining labels. Historical action is an observed alternative, not a normative gold answer.

## What explains the low correspondence?

1. **Approval and identity bookkeeping displaces operational communication.** Many outputs ask who the approver/provider is or what an approval means, where history sends an approval request, a tenant update, or a contractor message. Often the model is trying to establish authority to perform work even though the immediate historical act only asks permission or communicates a report.
2. **The representation creates additional uncertainty.** A single multi-item work order becomes multiple request entities in006–008 and019, then one job-level assignment cannot be mapped to each request. Some prefixes contain a clear issue but extraction supplies no request entity (028), while generic landlord mentions are inconsistently represented.
3. **Some historical decisions are genuinely unrecoverable.** In010 the prefix is only hold notes; solar readings first appear later.013 contains no dishwasher information;020 contains only a morning-slot note;027 contains no blocked-drain report. Exact manual advice in024 and the gardener’s annual leave in018 are also unavailable.
4. **Several different predictions are defensible.**004/005 explicitly demand manual resolution,009 already requests photos and says waiting for tenant, and012 explicitly questions whether the later door complaint is the dishwasher. A different historical continuation does not invalidate waiting, manual review, or clarification.
5. **The judge is unstable.** Comparable actions can receive different labels; even target predictability changes despite identical prefix/target input. Citation alignment repairs cannot settle these semantic disagreements.

## Corrected classification under the current benchmark contract

**Amended 2026-10-10 · assumption version `property-contextual-parties-v1` · review version `decision-difference-review-v1.1`.** Landlord and tenant are known contextual roles. Missing personal names, contact strings or extracted party IDs do not justify delaying a role-addressed proposal. The contract grants neither approval nor proof of delivery, and does not resolve conflicting relationships or identify providers.

**The13 affected predictions are now primarily classified `unnecessary_identity_blocking`, not `reasonable_alternative` or legitimate identity uncertainty.** Each also carries the overlapping cause `role_resolution_overblocking`. Prior-contract conclusions are retained only in the JSON's explicitly historical field; they are not current classifications. Frozen predictions and judge outputs are unchanged.

| Exact checkpoint/arm | Why the identity block is unnecessary | Independent concern retained |
|---|---|---|
| `011-at-003/control` | The rationale makes identifying the landlord/approver a prerequisite to asking approval. The contextual landlord is known under the benchmark contract. | No approval has been granted and repair scope is unspecified. Those facts justify requesting limited approval, not asking who the landlord is. |
| `011-at-003/progress` | The rationale makes identifying the landlord/approver a prerequisite to asking approval. The contextual landlord is known under the benchmark contract. | No approval has been granted and repair scope is unspecified. Those facts justify requesting limited approval, not asking who the landlord is. |
| `016-at-002/control` | Both rationales explicitly delay an inspection approval request because the landlord is not identified. Known contextual role removes this reason. | Actual inspection/repair authority and spending terms remain unconfirmed; reported availability is not a booking. These can be conditions of the approval request. |
| `016-at-002/progress` | Both rationales explicitly delay an inspection approval request because the landlord is not identified. Known contextual role removes this reason. | Actual inspection/repair authority and spending terms remain unconfirmed; reported availability is not a booking. These can be conditions of the approval request. |
| `025-at-002/control` | Control escalates to resolve landlord identity; progress asks the agency to identify that landlord before approval. The same known role is already available. | No approval decision or repair scope is supplied. Asking permission remains necessary; a missing grant does not prevent sending the approval request. |
| `025-at-002/progress` | Control escalates to resolve landlord identity; progress asks the agency to identify that landlord before approval. The same known role is already available. | No approval decision or repair scope is supplied. Asking permission remains necessary; a missing grant does not prevent sending the approval request. |
| `026-at-003/control` | Both escalate to identify/route the landlord before proposing approval. Known role means this identity prerequisite is unnecessary. | Approval remains ungranted and the named historical contractor is unobservable. Progress also overstates prerequisite text as an asserted workflow failure; this independent unsupported assertion is retained. |
| `026-at-003/progress` | Both escalate to identify/route the landlord before proposing approval. Known role means this identity prerequisite is unnecessary. | Approval remains ungranted and the named historical contractor is unobservable. Progress also overstates prerequisite text as an asserted workflow failure; this independent unsupported assertion is retained. |
| `028-at-002/control` | Control adds identifying the appropriate landlord as a prerequisite. That part is unnecessary under known contextual roles. | A separate real interface defect remains: no extracted maintenance-request entity, despite a clear loose-pipe report in original text. Correcting the landlord classification does not make the supplied request ID valid or remove request-identity repair. |
| `035-at-003/control` | Control escalates landlord identity; progress asks agency to identify the landlord/approver. Neither is warranted solely by absence of a name/entity ID under the contextual-role contract. | The historical call remains intent-unassessable. Control also asks about shutoff/access; those questions require separate relevance review and are not resolved by knowing the landlord. Approval and actual inspection/repair authority remain ungranted. |
| `035-at-003/progress` | Control escalates landlord identity; progress asks agency to identify the landlord/approver. Neither is warranted solely by absence of a name/entity ID under the contextual-role contract. | The historical call remains intent-unassessable. Control also asks about shutoff/access; those questions require separate relevance review and are not resolved by knowing the landlord. Approval and actual inspection/repair authority remain ungranted. |
| `038-at-003/control` | Both escalate to identify the landlord before a replacement approval proposal, although the contextual landlord role is known. | Existing-machine ownership and tenant replacement terms still need a decision. They can be presented to the landlord in the approval request. The removal amount is unavailable. Progress separately claims a rejected workflow without original-source proof. |
| `038-at-003/progress` | Both escalate to identify the landlord before a replacement approval proposal, although the contextual landlord role is known. | Existing-machine ownership and tenant replacement terms still need a decision. They can be presented to the landlord in the approval request. The removal amount is unavailable. Progress separately claims a rejected workflow without original-source proof. |

The machine-readable correction contains each exact prediction rationale quotation and JSON pointer plus prefix source evidence. In028 control, missing landlord identity is wrongly blocking, while the separate missing request-entity representation remains a real interface defect. In035, the proposed identity detour is classifiable even though correspondence with the historical mixed-speaker discussion remains `cannot_assess`.

Other provider/category/scope/approver questions are not blanket-reclassified. Knowing the landlord does not establish whether approval has been granted, what work or spend is covered, or which provider was selected. The current report separates those causes.

## Difference counts

Each cell counts checkpoint-arm membership, not individual actions. Labels overlap; do not sum rows. “Excess” denotes a candidate avoidable prerequisite or supervisory detour, not a finding of unsafe conduct. “Missing operational step” describes an omitted historical step, not proof that it should have been performed.

| Difference label | Control /40 | Progress /40 | Cases with either arm /40 |
|---|---:|---:|---:|
| `action_intent_changed` | 36 | 33 | 36 |
| `excess_clarification` | 18 | 16 | 20 |
| `excess_escalation` | 5 | 2 | 5 |
| `missing_operational_step` | 28 | 25 | 28 |
| `actor_or_role_difference` | 20 | 18 | 20 |
| `scope_or_condition_difference` | 5 | 6 | 6 |
| `timing_or_ordering` | 10 | 10 | 10 |
| `extra_actions` | 3 | 2 | 5 |
| `unobservable_target_specifics` | 23 | 23 | 23 |
| `insufficient_prefix` | 6 | 6 | 6 |
| `ontology_or_identity_fragmentation` | 27 | 27 | 27 |
| `target_annotation_ambiguity` | 3 | 3 | 3 |
| `judge_inconsistency` | 8 | 8 | 8 |
| `role_resolution_overblocking` | 7 | 6 | 7 |

## Exclusive primary conclusions — current contract

One primary conclusion per prediction, totaling40 per arm and80 overall. These are manual descriptive classifications, not an accuracy score. `reasonable_alternative` remains available for the other defensible proposals; it does not include the13 corrected identity blockers. Where several concerns coexist, the primary result identifies the next-step defect and secondary labels retain the rest.

| Primary conclusion | Control /40 | Progress /40 | All /80 |
|---|---:|---:|---:|
| `faithful_match` | 2 | 2 | 4 |
| `reasonable_alternative` | 24 | 26 | 50 |
| `unnecessary_identity_blocking` | 7 | 6 | 13 |
| `unsupported_prediction` | 1 | 0 | 1 |
| `target_not_predictable` | 6 | 6 | 12 |
| `cannot_assess` | 0 | 0 | 0 |

Overlapping secondary findings remain separate: three predictions contain a particular unsupported causal assertion (030 control,026 progress,038 progress). The latter two are primarily identity blockers but keep their unsupported-assertion finding.035 both arms retain historical-comparison `cannot_assess` as a separate dimension; this does not excuse their current identity blocking. Thus zero primary `cannot_assess` does not claim every historical intent is assessable.

The six essentially unobservable target cases are010,013,018,020,024,027. The three specific unsupported causal assertions flagged are030 control (claims an actual rejected step),026 progress (asserted workflow failure rather than prerequisite), and038 progress (rejected-workflow handover). These largely inherit stronger failure interpretations from extraction; a source instruction to complete approval first is not, by itself, proof of a failed attempted operation. This is a focused causal review, not an exhaustive safety/entailment certification.

## Paired changes: what the progress paragraph actually did

**12/40 cases changed action-type sequence or action count**:001,002,014,019,020,021,025,028,030,032,035,036. The other28 have the same type/count; some still differ in recipient, coverage or conditions. This is a descriptive syntactic grouping supported by manual notes, not a semantic score.

-021/032/036 move from preliminary clarification to a limited inspection-approval request. This is a useful general pattern, though the historical requests often allow repair or landlord self-arrangement, so scope still differs.
-025/035 replace escalation with clarification;038 and026 retain escalation.
-030 replaces workflow-failure escalation with two inspection-approval requests, reducing the unsupported failure assertion while retaining fragmented requests.
-001 reduces three requests to one but drops weeds/disputed-area coverage;019 expands one approval to five, including overlapping garden scope. Fewer or more actions are not automatically better.
-020/028 remove actions because request identifiers are missing;028 is a representation defect despite an intelligible pipe issue.
-002 changes waiting into an appointment query;014 removes an explicit wait after approval request.

The original judge reports2 matches in each arm, partial13→14 and different24→23. Those totals do not demonstrate a semantic gain. In016,023 and026, correspondence labels flip while the material proposed act remains essentially the same. In003,013,014,024 and040, target-predictability labels differ despite identical target/prefix evidence.040 additionally receives different support labels for equivalent inspection-approval proposals. These eight case flags are review evidence of judge instability, not corrected judge scores.

## Concrete examples

| Case | Prefix → history | Review |
|---|---|---|
|010|Only “waiting for mid june” → ask for solar-reading photo|Missing topic, not a reasoning failure to predict solar panels. Both clarification choices are grounded; exact historical target cannot be expected.|
|012|Explicit uncertain dishwasher linkage and unanswered troubleshooting → seven-step dishwasher guidance|Clarification first is defensible ordering. Progress adds whether earlier troubleshooting helped. The unseen guidance sequence should not be invented as an expected exact answer.|
|038|Tenant willing to replace washer and landlord approval first → replacement approval plus removal-cost responsibility|Known landlord role should permit a replacement-approval proposal; name/ID-driven escalation is overblocking. £24.37 and the named landlord are unavailable specifics. A rejected workflow is not established by the original prerequisite message.|
|004/005|Explicit vacancy pause/manual-resolution instruction → contractor message/quote request|Escalation has direct support. Do not call it excessive merely because later communication bypasses the visible pause.|
|006–008|One multi-item estimate request plus generic provider assignment → provider/tenant communications|Extraction splits requests, then models ask which split request the single assignment covers. Grouped job/task identity is an ontology/extraction issue.|
|028|Loose garden-pipe description → landlord contractor-choice request|Progress abstains because extracted request entity missing. Prompt polish cannot supply a valid absent entity; contextual request identity must be represented.|
|031/034|Approval confirmed/provider assigned → tenant triage/quote update|Models re-query approval scope as though notification authorizes repairs. Proposal type and side effects need separate treatment.|
|039|Washer clicks but works → ask tenant whether contents cause noise|Models query approval setup instead. A reversible diagnostic question need not wait for provider/category choice; known tenant role removes addressing excuse.|
|014/040|Issue and landlord approval prerequisite → ask landlord about inspection|Material next-step matches in both arms. These do not establish exact wording or full historical-detail reconstruction.|

## General hypotheses worth testing

1. **Propose the next communication at its actual commitment level.** Asking permission, seeking a quote, notifying of a reported assignment, and authorizing repair have different prerequisites. Unknown repair spend need not block a narrowly scoped request or report. Test this as one domain-general factor, not case-specific examples.
2. **Use contextual party roles for plans.** Landlord/tenant role references are supplied by the benchmark contract. Resolve concrete delivery identities at execution admission; do not make personal-name resolution a synthetic human escalation in a prediction-only benchmark. Requires response/interface support as well as prompt text.
3. **Clarify only uncertainty that changes the immediate choice.** Name the uncertainty and its effect on that action, rather than demanding completeness of every field. Preserve real ambiguity (012) and explicit manual-review demands (004/005).
4. **Do not manufacture a failure from a prerequisite.** Keep original message provenance and distinguish a rule/reminder from an observed rejected operation. This requires correcting extraction categories/support, not only weakening the decision prompt.
5. **Preserve whole-job scope and avoid duplicate questions.** A grouped work order can contain several issue/work items without becoming several unrelated approval workflows. Needs ontology/linking changes and extraction evaluation.

### What a prompt cannot fix

- Recover unseen solar/inspection/drain topics, provider names, manuals, dates, holiday status, or unobserved authorization from thin prefixes.
- Supply missing valid request/party references while the response contract only accepts extracted IDs.
- Establish external authority, policy, costs or actual execution from a historical email.
- Make a mixed-speaker summary reveal a definite outbound intent.
- Turn noisy model judgments into deterministic truth; literal citation repair validates text location, not entailment.

No target-informed few-shot examples or case-specific instructions were added. Any next experiment should freeze the role-context contract, repair representation separately, and keep prompt factors distinct from interface/extraction changes.

## Per-case review index

The JSON contains exact source positions and prediction pointers. Below is the compact material-difference index; arm-specific details remain in that artifact.

| Case | Material difference and limits |
|---|---|
|001|Both ask about approval mechanics rather than forwarding the report for broad direction. Treating one multi-item report as multiple independent requests creates avoidable scope questions.|
|002|History transmits job scope; neither prediction does. The prefix already reports contractor contact and imminent scheduling, so waiting or asking for scheduling is defensible. The terse target does not prove a new instruction rather than written follow-up.|
|003|Both request a quote, which is supported by the recorded estimate request and provider assignment. The preceding contractor email is absent, so predicting this exact reminder would assume an unseen communication.|
|004|Both escalate an explicitly requested manual review of a vacancy pause. History proceeds with contractor communication without showing the intervening resolution or referenced email. This is not evidence that escalation is erroneous or excessive.|
|005|Both escalate the explicit vacancy/pause instruction instead of sending the estimate request. Provider assignment does not establish that the pause was resolved. Historical continuation is not proof that ignoring the pause was authorized.|
|006|Both ask whether assignment covers carpet, repainting or both. The original note is one bundled estimate request; extracted separate request IDs introduce ambiguity. The named contractor/tenant are unavailable in the prefix.|
|007|Both ask the agency to link assignment to spotlight and ceiling-tile requests. These are subitems of one quote request; fragmentation blocks a provider communication. Exact prior-email reminder also needs unobserved context.|
|008|Both convert a directly stated grouped estimate request into assignment-coverage clarification. Request/entity fragmentation and generic provider identity become blockers to a draft quote request.|
|009|Both wait for a reply to the same request already in the prefix. No response deadline or elapsed decision clock justifies choosing reminder now. Historical repetition is plausible but waiting is a supported alternative.|
|010|The prefix contains only vague hold notes. Solar panels, readings, tenant and purpose are absent; neither arm can recover that topic from the supplied evidence.|
|011|Both ask who the approver is and how approval should work rather than proposing approval for inspection. Landlord role and the fault are in source; extraction omits a usable landlord entity. This is primarily a role-addressing/interface obstacle.|
|012|Both first disambiguate the later door report. The source explicitly says linkage was uncertain and prior troubleshooting went unanswered. This is a defensible ordering choice; exact seven-step guidance is not in prefix.|
|013|Only a generic approval-selection update is supplied. Dishwasher symptoms, tenant and landlord are absent. Both abstain because no maintenance-request entity exists; historical intent is unobservable.|
|014|Both propose inspection approval to landlord, matching the material maintenance choice. History also confirms fridge installation, which the prefix does not establish. This incidental extra is not required for matching the next repair decision.|
|015|Both seek proposed provider/category and approver details before seeking permission. Prefix identifies no landlord and no provider selection. Clarification is defensible under this interface, but operational approval can be proposed at role level without selecting a named contractor.|
|016|Both ask for landlord identity and approval scope instead of requesting a decision about attendance. Role is explicit but usable actor missing. Near-identical actions received different judge correspondence labels.|
|017|Both directly propose landlord inspection approval. This advances the stated next step rather than first sending the tenant an acknowledgement; the recipient and immediate speech act differ, but workflow direction agrees.|
|018|Both ask unanswered safety/tree questions rather than promise gardener scheduling. Annual leave, gardener availability and promised booking are absent. These details cannot be inferred; safety clarification is defensible.|
|019|Both replace broad direction-seeking with specific scope-approval proposals. Progress multiplies an overlapping garden description and bullet items into five approval requests. These are proposals, not unauthorized execution, but overlap and scope shaping are material.|
|020|The prefix has only a morning preference. Inspection purpose, confirmed booking, date, tenant, photography and key-access terms are absent.|
|021|Control asks agency for work scope/approval route; progress proposes landlord inspection approval. Progress removes a preliminary blocker but narrows historical necessary-work permission to inspection only. Agency spare-key check in history is absent.|
|022|Both query approval status and provider equivalence rather than coordinate attendance. Prefix does not confirm approval, proximity or time. The later call includes a customer answer, so exact confirmation is not a predictable outbound-only action.|
|023|Both ask agency for provider/category/approver rather than landlord attendance approval. Door location/material and named landlord are absent. The two agency queries have equivalent intent despite judge different-to-partial flip.|
|024|Both follow generic provider-approval setup instead of troubleshooting. The manual is unseen and neither settings nor prior-tenant working condition are supplied. Exact advice is unobservable and must not be invented.|
|025|Control escalates missing landlord identity; progress narrows to an agency clarification. Both stop short of landlord approval despite explicit role/prerequisite. Contact identity is a routing problem, not automatically a need for supervisory intervention.|
|026|Both escalate approver identity instead of proposing inspection approval. The named contractor is unavailable, but the landlord role is explicit. The source states a prerequisite, not a failed attempted operation. Same escalation received different correspondence labels.|
|027|Only generic approval-selection text exists in prefix. Blocked drain, tenancy terms and responsibility are absent. Historical liability assertions are observed speech, not verified policy.|
|028|Control asks agency to identify request/approver/scope. Progress produces no actions because extractor failed to represent a request that is clear in source. This is missing extraction/anchoring, not missing incident narrative.|
|029|Both clarify approval and provider linkage before any work proposal. Historical email merely announces quote arrangements and explicitly puts landlord quote approval later. Treating notification/quote coordination as repair authorization creates a sequencing mismatch.|
|030|Control asserts a rejected workflow step and escalates ambiguity across fragmented toilet/tap requests. Source only says approval first. Progress requests inspection approval for both, a defensible cautious alternative to asserting unobserved provider work.|
|031|Both re-query provider identity and approval scope instead of informing tenant of the reported assignment. Named provider absent, but a role-level notification need not direct repair or assume unlimited spend. Bookkeeping uncertainty is expanded into an operational blocker.|
|032|Control asks whether approval exists and what scope to submit. Progress asks for inspection approval directly, removing the preliminary loop but narrowing the historical options.|
|033|Both ask about selected provider/category/approver rather than request landlord direction. Prefix lacks named approver; generic workflow message is treated as requiring a preselected provider before even asking what the landlord wants.|
|034|Both ask approval-scope questions instead of tenant notification. Repair/spend authority is unknown, but the notification itself need not authorize repair. Progress switches recipient from agency to landlord and omits provider-identity query.|
|035|No reliable historical next-action intent can be inferred from the call summary. Judge correspondence should remain unassessable. Predictions can still be inspected independently for grounding and unnecessary escalation.|
|036|Control requests scope/limit/inspection terms before approval; progress proposes inspection approval. Neither reproduces conditional repair scope; no amount is needed to ask for inspection permission.|
|037|Both ask agency for provider/category/approver rather than give landlord the routing choice. The source establishes a fault but does not supply landlord identity. Avoid presuming generic provider-selection text means a provider must be picked before role-level direction can be sought.|
|038|Both escalate missing landlord identity instead of proposing the known replacement question to the landlord role. Replacement willingness/ownership condition are in prefix; named landlord and £24.37 removal cost are not. Exact cost cannot be expected.|
|039|Both query agency/provider approval metadata rather than a noncommittal tenant troubleshooting question. The noise and continued operation support asking about contents without choosing a provider. Historical statement that landlord was informed is not in prefix.|
|040|Both request landlord inspection approval and preserve check-before-replace ordering. This faithfully matches the material next step. Named address not needed. Equivalent proposals receive different support/predictability labels.|

Source artifact SHA256: `0090a3b02ba8aa689027c79e49cdc259c9383bd0c7eecdd487b5542a83ae0d80`. Existing judge labels are retained as provisional evidence; later citation repair does not rewrite this source review.
