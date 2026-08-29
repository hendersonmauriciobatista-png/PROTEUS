"""Immutable physical contracts for governed Core V1 measurements."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from .models import APSReference


class DataProvenance(str, Enum):
    MANUAL_ENTRY = "MANUAL_ENTRY"
    DEVICE_OR_SENSOR = "DEVICE_OR_SENSOR"
    EXTERNAL_RESULT = "EXTERNAL_RESULT"
    IMPORTED_DATA = "IMPORTED_DATA"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class GovernedMeasurementRequest:
    point_id: str
    parameter_reference: str
    value: float
    measured_at: datetime
    provenance: DataProvenance | str


@dataclass(frozen=True)
class GovernedMeasurement:
    measurement_id: str
    point_id: str
    context_revision_id: str
    aps_set_id: str
    aps_version: int
    parameter_reference: str
    value: float
    measured_at: str
    registered_at: str
    provenance: str


@dataclass(frozen=True)
class AuthorizationBasisResolution:
    basis_id: str
    authority_reference_ids: tuple[str, ...]
    evidence_reference_ids: tuple[str, ...]


@dataclass(frozen=True)
class APSMemberAuthorizationResolution:
    aps_reference: APSReference
    parameter_reference: str
    bases: tuple[AuthorizationBasisResolution, ...]
