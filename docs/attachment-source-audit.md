# Attachment source audit — development cases001–040

Audited2026-10-10 by the implementing assistant. Raw source files were not changed. Cases041–050 were not inspected. Machine-readable inventory: `annotations/attachment-source-audit-v1.json`.

## What is actually available

**16PDFs in7cases;63pages;88,773 extracted characters.** Fifteen files have explicit history links. One file has no history link. All16 contain extractable text; none contains an embedded raster image. Two trailing pages are blank (003 cleaning invoice p2;004 cleaning invoice p2), not scanned evidence requiring OCR.

These supplied PDFs are reconstructed text documents. Image descriptions appear inside boxes labelled **“Neutral image placeholder.”** In particular, case010's “photograph” is a one-page narrative describing a meter; visual inspection confirms there is no meter photograph on that page. A model can extract what that document reports, but cannot claim it independently read meter pixels.

Extraction used the existing bundled `pypdf`; representative pages005quote and010photograph were rendered with existing `pypdfium2`. No packages were installed. The inventory preserves file hashes, sizes, first-link event/timestamp, history line numbers, page-text hashes and exact page-span evidence. Text-order offsets are tied to the extraction output/version; they are not byte offsets into a PDF.

## Availability inventory

Numbers below identify the filename prefix `attachment-NN`. Full paths and hashes are in the JSON.

| Case | Attachment | Pages | First linked event | Important qualification |
|---|---|---:|---:|---|
|003|01 checkout report|12|004|Report date2026-03-16; linked2025-07-22.|
|003|02 cleaning invoice|2|020|£125; editorial reference to case completion; invoice statement remains reported evidence.|
|004|01 checkout report|5|006|Report date2026-06-23; linked2025-10-24.|
|004|02 cleaning quotation|1|010|£90; no detected future-outcome statement or date conflict.|
|004|03 cleaning invoice|2|037|£90; one blank trailing page.|
|005|01 checkout report|4|007|Report date2025-02-25; linked2024-11-10.|
|005|02 cleaning quote|2|013|Dated05/03/25; linked2024-11-13. £205 is a calculated sum.|
|005|03 cleaning quote|1|015|Dated05/03/25; linked2024-11-15. £205 is a calculated sum.|
|007|01 checkout report|7|005|Report date2026-08-25; linked2025-09-27.|
|007|02 tax invoice|1|033|£200 subtotal,£40VAT,£240 total; reported invoice amounts.|
|008|01 checkout report|12|003|Report date2026-01-05; linked2025-04-03.|
|008|02 estimate|1|**None**|Explicit later-outcome commentary. Exclude from prefix evidence.|
|008|03 checkout report|6|006|Report date2026-01-05; linked2025-04-06. Same link repeated twice in event006.|
|008|04 invoice|1|045|Issued09/03/2026; linked2025-06-02.|
|010|01 meter “photograph”|1|013|Text report+neutral placeholder; no underlying image.|
|020|01 property inspection report|5|017|Room/condition/defect extraction candidate; report date precedes link.|

**None of these files is explicitly linked before any current baseline checkpoint.** The40baseline cutoffs were chosen before the first outbound agency message. Loading every case-directory PDF would therefore leak later evidence into all relevant baseline inputs. Use separate later-prefix extraction probes; do not silently amend the existing frozen runs.

Only an exact history link establishes attachment availability in this audit. A filename, directory listing, document issue date, or a prose reference to an unavailable attachment does not prove availability. Case008event006 says an estimate is attached but actually links checkout report03 twice; that does not authorize silently substituting the unlinked estimate02.

## Retrospective and temporal contamination audit

All16text streams were inspected for retrospective case summaries and later outcomes. One explicit future-outcome statement was found:

**008/attachment-02-estimate.pdf, page1**

> The bathroom tap is included for replacement in this estimate; the case overview later
> records that it did not need replacing.

This is an unlinked document, so the exact-link admission rule already excludes it. Preserve its bytes and flag it; do not delete this sentence and describe the rest as a faithful contemporaneous original.

A second editorial statement appears in a **linked late invoice**, but is not demonstrated future leakage relative to its first availability:

**003/attachment-02-cleaning-invoice.pdf, page1**

> The invoice supports the case record that checkout cleaning, carpet cleaning and removal of
> dumped items were carried out.

It appears at event020, after the relevant cleaning episode. It is an editorial inference within the reconstruction, not independent verification of completion. Invoice line descriptions and the amount can be extracted as claims attributed to that document.

Separately, **9of15linked PDFs carry dates later than their first history link** (the nine flagged rows above). These are chronological contradictions, not proof that each document leaks a particular future action. They prevent claiming the reconstructed documents have trustworthy contemporaneous dates. Retain both the event availability timestamp and document-asserted date; never use the latter to reorder history or quietly repair synthetic dates.

No other explicit later-outcome sentence was identified. This is a bounded source audit, not proof that the reconstruction process preserved every original knowledge boundary. Generic inspection recommendations, quoted tenancy guidance, and invoice claims must remain attributed statements; they are not verified policy or completed operational effects.

## Recommended extraction probes

| Prefix | Available document | Size | What to evaluate |
|---|---|---:|---|
|010 through013|Meter-description PDF,1page|73,851bytes;911text chars|Meter entity; reported reading16845 with “appears” uncertainty; reported isolator position; no visual verification.|
|020 through017|Inspection report,5pages|98,171bytes;8,822text chars|Property→room relations; condition/cleanliness assessments; Bedroom1 wall-mark defect; tenant-remediation recommendation; source page/spans.|
|004 through010|Quotation02,1page|See inventory|Provider/quote/property relations; three service lines;£90 stated total; absent VAT remains unknown. Earlier linked report date conflict remains explicit.|
|007 through033|Tax invoice02,1page|See inventory|Supplier, invoice line,subtotal/tax/total; distinguish invoice issued, work claimed and payment verified. Earlier linked report date conflict remains explicit.|

These probes are availability-safe under the explicit-link rule and have no detected outcome leak in the selected document. They are not blanket certifications of every earlier source in those prefixes.010and020 are the cleanest small probes for the live integration.

005quotes are useful subsequent extraction diagnostics for **stated versus calculated amounts**, but require an explicit chronology warning. Never emit£205as a total explicitly stated by the original quoted text simply because a reconstruction added an arithmetic summary.

## Suggested ontology seam

Treat the attachment as an evidence-bearing entity, then extract typed entities and claims. The downstream decision input should receive those extracted records and provenance, rather than an undifferentiated PDF text dump.

1. **Document identity and availability:** content hash, case-relative path,media type, document kind, linked-event IDs, earliest available event, and an availability status. The same file linked twice is one document; different bytes with similar titles remain distinct until evidence supports version identity.
2. **Source units:** document ID,page number, block/line IDs, exact text, text-extractor/version, page-text hash, and optionally page-coordinate boxes. A citation selects an exact substring of a frozen source unit; its resolver also provides page and document identity.
3. **Entities:** property,room,asset,party-by-role,inspection,document,quote/invoice,line item,money amount and measurement. Link document entities to history entities using explicit addresses/job refs/roles and cited support; preserve uncertainty rather than merging merely similar names.
4. **Attributed records:** report assesses room condition; report describes asset defect; quote offers scoped service; invoice claims charge; measurement report states reading. Preserve modality, origin, polarity,time and qualifier. A document describing “appears to show16845” produces a qualified document report, not an agent-verified measurement.
5. **Derivation:** distinguish literal amount from calculated total; retain operands and deterministic arithmetic provenance for calculations. Do not count narrative and table repetitions as separate invoices, defects or line items.
6. **Admission diagnostics:** unavailable file,unlinked file,blank page,placeholder image,chronology conflict,retrospective commentary,unresolved entity link. These are source limitations rather than facts about property state.

A useful source reference is `{document_id, page, source_unit_id, start, end, quote}` plus the content and page-text hashes. The API may keep the existing compact `source_id/expression/occurrence` form if its source registry resolves unambiguously to this richer provenance. Document-reported facts remain distinct from later agency decisions or execution receipts.
