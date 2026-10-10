from pathlib import Path

from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from property_eval.attachments import load_prefix_attachments


def write_pdf(path: Path, texts: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    for text in texts:
        page = writer.add_blank_page(width=300, height=300)
        if text:
            font = DictionaryObject(
                {
                    NameObject("/Type"): NameObject("/Font"),
                    NameObject("/Subtype"): NameObject("/Type1"),
                    NameObject("/BaseFont"): NameObject("/Helvetica"),
                }
            )
            page[NameObject("/Resources")] = DictionaryObject(
                {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})}
            )
            stream = DecodedStreamObject()
            stream.set_data(f"BT /F1 12 Tf 30 250 Td ({text}) Tj ET".encode())
            page[NameObject("/Contents")] = stream
    with path.open("wb") as output:
        writer.write(output)


def event(number, text):
    return {"id": f"{number:03}", "text": text}


def test_only_visible_links_are_loaded(tmp_path):
    case = tmp_path / "Property Management/001/attachments"
    write_pdf(case / "quote.pdf", ["Repair quote GBP 90", "Provider Example Ltd"])
    write_pdf(case / "future.pdf", ["Future approval"])
    before = load_prefix_attachments(tmp_path, "001", [event(1, "A quote is expected.")])
    assert before["documents"] == []
    result = load_prefix_attachments(
        tmp_path, "001", [event(1, "A quote is expected."), event(2, "[Quote](attachments/quote.pdf)")]
    )
    assert len(result["documents"]) == 1
    document = result["documents"][0]
    assert document["available_at_event_ids"] == ["002"]
    assert document["status"] == "text_extracted"
    assert len(document["sha256"]) == 64
    assert [p["page_number"] for p in result["pages"]] == [1, 2]
    assert "GBP 90" in result["pages"][0]["text"]
    assert "Future approval" not in str(result)
    assert result["diagnostics"] == []


def test_equivalent_paths_and_repeated_links_share_document(tmp_path):
    write_pdf(tmp_path / "Property Management/001/attachments/my quote.pdf", ["Quote"])
    result = load_prefix_attachments(
        tmp_path,
        "001",
        [
            event(2, "[Quote](attachments/my%20quote.pdf)"),
            event(3, "[Quote](<./attachments/my quote.pdf>)"),
        ],
    )
    assert len(result["documents"]) == 1
    assert len(result["pages"]) == 1
    assert result["documents"][0]["available_at_event_ids"] == ["002", "003"]
    assert result["pages"][0]["available_at_event_ids"] == ["002", "003"]
    assert len(result["documents"][0]["references"]) == 2


def test_blank_page_remains_explicit(tmp_path):
    write_pdf(tmp_path / "Property Management/001/attachments/invoice.pdf", ["Invoice 70", ""])
    result = load_prefix_attachments(
        tmp_path, "001", [event(1, "[Invoice](attachments/invoice.pdf)")]
    )
    assert result["documents"][0]["status"] == "partially_extracted"
    assert result["pages"][1]["status"] == "no_extractable_text"
    assert result["diagnostics"][0]["page_number"] == 2


def test_missing_remote_and_outside_case_are_diagnostics(tmp_path):
    result = load_prefix_attachments(
        tmp_path,
        "001",
        [
            event(
                1,
                "[Missing](attachments/missing.pdf) "
                "[Remote](https://example.test/doc.pdf) "
                "[Outside](../002/attachments/private.pdf)",
            )
        ],
    )
    assert {d["status"] for d in result["documents"]} == {
        "unreadable_file", "remote_not_loaded", "outside_case"
    }
    assert result["pages"] == []


def test_symlink_escape_is_not_loaded(tmp_path):
    attachments = tmp_path / "Property Management/001/attachments"
    attachments.mkdir(parents=True)
    outside = tmp_path / "outside.pdf"
    write_pdf(outside, ["Not case evidence"])
    (attachments / "linked.pdf").symlink_to(outside)
    result = load_prefix_attachments(tmp_path, "001", [event(1, "[PDF](attachments/linked.pdf)")])
    assert result["documents"][0]["status"] == "outside_case"
    assert result["pages"] == []


def test_link_span_and_page_hash_are_exact(tmp_path):
    import hashlib

    write_pdf(tmp_path / "Property Management/001/attachments/quote.pdf", ["Quoted amount 123"])
    body = "See [quote](attachments/quote.pdf) for details."
    result = load_prefix_attachments(tmp_path, "001", [event(4, body)])
    ref = result["documents"][0]["references"][0]
    assert body[ref["start"] : ref["end"]] == ref["expression"]
    page = result["pages"][0]
    assert hashlib.sha256(page["text"].encode()).hexdigest() == page["text_sha256"]


def test_invalid_pdf_is_not_successful_empty_extraction(tmp_path):
    target = tmp_path / "Property Management/001/attachments/broken.pdf"
    target.parent.mkdir(parents=True)
    target.write_bytes(b"not a PDF")
    result = load_prefix_attachments(tmp_path, "001", [event(1, "[PDF](attachments/broken.pdf)")])
    assert result["documents"][0]["status"] == "invalid_pdf"
    assert result["diagnostics"]
