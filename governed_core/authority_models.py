from dataclasses import dataclass

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
