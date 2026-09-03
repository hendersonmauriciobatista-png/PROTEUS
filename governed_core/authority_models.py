from dataclasses import dataclass

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
