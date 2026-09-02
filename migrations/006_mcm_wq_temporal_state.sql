ALTER TABLE point_context_revision ADD COLUMN effective_from TEXT;
ALTER TABLE point_context_revision ADD COLUMN effective_until TEXT;
CREATE TABLE aps_temporal_applicability (
    aps_applicability_id TEXT PRIMARY KEY,
    context_revision_id TEXT NOT NULL,
    aps_set_id TEXT NOT NULL,
    aps_version INTEGER NOT NULL,
    effective_from TEXT NOT NULL,
    effective_until TEXT,
    FOREIGN KEY (context_revision_id) REFERENCES point_context_revision(context_revision_id) ON DELETE RESTRICT,
    FOREIGN KEY (aps_set_id, aps_version, context_revision_id) REFERENCES aps_version(set_id, version, context_revision_id) ON DELETE RESTRICT,
    CHECK (effective_until IS NULL OR effective_until > effective_from)
);
CREATE INDEX aps_temporal_lookup ON aps_temporal_applicability(context_revision_id, effective_from, effective_until);
CREATE TRIGGER aps_temporal_no_overlap BEFORE INSERT ON aps_temporal_applicability
WHEN EXISTS (SELECT 1 FROM aps_temporal_applicability old
 WHERE old.context_revision_id = NEW.context_revision_id
 AND old.effective_from < COALESCE(NEW.effective_until, '9999-12-31T23:59:59.999999Z')
 AND NEW.effective_from < COALESCE(old.effective_until, '9999-12-31T23:59:59.999999Z'))
BEGIN SELECT RAISE(ABORT, 'overlapping APS applicability'); END;
