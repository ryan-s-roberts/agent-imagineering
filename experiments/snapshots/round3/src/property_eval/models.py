"""Frozen property-evidence-v3 ontology. Types are authored, instances extracted."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Event(StrictModel):
    id: str
    timestamp: str
    channel: str
    sender: str
    recipient: str
    text: str


class Prefix(StrictModel):
    case_id: str
    cutoff: int
    source_sha256: str
    events: list[Event]


EntityKind = Literal[
    "person",
    "organization",
    "unresolved_party",
    "property",
    "asset",
    "maintenance_request",
    "work_order",
    "appointment",
    "quote",
    "invoice",
    "document",
]


class Mention(StrictModel):
    source_id: str = Field(description="Supplied source-unit ID")
    surface: str = Field(min_length=1, description="Short exact substring of the source unit")


class EvidenceSpan(StrictModel):
    source_id: str
    expression: str = Field(min_length=1)
    occurrence: int = Field(ge=1, description="One-based occurrence, mandatory even when unique")


class MentionCandidate(EvidenceSpan):
    kind: EntityKind


class MentionExtraction(StrictModel):
    mentions: list[MentionCandidate]


class IdentityLink(StrictModel):
    left_mention_id: str
    right_mention_id: str
    relationship: Literal["same", "different", "unresolved"]
    evidence: list[EvidenceSpan] = Field(min_length=1)


class LinkExtraction(StrictModel):
    links: list[IdentityLink]


class FieldEvidence(StrictModel):
    field: str = Field(
        description="Record field name or provenance.origin/modality/polarity/asserted_by_entity_id"
    )
    spans: list[EvidenceSpan] = Field(min_length=1)


class Entity(StrictModel):
    id: str = Field(min_length=1)
    kind: EntityKind
    label: str
    mentions: list[Mention] = Field(min_length=1)


class EntityExtraction(StrictModel):
    entities: list[Entity]


class Provenance(StrictModel):
    source_ids: list[str] = Field(
        min_length=1, description="Source IDs supporting ALL record fields"
    )
    asserted_by_entity_id: str | None = Field(
        description="Resolved speaker ENTITY ID; null if unknown. Never a name."
    )
    origin: Literal["system_record", "attributed_report", "unresolved"]
    modality: Literal["actual", "planned", "requested", "conditional", "unknown"]
    polarity: Literal["positive", "negative"]


class Record(StrictModel):
    id: str = Field(min_length=1)
    provenance: Provenance
    field_evidence: list[FieldEvidence]


class RoleRecord(Record):
    type: Literal["role"]
    party_id: str
    role: Literal["tenant", "landlord", "agent", "contractor", "inspector", "other"]
    context_id: str | None


class IssueRecord(Record):
    type: Literal["issue"]
    request_id: str
    asset_id: str | None
    property_id: str | None
    description: str
    troubleshooting: Literal["not_established", "requested", "reported_failed", "reported_resolved"]


class OwnershipRecord(Record):
    type: Literal["ownership"]
    owner_id: str
    asset_id: str
    conditions: list[str]


class AssignmentRecord(Record):
    type: Literal["assignment"]
    request_id: str
    provider_id: str


class AuthorizationRecord(Record):
    type: Literal["authorization"]
    request_id: str
    grantor_id: str | None
    grantee_id: str | None
    scope: list[
        Literal["inspect", "repair", "replace", "dispose", "quote", "access", "unspecified"]
    ] = Field(min_length=1)
    decision: Literal["approved", "denied", "requested", "uncertain"]
    amount_minor: int | None = Field(ge=0)
    currency: str | None
    conditions: list[str]


class AppointmentRecord(Record):
    type: Literal["appointment"]
    appointment_id: str
    request_id: str | None
    provider_id: str | None
    tenant_id: str | None
    status: Literal["proposed", "confirmed", "rescheduled", "cancelled", "arrival_announced"]
    time_text: str | None
    supersedes_record_id: str | None


class WorkRecord(Record):
    type: Literal["work_report"]
    request_id: str
    asset_id: str | None
    document_id: str | None
    outcome: Literal["attended", "repaired", "working", "unresolved", "not_attended", "unknown"]
    description: str


class StatusRecord(Record):
    type: Literal["request_status"]
    request_id: str
    status: Literal[
        "open",
        "on_hold",
        "awaiting_approval",
        "awaiting_provider",
        "awaiting_results",
        "completion_review",
        "closed",
        "completed_without_payment",
        "other",
    ]
    source_label: str


class ObligationRecord(Record):
    type: Literal["obligation"]
    request_id: str
    responsible_party_id: str | None
    requirement: Literal[
        "clarification",
        "approval",
        "quote",
        "appointment",
        "work_report",
        "invoice",
        "confirmation",
        "key_return",
        "other",
    ]
    status: Literal["requested", "pending", "satisfied", "waived", "uncertain"]
    conditions: list[str]


class IdentityRecord(Record):
    type: Literal["identity"]
    left_id: str
    right_id: str
    relationship: Literal["same", "different", "unresolved"]


class ProposalRecord(Record):
    type: Literal["work_proposal"]
    request_id: str
    asset_id: str | None
    provider_id: str | None
    scope: list[Literal["inspect", "repair", "replace", "dispose", "quote", "access"]]
    amount_minor: int | None
    currency: str | None
    conditions: list[str]
    valid_time_text: str | None


class AccessRecord(Record):
    type: Literal["access_constraint"]
    request_id: str
    party_id: str | None
    constraint: Literal["availability", "keyholder", "notice", "entry_permission", "other"]
    status: Literal["available", "unavailable", "required", "unknown"]
    time_text: str | None
    description: str


class CommunicationRecord(Record):
    type: Literal["communication"]
    request_id: str
    sender_id: str | None
    recipient_id: str | None
    purpose: Literal[
        "clarification", "approval", "appointment", "work_report", "confirmation", "other"
    ]
    status: Literal["requested", "answered", "no_response_reported"]
    responds_to_record_id: str | None
    deadline_text: str | None


class ConditionRecord(Record):
    type: Literal["condition"]
    request_id: str
    constrains_record_id: str
    requirement: Literal[
        "approval", "cost_limit", "access", "confirmation", "invoice", "key_return", "other"
    ]
    status: Literal["satisfied", "contradicted", "unknown"]
    description: str


OperationalRecord = (
    RoleRecord
    | IssueRecord
    | OwnershipRecord
    | AssignmentRecord
    | AuthorizationRecord
    | AppointmentRecord
    | WorkRecord
    | StatusRecord
    | ObligationRecord
    | IdentityRecord
    | ProposalRecord
    | AccessRecord
    | CommunicationRecord
    | ConditionRecord
)


class Gap(StrictModel):
    id: str
    kind: Literal[
        "identity", "authorization", "timing", "missing_evidence", "conflict", "unclassified"
    ]
    entity_ids: list[str]
    source_ids: list[str] = Field(min_length=1)
    description: str


class RecordExtraction(StrictModel):
    records: list[OperationalRecord]
    gaps: list[Gap]
