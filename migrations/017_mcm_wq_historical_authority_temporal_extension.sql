-- MCM-WQ historical authority temporal extension.
-- Existing authority_event rows are legacy: their effective time is unknown
-- and must remain unresolved rather than being inferred from registration.

DROP TRIGGER authority_event_append_only;
DROP TRIGGER authority_event_no_delete;

CREATE TABLE authority_event_new (
    event_id TEXT PRIMARY KEY,
    authority_id TEXT NOT NULL,
    authority_version INTEGER NOT NULL,
    event_type TEXT NOT NULL CHECK(event_type IN('PUBLISHED','ACTIVE','REVOKED','SUPERSEDED')),
    actor_reference TEXT NOT NULL,
    reason TEXT NOT NULL,
    successor_authority_id TEXT,
    successor_authority_version INTEGER,
    registered_at TEXT NOT NULL,
    effective_at TEXT,
    effective_at_source TEXT,
    effective_at_provenance TEXT,
    FOREIGN KEY(authority_id,authority_version)
        REFERENCES governed_authority(authority_id,authority_version),
    FOREIGN KEY(successor_authority_id,successor_authority_version)
        REFERENCES governed_authority(authority_id,authority_version)
        DEFERRABLE INITIALLY DEFERRED,
    CHECK (
        (effective_at IS NULL AND effective_at_source IS NULL AND effective_at_provenance IS NULL)
        OR (
            effective_at IS NOT NULL
            AND effective_at_source IN ('CALLER_SUPPLIED_EXPLICIT_TIME','SYSTEM_GENERATED_IMMEDIATE_TIME')
            AND effective_at_provenance IS NOT NULL
            AND length(trim(effective_at_provenance)) > 0
        )
    )
);

INSERT INTO authority_event_new (
    event_id, authority_id, authority_version, event_type, actor_reference,
    reason, successor_authority_id, successor_authority_version, registered_at,
    effective_at, effective_at_source, effective_at_provenance
)
SELECT event_id, authority_id, authority_version, event_type, actor_reference,
       reason, successor_authority_id, successor_authority_version, registered_at,
       NULL, NULL, NULL
FROM authority_event;

DROP TABLE authority_event;
ALTER TABLE authority_event_new RENAME TO authority_event;

CREATE INDEX authority_event_lookup
    ON authority_event(authority_id,authority_version,effective_at);
CREATE UNIQUE INDEX authority_event_effective_order
    ON authority_event(authority_id,authority_version,effective_at)
    WHERE effective_at IS NOT NULL;

CREATE TRIGGER authority_event_append_only
BEFORE UPDATE ON authority_event
BEGIN SELECT RAISE(ABORT,'append only'); END;

CREATE TRIGGER authority_event_no_delete
BEFORE DELETE ON authority_event
BEGIN SELECT RAISE(ABORT,'no delete'); END;

CREATE TRIGGER authority_event_new_temporal_contract
BEFORE INSERT ON authority_event
WHEN NEW.effective_at IS NULL
  OR NEW.effective_at_source NOT IN ('CALLER_SUPPLIED_EXPLICIT_TIME','SYSTEM_GENERATED_IMMEDIATE_TIME')
  OR NEW.effective_at_provenance IS NULL
  OR length(trim(NEW.effective_at_provenance)) = 0
  OR NEW.effective_at = NEW.registered_at
BEGIN
    SELECT RAISE(ROLLBACK,'authority event effective-time contract failed');
END;

CREATE TRIGGER authority_event_effective_at_canonical
BEFORE INSERT ON authority_event
WHEN NOT (
    typeof(NEW.effective_at) = 'text'
    AND length(NEW.effective_at) = 27
    AND length(CAST(NEW.effective_at AS BLOB)) = 27
    AND hex(CAST(NEW.effective_at AS BLOB)) GLOB '3[0-9]3[0-9]3[0-9]3[0-9]2D3[0-9]3[0-9]2D3[0-9]3[0-9]543[0-9]3[0-9]3A3[0-9]3[0-9]3A3[0-9]3[0-9]2E3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]5A'
    AND CAST(substr(NEW.effective_at,1,4) AS INTEGER) BETWEEN 1 AND 9999
    AND CAST(substr(NEW.effective_at,6,2) AS INTEGER) BETWEEN 1 AND 12
    AND CAST(substr(NEW.effective_at,9,2) AS INTEGER) BETWEEN 1 AND
        CASE CAST(substr(NEW.effective_at,6,2) AS INTEGER)
            WHEN 2 THEN CASE
                WHEN CAST(substr(NEW.effective_at,1,4) AS INTEGER) % 400 = 0
                  OR (CAST(substr(NEW.effective_at,1,4) AS INTEGER) % 4 = 0
                      AND CAST(substr(NEW.effective_at,1,4) AS INTEGER) % 100 <> 0)
                THEN 29 ELSE 28 END
            WHEN 4 THEN 30 WHEN 6 THEN 30 WHEN 9 THEN 30 WHEN 11 THEN 30
            ELSE 31
        END
    AND CAST(substr(NEW.effective_at,12,2) AS INTEGER) BETWEEN 0 AND 23
    AND CAST(substr(NEW.effective_at,15,2) AS INTEGER) BETWEEN 0 AND 59
    AND CAST(substr(NEW.effective_at,18,2) AS INTEGER) BETWEEN 0 AND 59
    AND CAST(substr(NEW.effective_at,21,6) AS INTEGER) BETWEEN 0 AND 999999
)
BEGIN
    SELECT RAISE(ROLLBACK,'authority event effective_at is not canonical');
END;

CREATE TRIGGER authority_event_legacy_history_block
BEFORE INSERT ON authority_event
WHEN EXISTS (
    SELECT 1 FROM authority_event
    WHERE authority_id = NEW.authority_id
      AND authority_version = NEW.authority_version
      AND effective_at IS NULL
)
BEGIN
    SELECT RAISE(ROLLBACK,'legacy authority history is unresolved');
END;

CREATE TRIGGER authority_event_first_is_published
BEFORE INSERT ON authority_event
WHEN NOT EXISTS (
    SELECT 1 FROM authority_event
    WHERE authority_id = NEW.authority_id
      AND authority_version = NEW.authority_version
)
AND NEW.event_type <> 'PUBLISHED'
BEGIN SELECT RAISE(ROLLBACK,'first authority event must be PUBLISHED'); END;

CREATE TRIGGER authority_event_published_is_first
BEFORE INSERT ON authority_event
WHEN NEW.event_type = 'PUBLISHED'
 AND EXISTS (
    SELECT 1 FROM authority_event
    WHERE authority_id = NEW.authority_id
      AND authority_version = NEW.authority_version
 )
BEGIN SELECT RAISE(ROLLBACK,'PUBLISHED authority event must be first'); END;

CREATE TRIGGER authority_event_active_requires_published
BEFORE INSERT ON authority_event
WHEN NEW.event_type = 'ACTIVE'
 AND (
    NOT EXISTS (
        SELECT 1 FROM authority_event
        WHERE authority_id = NEW.authority_id
          AND authority_version = NEW.authority_version
          AND event_type = 'PUBLISHED'
          AND effective_at < NEW.effective_at
    )
    OR EXISTS (
        SELECT 1 FROM authority_event
        WHERE authority_id = NEW.authority_id
          AND authority_version = NEW.authority_version
          AND event_type = 'ACTIVE'
    )
    OR EXISTS (
        SELECT 1 FROM authority_event
        WHERE authority_id = NEW.authority_id
          AND authority_version = NEW.authority_version
          AND event_type IN ('REVOKED','SUPERSEDED')
          AND effective_at < NEW.effective_at
    )
 )
BEGIN SELECT RAISE(ROLLBACK,'ACTIVE authority event sequence invalid'); END;

CREATE TRIGGER authority_event_terminal_requires_active
BEFORE INSERT ON authority_event
WHEN NEW.event_type IN ('REVOKED','SUPERSEDED')
 AND (
    NOT EXISTS (
        SELECT 1 FROM authority_event
        WHERE authority_id = NEW.authority_id
          AND authority_version = NEW.authority_version
          AND event_type = 'ACTIVE'
          AND effective_at < NEW.effective_at
    )
    OR EXISTS (
        SELECT 1 FROM authority_event
        WHERE authority_id = NEW.authority_id
          AND authority_version = NEW.authority_version
          AND event_type IN ('REVOKED','SUPERSEDED')
    )
    OR EXISTS (
        SELECT 1 FROM authority_event
        WHERE authority_id = NEW.authority_id
          AND authority_version = NEW.authority_version
          AND effective_at > NEW.effective_at
    )
 )
BEGIN SELECT RAISE(ROLLBACK,'terminal authority event sequence invalid'); END;

CREATE TRIGGER authority_event_no_after_terminal
BEFORE INSERT ON authority_event
WHEN EXISTS (
    SELECT 1 FROM authority_event
    WHERE authority_id = NEW.authority_id
      AND authority_version = NEW.authority_version
      AND event_type IN ('REVOKED','SUPERSEDED')
      AND effective_at < NEW.effective_at
)
BEGIN SELECT RAISE(ROLLBACK,'authority event after terminal state'); END;

CREATE TRIGGER authority_event_successor_contract
BEFORE INSERT ON authority_event
WHEN (NEW.event_type = 'SUPERSEDED'
      AND (NEW.successor_authority_id IS NULL OR NEW.successor_authority_version IS NULL
           OR (NEW.successor_authority_id = NEW.authority_id
               AND NEW.successor_authority_version = NEW.authority_version)))
   OR (NEW.event_type <> 'SUPERSEDED'
       AND (NEW.successor_authority_id IS NOT NULL OR NEW.successor_authority_version IS NOT NULL))
BEGIN SELECT RAISE(ROLLBACK,'authority successor linkage invalid'); END;

CREATE TRIGGER authority_event_projection_published
AFTER INSERT ON authority_event
WHEN NEW.event_type = 'PUBLISHED'
BEGIN
    UPDATE authority_state
       SET last_event_id = NEW.event_id
     WHERE authority_id = NEW.authority_id
       AND authority_version = NEW.authority_version;
END;

CREATE TRIGGER authority_event_projection_transition
AFTER INSERT ON authority_event
WHEN NEW.event_type IN ('ACTIVE','REVOKED','SUPERSEDED')
BEGIN
    UPDATE authority_state
       SET status = NEW.event_type,
           state_changed_at = NEW.registered_at,
           last_event_id = NEW.event_id
     WHERE authority_id = NEW.authority_id
       AND authority_version = NEW.authority_version;
END;
