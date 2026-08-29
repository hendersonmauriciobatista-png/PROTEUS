CREATE TABLE governed_measurement (
    measurement_id TEXT PRIMARY KEY,
    point_id TEXT NOT NULL,
    context_revision_id TEXT NOT NULL,
    aps_set_id TEXT NOT NULL,
    aps_version INTEGER NOT NULL CHECK (aps_version >= 1),
    parameter_reference TEXT NOT NULL CHECK (length(trim(parameter_reference)) > 0),
    value REAL NOT NULL,
    measured_at TEXT NOT NULL,
    registered_at TEXT NOT NULL,
    provenance TEXT NOT NULL CHECK (provenance IN (
        'MANUAL_ENTRY',
        'DEVICE_OR_SENSOR',
        'EXTERNAL_RESULT',
        'IMPORTED_DATA',
        'UNKNOWN'
    )),
    FOREIGN KEY (point_id)
        REFERENCES governed_monitoring_point(point_id) ON DELETE RESTRICT,
    FOREIGN KEY (context_revision_id, point_id)
        REFERENCES point_context_revision(context_revision_id, point_id) ON DELETE RESTRICT,
    FOREIGN KEY (aps_set_id, aps_version, context_revision_id)
        REFERENCES aps_version(set_id, version, context_revision_id) ON DELETE RESTRICT,
    FOREIGN KEY (aps_set_id, aps_version, parameter_reference)
        REFERENCES aps_member(set_id, version, parameter_reference) ON DELETE RESTRICT
);

CREATE TRIGGER governed_measurement_immutable_update
BEFORE UPDATE ON governed_measurement
BEGIN
    SELECT RAISE(ABORT, 'governed_measurement is immutable');
END;

CREATE TRIGGER governed_measurement_immutable_delete
BEFORE DELETE ON governed_measurement
BEGIN
    SELECT RAISE(ABORT, 'governed_measurement deletion is not authorized');
END;

CREATE TRIGGER authority_reference_immutable_update
BEFORE UPDATE ON authority_reference
BEGIN
    SELECT RAISE(ABORT, 'authority_reference is immutable');
END;

CREATE TRIGGER authority_reference_immutable_delete
BEFORE DELETE ON authority_reference
BEGIN
    SELECT RAISE(ABORT, 'authority_reference is immutable');
END;

CREATE TRIGGER evidence_reference_immutable_update
BEFORE UPDATE ON evidence_reference
BEGIN
    SELECT RAISE(ABORT, 'evidence_reference is immutable');
END;

CREATE TRIGGER evidence_reference_immutable_delete
BEFORE DELETE ON evidence_reference
BEGIN
    SELECT RAISE(ABORT, 'evidence_reference is immutable');
END;

CREATE TRIGGER basis_authority_immutable_update
BEFORE UPDATE ON basis_authority
BEGIN
    SELECT RAISE(ABORT, 'basis_authority is immutable');
END;

CREATE TRIGGER basis_authority_immutable_delete
BEFORE DELETE ON basis_authority
BEGIN
    SELECT RAISE(ABORT, 'basis_authority is immutable');
END;

CREATE TRIGGER basis_evidence_immutable_update
BEFORE UPDATE ON basis_evidence
BEGIN
    SELECT RAISE(ABORT, 'basis_evidence is immutable');
END;

CREATE TRIGGER basis_evidence_immutable_delete
BEFORE DELETE ON basis_evidence
BEGIN
    SELECT RAISE(ABORT, 'basis_evidence is immutable');
END;

CREATE TRIGGER member_authorization_basis_immutable_update
BEFORE UPDATE ON member_authorization_basis
BEGIN
    SELECT RAISE(ABORT, 'member_authorization_basis is immutable');
END;

CREATE TRIGGER member_authorization_basis_immutable_delete
BEFORE DELETE ON member_authorization_basis
BEGIN
    SELECT RAISE(ABORT, 'member_authorization_basis is immutable');
END;
