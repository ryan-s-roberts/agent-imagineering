"""Target-free evidence-to-response assessment contract, separate from history matching."""

from typing import Literal

from .citation_catalog import PrefixSpanSelection
from .models import StrictModel


class Dimension(StrictModel):
    verdict: Literal["supported", "partly_supported", "unsupported", "unassessable"]
    explanation: str
    citations: list[PrefixSpanSelection]


class ActionAssessment(StrictModel):
    action_id: str
    evidence_availability: Dimension
    evidence_warrant: Dimension
    authority_preconditions: Dimension
    epistemic_calibration: Dimension
    dependencies: Dimension
    rationale_fidelity: Dimension
    relevance_progress: Dimension


class Obligation(StrictModel):
    id: str
    description: str
    prefix_citations: list[PrefixSpanSelection]
    action_ids: list[str]
    coverage: Literal["covered", "partly_covered", "unmet", "unassessable"]
    explanation: str


class EvidenceResponseJudgment(StrictModel):
    version: Literal["evidence-response-v1"]
    actions: list[ActionAssessment]
    obligations: list[Obligation]
    duplicate_action_groups: list[list[str]]
    empty_response_assessment: str | None
    representation_limits: list[str]


def evidence_response_payload(packet, tbox, prediction, catalog):
    """Whitelist the input boundary; historical data is rejected, never summarized in."""
    if any(s["origin"] != "prefix" for s in catalog["spans"]):
        raise ValueError("Evidence-response judging requires a prefix-only citation catalog")
    if any(s["origin"] != "prefix" for s in catalog["sources"]):
        raise ValueError("Evidence-response judging requires prefix-only sources")
    return {
        "ontology_tbox": tbox,
        "prefix_evidence": packet,
        "prediction": prediction,
        "citation_catalog": catalog,
    }


def validate_judgment(raw, prediction, catalog):
    parsed = EvidenceResponseJudgment.model_validate(raw)
    ids = {a["id"] for a in prediction["actions"]}
    emitted = [a.action_id for a in parsed.actions]
    if len(emitted) != len(set(emitted)) or set(emitted) != ids:
        raise ValueError("Assess every proposed action exactly once")
    prefix_spans = {s["id"] for s in catalog["spans"] if s["origin"] == "prefix"}

    def walk(value):
        if isinstance(value, dict):
            if "span_id" in value and value["span_id"] not in prefix_spans:
                raise ValueError("Assessment citation is not a supplied prefix span")
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(parsed.model_dump())
    if len({o.id for o in parsed.obligations}) != len(parsed.obligations):
        raise ValueError("Duplicate obligation IDs")
    for obligation in parsed.obligations:
        if not obligation.prefix_citations:
            raise ValueError("Obligations must be evidenced in the prefix")
        if not set(obligation.action_ids) <= ids:
            raise ValueError("Obligation mapping references an absent action")
        if obligation.coverage == "covered" and not obligation.action_ids:
            raise ValueError("Covered obligation requires a proposed action")
    for group in parsed.duplicate_action_groups:
        if len(set(group)) < 2 or len(group) != len(set(group)) or not set(group) <= ids:
            raise ValueError("Duplicate group must name at least two distinct supplied actions")
    if not ids and not parsed.empty_response_assessment:
        raise ValueError("Empty response requires an explicit assessment")
    return parsed
