"""Append-only observational evaluation persistence for governed measurements."""
import json
import hashlib
from datetime import datetime, timezone

from .identifiers import IdentifierFactory
from .measurement_models import GovernedEvaluation
from .measurement_service import serialize_utc_instant
from .repository import GovernedReferenceError
from .rule_service import RuleResolutionService

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

    def evaluate_temporal(self, measurement_id):
        measurement = self.repository.fetch_measurement(measurement_id)
        with self.repository.transaction() as connection:
            context, reference = self.repository.fetch_temporal_context(measurement.point_id, measurement.measured_at, connection), None
            reference = self.repository.fetch_temporal_aps(context.context_revision_id, measurement.measured_at, connection)
            if context.context_revision_id != measurement.context_revision_id or (reference.set_id, reference.version) != (measurement.aps_set_id, measurement.aps_version):
                raise GovernedReferenceError("Temporal measurement provenance mismatch.")
            self.repository.resolve_member_authorization(reference, measurement.parameter_reference, connection)
            measured_at = datetime.fromisoformat(measurement.measured_at.replace("Z", "+00:00"))
            resolution = RuleResolutionService(self.repository).resolve(context.context_revision_id, measurement.parameter_reference, measured_at)
            if resolution.state == "BLOCKED":
                raise GovernedReferenceError(resolution.reason)
            rule = resolution.rule
            if rule:
                if hashlib.sha256(rule.rule_payload.encode()).hexdigest() != rule.payload_hash:
                    raise GovernedReferenceError("Rule payload hash mismatch.")
                payload = json.loads(rule.rule_payload)
                status, message = _evaluate_payload(payload, measurement.value)
                origin = rule.origin
                explanation = {"rule_id": rule.rule_id, "rule_version": rule.rule_version, "rule_payload_hash": rule.payload_hash, "authority_reference_ids": rule.authority_reference_ids, "evidence_reference_ids": rule.evidence_reference_ids}
            else:
                status, message, origin, explanation = "NAO_AVALIAVEL", "Nenhuma regra temporal aplicavel.", "NO_APPLICABLE_RULE", {"resolution": "ZERO_RULE"}
            item = GovernedEvaluation(self.identifiers.new("evaluation"), measurement_id, measurement.parameter_reference, status, message, origin, serialize_utc_instant(datetime.fromisoformat(measurement.measured_at.replace("Z", "+00:00"))), serialize_utc_instant(self.clock()), ENGINE, ENGINE_VERSION, json.dumps(explanation, sort_keys=True))
            self.repository.insert_evaluation(item, connection)
        return item

def _evaluate_payload(payload, value):
    op = payload["operator"]
    if op == "MIN_INCLUSIVE": ok = value >= float(payload["min"])
    elif op == "MAX_INCLUSIVE": ok = value <= float(payload["max"])
    elif op == "RANGE_INCLUSIVE": ok = float(payload["min"]) <= value <= float(payload["max"])
    else: ok = value == float(payload["value"])
    return ("NORMAL", "Valor dentro da regra temporal.") if ok else ("CRITICO", "Valor fora da regra temporal.")
