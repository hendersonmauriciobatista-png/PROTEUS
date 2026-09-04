"""Fail-safe Authority Gate for the integrated temporal evaluation path."""

from datetime import datetime

from .authority_models import AuthorityGateResult
from .authority_service import AuthorityService
from .repository import GovernedCoreError, GovernedReferenceError


AUTHORITY_GATE_POLICY_CONTRACT_VERSION = (
    "mcm-wq-authority-gate-technical-admission/v1"
)
LIFECYCLE_POLICY_RESULT = "TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION"
AUTHORITY_GATE_RESOLVER_VERSION = "1"


class AuthorityGateBlockedError(GovernedReferenceError):
    """Raised when the integrated path fails closed at the Authority Gate."""

    def __init__(self, result):
        super().__init__(result.reason_code or "AUTHORITY_GATE_BLOCKED")
        self.result = result
        self.reason_code = result.reason_code


class AuthorityGate:
    """Resolve exactly one historically admissible authority candidate."""

    def __init__(
        self,
        repository,
        *,
        authority_service=None,
        policy_contract_version=AUTHORITY_GATE_POLICY_CONTRACT_VERSION,
    ):
        self.repository = repository
        self.authority_service = authority_service or AuthorityService(repository)
        self.policy_contract_version = policy_contract_version

    @staticmethod
    def _provenance(
        measurement,
        candidates,
        *,
        stage,
        reason_code=None,
        selected=None,
        policy_id=AUTHORITY_GATE_POLICY_CONTRACT_VERSION,
    ):
        evidence = {
            "policy_id": policy_id,
            "resolver_version": AUTHORITY_GATE_RESOLVER_VERSION,
            "measured_at": measurement.measured_at,
            "measurement_id": measurement.measurement_id,
            "context_revision_id": measurement.context_revision_id,
            "parameter_reference": measurement.parameter_reference,
            "candidate_count": len(candidates),
            "candidate_ids": tuple(row[0] for row in candidates),
            "stage": stage,
        }
        if reason_code is not None:
            evidence["reason_code"] = reason_code
        if selected is not None:
            evidence["selected_applicability_id"] = selected[0]
            evidence["selected_authority_id"] = selected[1]
            evidence["selected_authority_version"] = selected[2]
        return evidence

    def _blocked(self, measurement, candidates, reason_code, stage):
        return AuthorityGateResult(
            status="BLOCKED",
            authority_gate_policy_contract_version=self.policy_contract_version,
            reason_code=reason_code,
            resolution_provenance=self._provenance(
                measurement,
                candidates,
                stage=stage,
                reason_code=reason_code,
                policy_id=self.policy_contract_version,
            ),
        )

    @classmethod
    def blocked_result(cls, measurement, reason_code, stage, candidates=()):
        return cls._blocked_static(measurement, candidates, reason_code, stage)

    @classmethod
    def blocked_result_for_measurement_id(cls, measurement_id, reason_code, stage):
        return AuthorityGateResult(
            status="BLOCKED",
            reason_code=reason_code,
            resolution_provenance={
                "policy_id": AUTHORITY_GATE_POLICY_CONTRACT_VERSION,
                "resolver_version": AUTHORITY_GATE_RESOLVER_VERSION,
                "measurement_id": measurement_id,
                "candidate_count": 0,
                "candidate_ids": (),
                "stage": stage,
                "reason_code": reason_code,
            },
        )

    @staticmethod
    def _blocked_static(measurement, candidates, reason_code, stage):
        return AuthorityGateResult(
            status="BLOCKED",
            reason_code=reason_code,
            resolution_provenance=AuthorityGate._provenance(
                measurement, candidates, stage=stage, reason_code=reason_code
            ),
        )

    def resolve(self, measurement, context, member_authorization, connection):
        try:
            return self._resolve(measurement, context, member_authorization, connection)
        except Exception:
            return self._blocked(
                measurement, (), "INTERNAL_RESOLUTION_FAILURE", "authority_gate"
            )

    def _resolve(self, measurement, context, member_authorization, connection):
        candidates = ()
        if self.policy_contract_version != AUTHORITY_GATE_POLICY_CONTRACT_VERSION:
            return self._blocked(
                measurement, candidates, "UNKNOWN_POLICY_VERSION", "policy_version"
            )

        try:
            candidates = self.repository.fetch_authority_applicability_candidates(
                measurement.context_revision_id,
                measurement.parameter_reference,
                measurement.measured_at,
                connection,
            )
        except GovernedCoreError:
            return self._blocked(
                measurement, candidates, "INTERNAL_RESOLUTION_FAILURE", "candidate_query"
            )

        if not candidates:
            return self._blocked(
                measurement, candidates, "NO_AUTHORITY_CANDIDATE", "candidate_discovery"
            )

        try:
            temporal = tuple(
                row for row in candidates
                if row[5] <= measurement.measured_at
                and (row[6] is None or measurement.measured_at < row[6])
            )
        except (TypeError, ValueError):
            return self._blocked(
                measurement, candidates, "APPLICABILITY_INVALID", "temporal_applicability"
            )

        if not temporal:
            return self._blocked(
                measurement, candidates, "APPLICABILITY_INVALID", "temporal_applicability"
            )

        authority_keys = {(row[1], row[2]) for row in temporal}
        if len(authority_keys) > 1:
            return self._blocked(
                measurement, temporal, "CONFLICTING_AUTHORITY", "candidate_cardinality"
            )
        if len(temporal) != 1:
            return self._blocked(
                measurement,
                temporal,
                "MULTIPLE_AUTHORITY_CANDIDATES",
                "candidate_cardinality",
            )

        candidate = temporal[0]
        applicability_event_ids = self.repository.fetch_authority_applicability_event_ids(
                candidate[0], measurement.measured_at, connection
            )
        if len(applicability_event_ids) == 0:
            return self._blocked(
                measurement, temporal, "INCOMPLETE_AUTHORITY_HISTORY", "applicability_history"
            )
        if len(applicability_event_ids) != 1:
            return self._blocked(
                measurement, temporal, "INCOMPLETE_AUTHORITY_HISTORY", "applicability_history"
            )
        applicability_event_id = applicability_event_ids[0]

        if len(self.repository.fetch_authority_scope(
            candidate[1],
            candidate[2],
            measurement.context_revision_id,
            measurement.parameter_reference,
            connection,
        )) != 1:
            return self._blocked(
                measurement, temporal, "AUTHORITY_SCOPE_MISMATCH", "authority_scope"
            )

        verification = self.repository.fetch_authority_artifact_verification(
            candidate[1], candidate[2], connection=connection
        )
        if verification is None:
            return self._blocked(
                measurement, temporal, "MISSING_VERIFICATION", "schema_a_verification"
            )
        if verification.verification_result != "VERIFIED":
            return self._blocked(
                measurement, temporal, "VERIFICATION_NOT_ACCEPTED", "schema_a_verification"
            )

        measured_at = datetime.fromisoformat(measurement.measured_at.replace("Z", "+00:00"))
        historical = self.authority_service.resolve_historical_authority(
            candidate[1],
            candidate[2],
            measured_at,
            measurement.context_revision_id,
            measurement.parameter_reference,
            connection=connection,
        )
        if historical.state == "TECHNICALLY_INELIGIBLE":
            return self._blocked(
                measurement, temporal, "LIFECYCLE_INELIGIBLE", "authority_boundary"
            )
        if historical.state != "RESOLVED" or historical.event is None:
            return self._blocked(measurement, temporal, "LIFECYCLE_UNDEFINED", "lifecycle_history")

        if historical.event.event_type in {"REVOKED", "SUPERSEDED"}:
            return self._blocked(
                measurement, temporal, "LIFECYCLE_INELIGIBLE", "lifecycle_policy"
            )
        if historical.event.event_type not in {"PUBLISHED", "ACTIVE"}:
            return self._blocked(
                measurement, temporal, "MALFORMED_AUTHORITY_STATE", "lifecycle_policy"
            )

        basis_ids = tuple(basis.basis_id for basis in member_authorization.bases)
        if not basis_ids:
            return self._blocked(
                measurement,
                temporal,
                "APS_MEMBER_AUTHORIZATION_UNRESOLVED",
                "member_authorization",
            )

        provenance = self._provenance(
            measurement,
            temporal,
            stage="resolved",
            selected=candidate,
        )
        provenance.update({
            "aps_set_id": member_authorization.aps_reference.set_id,
            "aps_version": member_authorization.aps_reference.version,
            "member_authorization_basis_ids": basis_ids,
            "authority_lifecycle_event_id": historical.event.event_id,
            "authority_applicability_event_id": applicability_event_id,
            "verification_id": verification.verification_id,
            "resolved_lifecycle_event_type": historical.event.event_type,
            "resolver": "AuthorityGate",
        })
        return AuthorityGateResult(
            status="RESOLVED",
            authority_id=candidate[1],
            authority_version=candidate[2],
            authority_applicability_id=candidate[0],
            authority_lifecycle_event_id=historical.event.event_id,
            authority_applicability_event_id=applicability_event_id,
            verification_id=verification.verification_id,
            authority_gate_policy_contract_version=self.policy_contract_version,
            lifecycle_policy_result=LIFECYCLE_POLICY_RESULT,
            resolution_provenance=provenance,
            exact_member_authorization_basis=basis_ids,
        )
