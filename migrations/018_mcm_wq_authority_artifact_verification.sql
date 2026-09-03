-- MCM-WQ Schema A: immutable authority artifact custody and verification.
-- Existing authorities remain unchanged; new canonical publication requires proof.

CREATE TABLE authority_artifact (
    artifact_id TEXT NOT NULL,
    artifact_version INTEGER NOT NULL CHECK(artifact_version > 0),
    artifact_locator_reference TEXT NOT NULL CHECK(length(trim(artifact_locator_reference)) > 0),
    artifact_bytes BLOB NOT NULL CHECK(typeof(artifact_bytes) = 'blob'),
    artifact_digest TEXT NOT NULL CHECK(
        typeof(artifact_digest) = 'text'
        AND length(artifact_digest) = 64
        AND artifact_digest NOT GLOB '*[^0-9a-f]*'
    ),
    digest_algorithm TEXT NOT NULL CHECK(digest_algorithm = 'sha-256/v1'),
    registered_at TEXT NOT NULL,
    PRIMARY KEY (artifact_id, artifact_version)
);

CREATE TABLE authority_artifact_binding (
    authority_id TEXT NOT NULL,
    authority_version INTEGER NOT NULL,
    artifact_id TEXT NOT NULL,
    artifact_version INTEGER NOT NULL,
    PRIMARY KEY (authority_id, authority_version),
    UNIQUE (authority_id, authority_version, artifact_id, artifact_version),
    FOREIGN KEY (authority_id, authority_version)
        REFERENCES governed_authority(authority_id, authority_version),
    FOREIGN KEY (artifact_id, artifact_version)
        REFERENCES authority_artifact(artifact_id, artifact_version)
);

CREATE TABLE authority_artifact_verification (
    verification_id TEXT PRIMARY KEY,
    authority_id TEXT NOT NULL,
    authority_version INTEGER NOT NULL,
    artifact_id TEXT NOT NULL,
    artifact_version INTEGER NOT NULL,
    algorithm_id TEXT NOT NULL CHECK(algorithm_id = 'sha-256/v1'),
    verification_contract_version TEXT NOT NULL CHECK(length(trim(verification_contract_version)) > 0),
    expected_digest TEXT NOT NULL CHECK(
        typeof(expected_digest) = 'text'
        AND length(expected_digest) = 64
        AND expected_digest NOT GLOB '*[^0-9a-f]*'
    ),
    computed_digest TEXT NOT NULL CHECK(
        typeof(computed_digest) = 'text'
        AND length(computed_digest) = 64
        AND computed_digest NOT GLOB '*[^0-9a-f]*'
    ),
    verification_result TEXT NOT NULL CHECK(verification_result = 'VERIFIED'),
    verified_at TEXT NOT NULL,
    verification_provenance TEXT NOT NULL CHECK(length(trim(verification_provenance)) > 0),
    UNIQUE (authority_id, authority_version, verification_contract_version),
    FOREIGN KEY (authority_id, authority_version, artifact_id, artifact_version)
        REFERENCES authority_artifact_binding(
            authority_id, authority_version, artifact_id, artifact_version
        )
);

CREATE TRIGGER authority_artifact_immutable_update
BEFORE UPDATE ON authority_artifact
BEGIN SELECT RAISE(ABORT, 'authority artifact is immutable'); END;
CREATE TRIGGER authority_artifact_immutable_delete
BEFORE DELETE ON authority_artifact
BEGIN SELECT RAISE(ABORT, 'authority artifact is immutable'); END;
CREATE TRIGGER authority_artifact_binding_immutable_update
BEFORE UPDATE ON authority_artifact_binding
BEGIN SELECT RAISE(ABORT, 'authority artifact binding is immutable'); END;
CREATE TRIGGER authority_artifact_binding_immutable_delete
BEFORE DELETE ON authority_artifact_binding
BEGIN SELECT RAISE(ABORT, 'authority artifact binding is immutable'); END;
CREATE TRIGGER authority_artifact_verification_immutable_update
BEFORE UPDATE ON authority_artifact_verification
BEGIN SELECT RAISE(ABORT, 'authority artifact verification is immutable'); END;
CREATE TRIGGER authority_artifact_verification_immutable_delete
BEFORE DELETE ON authority_artifact_verification
BEGIN SELECT RAISE(ABORT, 'authority artifact verification is immutable'); END;

CREATE TRIGGER authority_artifact_verification_digest_contract
BEFORE INSERT ON authority_artifact_verification
WHEN NEW.expected_digest <> (
    SELECT content_hash FROM governed_authority
    WHERE authority_id = NEW.authority_id AND authority_version = NEW.authority_version
)
OR NEW.computed_digest <> (
    SELECT artifact_digest FROM authority_artifact
    WHERE artifact_id = NEW.artifact_id AND artifact_version = NEW.artifact_version
)
OR NEW.expected_digest <> NEW.computed_digest
BEGIN SELECT RAISE(ROLLBACK, 'authority artifact digest verification failed'); END;

CREATE TRIGGER authority_artifact_verification_canonical_time
BEFORE INSERT ON authority_artifact_verification
WHEN NOT (
    typeof(NEW.verified_at) = 'text' AND length(NEW.verified_at) = 27
    AND length(CAST(NEW.verified_at AS BLOB)) = 27
    AND hex(CAST(NEW.verified_at AS BLOB)) GLOB '3[0-9]3[0-9]3[0-9]3[0-9]2D3[0-9]3[0-9]2D3[0-9]3[0-9]543[0-9]3[0-9]3A3[0-9]3[0-9]3A3[0-9]3[0-9]2E3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]3[0-9]5A'
    AND CAST(substr(NEW.verified_at,1,4) AS INTEGER) BETWEEN 1 AND 9999
    AND CAST(substr(NEW.verified_at,6,2) AS INTEGER) BETWEEN 1 AND 12
    AND CAST(substr(NEW.verified_at,9,2) AS INTEGER) BETWEEN 1 AND
        CASE CAST(substr(NEW.verified_at,6,2) AS INTEGER)
            WHEN 2 THEN CASE
                WHEN CAST(substr(NEW.verified_at,1,4) AS INTEGER) % 400 = 0
                  OR (CAST(substr(NEW.verified_at,1,4) AS INTEGER) % 4 = 0
                      AND CAST(substr(NEW.verified_at,1,4) AS INTEGER) % 100 <> 0)
                THEN 29 ELSE 28 END
            WHEN 4 THEN 30 WHEN 6 THEN 30 WHEN 9 THEN 30 WHEN 11 THEN 30
            ELSE 31
        END
    AND CAST(substr(NEW.verified_at,12,2) AS INTEGER) BETWEEN 0 AND 23
    AND CAST(substr(NEW.verified_at,15,2) AS INTEGER) BETWEEN 0 AND 59
    AND CAST(substr(NEW.verified_at,18,2) AS INTEGER) BETWEEN 0 AND 59
    AND CAST(substr(NEW.verified_at,21,6) AS INTEGER) BETWEEN 0 AND 999999
)
BEGIN SELECT RAISE(ROLLBACK, 'verification time is not canonical'); END;

-- Existing legacy rows are preserved and are not retroactively backfilled;
-- every newly inserted PUBLISHED state/event requires accepted proof.
CREATE TRIGGER authority_state_schema_a_publication_guard
BEFORE INSERT ON authority_state
WHEN NEW.status = 'PUBLISHED'
 AND NOT EXISTS (SELECT 1 FROM authority_state
                 WHERE authority_id=NEW.authority_id
                   AND authority_version=NEW.authority_version)
 AND NOT EXISTS (
     SELECT 1 FROM authority_artifact_verification v
     WHERE v.authority_id=NEW.authority_id AND v.authority_version=NEW.authority_version
       AND v.verification_result='VERIFIED'
 )
BEGIN SELECT RAISE(ROLLBACK, 'Schema A verification required before publication'); END;

CREATE TRIGGER authority_event_schema_a_publication_guard
BEFORE INSERT ON authority_event
WHEN NEW.event_type = 'PUBLISHED'
 AND NOT EXISTS (SELECT 1 FROM authority_event
                 WHERE authority_id=NEW.authority_id
                   AND authority_version=NEW.authority_version)
 AND NOT EXISTS (
     SELECT 1 FROM authority_artifact_verification v
     WHERE v.authority_id=NEW.authority_id AND v.authority_version=NEW.authority_version
       AND v.verification_result='VERIFIED'
 )
BEGIN SELECT RAISE(ROLLBACK, 'Schema A verification required before publication'); END;
