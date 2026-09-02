DROP VIEW authority_applicability_temporal;
DROP TRIGGER authority_app_event_no_update;
DROP TRIGGER authority_app_event_no_delete;
DROP TRIGGER authority_app_terminal_once;
DROP TRIGGER authority_app_no_reopen;
DROP TRIGGER authority_app_state_sync;
DROP INDEX authority_applicability_event_lookup;

CREATE TABLE authority_applicability_event_new (
    event_id TEXT PRIMARY KEY,
    applicability_id TEXT NOT NULL,
    event_type TEXT NOT NULL CHECK (event_type IN ('PUBLISHED', 'REVOKED', 'SUPERSEDED')),
    effective_at TEXT NOT NULL,
    registered_at TEXT NOT NULL,
    actor_reference TEXT NOT NULL,
    reason TEXT NOT NULL,
    successor_applicability_id TEXT,
    FOREIGN KEY (applicability_id) REFERENCES authority_applicability(applicability_id),
    FOREIGN KEY (successor_applicability_id)
        REFERENCES authority_applicability(applicability_id)
        DEFERRABLE INITIALLY DEFERRED,
    CHECK (effective_at <> registered_at OR event_type = 'PUBLISHED')
);

INSERT INTO authority_applicability_event_new
SELECT event_id, applicability_id, event_type, effective_at, registered_at,
       actor_reference, reason, successor_applicability_id
FROM authority_applicability_event;

DROP TABLE authority_applicability_event;
ALTER TABLE authority_applicability_event_new RENAME TO authority_applicability_event;

CREATE INDEX authority_applicability_event_lookup
    ON authority_applicability_event(applicability_id, effective_at);
CREATE TRIGGER authority_app_event_no_update BEFORE UPDATE ON authority_applicability_event
BEGIN SELECT RAISE(ABORT, 'applicability events are append-only'); END;
CREATE TRIGGER authority_app_event_no_delete BEFORE DELETE ON authority_applicability_event
BEGIN SELECT RAISE(ABORT, 'applicability events are append-only'); END;
CREATE TRIGGER authority_app_terminal_once BEFORE INSERT ON authority_applicability_event
WHEN NEW.event_type IN ('REVOKED','SUPERSEDED') AND EXISTS (SELECT 1 FROM authority_applicability_event WHERE applicability_id=NEW.applicability_id AND event_type IN ('REVOKED','SUPERSEDED'))
BEGIN SELECT RAISE(ABORT, 'terminal event already exists'); END;
CREATE TRIGGER authority_app_no_reopen BEFORE INSERT ON authority_applicability_event
WHEN NEW.event_type='PUBLISHED' AND EXISTS (SELECT 1 FROM authority_applicability_event WHERE applicability_id=NEW.applicability_id AND event_type IN ('REVOKED','SUPERSEDED'))
BEGIN SELECT RAISE(ABORT, 'reopen is not permitted'); END;
CREATE TRIGGER authority_app_state_sync AFTER INSERT ON authority_applicability_event
BEGIN INSERT INTO authority_applicability_state(applicability_id,state,terminal_effective_at,updated_at) VALUES(NEW.applicability_id,CASE WHEN NEW.event_type='PUBLISHED' THEN 'ACTIVE' ELSE NEW.event_type END,CASE WHEN NEW.event_type IN ('REVOKED','SUPERSEDED') THEN NEW.effective_at END,NEW.registered_at) ON CONFLICT(applicability_id) DO UPDATE SET state=CASE WHEN NEW.event_type='REVOKED' THEN 'REVOKED' ELSE 'SUPERSEDED' END,terminal_effective_at=NEW.effective_at,updated_at=NEW.registered_at; END;

CREATE VIEW authority_applicability_temporal AS
SELECT a.applicability_id, a.authority_id, a.authority_version,
       a.context_revision_id, a.parameter_reference, a.effective_from,
       MIN(e.effective_at) AS terminal_effective_at
FROM authority_applicability AS a
LEFT JOIN authority_applicability_event AS e
  ON e.applicability_id = a.applicability_id
 AND e.event_type IN ('REVOKED', 'SUPERSEDED')
GROUP BY a.applicability_id, a.authority_id, a.authority_version,
         a.context_revision_id, a.parameter_reference, a.effective_from;
