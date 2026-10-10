"""Explicit user-supplied addressability assumptions, never extracted facts."""

from typing import Literal

from .models import StrictModel


class ContextualPartyReference(StrictModel):
    kind: Literal["contextual_role"]
    role: Literal["landlord", "tenant"]
    case_id: str
    provenance: Literal["benchmark_assumption"]


# An observed entity ID and an assumed addressable contextual role are distinct references.
PartyReference = str | ContextualPartyReference


class BenchmarkContext(StrictModel):
    version: Literal["property-benchmark-context-v1"]
    case_id: str
    provenance: Literal["benchmark_assumption"]
    authority: Literal["explicit_user_instruction"]
    addressable_roles: list[ContextualPartyReference]
    assumption: str
    limits: list[str]


def context_for_case(case_id):
    return BenchmarkContext(
        version="property-benchmark-context-v1",
        case_id=case_id,
        provenance="benchmark_assumption",
        authority="explicit_user_instruction",
        addressable_roles=[
            ContextualPartyReference(
                kind="contextual_role",
                role=role,
                case_id=case_id,
                provenance="benchmark_assumption",
            )
            for role in ("landlord", "tenant")
        ],
        assumption="The landlord and tenant are known and addressable through the case/property context even when names or CRM IDs are omitted.",
        limits=[
            "Does not identify a named person or invent an extracted entity.",
            "Does not supply approval, work completion, policy or permission.",
            "Actual conflicting relationships or ambiguous applicable properties remain material uncertainty.",
        ],
    ).model_dump()


def is_contextual_reference(value, context, case_id):
    if isinstance(value, ContextualPartyReference):
        value = value.model_dump()
    if not isinstance(value, dict) or not context:
        return False
    return (
        context.get("case_id") == case_id
        and value.get("case_id") == case_id
        and value in context.get("addressable_roles", [])
    )
