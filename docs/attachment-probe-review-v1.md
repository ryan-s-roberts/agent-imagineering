# Attachment extraction probes — independent review

Reviewed2026-10-10 against `annotations/attachment-probes-v1.json`, authored before outputs and excluded from prompts. Full evidence and JSON pointers: `annotations/attachment-probe-review-v1.json`. Frozen run: `runs/attachment-extraction-v1`. No source or model output was changed; reviewer made no model calls.

## Result

Attachment ingestion reaches the model entity graph and decisions. It does **not yet provide a complete typed state interface**.

| Probe | Entities | Records | Document-report records | Material limitation |
|---|---:|---:|---:|---|
|010at13|19|2|0|Meter observations retained in an explicit modeling gap; decision fails `invalid_request` because request ID is empty.|
|020at17|39|9|3|Wall defect and make-good requirement extracted, but room is misbound as property;2mention spans fail grounding.|

Both pipelines completed. Only one of two final decisions passed deterministic structural validation, and only one of two mention stages was fully grounded. Record validation passes for both final record sets.020required one repair because its initial record response hit the length limit. These counts concern interfaces and grounding, not semantic correctness.

##010: meter description

All five reviewed entity categories are recovered: meter,property,document,isolator and Juniper Utilities. Meter/isolator appear because attachment content was extracted, not because the host invented domain entities. Property, agency and solar-panel mentions have real cross-source links.

The record stage correctly avoids encoding a meter reading as a price, appointment or repair outcome. Its gap preserves “appears to show16845,” reported isolator position“I ON,” and the neutral image placeholder. No typed measurement exists. The1000imp/kWh specification is cited but not retained as structured state or explicit gap detail. The decision cites the document reading and retains uncertainty; it does not claim to have seen actual meter pixels.

Identity linking remains incomplete:

- The exact same flat address in the placeholder caption becomes a second property entity.
- Two further“solar PV”mentions remain separate from the SolarPVSystem entity.
- The filename document is separate from the title/attached-photo entity. The opaque attachment80reference may genuinely need an uncertain link; it should not be merged blindly.

The decision proposes asking the landlord for clarification. Its empty `request_id` is a deterministic contract failure. Its rationale also treats missing request representation as uncertainty about which matter the photo concerns, despite the explicit same-case forwarding description. Missing date/year is a genuine evidence gap; absent task identity in the extraction is a representation problem. These are different causes.

##020: inspection report

The graph joins the report's property and agency to history, joins filename and PDF title, and extracts the dog flap and detectors. It preserves three document-report records:

1. A report of inspection attendance, with date and eleven Good-rated areas in descriptive text.
2. The Bedroom1wall-mark issue, including“apparently from command strips.”
3. A pending/planned tenant make-good obligation, without claiming completion.

It also preserves the useful conflict: the agency email says no issues were identified, but the attachment records one defect. The decision makes two clarification proposals and cites actual page evidence. The saved rationale is original model text, not regenerated prose.

Defects remain:

- `issue-bedroom-1-wall-marks.property_id` points to the Bedroom1entity, classified as `property`, rather than the flat. The ontology lacks a room kind/relation, but substituting the room into the property slot loses the intended scope.
- No wall asset mention is extracted. This is an extraction omission independent of the missing room kind.
- A dog-flap mention remains unmerged; generic“inspection area”and“11inspection areas”are emitted as property entities.
- The source says **“Signature received16February2024at16:32:45.”** The work report and timing gap paraphrase this as receipt of the report. Signature timestamp and report receipt are distinct.
- Two attempted mentions are unmatched against their submitted source units. The successful remainder is usable for inspection, but the mention-stage validity is false.

The physical condition ratings, checklist negatives and detector states lack dedicated typed records. A generic modeling gap cites the relevant lines, but does not retain each boolean or negative proposition as independently addressable state. This is an ontology coverage gap. It is not correct to count those missing typed observations as ordinary extraction failures under the existing contract.

## What this establishes

The probes establish that linked PDFs can contribute source-grounded entity mentions, identity links, assertions and decision citations. They also expose why a general observation record is needed: readings, physical states, categorical ratings and negative checklist findings are different from workflow preconditions.

Future comparison should reuse the frozen source expectations, distinguish newly representable observation claims from prior ontology gaps, and keep the v1outputs intact. Improvements should separately measure parsing/grounding, correct identity links, retained claim values/qualification/polarity, and decision contract validity. No aggregate decision-accuracy claim follows from these two development probes.
