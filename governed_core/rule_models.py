from dataclasses import dataclass

@dataclass(frozen=True)
class GovernedRule:
    rule_id: str
    rule_version: int
    parameter_reference: str
    context_revision_id: str
    effective_from: str
    effective_until: str | None
    origin: str
    rule_payload: str
    payload_hash: str
    authority_reference_ids: tuple[str, ...]
    evidence_reference_ids: tuple[str, ...]

@dataclass(frozen=True)
class RuleResolution:
    state: str
    rule: GovernedRule | None = None
    reason: str = ""
