"""Application seam for one explicit governed measurement entry."""

from datetime import datetime

from .measurement_models import DataProvenance, GovernedMeasurementRequest
from .measurement_service import GovernedMeasurementService
from .reference_resolver import GovernedReferenceResolver

CANONICAL_APS_PARAMETERS = ("PH", "TURBIDITY", "DISSOLVED_OXYGEN")


class ExplicitGovernedEntryService:
    def __init__(self, repository, measurement_service=None):
        self.repository = repository
        self.resolver = GovernedReferenceResolver(repository)
        self.measurements = measurement_service or GovernedMeasurementService(repository)

    def active_points(self):
        return self.repository.list_active_points()

    def canonical_parameters(self, point_id):
        reference = self.resolver.resolve_operational_aps(point_id)
        with self.repository._optional_connection(None) as connection:
            rows = connection.execute(
                "SELECT parameter_reference FROM aps_member "
                "WHERE set_id = ? AND version = ?",
                (reference.set_id, reference.version),
            ).fetchall()
        available = {row[0] for row in rows}
        return tuple(parameter for parameter in CANONICAL_APS_PARAMETERS if parameter in available)

    def submit(self, point_id, parameter_reference, value, measured_at):
        if parameter_reference not in CANONICAL_APS_PARAMETERS:
            raise ValueError("Parametro fora do conjunto APS canonico.")
        if not isinstance(measured_at, datetime) or measured_at.tzinfo is None:
            raise ValueError("Measured_at timezone-aware explicito e obrigatorio.")
        return self.measurements.accept(
            GovernedMeasurementRequest(
                point_id=point_id,
                parameter_reference=parameter_reference,
                value=value,
                measured_at=measured_at,
                provenance=DataProvenance.MANUAL_ENTRY,
            )
        )
