"""Read only attachments explicitly linked from visible events, preserving page text.

This module locates and decodes evidence. Entity identity and assertions are left
to the same model extraction pipeline that consumes event evidence.
"""

import hashlib
import io
import re
from importlib.metadata import version
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pypdf import PdfReader
from pypdf.errors import PdfReadError

LINK = re.compile(r"\[([^\]]*)\]\((?:<([^>]+)>|([^\s)]+))(?:\s+\"[^\"]*\")?\)")
FILE_SUFFIXES = {".pdf", ".png", ".jpg", ".jpeg", ".webp", ".docx", ".txt", ".csv"}


def _field(event, name):
    return event[name] if isinstance(event, dict) else getattr(event, name)


def _diagnostic(code, message, **context):
    return {"code": code, "message": message, **context}


def load_prefix_attachments(source_root: Path, case: str, events) -> dict:
    """Return documents, exact extracted pages, and explicit ingestion diagnostics.

    Availability is established only by the supplied events. Do not enumerate the
    attachments directory or use the case overview to infer availability. Offset
    positions inside pages refer to extracted Unicode text, not PDF byte offsets.
    """
    if not re.fullmatch(r"\d{3}", case):
        raise ValueError("Case must be three digits")
    case_root = (Path(source_root) / case).resolve()
    documents, pages, diagnostics = [], [], []
    refs = {}
    for event in events:
        event_id, text = _field(event, "id"), _field(event, "text")
        for match in LINK.finditer(text):
            label, angle, plain = match.groups()
            destination = angle or plain
            url = urlsplit(destination)
            path = unquote(url.path)
            if not (
                "attachment" in label.lower()
                or "attachments/" in path.lower()
                or Path(path).suffix.lower() in FILE_SUFFIXES
            ):
                continue
            item = refs.setdefault(destination, {"path": path, "url": url, "links": []})
            item["links"].append(
                {
                    "event_id": event_id,
                    "label": label,
                    "destination": destination,
                    "expression": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                    "offset_basis": "event_text_unicode_codepoints_end_exclusive",
                }
            )

    by_path = {}
    for destination, ref in refs.items():
        url, path = ref["url"], ref["path"]
        identifier = hashlib.sha256(f"{case}:{destination}".encode()).hexdigest()[:20]
        doc = {
            "id": f"{case}:{identifier}",
            "relative_path": path,
            "sha256": None,
            "available_at_event_ids": list(dict.fromkeys(r["event_id"] for r in ref["links"])),
            "references": ref["links"],
            "status": "pending",
            "diagnostics": [],
            "page_count": None,
            "extraction_method": "pypdf.extract_text",
            "extractor_version": version("pypdf"),
            "content_semantics": "document_report_not_independently_verified_world_state",
        }

        def fail(code, message, doc=doc, **context):
            issue = _diagnostic(code, message, document_id=doc["id"], **context)
            doc["diagnostics"].append(issue)
            diagnostics.append(issue)
            doc["status"] = code

        documents.append(doc)
        if url.scheme or url.netloc:
            fail("remote_not_loaded", "Remote attachment contents were not retrieved.")
            continue
        resolved = (case_root / path).resolve()
        if Path(path).is_absolute() or not resolved.is_relative_to(case_root):
            fail("outside_case", "Attachment path is outside its case directory.")
            continue
        doc["relative_path"] = resolved.relative_to(case_root).as_posix()
        identifier = hashlib.sha256(f"{case}:{doc['relative_path']}".encode()).hexdigest()[:20]
        doc["id"] = f"{case}:{identifier}"
        if resolved in by_path:
            # The same file linked through equivalent URLs is one document.
            previous = by_path[resolved]
            previous["references"].extend(doc["references"])
            previous["available_at_event_ids"] = list(
                dict.fromkeys(previous["available_at_event_ids"] + doc["available_at_event_ids"])
            )
            documents.pop()
            continue
        by_path[resolved] = doc
        try:
            data = resolved.read_bytes()
        except OSError as error:
            fail("unreadable_file", str(error))
            continue
        doc["sha256"] = hashlib.sha256(data).hexdigest()
        if resolved.suffix.lower() != ".pdf":
            fail("unsupported_format", "Only PDF attachment decoding is implemented.")
            continue
        try:
            reader = PdfReader(io.BytesIO(data))
            if reader.is_encrypted:
                fail("encrypted_pdf", "Encrypted PDF contents were not decoded.")
                continue
            doc["page_count"] = len(reader.pages)
            for page_number, page in enumerate(reader.pages, 1):
                try:
                    text = page.extract_text() or ""
                except (PdfReadError, ValueError, TypeError, NotImplementedError) as error:
                    fail("page_extraction_error", str(error), page_number=page_number)
                    continue
                page_id = f"{doc['id']}:p{page_number}"
                pages.append(
                    {
                        "id": page_id,
                        "document_id": doc["id"],
                        "document_sha256": doc["sha256"],
                        "relative_path": doc["relative_path"],
                        "page_number": page_number,
                        "text": text,
                        "text_sha256": hashlib.sha256(text.encode()).hexdigest(),
                        "available_at_event_ids": doc["available_at_event_ids"],
                        "extraction_method": doc["extraction_method"],
                        "extractor_version": doc["extractor_version"],
                        "offset_basis": "extracted_page_unicode_codepoints_end_exclusive",
                        "status": "text_extracted" if text.strip() else "no_extractable_text",
                    }
                )
                if not text.strip():
                    fail(
                        "no_extractable_text",
                        "No text was decoded on this page; visual content remains unexamined.",
                        page_number=page_number,
                    )
        except (PdfReadError, ValueError, TypeError, OSError, NotImplementedError) as error:
            fail("invalid_pdf", str(error))
            continue
        extracted = [p for p in pages if p["document_id"] == doc["id"] and p["text"].strip()]
        if doc["diagnostics"]:
            if extracted:
                doc["status"] = "partially_extracted"
        elif not doc["page_count"]:
            fail("empty_pdf", "PDF contains no pages.")
        else:
            doc["status"] = "text_extracted"

    # Equivalent reference paths may be encountered after a document was decoded.
    for page in pages:
        document = next(d for d in documents if d["id"] == page["document_id"])
        page["available_at_event_ids"] = document["available_at_event_ids"]
    return {
        "version": "prefix-attachments-v1",
        "case_id": case,
        "documents": documents,
        "pages": pages,
        "diagnostics": diagnostics,
        "semantics": {
            "availability": "explicit_link_in_supplied_prefix_only",
            "assertions": "document_claims_require_model_extraction_and_provenance",
            "visual_content": "not_extracted; empty_text_is_explicit_diagnostic",
            "offsets": "exact_extracted_page_text_not_pdf_bytes_or_visual_coordinates",
        },
    }
