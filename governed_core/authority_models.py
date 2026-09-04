from dataclasses import dataclass
from typing import Literal

EFFECTIVE_TIME_SOURCES = {
    "CALLER_SUPPLIED_EXPLICIT_TIME",
    "SYSTEM_GENERATED_IMMEDIATE_TIME",
}

@dataclass(frozen=True)
class GovernedAuthority:
    authority_id: str
    authority_version: int
    origin_locator: str
    content_hash: str
    created_at: str
    context_revision_id: str
    parameter_reference: str
    effective_from: str
    effective_until: str | None
    status: str

@dataclass(frozen=True)
class GovernedApplicability:
    applicability_id: str
    authority_id: str
    authority_version: int
    context_revision_id: str
    parameter_reference: str
    effective_from: str
    created_at: str


@dataclass(frozen=True)
class AuthorityEvent:
    event_id: str
    authority_id: str
    authority_version: int
    event_type: str
    actor_reference: str
    reason: str
    successor_authority_id: str | None
    successor_authority_version: int | None
    registered_at: str
    effective_at: str | None
    effective_at_source: str | None
    effective_at_provenance: str | None


@dataclass(frozen=True)
class HistoricalAuthorityResolution:
    state: str
    reason: str = ""
    event: AuthorityEvent | None = None


@dataclass(frozen=True)
class AuthorityGateResult:
    """Typed, fail-safe result of the future integrated Authority Gate."""

    status: Literal["RESOLVED", "BLOCKED"]
    authority_id: str | None = None
    authority_version: int | None = None
    authority_applicability_id: str | None = None
    authority_lifecycle_event_id: str | None = None
    authority_applicability_event_id: str | None = None
    verification_id: str | None = None
    authority_gate_policy_contract_version: str = (
        "mcm-wq-authority-gate-technical-admission/v1"
    )
    lifecycle_policy_result: str | None = None
    resolution_provenance: dict | None = None
    exact_member_authorization_basis: tuple[str, ...] = ()
    reason_code: str | None = None

    def __post_init__(self):
        if self.status not in {"RESOLVED", "BLOCKED"}:
            raise ValueError("Authority Gate status must be RESOLVED or BLOCKED")
        if self.status == "BLOCKED":
            if not self.reason_code or any(
                value is not None
                for value in (
                    self.authority_id,
                    self.authority_version,
                    self.authority_applicability_id,
                    self.authority_lifecycle_event_id,
                    self.authority_applicability_event_id,
                    self.verification_id,
                    self.lifecycle_policy_result,
                )
            ):
                raise ValueError("BLOCKED result contains resolved payload")
        elif self.reason_code is not None:
            raise ValueError("RESOLVED result contains a blocked reason")

@dataclass(frozen=True)
class GovernedAuthorityArtifact:
    artifact_id: str
    artifact_version: int
    artifact_locator_reference: str
    artifact_bytes: bytes
    artifact_digest: str
    digest_algorithm: str
    registered_at: str

@dataclass(frozen=True)
class AuthorityArtifactBinding:
    authority_id: str
    authority_version: int
    artifact_id: str
    artifact_version: int

@dataclass(frozen=True)
class AuthorityArtifactVerification:
    verification_id: str
    authority_id: str
    authority_version: int
    artifact_id: str
    artifact_version: int
    algorithm_id: str
    verification_contract_version: str
    expected_digest: str
    computed_digest: str
    verification_result: str
    verified_at: str
    verification_provenance: str
