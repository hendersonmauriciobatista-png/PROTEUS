"""Atomic fail-safe acceptance of governed water-quality measurements."""

import math
from datetime import datetime, timezone
from numbers import Real

from .identifiers import IdentifierFactory
from .measurement_models import (
    DataProvenance,
    GovernedMeasurement,
    GovernedMeasurementRequest,
)
from .reference_resolver import GovernedReferenceResolver


class GovernedMeasurementService:
    def __init__(self, repository, identifiers=None, clock=None):
        self.repository = repository
        self.identifiers = identifiers or IdentifierFactory()
        self.resolver = GovernedReferenceResolver(repository)
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def accept(self, request):
        if not isinstance(request, GovernedMeasurementRequest):
            raise TypeError("GovernedMeasurementRequest is required.")

        with self.repository.transaction() as connection:
            context, reference = self.resolver.resolve_operational_references(
                request.point_id,
                connection,
            )
            self.repository.resolve_member_authorization(
                reference,
                request.parameter_reference,
                connection,
            )
            provenance = _validate_provenance(request.provenance)
            measured_at = serialize_utc_instant(request.measured_at)
            value = _validate_value(request.value)
            measurement = GovernedMeasurement(
                measurement_id=self.identifiers.new("measurement"),
                point_id=request.point_id,
                context_revision_id=context.context_revision_id,
                aps_set_id=reference.set_id,
                aps_version=reference.version,
                parameter_reference=request.parameter_reference,
                value=value,
                measured_at=measured_at,
                registered_at=serialize_utc_instant(self.clock()),
                provenance=provenance,
            )
            self.repository.insert_measurement(measurement, connection)
        return self.repository.fetch_measurement(measurement.measurement_id)


def serialize_utc_instant(value):
    if not isinstance(value, datetime):
        raise ValueError("Timezone-aware datetime is required.")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("Timezone-aware datetime is required.")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00",
        "Z",
    )


def _validate_provenance(value):
    try:
        return DataProvenance(value).value
    except (TypeError, ValueError) as error:
        raise ValueError(f"Invalid explicit data provenance: {value}") from error


def _validate_value(value):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError("Measurement value must be numeric.")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ValueError("Measurement value must be finite.")
    return numeric
