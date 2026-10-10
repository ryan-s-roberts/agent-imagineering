# Attachment evidence extraction

Attachments are evidence sources for the existing mention detection, entity
linking and typed assertion extraction pipeline. Reading PDF text alone does not
produce an entity, assertion, permission or independently verified fact.

## Availability

`load_prefix_attachments(source_root, case, events)` reads only local files linked
from the supplied visible events. It never enumerates a case's attachments folder
to infer what was available. Files linked only after the cutoff, unlinked files,
case overviews and summaries do not enter the prefix. Repeated links to the same
file retain each linking event but share one document and its pages.

Local file resolution must remain within the case directory, including after
resolving symlinks. Remote URLs are recorded as unavailable; this ingestion path
does not retrieve them. Missing, unsupported, encrypted and malformed files have
explicit diagnostics rather than successful empty content.

## Three different times

- The linking event establishes **availability in the benchmark history**.
- A date printed in the document is an **assertion made by the document**.
- The date of the described inspection, work or approval may be different again.

Do not equate these dates or silently repair contradictions. This source corpus
contains reconstructed documents and chronological inconsistencies; see the
attachment source audit. A document being linked does not certify its contents.

## Stable, inspectable provenance

The manifest stores a case-local physical document ID, canonical relative path,
file SHA-256, all visible linking events, and exact link spans in event text.
For each PDF page it preserves the exact extracted Unicode text, text hash,
one-based page number, parser name/version and availability references.

Page source units use a document/page namespace so equal offsets on different
pages or in the linking email cannot collide. Mention and field-level evidence
offsets refer to the saved extracted page text, with an exclusive end. They are
not PDF byte offsets or visual bounding boxes. Alignment must not relocate a
quote into another document or page merely because the email event is shared.

Physical source handles are distinct from model-extracted document entity IDs.
Linking a party mentioned in an email to a party in a PDF requires an explicit
model-predicted same-entity relation with evidence, just as linking two event
mentions does. Filename or name similarity alone must not merge identities.

## Extraction and downstream use

The extraction model sees event and attachment source units together and emits
mentions, explicit identity links, typed assertions and field-level citations.
Document statements retain attribution, modality, polarity, conditions and gaps.
An invoice is not proof of payment; a quote is not approval; an inspection report
is a report of observations. A document labelled as a photograph does not prove
that a photograph or its claimed visual observation was actually supplied.

The decision agent consumes the resulting evidence graph and provenance. Adding
raw PDF text without extracted entities and assertions does not satisfy this
contract. Saved source text remains available to inspect and substantiate model
citations; the run records whether attachment extraction actually occurred.

## Current parser scope

PDF text decoding uses the declared `pypdf` dependency. Every page is processed.
Blank or image-only pages remain explicitly `no_extractable_text`; mixed success
is `partially_extracted`. This implementation does not OCR or interpret images.
Extracted text is not a guarantee of faithful table layout or complete visual
information. No page limit silently drops later pages.

Each new extraction run must include its attachment manifest and page sources in
its input hash and canonical artifact. Existing frozen runs remain unchanged.
Validation probes with later cutoffs are separate development diagnostics, not
improved results on the original forty checkpoints.
