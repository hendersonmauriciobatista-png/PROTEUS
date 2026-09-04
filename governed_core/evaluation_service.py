"""Append-only observational evaluation persistence for governed measurements."""
import json
import hashlib
from datetime import datetime, timezone

from .identifiers import IdentifierFactory
from .measurement_models import GovernedEvaluation
from .measurement_service import serialize_utc_instant
from .repository import GovernedReferenceError
from .rule_service import RuleResolutionService
from .authority_gate import AuthorityGate, AuthorityGateBlockedError

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
        measurement = None
        try:
            with self.repository.transaction() as connection:
                measurement = self.repository.fetch_measurement(measurement_id, connection)
                return self._evaluate_temporal_in_transaction(measurement, connection)
        except AuthorityGateBlockedError:
            raise
        except GovernedReferenceError as exc:
            code = getattr(exc, "reason_code", "INTERNAL_RESOLUTION_FAILURE")
            result = (
                AuthorityGate.blocked_result(measurement, code, "integrated_resolution")
                if measurement is not None
                else AuthorityGate.blocked_result_for_measurement_id(
                    measurement_id, code, "measurement_resolution"
                )
            )
            raise AuthorityGateBlockedError(result) from exc
        except Exception as exc:
            result = (
                AuthorityGate.blocked_result(measurement, "INTERNAL_RESOLUTION_FAILURE", "integrated_resolution")
                if measurement is not None
                else AuthorityGate.blocked_result_for_measurement_id(
                    measurement_id, "INTERNAL_RESOLUTION_FAILURE", "measurement_resolution"
                )
            )
            raise AuthorityGateBlockedError(result) from exc

    def _evaluate_temporal_in_transaction(self, measurement, connection):
        measured_at = datetime.fromisoformat(
            measurement.measured_at.replace("Z", "+00:00")
        )
        context = self.repository.fetch_temporal_context(
            measurement.point_id, measurement.measured_at, connection
        )
        reference = self.repository.fetch_temporal_aps(
            context.context_revision_id, measurement.measured_at, connection
        )
        if context.context_revision_id != measurement.context_revision_id or (
            reference.set_id, reference.version
        ) != (measurement.aps_set_id, measurement.aps_version):
            raise GovernedReferenceError("Temporal measurement provenance mismatch.")
        member_authorization = self.repository.resolve_member_authorization(
            reference, measurement.parameter_reference, connection
        )
        authority_result = AuthorityGate(self.repository).resolve(
            measurement, context, member_authorization, connection
        )
        if authority_result.status == "BLOCKED":
            raise AuthorityGateBlockedError(authority_result)
        resolution = RuleResolutionService(self.repository).resolve(
            context.context_revision_id,
            measurement.parameter_reference,
            measured_at,
            connection,
        )
        if resolution.state == "BLOCKED":
            raise AuthorityGateBlockedError(
                AuthorityGate.blocked_result(
                    measurement, resolution.reason, "rule_resolution"
                )
            )
        rule = resolution.rule
        if rule:
            if hashlib.sha256(rule.rule_payload.encode()).hexdigest() != rule.payload_hash:
                raise GovernedReferenceError("Rule payload hash mismatch.")
            payload = json.loads(rule.rule_payload)
            status, message = _evaluate_payload(payload, measurement.value)
            origin = rule.origin
            explanation = {
                "rule_id": rule.rule_id,
                "rule_version": rule.rule_version,
                "rule_payload_hash": rule.payload_hash,
                "authority_reference_ids": rule.authority_reference_ids,
                "evidence_reference_ids": rule.evidence_reference_ids,
            }
        else:
            status, message, origin, explanation = (
                "NAO_AVALIAVEL",
                "Nenhuma regra temporal aplicavel.",
                "NO_APPLICABLE_RULE",
                {"resolution": "ZERO_RULE"},
            )
        evaluation_id = self.identifiers.new("evaluation")
        item = GovernedEvaluation(
            evaluation_id,
            measurement.measurement_id,
            measurement.parameter_reference,
            status,
            message,
            origin,
            serialize_utc_instant(measured_at),
            serialize_utc_instant(self.clock()),
            ENGINE,
            ENGINE_VERSION,
            json.dumps(explanation, sort_keys=True),
        )
        self.repository.insert_evaluation(item, connection)
        for basis_id in authority_result.exact_member_authorization_basis:
            self.repository.insert_authority_snapshot_basis(
                (
                    evaluation_id,
                    basis_id,
                    reference.set_id,
                    reference.version,
                    measurement.parameter_reference,
                ),
                connection,
            )
        rule_outcome = (
            "ZERO_APPLICABLE_RULE" if rule is None else "ONE_APPLICABLE_RULE"
        )
        self.repository.insert_authority_snapshot(
            (
                evaluation_id,
                authority_result.authority_id,
                authority_result.authority_version,
                authority_result.authority_applicability_id,
                authority_result.authority_lifecycle_event_id,
                authority_result.authority_applicability_event_id,
                authority_result.verification_id,
                authority_result.status,
                authority_result.lifecycle_policy_result,
                rule_outcome,
                authority_result.authority_gate_policy_contract_version,
            ),
            connection,
        )
        return item

def _evaluate_payload(payload, value):
    op = payload["operator"]
    if op == "MIN_INCLUSIVE": ok = value >= float(payload["min"])
    elif op == "MAX_INCLUSIVE": ok = value <= float(payload["max"])
    elif op == "RANGE_INCLUSIVE": ok = float(payload["min"]) <= value <= float(payload["max"])
    else: ok = value == float(payload["value"])
    return ("NORMAL", "Valor dentro da regra temporal.") if ok else ("CRITICO", "Valor fora da regra temporal.")
