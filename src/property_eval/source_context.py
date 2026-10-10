"""One prefix evidence surface for events and explicitly linked attachment pages."""

import hashlib
import json

from .attachments import load_prefix_attachments
from .validation import source_units


def prefix_source_context(source_root, case, prefix):
    attachments = load_prefix_attachments(source_root, case, prefix.events)
    units = source_units(prefix)
    events = {event.id: event for event in prefix.events}
    source_texts = {event.id: event.text for event in prefix.events}
    for page in attachments["pages"]:
        first = min(page["available_at_event_ids"], key=int)
        if first not in events:
            raise ValueError("Attachment available outside supplied prefix")
        namespace = (
            f"attachment:{page['document_id']}:{page['document_sha256']}:p{page['page_number']}"
        )
        source_texts[namespace] = page["text"]
        offset = 0
        for line_number, line in enumerate(page["text"].splitlines(keepends=True), 1):
            text = line.rstrip("\r\n")
            if text.strip():
                units.append(
                    {
                        "id": f"{namespace}:L{line_number}",
                        "event_id": first,
                        "anchor_namespace": namespace,
                        "origin": "attachment",
                        "document_id": page["document_id"],
                        "document_sha256": page["document_sha256"],
                        "page_number": page["page_number"],
                        "relative_path": page["relative_path"],
                        "text_sha256": page["text_sha256"],
                        "available_at_event_ids": page["available_at_event_ids"],
                        "timestamp": events[first].timestamp,
                        "timestamp_semantics": "first_linked_availability_not_document_assertion_time",
                        "sender": "document author not established by attachment sender",
                        "channel": "attachment_text",
                        "text": text,
                        "start": offset,
                        "end": offset + len(text),
                        "offset_basis": page["offset_basis"],
                        "extraction_method": page["extraction_method"],
                        "extractor_version": page["extractor_version"],
                    }
                )
            offset += len(line)
    digest = hashlib.sha256(
        json.dumps(
            {"event_prefix_sha256": prefix.source_sha256, "attachments": attachments},
            ensure_ascii=False,
            sort_keys=True,
        ).encode()
    ).hexdigest()
    return {
        "sources": units,
        "attachments": attachments,
        "context_sha256": digest,
        "source_texts": source_texts,
    }
