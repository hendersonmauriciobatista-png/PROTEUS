"""Immutable normalized GEO records and their governed state vocabulary."""

from dataclasses import dataclass
from enum import Enum


class GeoAvailabilityState(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    UNVERIFIED = "UNVERIFIED"
    LEGACY_UNCLASSIFIED = "LEGACY_UNCLASSIFIED"


class SourceAxisOrder(str, Enum):
    LATITUDE_LONGITUDE = "LATITUDE_LONGITUDE"
    LONGITUDE_LATITUDE = "LONGITUDE_LATITUDE"
    SOURCE_DECLARED_AXES = "SOURCE_DECLARED_AXES"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class LocationProvenance:
    provenance_id: str
    source_reference: str
    source_coordinate_1_raw: str
    source_coordinate_2_raw: str
    source_coordinate_1_numeric: float | None
    source_coordinate_2_numeric: float | None
    source_axis_order: str
    source_crs_identifier: str
    acquisition_method: str | None
    captured_at: str | None
    captured_at_status: str
    transformation_method: str | None
    transformation_parameters: str | None
    transformation_provenance: str | None
    accuracy_or_uncertainty_kind: str | None
    accuracy_or_uncertainty_value: float | None
    accuracy_or_uncertainty_unit: str | None
    registered_at: str

@dataclass(frozen=True)
class GeoReference:
    geo_reference_id: str
    context_revision_id: str
    availability_state: str
    latitude: float | None
    longitude: float | None
    crs_identifier: str | None
    location_provenance_id: str | None
    state_reason: str | None
    registered_at: str
