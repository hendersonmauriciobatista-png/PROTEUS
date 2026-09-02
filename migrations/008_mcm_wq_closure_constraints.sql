ALTER TABLE governance_event_resolution RENAME TO governance_event_resolution_old;
ALTER TABLE governance_event RENAME TO governance_event_old;
CREATE TABLE governance_event (
 event_id TEXT PRIMARY KEY, action TEXT NOT NULL CHECK (action IN ('CURRENT_CONTEXT_REFERENCE_CHANGED','APPLICABILITY_ASSIGNED','APPLICABILITY_CHANGED','APPLICABILITY_REMOVED','APS_VERSION_DISQUALIFIED','APS_VERSION_REQUALIFIED','CLOSE_TEMPORAL_INTERVAL','CLOSE_AND_APPEND_SUCCESSOR')),
 actor_reference TEXT NOT NULL, registered_at TEXT NOT NULL, context_revision_id TEXT, previous_context_revision_id TEXT, new_context_revision_id TEXT, previous_set_id TEXT, previous_version INTEGER, new_set_id TEXT, new_version INTEGER, target_set_id TEXT, target_version INTEGER, authorization_basis_id TEXT, decision_timestamp TEXT, affected_record_type TEXT, affected_record_id TEXT, previous_effective_until TEXT, new_effective_until TEXT, successor_record_id TEXT,
 CHECK (affected_record_type IS NULL OR affected_record_type IN ('POINT_CONTEXT_REVISION','APS_TEMPORAL_APPLICABILITY'))
);
INSERT INTO governance_event SELECT event_id,action,actor_reference,registered_at,context_revision_id,previous_context_revision_id,new_context_revision_id,previous_set_id,previous_version,new_set_id,new_version,target_set_id,target_version,authorization_basis_id,decision_timestamp,affected_record_type,affected_record_id,previous_effective_until,new_effective_until,successor_record_id FROM governance_event_old;
DROP TABLE governance_event_old;
CREATE TABLE governance_event_resolution (requalification_event_id TEXT NOT NULL, disqualification_event_id TEXT NOT NULL, PRIMARY KEY (requalification_event_id, disqualification_event_id), FOREIGN KEY (requalification_event_id) REFERENCES governance_event(event_id), FOREIGN KEY (disqualification_event_id) REFERENCES governance_event(event_id));
INSERT INTO governance_event_resolution SELECT * FROM governance_event_resolution_old;
DROP TABLE governance_event_resolution_old;
CREATE TRIGGER governance_event_immutable_update BEFORE UPDATE ON governance_event BEGIN SELECT RAISE(ABORT,'governance_event is immutable'); END;
CREATE TRIGGER governance_event_immutable_delete BEFORE DELETE ON governance_event BEGIN SELECT RAISE(ABORT,'governance_event deletion is not authorized'); END;
CREATE TRIGGER context_temporal_no_overlap_update BEFORE UPDATE OF effective_from,effective_until,point_id ON point_context_revision
WHEN NEW.effective_from IS NOT NULL AND EXISTS (SELECT 1 FROM point_context_revision old WHERE old.rowid<>OLD.rowid AND old.point_id=NEW.point_id AND old.effective_from IS NOT NULL AND old.effective_from < COALESCE(NEW.effective_until,'9999-12-31T23:59:59.999999Z') AND NEW.effective_from < COALESCE(old.effective_until,'9999-12-31T23:59:59.999999Z')) BEGIN SELECT RAISE(ABORT,'overlapping context interval'); END;
