"""Historical correspondence is a soft target, never normative correctness."""

from copy import deepcopy
from typing import Literal, Union, get_args

from pydantic import Field, create_model

from .models import StrictModel
from .response import EvidenceRef, ResponseAction


def historical_action_model(model):
    """Same result vocabulary/ranges, with explicit unknown observation slots."""
    fields = {}
    for name, original in model.model_fields.items():
        field = deepcopy(original)
        if name == "type":
            fields[name] = (original.annotation, field)
        else:
            field.default = None
            fields[name] = (original.annotation | None, field)
    return create_model(
        "Observed" + model.__name__,
        __base__=StrictModel,
        **fields,
    )


ObservedAction = Union[tuple(historical_action_model(m) for m in get_args(ResponseAction))]  # noqa: UP007


class TargetActor(StrictModel):
    id: str
    role: Literal["tenant", "landlord", "provider", "agency", "unknown"]
    surface: str
    evidence: list[EvidenceRef]
    prefix_entity_id: str | None


class HistoricalAction(StrictModel):
    action: ObservedAction = Field(discriminator="type")
    evidence: list[EvidenceRef]
    slot_evidence: dict[str, list[EvidenceRef]]
    unknown_slots: list[str]
    alternative_action_types: list[str]
    interpretation: str


class HistoricalTarget(StrictModel):
    version: Literal["historical-target-v1"]
    id: str
    case_id: str
    visibility: Literal["evaluation_only"]
    observation: Literal["recorded_communication", "mixed_speaker_call_summary"]
    intent_assessability: Literal["assessable", "partially_assessable", "unassessable"]
    actors: list[TargetActor]
    actions: list[HistoricalAction]
    source: dict
    review_status: str
    limits: list[str]


Verdict = Literal["match", "partial", "different", "unassessable"]


class JudgeCitation(StrictModel):
    origin: Literal["prefix", "target", "prediction"]
    source_id: str
    expression: str
    occurrence: int = Field(ge=1)


class DimensionJudgment(StrictModel):
    verdict: Verdict
    explanation: str
    citations: list[JudgeCitation]


class SemanticJudgment(StrictModel):
    version: Literal["soft-judge-v1"]
    overall_correspondence: Verdict
    action_intent: DimensionJudgment
    participants_roles: DimensionJudgment
    scope_conditions: DimensionJudgment
    sequencing: DimensionJudgment
    omissions_extras: DimensionJudgment
    target_predictability: Literal["observable", "partly_observable", "unobservable", "uncertain"]
    unobservable_target_specifics: list[str]
    prediction_supportedness: Literal["supported", "partly_supported", "unsupported", "uncertain"]
    support_explanation: str
    support_citations: list[JudgeCitation]
    target_encoding_concerns: list[str]
    confidence: Literal["low", "medium", "high"]


def mechanical_comparison(prediction, target):
    """Literal slots and type intersections: no claim of semantic equivalence."""
    predicted = prediction["actions"]
    pairs = []
    for expected in target["actions"]:
        action = expected["action"]
        for actual in predicted:
            if actual["type"] != action["type"]:
                continue
            slots = {
                key: {
                    "observed": value,
                    "predicted": actual.get(key),
                    "exact": actual.get(key) == value,
                }
                for key, value in action.items()
                if value is not None
                and key
                not in {
                    "id",
                    "type",
                    "request_id",
                    "recipient_id",
                    "provider_id",
                    "tenant_id",
                    "basis_record_ids",
                    "basis_gap_ids",
                    "depends_on_action_ids",
                }
            }
            pairs.append({"type": action["type"], "slots": slots})
    return {
        "same_type_pairs": pairs,
        "meaning": "Literal comparison only; unknown target slots and target-local identifiers excluded",
    }
