# Attachment v2 — independent design and output review

This is an implementing-assistant review. No model calls were made by the reviewer and no frozen output was changed. V2 changes the ontology, source identity presentation, provenance wire representation, assertion batching and request prefix layout together. It is a combined engineering comparison, not a controlled one-factor ablation.

## Design review

- **Source admission:** attachment pages still require an explicit link in the event prefix. Page text stays literal, with file/page hashes and Unicode offsets retained canonically. Availability time remains distinct from the document's claimed observation time.
- **Model source view:** source prose is unchanged. Compact source IDs are globally assigned for the prefix; group metadata retains page/path, event, attribution and availability context. Hashes and absolute text offsets are omitted from model input but remain in the canonical source registry. This is appropriate for exact quote extraction; it does not discard domain text.
- **Shared prefix:** each assertion batch receives the full source context and unified entity graph. Its ownership source IDs are appended in the final user message. This preserves the requested common-prefix layout and supports cross-source identity reasoning. Actual cache hits require provider usage evidence.
- **Provenance wire:** omitted redundant `provenance.source_ids` is reconstructed as the union of field and causal evidence source IDs. Empty evidence remains invalid. This changes representation without manufacturing claims.
- **Batch ownership:** sources have disjoint primary owners; each record/gap must cite a primary source. This is a structural check, not proof that the asserted proposition is actually owned by that source. Records can still overlap semantically if attribution/context citations include primary sources; no semantic deduplication is claimed.
- **Batch references:** local record IDs are namespaced deterministically. Cross-batch record-level supersession or intervention-response links cannot currently be represented, because each call can reference only its own output records. Full source visibility does not eliminate that limitation.
- **Observation semantics:** numeric/text/boolean values, exact hedges, document-report provenance, location and observation time cover the missing physical observations. Presence `false` and negative source polarity must not be interpreted as two logical negations. Detector tested-and-working must not become mere detector presence; a meter constant is distinct from its reading.

## Defects reported during review

The initial compact-view typed-reference inventory omitted `supersedes_record_id`, `previous_intervention_record_id`, `authorization_record_ids`, `completion_record_ids`, `about_record_ids`, `obligation_record_id`, and `replaces_appointment_id`. Once entities/records are aliased, omitted fields can retain canonical IDs in input or unexpanded aliases in output. This was reported to the parent for correction before the next live attempt. Frozen request bodies establish whether an individual run exercised these fields; current source changes do not retrospectively repair old wire artifacts.

## Completed output review

Final reviewed artifact: `runs/attachment-extraction-v2/run.json`, SHA256 `abfdbcbf6201b8f6e5f198005b0a75c9d09ebae99e50d223d6124a28a32a0d76`. The rejected cache-key attempt is preserved separately at `runs/attachment-extraction-v2-rejected-cache-key`. The successful run completes both probes; both final decisions pass deterministic validation. This does not imply all extraction stages are clean.

| Probe | Entities | Records | Observations | Mention grounding issues | Decision |
|---|---:|---:|---:|---:|---|
|010-at-013|15|7|5|1|conclude|
|020-at-017|41|44|36|7|escalate|

### Claim coverage

Against the same sixteen pre-output selected source claims, fifteen have their material meaning represented. One remains absent as a typed value: the inspection's count of **one recorded defect** appears only in a table quotation, while that record's value contains the room ratings. This bounded coverage finding is not an accuracy score. It includes a dog-flap observation whose location citation is wrong, so it must not be reported as fifteen completely grounded records.

010 now preserves the apparent meter reading **16845**, unknown unit and timestamp, isolator position **I ON**, and separately **1000 imp/kWh** as a meter rating. It does not equate a switch position with safe or functioning equipment. Its decision proposes no further action, explicitly distinct from formal request closure. Missing task representation remains a weakness in its reasoning.

020 retains eleven room ratings, five checklist booleans with **evidence-of** scope, detectors **tested and working**, apparent wall marks and the pending tenant make-good obligation. It uses the actual property plus location text instead of classifying Bedroom 1 as the property. The earlier signature-time/report-receipt error is absent. Repeated detail and summary checklist statements are kept as document reports; they do not establish independent corroboration.

### Remaining interface and semantic limits

- Five `observation_quote_not_exact` diagnostics across the two probes arise from wrapped sentences already grounded as multiple exact adjacent spans. This is a single-span checker limitation, not fabricated quotations. Frozen diagnostics and the decisions' actual inputs remain unchanged.
- 020 has a genuine wrong location citation: `b003:r21.location_text` cites page 3 line 41 for “Utility Room”; the heading occurs at line 36. Its `b001:r4.blocking_effect` lacks field evidence. Neither error should be hidden among quotation-checker false positives.
- Both mention stages contain unmatched spans: one in 010 and seven in 020. Their usable subsets do not justify a fully grounded-stage claim.
- The alias omission is exercised in 020's frozen decision input: `supersedes_record_id: b001:r1` and `responds_to_record_id: b001:r3` remain canonical while record IDs are compact aliases. Final decision references still decode and validate. Fixing future code does not change what this model saw.
- No primary batch ownership errors were reported. Appointment supersession and communication response links are within the same batch and survive canonical combination. No required lost cross-batch relationship was demonstrated in these two probes; the general limitation remains.
- 020's proposed escalation uses the genuine no-issues/email versus wall-defect/report discrepancy. This is a possible action, not proof that human review is necessary. No decision-quality benchmark claim follows.

Full expectation mappings, record IDs, exact artifact hashes and literal model rationales are in `annotations/attachment-probe-review-v2.json`. The original source expectation file is unchanged and excluded from prompts. The reviewer made no model calls or output patches.
