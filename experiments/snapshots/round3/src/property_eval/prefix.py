"""Parse history only: never send index summaries, outcomes or future attachments."""

import hashlib
import re
from pathlib import Path

from .models import Event, Prefix

HEADER = re.compile(r"^## (.+?) — event (\d+)\s*$", re.MULTILINE)


def load_prefix(source: Path, case: str, cutoff: int) -> Prefix:
    if not re.fullmatch(r"\d{3}", case):
        raise ValueError("Case must be three digits")
    text = (source / "Property Management" / case / "history.md").read_text()
    headers = list(HEADER.finditer(text))
    events = []
    for i, header in enumerate(headers):
        number = int(header[2])
        if number != i + 1:
            raise ValueError("Non-contiguous event numbering")
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        body = re.sub(r'<a id="event-\d+"></a>', "", text[header.end() : end]).strip()

        def field(name: str, body=body, number=number) -> str:
            match = re.search(rf"^- \*\*{name}:\*\* (.+)$", body, re.MULTILINE)
            if not match:
                raise ValueError(f"Missing {name} on event {number}")
            return match[1]

        events.append(
            Event(
                id=f"{number:03}",
                timestamp=header[1],
                channel=field("Channel"),
                sender=field("From"),
                recipient=field("To"),
                text=body,
            )
        )
    if not 1 <= cutoff <= len(events):
        raise ValueError(f"Cutoff must be in 1..{len(events)}")
    selected = events[:cutoff]
    payload = "\n".join(e.model_dump_json() for e in selected)
    return Prefix(
        case_id=f"property-{case}",
        cutoff=cutoff,
        source_sha256=hashlib.sha256(payload.encode()).hexdigest(),
        events=selected,
    )
