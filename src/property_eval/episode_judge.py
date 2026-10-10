"""Action-set assessment: many-to-many historical coverage, support and ordering."""

from copy import deepcopy
from typing import Literal

from .citation_catalog import PrefixSpanSelection, SpanSelection
from .models import StrictModel


class TargetAssessment(StrictModel):
    target_action_id: str
    prediction_action_ids: list[str]
    coverage: Literal["covered", "partial", "missing", "unassessable"]
    participants: Literal["match", "partial", "different", "unassessable"]
    scope_conditions: Literal["match", "partial", "different", "unassessable"]
    prefix_predictability: Literal[
        "observable", "partly_observable", "unobservable", "unassessable"
    ]
    explanation: str
    unobservable_specifics: list[str]
    citations: list[SpanSelection]
    predictability_citations: list[PrefixSpanSelection]


class PredictionAssessment(StrictModel):
    prediction_action_id: str
    supportedness: Literal["supported", "partly_supported", "unsupported", "unassessable"]
    extra_status: Literal[
        "mapped",
        "supported_extra",
        "unsupported_extra",
        "unassessable_extra",
        "auxiliary_duplicate",
    ]
    explanation: str
    citations: list[SpanSelection]
    support_citations: list[PrefixSpanSelection]


class OrderAssessment(StrictModel):
    order_id: str
    requiredness: Literal["required_by_meaning", "observed_only", "uncertain"]
    verdict: Literal["satisfied", "not_represented", "violated", "not_required", "unassessable"]
    explanation: str
    citations: list[SpanSelection]


class EpisodeJudgment(StrictModel):
    version: Literal["episode-judge-v1"]
    overall_correspondence: Literal["full", "partial", "different", "unassessable"]
    target_assessments: list[TargetAssessment]
    prediction_assessments: list[PredictionAssessment]
    necessary_order_assessments: list[OrderAssessment]
    boundary_assessability: Literal["clear", "uncertain", "unassessable"]
    boundary_concerns: list[str]
    explanation: str
    citations: list[SpanSelection]


def constrained_schema(catalog, target, prediction):
    schema = deepcopy(EpisodeJudgment.model_json_schema())
    definitions = schema["$defs"]
    definitions["SpanSelection"]["properties"]["span_id"]["enum"] = [
        s["id"] for s in catalog["spans"]
    ]
    definitions["PrefixSpanSelection"]["properties"]["span_id"]["enum"] = [
        s["id"] for s in catalog["spans"] if s["origin"] == "prefix"
    ]
    target_ids = [a["id"] for a in target["episode"]["actions"]]
    prediction_ids = [a["id"] for a in prediction["actions"]]
    order_ids = [o["id"] for o in target["necessary_order"]]
    for definition, field, ids in [
        ("TargetAssessment", "target_action_id", target_ids),
        ("PredictionAssessment", "prediction_action_id", prediction_ids),
        ("OrderAssessment", "order_id", order_ids),
    ]:
        if ids:
            definitions[definition]["properties"][field]["enum"] = ids
    mapping = definitions["TargetAssessment"]["properties"]["prediction_action_ids"]
    if prediction_ids:
        mapping["items"]["enum"] = prediction_ids
    else:
        mapping["maxItems"] = 0
    for field, ids in [
        ("target_assessments", target_ids),
        ("prediction_assessments", prediction_ids),
        ("necessary_order_assessments", order_ids),
    ]:
        schema["properties"][field]["minItems"] = len(ids)
        schema["properties"][field]["maxItems"] = len(ids)
    return schema


def materialize_episode(selection, catalog):
    spans = {s["id"]: s for s in catalog["spans"]}
    sources = {(s["origin"], s["id"]): s["text"] for s in catalog["sources"]}
    selected = []

    def walk(value, path=""):
        if isinstance(value, dict):
            if set(value) == {"span_id"}:
                item = spans[value["span_id"]]
                if (
                    any(
                        part in path
                        for part in ("/support_citations/", "/predictability_citations/")
                    )
                    and item["origin"] != "prefix"
                ):
                    raise ValueError("Support and predictability evidence must select prefix spans")
                text = sources[(item["origin"], item["source_id"])]
                if text[item["start"] : item["end"]] != item["expression"]:
                    raise ValueError("Catalog source slice changed")
                selected.append({"judgment_path": path, **item})
                return {k: item[k] for k in ("origin", "source_id", "expression", "occurrence")}
            return {k: walk(v, path + "/" + k) for k, v in value.items()}
        if isinstance(value, list):
            return [walk(v, path + "/" + str(i)) for i, v in enumerate(value)]
        return value

    return walk(selection), selected


class EpisodeValidator:
    def __init__(self, catalog, target, prediction):
        self.catalog, self.target, self.prediction = catalog, target, prediction

    def model_validate(self, raw):
        parsed = EpisodeJudgment.model_validate(raw)
        targets = {a["id"] for a in self.target["episode"]["actions"]}
        predictions = {a["id"] for a in self.prediction["actions"]}
        orders = {o["id"] for o in self.target["necessary_order"]}
        for rows, field, expected in [
            (parsed.target_assessments, "target_action_id", targets),
            (parsed.prediction_assessments, "prediction_action_id", predictions),
            (parsed.necessary_order_assessments, "order_id", orders),
        ]:
            emitted = [getattr(row, field) for row in rows]
            if len(emitted) != len(set(emitted)) or set(emitted) != expected:
                raise ValueError(f"Assess each {field} exactly once: expected {sorted(expected)}")
        for row in parsed.target_assessments:
            if not set(row.prediction_action_ids) <= predictions:
                raise ValueError("Mapping must use supplied prediction action IDs")
        if (
            not any(
                a["materiality"] in {"material", "workflow"}
                for a in self.target["episode"]["actions"]
            )
            and parsed.overall_correspondence != "unassessable"
        ):
            raise ValueError("No assessable operational target: overall must be unassessable")
        mapped = set()
        span_rows = {s["id"]: s for s in self.catalog["spans"]}
        annotations = {a["id"]: a for a in self.target["episode"]["actions"]}
        prediction_paths = {
            a["id"]: f"/actions/{i}/" for i, a in enumerate(self.prediction["actions"])
        }
        span_origins = {s["id"]: s["origin"] for s in self.catalog["spans"]}
        for row in parsed.target_assessments:
            ids = row.prediction_action_ids
            if len(ids) != len(set(ids)):
                raise ValueError("Do not repeat a prediction ID within one target assessment")
            if row.coverage in {"covered", "partial"} and not ids:
                raise ValueError("Covered/partial targets require prediction action mappings")
            if row.coverage == "missing" and ids:
                raise ValueError("Missing targets must have no prediction action mappings")
            if ids:
                origins = {span_origins.get(c.span_id) for c in row.citations}
                if not {"target", "prediction"} <= origins:
                    raise ValueError(
                        "Mapped correspondence requires target and prediction citations"
                    )
                quoted_sources = [
                    c["quote"] for c in annotations[row.target_action_id]["source_citations"]
                ]
                if not any(
                    span_rows.get(c.span_id, {}).get("origin") == "target"
                    and any(span_rows[c.span_id]["expression"] in q for q in quoted_sources)
                    for c in row.citations
                ):
                    raise ValueError(
                        "Mapped target needs citation to that included action source, not excluded tail"
                    )
                if not any(
                    span_rows.get(c.span_id, {}).get("origin") == "prediction"
                    and any(
                        span_rows[c.span_id]["path"].startswith(prediction_paths[i]) for i in ids
                    )
                    for c in row.citations
                ):
                    raise ValueError("Mapped prediction citation must reference a mapped action")
            mapped.update(ids)
        for row in parsed.prediction_assessments:
            if row.extra_status == "auxiliary_duplicate":
                continue
            if (row.extra_status == "mapped") != (row.prediction_action_id in mapped):
                raise ValueError("extra_status mapped must agree with supplied action mappings")
        try:
            materialize_episode(parsed.model_dump(), self.catalog)
        except KeyError as error:
            raise ValueError(f"Select only catalog span IDs: {error}") from error
        return parsed
