"""The judge selects immutable host spans; it never writes quotes or offsets."""

import json
from copy import deepcopy
from typing import Literal

from .models import StrictModel
from .soft_eval import SemanticJudgment, Verdict


class SpanSelection(StrictModel):
    span_id: str


class PrefixSpanSelection(StrictModel):
    span_id: str


class SelectedDimension(StrictModel):
    verdict: Verdict
    explanation: str
    citations: list[SpanSelection]


class SelectedJudgment(SemanticJudgment):
    version: Literal["soft-judge-v2"]
    action_intent: SelectedDimension
    participants_roles: SelectedDimension
    scope_conditions: SelectedDimension
    sequencing: SelectedDimension
    omissions_extras: SelectedDimension
    support_citations: list[PrefixSpanSelection]


class MaterializedJudgment(SemanticJudgment):
    version: Literal["soft-judge-v2"]


def json_leaf_spans(value):
    """Serialize identically to sorted json.dumps, recording literal leaf positions."""
    chunks, spans, position = [], [], 0

    def emit(text):
        nonlocal position
        chunks.append(text)
        position += len(text)

    def walk(item, path):
        start = position
        if isinstance(item, dict) and item:
            emit("{")
            for i, key in enumerate(sorted(item)):
                if i:
                    emit(", ")
                emit(json.dumps(key, ensure_ascii=False) + ": ")
                walk(item[key], path + "/" + key.replace("~", "~0").replace("/", "~1"))
            emit("}")
        elif isinstance(item, list) and item:
            emit("[")
            for i, child in enumerate(item):
                if i:
                    emit(", ")
                walk(child, path + "/" + str(i))
            emit("]")
        else:
            emit(json.dumps(item, ensure_ascii=False))
            spans.append({"start": start, "end": position, "path": path or "/"})

    walk(value, "")
    text = "".join(chunks)
    assert text == json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text, spans


def build_catalog(packet, target, prediction):
    sources, spans = [], []

    def source(origin, source_id, text):
        sources.append({"origin": origin, "id": source_id, "text": text})

    def span(origin, source_id, text, start, end, path):
        quote = text[start:end]
        if not quote:
            return
        spans.append(
            {
                "id": f"span{len(spans) + 1:04}",
                "origin": origin,
                "source_id": source_id,
                "start": start,
                "end": end,
                "expression": quote,
                "occurrence": text[:start].count(quote) + 1,
                "path": path,
            }
        )

    for unit in packet["sources"]:
        source("prefix", unit["id"], unit["text"])
        span("prefix", unit["id"], unit["text"], 0, len(unit["text"]), unit["id"])
    target_source = target["source"]
    source("target", target_source["id"], target_source["text"])
    start = 0
    for line in target_source["text"].splitlines(keepends=True):
        end = start + len(line.rstrip("\r\n"))
        if line.strip():
            span("target", target_source["id"], target_source["text"], start, end, f"line@{start}")
        start += len(line)
    text, leaves = json_leaf_spans(prediction)
    source("prediction", "prediction", text)
    for leaf in leaves:
        span("prediction", "prediction", text, leaf["start"], leaf["end"], leaf["path"])
    return {
        "version": "citation-catalog-v1",
        "sources": sources,
        "spans": spans,
        "meaning": "Host-authored immutable positions. Prediction spans are generated claims, not evidence about the external world.",
    }


def selection_schema(catalog, response_model=SelectedJudgment):
    schema = deepcopy(response_model.model_json_schema())
    schema["$defs"]["SpanSelection"]["properties"]["span_id"]["enum"] = [
        s["id"] for s in catalog["spans"]
    ]
    schema["$defs"]["PrefixSpanSelection"]["properties"]["span_id"]["enum"] = [
        s["id"] for s in catalog["spans"] if s["origin"] == "prefix"
    ]
    return schema


def materialize(selection, catalog, response_model=MaterializedJudgment):
    spans = {s["id"]: s for s in catalog["spans"]}
    sources = {(s["origin"], s["id"]): s["text"] for s in catalog["sources"]}
    selected = []

    def walk(value, path=""):
        if isinstance(value, dict):
            if set(value) == {"span_id"}:
                item = spans[value["span_id"]]  # Unknown IDs fail; no fuzzy lookup.
                if path.startswith("/support_citations") and item["origin"] != "prefix":
                    raise ValueError("World-support citations must select prefix spans")
                text = sources[(item["origin"], item["source_id"])]
                if text[item["start"] : item["end"]] != item["expression"]:
                    raise ValueError("Immutable citation catalog was altered")
                selected.append({"judgment_path": path, **item})
                return {k: item[k] for k in ("origin", "source_id", "expression", "occurrence")}
            return {key: walk(child, path + "/" + key) for key, child in value.items()}
        if isinstance(value, list):
            return [walk(child, path + "/" + str(i)) for i, child in enumerate(value)]
        return value

    result = response_model.model_validate(walk(selection))
    return result.model_dump(), selected
