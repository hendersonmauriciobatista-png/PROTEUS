"""Append-only observational evaluation persistence for governed measurements."""
import json
from datetime import datetime, timezone

from .identifiers import IdentifierFactory
from .measurement_models import GovernedEvaluation
from .measurement_service import serialize_utc_instant
from .repository import GovernedReferenceError

ENGINE = "OBSERVATIONAL_EVALUATOR_V1"
ENGINE_VERSION = "1"
VALID = {"NORMAL", "ATENCAO", "CRITICO", "NAO_AVALIAVEL"}

class GovernedEvaluationService:
    def __init__(self, repository, identifiers=None, clock=None):
        self.repository = repository
        self.identifiers = identifiers or IdentifierFactory()
        self.clock = clock or (lambda: datetime.now(timezone.utc))

    def record(self, measurement_id, status, message, rule_origin, evaluated_at,
               explanation_data=None):
        if status not in VALID:
            raise ValueError("Invalid observational evaluation status.")
        if not message or not rule_origin:
            raise ValueError("Evaluation message and rule origin are required.")
        measurement = self.repository.fetch_measurement(measurement_id)
        # Resolution is revalidated before persistence; failure means BLOCKED.
        with self.repository.transaction() as connection:
            self.repository.fetch_context_revision(measurement.context_revision_id, connection)
            reference = self.repository.fetch_applicable_aps(measurement.context_revision_id, connection)
            if (reference.set_id, reference.version) != (measurement.aps_set_id, measurement.aps_version):
                raise GovernedReferenceError("Measurement APS reference is not applicable.")
            self.repository.resolve_member_authorization(reference, measurement.parameter_reference, connection)
            item = GovernedEvaluation(
                self.identifiers.new("evaluation"), measurement_id,
                measurement.parameter_reference, status, message, rule_origin,
                serialize_utc_instant(evaluated_at), serialize_utc_instant(self.clock()),
                ENGINE, ENGINE_VERSION,
                json.dumps(explanation_data, sort_keys=True) if explanation_data is not None else None,
            )
            self.repository.insert_evaluation(item, connection)
        return item
