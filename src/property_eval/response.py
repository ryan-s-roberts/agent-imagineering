"""Static response ontology. A proposal is never an execution receipt."""

from typing import Literal

from pydantic import Field

from .benchmark_context import PartyReference, is_contextual_reference
from .grounding import resolve_span
from .models import StrictModel
from .validation import PARTY


class Action(StrictModel):
    id: str
    request_id: str
    basis_record_ids: list[str]
    basis_gap_ids: list[str]
    depends_on_action_ids: list[str]


class EvidenceRef(StrictModel):
    source_id: str
    expression: str = Field(min_length=1)
    occurrence: int = Field(ge=1)


class EscalationCause(StrictModel):
    category: Literal[
        "identity_conflict",
        "authority_required",
        "conflicting_evidence",
        "missing_evidence",
        "workflow_failure",
        "explicit_human_review",
        "safety_concern",
        "policy_exception",
        "other",
    ]
    explanation: str = Field(min_length=1)
    causal_status: Literal["asserted", "inferred", "unresolved"]
    evidence: list[EvidenceRef] = Field(min_length=1)
    record_ids: list[str]
    gap_ids: list[str]


class Clarify(Action):
    type: Literal["request_clarification"]
    recipient_id: PartyReference | None
    topic: Literal["identity", "authorization", "issue", "appointment", "work_outcome", "other"]
    question: str


class ApprovalRequest(Action):
    type: Literal["request_approval"]
    recipient_id: PartyReference
    scope: list[Literal["inspect", "repair", "replace", "dispose", "quote", "access"]] = Field(
        min_length=1
    )
    proposed_amount_minor: int | None = Field(ge=0)
    currency: str | None


class Instruct(Action):
    type: Literal["instruct_provider"]
    provider_id: str
    scope: list[Literal["inspect", "repair", "replace", "dispose", "quote", "access"]] = Field(
        min_length=1
    )
    authorization_record_ids: list[str]
    conditions: list[str]


class Booking(Action):
    type: Literal["propose_booking"]
    provider_id: str
    tenant_id: PartyReference | None
    time_text: str
    replaces_appointment_id: str | None


class WorkRequest(Action):
    type: Literal["request_work_report"]
    provider_id: str
    requested_fields: list[
        Literal["attendance", "diagnosis", "repair", "test_result", "invoice"]
    ] = Field(min_length=1)


class Closure(Action):
    type: Literal["propose_closure"]
    completion_record_ids: list[str]
    outstanding_gap_ids: list[str]
    reason: Literal["resolved", "tenant_managed", "cancelled", "duplicate", "no_work_required"]


class Escalate(Action):
    type: Literal["escalate"]
    recipient_id: PartyReference | None
    responsible_role: Literal["property_manager", "landlord", "supervisor", "specialist", "unknown"]
    causes: list[EscalationCause] = Field(min_length=1)
    requested_intervention: Literal[
        "resolve_identity",
        "approve_scope",
        "approve_spend",
        "adjudicate_evidence",
        "resolve_workflow_failure",
        "assess_safety",
        "review_case",
        "other",
    ]
    intervention_detail: str = Field(min_length=1)
    blocking: bool
    blocked_action_ids: list[str]
    handover: str


class Wait(Action):
    type: Literal["await_response"]
    responsible_party_id: PartyReference | None
    awaited: Literal["clarification", "approval", "appointment", "work_report", "confirmation"]


class Guidance(Action):
    type: Literal["provide_guidance"]
    recipient_id: PartyReference
    steps: list[str] = Field(min_length=1)
    requested_feedback: str | None


class Assignment(Action):
    type: Literal["assign_provider"]
    provider_id: str
    scope: list[str] = Field(min_length=1)


class Notify(Action):
    type: Literal["notify"]
    recipient_id: PartyReference
    purpose: Literal["confirmation", "reminder", "progress", "approval_outcome", "acknowledgement"]
    message: str = Field(min_length=1)
    about_record_ids: list[str]


class DocumentAction(Action):
    type: Literal["handle_document"]
    operation: Literal["request", "send", "register"]
    document_id: str | None
    recipient_id: PartyReference | None
    document_kind: Literal["quote", "invoice", "inspection_report", "work_report", "other"]


class Workflow(Action):
    type: Literal["change_workflow"]
    operation: Literal["hold", "resume", "review_completion", "change_mode", "revise_description"]
    value: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class Requirement(Action):
    type: Literal["resolve_requirement"]
    obligation_record_id: str
    resolution: Literal["satisfied", "waived"]
    reason: str = Field(min_length=1)


class CancelBooking(Action):
    type: Literal["cancel_booking"]
    appointment_id: str
    reason: str = Field(min_length=1)


class RecordEvidence(Action):
    type: Literal["record_evidence"]
    record_ids: list[str] = Field(min_length=1)


class HumanIntervention(StrictModel):
    """Observed lifecycle, separate from a proposed escalation."""

    id: str
    request_id: str
    escalation_action_id: str | None
    status: Literal["required", "requested", "sent", "acknowledged", "resolved", "declined"]
    responsible_role: str
    recipient_id: PartyReference | None
    causes: list[EscalationCause] = Field(min_length=1)
    requested_intervention: str
    evidence: list[EvidenceRef] = Field(min_length=1)
    response_record_ids: list[str]
    blocking_effect: Literal["blocked", "released", "unchanged", "unknown"]


ResponseAction = (
    Clarify
    | ApprovalRequest
    | Instruct
    | Booking
    | WorkRequest
    | Closure
    | Escalate
    | Wait
    | Guidance
    | Assignment
    | Notify
    | DocumentAction
    | Workflow
    | Requirement
    | CancelBooking
    | RecordEvidence
)


class DecisionRationale(StrictModel):
    selected_because: str
    evidence: list[EvidenceRef]
    uncertainties: list[str]
    assumptions: list[str]
    alternatives_considered: list[str]


class DecisionResponse(StrictModel):
    ontology_version: Literal["property-response-v4"]
    rationale: DecisionRationale
    case_id: str
    disposition: Literal["act", "clarify", "wait", "escalate", "conclude"]
    actions: list[ResponseAction]
    conclusion_record_ids: list[str]
    human_interventions: list[HumanIntervention]


def validate_response(
    response: DecisionResponse, packet: dict, benchmark_context: dict | None = None
) -> dict:
    entities = {e["id"]: e for e in packet["entities"]}
    records = {r["id"]: r for r in packet["records"]}
    gaps = {g["id"] for g in packet["gaps"]}
    issues, seen = [], set()
    action_ids = {a.id for a in response.actions}

    def valid_party(value):
        if isinstance(value, str):
            return entities.get(value, {}).get("kind") in PARTY
        return is_contextual_reference(value, benchmark_context, response.case_id)

    def record_refs(refs):
        for ref in refs:
            if ref not in records:
                issues.append("unknown_record")

    def evidence_refs(refs):
        for ref in refs:
            try:
                resolve_span(ref, packet.get("sources", []))
            except ValueError:
                issues.append("ungrounded_source_evidence")

    def causes(values):
        for cause in values:
            evidence_refs(cause.evidence)
            record_refs(cause.record_ids)
            if any(g not in gaps for g in cause.gap_ids):
                issues.append("unknown_gap")

    if response.case_id != packet["case_id"]:
        issues.append("wrong_case")
    evidence_refs(response.rationale.evidence)
    if not response.rationale.evidence:
        issues.append("missing_rationale_citations")
    if not response.rationale.selected_because.strip():
        issues.append("missing_decision_rationale")
    if response.disposition != "conclude" and not response.actions:
        issues.append("missing_actions")
    if response.disposition == "conclude" and not response.conclusion_record_ids:
        issues.append("unsupported_conclusion")
    if any(r not in records for r in response.conclusion_record_ids):
        issues.append("unknown_conclusion_record")
    for action in response.actions:
        data = action.model_dump()
        if not action.basis_record_ids and not action.basis_gap_ids:
            issues.append("unsupported_action_basis")
        if action.id in seen or any(a not in seen for a in action.depends_on_action_ids):
            issues.append("invalid_action_dependency")
        seen.add(action.id)
        req = entities.get(action.request_id)
        if req is None or req["kind"] not in {"maintenance_request", "work_order"}:
            issues.append("invalid_request")
        for field in ("recipient_id", "provider_id", "tenant_id", "responsible_party_id"):
            value = data.get(field)
            if value is not None and not valid_party(value):
                issues.append("invalid_party")
            if field == "tenant_id" and isinstance(value, dict) and value.get("role") != "tenant":
                issues.append("invalid_tenant_role")
        for record_id in action.basis_record_ids:
            if record_id not in records:
                issues.append("unknown_basis_record")
            elif records[record_id].get("request_id", action.request_id) not in {
                None,
                action.request_id,
            }:
                issues.append("cross_request_evidence")
        if any(g not in gaps for g in action.basis_gap_ids):
            issues.append("unknown_gap")
        for field in ("record_ids", "about_record_ids"):
            record_refs(data.get(field, []))
        for field, kinds in {
            "appointment_id": {"appointment"},
            "document_id": {"document", "quote", "invoice"},
        }.items():
            ref = data.get(field)
            if ref is not None and entities.get(ref, {}).get("kind") not in kinds:
                issues.append("invalid_" + field)
        if (
            action.type == "resolve_requirement"
            and records.get(action.obligation_record_id, {}).get("type") != "obligation"
        ):
            issues.append("invalid_obligation")
        if action.type == "escalate":
            causes(action.causes)
            if any(a not in action_ids or a == action.id for a in action.blocked_action_ids):
                issues.append("invalid_blocked_action")
            if not action.blocking and action.blocked_action_ids:
                issues.append("inconsistent_blocking_effect")
        if action.type == "instruct_provider":
            if not action.authorization_record_ids:
                issues.append("unestablished_authorization")
            for record_id in action.authorization_record_ids:
                record = records.get(record_id, {})
                if record.get("type") != "authorization" or record.get("decision") != "approved":
                    issues.append("unsupported_authorization")
                elif record.get("request_id") != action.request_id or not set(action.scope) <= set(
                    record["scope"]
                ):
                    issues.append("authorization_scope_mismatch")
                elif record.get("grantee_id") not in {None, action.provider_id}:
                    issues.append("authorization_grantee_mismatch")
                elif record.get("provenance", {}).get("polarity") != "positive":
                    issues.append("negated_authorization")
                elif record.get("provenance", {}).get("modality") in {
                    "planned",
                    "requested",
                    "unknown",
                }:
                    issues.append("unestablished_authorization")
        if action.type == "propose_booking" and action.replaces_appointment_id is not None:
            previous = entities.get(action.replaces_appointment_id, {})
            if previous.get("kind") != "appointment":
                issues.append("invalid_replaced_appointment")
        if action.type == "propose_closure":
            if action.reason == "resolved" and not action.completion_record_ids:
                issues.append("invalid_completion_evidence")
            if any(
                records.get(r, {}).get("type") != "work_report"
                or records.get(r, {}).get("request_id") != action.request_id
                or records.get(r, {}).get("outcome") not in {"repaired", "working"}
                or records.get(r, {}).get("provenance", {}).get("polarity") != "positive"
                or records.get(r, {}).get("provenance", {}).get("modality") != "actual"
                for r in action.completion_record_ids
                if action.reason == "resolved"
            ):
                issues.append("invalid_completion_evidence")
            record_refs(action.completion_record_ids)
            if any(g not in gaps for g in action.outstanding_gap_ids):
                issues.append("unknown_gap")
    intervention_ids = set()
    for intervention in response.human_interventions:
        if intervention.id in intervention_ids:
            issues.append("duplicate_intervention")
        intervention_ids.add(intervention.id)
        if entities.get(intervention.request_id, {}).get("kind") not in {
            "maintenance_request",
            "work_order",
        }:
            issues.append("invalid_request")
        if intervention.recipient_id is not None and not valid_party(intervention.recipient_id):
            issues.append("invalid_party")
        if intervention.escalation_action_id is not None and not any(
            a.id == intervention.escalation_action_id and a.type == "escalate"
            for a in response.actions
        ):
            issues.append("invalid_escalation_link")
        causes(intervention.causes)
        evidence_refs(intervention.evidence)
        record_refs(intervention.response_record_ids)
        if intervention.status in {"resolved", "declined"} and not intervention.response_record_ids:
            issues.append("unsupported_human_resolution")
    compatibility_codes = {
        "unsupported_authorization",
        "authorization_scope_mismatch",
        "authorization_grantee_mismatch",
        "negated_authorization",
        "unestablished_authorization",
        "invalid_completion_evidence",
        "unsupported_human_resolution",
    }
    return {
        "valid": not issues,
        "structurally_valid": not any(i not in compatibility_codes for i in issues),
        "evidence_compatible": not any(i in compatibility_codes for i in issues),
        "issues": issues,
        "meaning": "Structural and evidence compatibility only; no execution or policy approval",
    }
