ALTER TABLE governance_event ADD COLUMN authorization_basis_id TEXT;
ALTER TABLE governance_event ADD COLUMN decision_timestamp TEXT;
ALTER TABLE governance_event ADD COLUMN affected_record_type TEXT;
ALTER TABLE governance_event ADD COLUMN affected_record_id TEXT;
ALTER TABLE governance_event ADD COLUMN previous_effective_until TEXT;
ALTER TABLE governance_event ADD COLUMN new_effective_until TEXT;
ALTER TABLE governance_event ADD COLUMN successor_record_id TEXT;
CREATE TRIGGER context_temporal_no_overlap BEFORE INSERT ON point_context_revision
WHEN NEW.effective_from IS NOT NULL AND EXISTS (SELECT 1 FROM point_context_revision old WHERE old.point_id=NEW.point_id AND old.effective_from IS NOT NULL AND old.effective_from < COALESCE(NEW.effective_until,'9999-12-31T23:59:59.999999Z') AND NEW.effective_from < COALESCE(old.effective_until,'9999-12-31T23:59:59.999999Z'))
BEGIN SELECT RAISE(ABORT,'overlapping context interval'); END;
