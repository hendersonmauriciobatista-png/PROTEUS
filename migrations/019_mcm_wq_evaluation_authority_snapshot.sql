-- MCM-WQ Schema B: immutable authority snapshot and exact member basis.
-- No legacy rows are backfilled; the snapshot row is the governed discriminator.

-- SQLite requires an exact UNIQUE parent key for composite foreign keys. These
-- indexes are redundant with the existing leading primary keys and add no new
-- accepted/rejected data states.
CREATE UNIQUE INDEX schema_b_applicability_identity_unique
    ON authority_applicability(applicability_id, authority_id, authority_version);
CREATE UNIQUE INDEX schema_b_authority_event_identity_unique
    ON authority_event(event_id, authority_id, authority_version);
CREATE UNIQUE INDEX schema_b_applicability_event_identity_unique
    ON authority_applicability_event(event_id, applicability_id);
CREATE UNIQUE INDEX schema_b_verification_identity_unique
    ON authority_artifact_verification(verification_id, authority_id, authority_version);

CREATE TABLE governed_evaluation_authority_snapshot (
    evaluation_id TEXT NOT NULL PRIMARY KEY,
    authority_id TEXT NOT NULL,
    authority_version INTEGER NOT NULL CHECK (authority_version > 0),
    authority_applicability_id TEXT NOT NULL,
    authority_lifecycle_event_id TEXT NOT NULL,
    authority_applicability_event_id TEXT NOT NULL,
    verification_id TEXT NOT NULL,
    authority_gate_status TEXT NOT NULL CHECK (authority_gate_status = 'RESOLVED'),
    lifecycle_policy_result TEXT NOT NULL CHECK (
        lifecycle_policy_result = 'TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION'
    ),
    rule_resolution_outcome TEXT NOT NULL CHECK (
        rule_resolution_outcome IN ('ZERO_APPLICABLE_RULE', 'ONE_APPLICABLE_RULE')
    ),
    authority_gate_policy_contract_version TEXT NOT NULL CHECK (
        authority_gate_policy_contract_version =
        'mcm-wq-authority-gate-technical-admission/v1'
    ),
    FOREIGN KEY (evaluation_id)
        REFERENCES governed_evaluation(evaluation_id),
    FOREIGN KEY (authority_id, authority_version)
        REFERENCES governed_authority(authority_id, authority_version),
    FOREIGN KEY (
        authority_applicability_id, authority_id, authority_version
    ) REFERENCES authority_applicability(
        applicability_id, authority_id, authority_version
    ),
    FOREIGN KEY (
        authority_lifecycle_event_id, authority_id, authority_version
    ) REFERENCES authority_event(
        event_id, authority_id, authority_version
    ),
    FOREIGN KEY (
        authority_applicability_event_id, authority_applicability_id
    ) REFERENCES authority_applicability_event(event_id, applicability_id),
    FOREIGN KEY (
        verification_id, authority_id, authority_version
    ) REFERENCES authority_artifact_verification(
        verification_id, authority_id, authority_version
    )
);

CREATE TABLE governed_evaluation_authority_snapshot_basis (
    evaluation_id TEXT NOT NULL,
    basis_id TEXT NOT NULL,
    aps_set_id TEXT NOT NULL,
    aps_version INTEGER NOT NULL CHECK (aps_version > 0),
    parameter_reference TEXT NOT NULL CHECK (length(trim(parameter_reference)) > 0),
    PRIMARY KEY (evaluation_id, basis_id),
    FOREIGN KEY (evaluation_id)
        REFERENCES governed_evaluation_authority_snapshot(evaluation_id)
        DEFERRABLE INITIALLY DEFERRED,
    FOREIGN KEY (aps_set_id, aps_version, parameter_reference)
        REFERENCES aps_member(set_id, version, parameter_reference),
    FOREIGN KEY (basis_id, aps_set_id, aps_version)
        REFERENCES authorization_basis(basis_id, set_id, version)
);

CREATE INDEX schema_b_snapshot_authority_lookup
    ON governed_evaluation_authority_snapshot(authority_id, authority_version);
CREATE INDEX schema_b_snapshot_applicability_lookup
    ON governed_evaluation_authority_snapshot(authority_applicability_id);
CREATE INDEX schema_b_snapshot_lifecycle_event_lookup
    ON governed_evaluation_authority_snapshot(authority_lifecycle_event_id);
CREATE INDEX schema_b_snapshot_verification_lookup
    ON governed_evaluation_authority_snapshot(verification_id);
CREATE INDEX schema_b_snapshot_basis_basis_lookup
    ON governed_evaluation_authority_snapshot_basis(basis_id);
CREATE INDEX schema_b_snapshot_basis_scope_lookup
    ON governed_evaluation_authority_snapshot_basis(
        aps_set_id, aps_version, parameter_reference
    );

CREATE TRIGGER schema_b_snapshot_basis_scope_guard
BEFORE INSERT ON governed_evaluation_authority_snapshot_basis
BEGIN
    SELECT CASE WHEN EXISTS (
        SELECT 1 FROM governed_evaluation_authority_snapshot
        WHERE evaluation_id = NEW.evaluation_id
    ) THEN RAISE(ROLLBACK, 'Schema B basis cannot be added after snapshot') END;

    SELECT CASE WHEN NOT EXISTS (
        SELECT 1
        FROM governed_evaluation e
        JOIN governed_measurement m ON m.measurement_id = e.measurement_id
        WHERE e.evaluation_id = NEW.evaluation_id
          AND e.parameter_reference = m.parameter_reference
          AND NEW.aps_set_id = m.aps_set_id
          AND NEW.aps_version = m.aps_version
          AND NEW.parameter_reference = e.parameter_reference
    ) THEN RAISE(ROLLBACK, 'Schema B basis evaluation scope mismatch') END;

    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM member_authorization_basis m
        WHERE m.set_id = NEW.aps_set_id
          AND m.version = NEW.aps_version
          AND m.parameter_reference = NEW.parameter_reference
          AND m.basis_id = NEW.basis_id
    ) THEN RAISE(ROLLBACK, 'Schema B basis is not an exact member basis') END;

    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM basis_authority a WHERE a.basis_id = NEW.basis_id
    ) OR NOT EXISTS (
        SELECT 1 FROM basis_evidence e WHERE e.basis_id = NEW.basis_id
    ) THEN RAISE(ROLLBACK, 'Schema B basis authorization chain is incomplete') END;
END;

CREATE TRIGGER schema_b_snapshot_complete_guard
BEFORE INSERT ON governed_evaluation_authority_snapshot
BEGIN
    SELECT CASE WHEN NOT EXISTS (
        SELECT 1
        FROM governed_evaluation e
        JOIN governed_measurement m ON m.measurement_id = e.measurement_id
        JOIN authority_applicability a
          ON a.applicability_id = NEW.authority_applicability_id
        WHERE e.evaluation_id = NEW.evaluation_id
          AND e.parameter_reference = m.parameter_reference
          AND a.authority_id = NEW.authority_id
          AND a.authority_version = NEW.authority_version
          AND a.context_revision_id = m.context_revision_id
          AND a.parameter_reference = e.parameter_reference
    ) THEN RAISE(ROLLBACK, 'Schema B applicability evaluation scope mismatch') END;

    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM authority_event e
        WHERE e.event_id = NEW.authority_lifecycle_event_id
          AND e.authority_id = NEW.authority_id
          AND e.authority_version = NEW.authority_version
    ) THEN RAISE(ROLLBACK, 'Schema B lifecycle event identity mismatch') END;

    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM authority_applicability_event e
        WHERE e.event_id = NEW.authority_applicability_event_id
          AND e.applicability_id = NEW.authority_applicability_id
    ) THEN RAISE(ROLLBACK, 'Schema B applicability event identity mismatch') END;

    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM authority_artifact_verification v
        WHERE v.verification_id = NEW.verification_id
          AND v.authority_id = NEW.authority_id
          AND v.authority_version = NEW.authority_version
          AND v.verification_result = 'VERIFIED'
    ) THEN RAISE(ROLLBACK, 'Schema B verification identity mismatch') END;

    SELECT CASE WHEN NOT EXISTS (
        SELECT 1 FROM governed_evaluation_authority_snapshot_basis b
        WHERE b.evaluation_id = NEW.evaluation_id
    ) THEN RAISE(ROLLBACK, 'Schema B snapshot requires at least one basis') END;

    SELECT CASE WHEN EXISTS (
        SELECT 1
        FROM governed_evaluation e
        JOIN governed_measurement m ON m.measurement_id = e.measurement_id
        WHERE e.evaluation_id = NEW.evaluation_id
          AND (
              e.parameter_reference <> m.parameter_reference
              OR EXISTS (
                  SELECT 1
                  FROM governed_evaluation_authority_snapshot_basis b
                  WHERE b.evaluation_id = NEW.evaluation_id
                    AND (
                        b.aps_set_id <> m.aps_set_id
                        OR b.aps_version <> m.aps_version
                        OR b.parameter_reference <> e.parameter_reference
                    )
              )
          )
    ) THEN RAISE(ROLLBACK, 'Schema B snapshot evaluation scope mismatch') END;

    SELECT CASE WHEN EXISTS (
        SELECT 1
        FROM governed_evaluation_authority_snapshot_basis b
        WHERE b.evaluation_id = NEW.evaluation_id
          AND NOT EXISTS (
              SELECT 1 FROM member_authorization_basis m
              WHERE m.set_id = b.aps_set_id
                AND m.version = b.aps_version
                AND m.parameter_reference = b.parameter_reference
                AND m.basis_id = b.basis_id
          )
    ) THEN RAISE(ROLLBACK, 'Schema B snapshot contains an extra basis') END;

    SELECT CASE WHEN EXISTS (
        SELECT 1
        FROM governed_evaluation_authority_snapshot_basis seed
        JOIN member_authorization_basis expected
          ON expected.set_id = seed.aps_set_id
         AND expected.version = seed.aps_version
         AND expected.parameter_reference = seed.parameter_reference
        WHERE seed.evaluation_id = NEW.evaluation_id
          AND NOT EXISTS (
              SELECT 1
              FROM governed_evaluation_authority_snapshot_basis actual
              WHERE actual.evaluation_id = NEW.evaluation_id
                AND actual.aps_set_id = expected.set_id
                AND actual.aps_version = expected.version
                AND actual.parameter_reference = expected.parameter_reference
                AND actual.basis_id = expected.basis_id
          )
    ) THEN RAISE(ROLLBACK, 'Schema B snapshot basis set is incomplete') END;
END;

CREATE TRIGGER schema_b_snapshot_immutable_update
BEFORE UPDATE ON governed_evaluation_authority_snapshot
BEGIN SELECT RAISE(ROLLBACK, 'Schema B snapshot is immutable'); END;
CREATE TRIGGER schema_b_snapshot_immutable_delete
BEFORE DELETE ON governed_evaluation_authority_snapshot
BEGIN SELECT RAISE(ROLLBACK, 'Schema B snapshot is immutable'); END;
CREATE TRIGGER schema_b_snapshot_basis_immutable_update
BEFORE UPDATE ON governed_evaluation_authority_snapshot_basis
BEGIN SELECT RAISE(ROLLBACK, 'Schema B snapshot basis is immutable'); END;
CREATE TRIGGER schema_b_snapshot_basis_immutable_delete
BEFORE DELETE ON governed_evaluation_authority_snapshot_basis
BEGIN SELECT RAISE(ROLLBACK, 'Schema B snapshot basis is immutable'); END;
