import hashlib, json, math
from datetime import datetime, timezone
from .rule_models import GovernedRule, RuleResolution
from .repository import GovernedReferenceError
from .identifiers import IdentifierFactory

OPS = {"MIN_INCLUSIVE", "MAX_INCLUSIVE", "RANGE_INCLUSIVE", "EQUALS"}

def canonical_payload(payload, unit):
    if not isinstance(payload, dict) or set(payload) - {"operator", "min", "max", "value", "unit"}:
        raise ValueError("Invalid rule payload keys")
    if "unit" in payload and payload["unit"] != unit:
        raise ValueError("Rule unit mismatch")
    op = payload.get("operator")
    fields = {"MIN_INCLUSIVE":{"min"}, "MAX_INCLUSIVE":{"max"}, "RANGE_INCLUSIVE":{"min","max"}, "EQUALS":{"value"}}.get(op)
    if fields is None or set(payload) - {"operator", "unit", *fields} or not unit:
        raise ValueError("Invalid rule payload")
    values = {key: str(payload[key]) for key in fields}
    try:
        nums = {key: float(value) for key, value in values.items()}
    except (TypeError, ValueError): raise ValueError("Rule operands must be numeric")
    if any(not math.isfinite(v) for v in nums.values()) or (op == "RANGE_INCLUSIVE" and nums["min"] > nums["max"]):
        raise ValueError("Invalid finite rule operands")
    return json.dumps({"operator": op, **values, "unit": unit}, sort_keys=True, separators=(",", ":"))

class RuleResolutionService:
    def __init__(self, repository): self.repository = repository
    def resolve(self, context_revision_id, parameter_reference, measured_at):
        instant = _instant(measured_at)
        rows = self.repository.fetch_rules(context_revision_id, parameter_reference, instant)
        if len(rows) == 0: return RuleResolution("NAO_AVALIAVEL", reason="NO_APPLICABLE_RULE")
        if len(rows) != 1: return RuleResolution("BLOCKED", reason="AMBIGUOUS_RULE_RESOLUTION")
        rule = rows[0]
        if not rule.authority_reference_ids or not rule.evidence_reference_ids:
            return RuleResolution("BLOCKED", reason="BROKEN_AUTHORITY_EVIDENCE_CHAIN")
        for reference_id in rule.authority_reference_ids:
            with self.repository._optional_connection(None) as connection:
                exists = connection.execute("SELECT 1 FROM authority_reference WHERE authority_reference_id = ?", (reference_id,)).fetchone()
            if exists is None:
                return RuleResolution("BLOCKED", reason="MISSING_AUTHORITY_REFERENCE")
        for reference_id in rule.evidence_reference_ids:
            with self.repository._optional_connection(None) as connection:
                exists = connection.execute("SELECT 1 FROM evidence_reference WHERE evidence_reference_id = ?", (reference_id,)).fetchone()
            if exists is None:
                return RuleResolution("BLOCKED", reason="MISSING_EVIDENCE_REFERENCE")
        return RuleResolution("RESOLVED", rule)

class RuleService:
    def __init__(self, repository, identifiers=None):
        self.repository, self.identifiers = repository, identifiers or IdentifierFactory()

    def create_version(self, context_revision_id, parameter_reference, effective_from,
                       origin, payload, unit, authority_reference_ids, evidence_reference_ids,
                       rule_id=None, rule_version=1, effective_until=None):
        if not parameter_reference or not origin or not authority_reference_ids or not evidence_reference_ids:
            raise ValueError("Rule identity, origin, authority and evidence are required")
        canonical = canonical_payload(payload, unit)
        start = _instant(effective_from); end = _instant(effective_until) if effective_until else None
        if end and end <= start: raise ValueError("Invalid rule interval")
        authorities = tuple(sorted(set(authority_reference_ids))); evidence = tuple(sorted(set(evidence_reference_ids)))
        with self.repository.transaction() as connection:
            self.repository.fetch_context_revision(context_revision_id, connection)
            for ref in authorities:
                if not connection.execute("SELECT 1 FROM authority_reference WHERE authority_reference_id = ?", (ref,)).fetchone():
                    raise GovernedReferenceError("Unknown authority reference")
            for ref in evidence:
                if not connection.execute("SELECT 1 FROM evidence_reference WHERE evidence_reference_id = ?", (ref,)).fetchone():
                    raise GovernedReferenceError("Unknown evidence reference")
            rule = GovernedRule(rule_id or self.identifiers.new("rule"), rule_version, parameter_reference,
                context_revision_id, start, end, origin, canonical, hashlib.sha256(canonical.encode()).hexdigest(), authorities, evidence)
            self.repository.insert_rule(rule, connection)
        return rule

def _instant(value):
    if not isinstance(value, datetime) or value.tzinfo is None: raise ValueError("Timezone-aware measured_at required")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00", "Z") if isinstance(value, datetime) else value
