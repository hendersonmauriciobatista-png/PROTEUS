"""Immutable logical records authorized for DFA-02 Core V1 Wave 01."""

from dataclasses import dataclass, field
from enum import Enum


PURPOSES = {
    "ENVIRONMENTAL_CONDITION_MONITORING",
    "ENVIRONMENTAL_IMPACT_MONITORING",
    "COMPLIANCE_MONITORING",
    "WATER_USE_MONITORING",
}

WATER_CONTEXTS = {
    "FLOWING_SURFACE_WATER",
    "STANDING_SURFACE_WATER",
    "GROUNDWATER",
}

POINT_TYPES = {"GENERAL", "SPRING", "WELL", "ABSTRACTION_POINT"}


class PointStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class GovernanceAction(str, Enum):
    CURRENT_CONTEXT_REFERENCE_CHANGED = "CURRENT_CONTEXT_REFERENCE_CHANGED"
    APPLICABILITY_ASSIGNED = "APPLICABILITY_ASSIGNED"
    APPLICABILITY_CHANGED = "APPLICABILITY_CHANGED"
    APPLICABILITY_REMOVED = "APPLICABILITY_REMOVED"
    APS_VERSION_DISQUALIFIED = "APS_VERSION_DISQUALIFIED"
    APS_VERSION_REQUALIFIED = "APS_VERSION_REQUALIFIED"


@dataclass(frozen=True)
class GovernedMonitoringPoint:
    point_id: str
    project_reference: str
    display_name: str
    status: str
    current_context_revision_id: str | None = None
    external_station_reference: str | None = None


@dataclass(frozen=True)
class PointContextRevision:
    context_revision_id: str
    revision: int
    point_reference: str
    purpose: str
    water_context: str
    point_type: str
    geo_reference: str | None
    created_at: str
    effective_from: str | None = None
    effective_until: str | None = None


@dataclass(frozen=True)
class APSReference:
    set_id: str
    version: int


@dataclass(frozen=True)
class AuthorizationBasisDraft:
    basis_id: str
    authority_references: tuple[str, ...]
    evidence_references: tuple[str, ...]
    member_references: tuple[str, ...]


@dataclass(frozen=True)
class APSVersionDraft:
    set_id: str
    version: int
    context_revision_id: str
    parameter_references: tuple[str, ...]
    bases: tuple[AuthorizationBasisDraft, ...]


@dataclass(frozen=True)
class GovernanceEvent:
    event_id: str
    action: str
    actor_reference: str
    registered_at: str
    context_revision_id: str | None = None
    previous_aps: APSReference | None = None
    new_aps: APSReference | None = None
    target_aps: APSReference | None = None
    resolves_event_ids: tuple[str, ...] = field(default_factory=tuple)
