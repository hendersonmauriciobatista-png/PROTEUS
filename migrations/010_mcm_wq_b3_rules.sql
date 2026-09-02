CREATE TABLE governed_rule (
    rule_id TEXT NOT NULL,
    rule_version INTEGER NOT NULL CHECK (rule_version >= 1),
    parameter_reference TEXT NOT NULL,
    context_revision_id TEXT NOT NULL,
    effective_from TEXT NOT NULL,
    effective_until TEXT,
    origin TEXT NOT NULL CHECK (length(trim(origin)) > 0),
    rule_payload TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    authority_reference_ids TEXT NOT NULL,
    evidence_reference_ids TEXT NOT NULL,
    PRIMARY KEY (rule_id, rule_version),
    FOREIGN KEY (context_revision_id) REFERENCES point_context_revision(context_revision_id),
    CHECK (effective_until IS NULL OR effective_until > effective_from)
);
CREATE INDEX governed_rule_temporal_lookup ON governed_rule(context_revision_id, parameter_reference, effective_from, effective_until);
CREATE TRIGGER governed_rule_no_overlap BEFORE INSERT ON governed_rule
WHEN EXISTS (SELECT 1 FROM governed_rule old WHERE old.context_revision_id = NEW.context_revision_id AND old.parameter_reference = NEW.parameter_reference AND old.effective_from < COALESCE(NEW.effective_until, '9999-12-31T23:59:59.999999Z') AND NEW.effective_from < COALESCE(old.effective_until, '9999-12-31T23:59:59.999999Z'))
BEGIN SELECT RAISE(ABORT, 'overlapping governed rules'); END;
CREATE TRIGGER governed_rule_immutable_update BEFORE UPDATE ON governed_rule BEGIN SELECT RAISE(ABORT, 'governed_rule is immutable'); END;
CREATE TRIGGER governed_rule_immutable_delete BEFORE DELETE ON governed_rule BEGIN SELECT RAISE(ABORT, 'governed_rule deletion is not authorized'); END;
