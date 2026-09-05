"""Governed normalized GEO persistence and historical resolution."""

import math
import re
from contextlib import contextmanager
from datetime import datetime, timezone

from .geo_models import GeoAvailabilityState, GeoReference, LocationProvenance, SourceAxisOrder
from .geo_crs import CRSResolver, CoordinateTransformer
from .identifiers import IdentifierFactory
from .measurement_service import serialize_utc_instant
from .repository import GovernedReferenceError


class GeoReferenceResolutionError(GovernedReferenceError):
    reason_code = "GEO_REFERENCE_UNRESOLVED"

    def __init__(self, message=None, reason_code=None):
        self.reason_code = reason_code or self.reason_code
        super().__init__(message or self.reason_code)


class GeoService:
    def __init__(self, repository, identifiers=None, clock=None):
        self.repository = repository
        self.identifiers = identifiers or IdentifierFactory()
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def register_provenance(self, record, connection=None):
        try:
            self._validate_provenance(record)
        except (TypeError, ValueError) as error:
            raise GeoReferenceResolutionError(str(error), "GEO_PROVENANCE_INVALID") from error
        with _operation(self.repository, connection) as active:
            self.repository.insert_location_provenance(record, active)
        return record

    def create_reference(self, context_revision_id, availability_state,
                         *, latitude=None, longitude=None, crs_identifier=None,
                         location_provenance_id=None, state_reason=None,
                         geo_reference_id=None, registered_at=None, connection=None):
        try:
            state = GeoAvailabilityState(availability_state).value
        except (TypeError, ValueError) as error:
            raise GeoReferenceResolutionError("Invalid GEO availability state.", "GEO_STATE_INVALID") from error
        self._validate_reference(state, latitude, longitude, crs_identifier,
                                 location_provenance_id, state_reason)
        if state == GeoAvailabilityState.AVAILABLE.value:
            canonical = CRSResolver().resolve(crs_identifier)
            if canonical.state != "RESOLVED_CRS":
                raise GeoReferenceResolutionError(canonical.reason_code or "CRS_UNRESOLVED", canonical.reason_code)
            from pyproj import CRS
            target_crs = CRS.from_user_input(crs_identifier)
            if not target_crs.is_geographic or len(target_crs.axis_info) != 2:
                raise GeoReferenceResolutionError("CRS_NOT_GEOGRAPHIC_LATLON", "CRS_NOT_GEOGRAPHIC_LATLON")
            provenance = self.repository.fetch_location_provenance(
                location_provenance_id, connection
            )
            if provenance is None:
                raise GeoReferenceResolutionError("GEO provenance is not resolvable.", "GEO_PROVENANCE_UNRESOLVED")
            source_resolution = CRSResolver().resolve(provenance.source_crs_identifier)
            if source_resolution.state != "RESOLVED_CRS":
                raise GeoReferenceResolutionError(source_resolution.reason_code or "CRS_UNRESOLVED", source_resolution.reason_code)
            if provenance.source_axis_order == SourceAxisOrder.UNKNOWN.value:
                raise GeoReferenceResolutionError("CRS_AXIS_ORDER_UNRESOLVED", "CRS_AXIS_ORDER_UNRESOLVED")
            if provenance.source_coordinate_1_numeric is None or provenance.source_coordinate_2_numeric is None:
                raise GeoReferenceResolutionError("SOURCE_COORDINATES_UNRESOLVED", "SOURCE_COORDINATES_UNRESOLVED")
            source_crs = CRS.from_user_input(provenance.source_crs_identifier)
            if source_crs != target_crs and not (
                provenance.transformation_method and provenance.transformation_provenance
            ):
                raise GeoReferenceResolutionError(
                    "Transformation provenance is required when CRS differs.",
                    "TRANSFORMATION_PROVENANCE_MISSING",
                )
            transformed = CoordinateTransformer(crs_identifier).transform(
                provenance.source_crs_identifier,
                (provenance.source_coordinate_1_numeric, provenance.source_coordinate_2_numeric),
                provenance.source_axis_order,
            )
            if transformed.state != "TRANSFORMED_COORDINATE":
                raise GeoReferenceResolutionError(
                    transformed.reason_code or "TRANSFORMATION_UNAVAILABLE",
                    transformed.reason_code,
                )
            if float(latitude) != transformed.latitude or float(longitude) != transformed.longitude:
                raise GeoReferenceResolutionError(
                    "Canonical coordinates do not match the resolved transformation.",
                    "CANONICAL_COORDINATE_MISMATCH",
                )
        if geo_reference_id is None:
            geo_reference_id = self.identifiers.new("geo_reference")
        if registered_at is not None:
            try:
                _validate_utc_timestamp(registered_at, "registered_at")
            except ValueError as error:
                raise GeoReferenceResolutionError(str(error), "GEO_TIMESTAMP_INVALID") from error
        record = GeoReference(
            geo_reference_id, context_revision_id, state, latitude, longitude,
            crs_identifier, location_provenance_id, state_reason,
            registered_at or serialize_utc_instant(self.clock()),
        )
        with _operation(self.repository, connection) as active:
            self.repository.insert_geo_reference(record, active)
        return record

    def fetch_for_context(self, context_revision_id, connection=None):
        record = self.repository.fetch_geo_reference(context_revision_id, connection)
        if record is None:
            raise GeoReferenceResolutionError(
                f"GEO reference not resolvable: {context_revision_id}"
            )
        return record

    def resolve_for_measurement(self, measurement, connection=None):
        context = self.repository.fetch_temporal_context(
            measurement.point_id, measurement.measured_at, connection
        )
        if context.context_revision_id != measurement.context_revision_id:
            raise GeoReferenceResolutionError("Measurement context provenance mismatch.")
        return self.fetch_for_context(context.context_revision_id, connection)

    @staticmethod
    def _validate_provenance(record):
        if not isinstance(record, LocationProvenance):
            raise TypeError("LocationProvenance is required.")
        for value in (record.provenance_id, record.source_reference,
                      record.source_coordinate_1_raw, record.source_coordinate_2_raw,
                      record.source_crs_identifier, record.registered_at):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("GEO provenance required text is nonempty.")
        _validate_utc_timestamp(record.registered_at, "registered_at")
        if record.source_axis_order not in {item.value for item in SourceAxisOrder}:
            raise ValueError("Invalid source axis order.")
        if record.captured_at_status == "KNOWN" and not record.captured_at:
            raise ValueError("KNOWN capture time requires captured_at.")
        if record.captured_at is not None:
            _validate_utc_timestamp(record.captured_at, "captured_at")
        if record.captured_at_status == "UNKNOWN" and record.captured_at is not None:
            raise ValueError("UNKNOWN capture time cannot have captured_at.")
        if record.captured_at_status not in {"KNOWN", "UNKNOWN"}:
            raise ValueError("Invalid capture time status.")
        for number in (record.source_coordinate_1_numeric, record.source_coordinate_2_numeric,
                       record.accuracy_or_uncertainty_value):
            if number is not None and not math.isfinite(float(number)):
                raise ValueError("GEO numeric provenance must be finite.")
        if record.accuracy_or_uncertainty_value is not None and record.accuracy_or_uncertainty_value < 0:
            raise ValueError("Accuracy or uncertainty cannot be negative.")
        accuracy_values = (record.accuracy_or_uncertainty_kind,
                           record.accuracy_or_uncertainty_value,
                           record.accuracy_or_uncertainty_unit)
        if any(value is not None for value in accuracy_values) and not all(value is not None for value in accuracy_values):
            raise ValueError("Accuracy or uncertainty fields must be complete.")
        transformation_values = (record.transformation_method, record.transformation_provenance)
        if any(value is not None for value in transformation_values) and not all(
            isinstance(value, str) and value.strip() for value in transformation_values
        ):
            raise ValueError("Transformation provenance must be complete.")

    @staticmethod
    def _validate_reference(state, latitude, longitude, crs_identifier,
                            provenance_id, state_reason):
        if state == GeoAvailabilityState.AVAILABLE.value:
            if latitude is None or longitude is None or not crs_identifier or not provenance_id:
                raise GeoReferenceResolutionError("AVAILABLE GEO requires coordinates, CRS and provenance.", "GEO_REFERENCE_INVALID")
            try:
                canonical_latitude = float(latitude)
                canonical_longitude = float(longitude)
            except (TypeError, ValueError, OverflowError) as error:
                raise GeoReferenceResolutionError("GEO coordinates must be numeric.", "GEO_COORDINATES_INVALID") from error
            if not math.isfinite(canonical_latitude) or not math.isfinite(canonical_longitude):
                raise GeoReferenceResolutionError("GEO coordinates must be finite.", "GEO_COORDINATES_INVALID")
            if not -90 <= canonical_latitude <= 90 or not -180 <= canonical_longitude <= 180:
                raise GeoReferenceResolutionError("GEO coordinates are outside canonical bounds.", "GEO_COORDINATES_INVALID")
            if state_reason is not None:
                raise GeoReferenceResolutionError("AVAILABLE GEO cannot have a state reason.", "GEO_REFERENCE_INVALID")
        elif state in {GeoAvailabilityState.UNAVAILABLE.value, GeoAvailabilityState.LEGACY_UNCLASSIFIED.value}:
            if any(value is not None for value in (latitude, longitude, crs_identifier, provenance_id)):
                raise GeoReferenceResolutionError("Unavailable GEO cannot contain canonical location data.", "GEO_REFERENCE_INVALID")
            if not state_reason or not state_reason.strip():
                raise GeoReferenceResolutionError("Unavailable GEO requires a reason.", "GEO_REFERENCE_INVALID")
        elif state == GeoAvailabilityState.UNVERIFIED.value:
            if (latitude is not None or longitude is not None or crs_identifier is not None
                    or not provenance_id or not state_reason or not state_reason.strip()):
                raise GeoReferenceResolutionError(
                    "UNVERIFIED GEO requires no canonical coordinates or CRS, plus provenance and a reason.",
                    "GEO_REFERENCE_INVALID",
                )


@contextmanager
def _operation(repository, connection):
    if connection is not None:
        yield connection
    else:
        with repository.transaction() as active:
            yield active


def _validate_utc_timestamp(value, field):
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{6})?Z", value
    ):
        raise ValueError(f"{field} must be a canonical UTC timestamp.")
    formats = ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ")
    for timestamp_format in formats:
        try:
            datetime.strptime(value, timestamp_format)
            return
        except ValueError:
            continue
    raise ValueError(f"{field} must be a valid canonical UTC timestamp.")
