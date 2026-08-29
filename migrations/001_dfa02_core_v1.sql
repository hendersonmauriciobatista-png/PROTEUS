PRAGMA foreign_keys = ON;

CREATE TABLE governed_monitoring_point (
    point_id TEXT PRIMARY KEY,
    project_reference TEXT NOT NULL,
    display_name TEXT NOT NULL CHECK (length(trim(display_name)) > 0),
    status TEXT NOT NULL CHECK (status IN ('ACTIVE', 'INACTIVE')),
    current_context_revision_id TEXT,
    FOREIGN KEY (current_context_revision_id)
        REFERENCES point_context_revision(context_revision_id)
        DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE point_context_revision (
    context_revision_id TEXT PRIMARY KEY,
    point_id TEXT NOT NULL,
    revision INTEGER NOT NULL CHECK (revision >= 1),
    purpose TEXT NOT NULL CHECK (purpose IN (
        'ENVIRONMENTAL_CONDITION_MONITORING',
        'ENVIRONMENTAL_IMPACT_MONITORING',
        'COMPLIANCE_MONITORING',
        'WATER_USE_MONITORING'
    )),
    water_context TEXT NOT NULL CHECK (water_context IN (
        'FLOWING_SURFACE_WATER',
        'STANDING_SURFACE_WATER',
        'GROUNDWATER'
    )),
    point_type TEXT NOT NULL CHECK (point_type IN (
        'GENERAL', 'SPRING', 'WELL', 'ABSTRACTION_POINT'
    )),
    geo_reference TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (point_id, revision),
    UNIQUE (context_revision_id, point_id),
    FOREIGN KEY (point_id) REFERENCES governed_monitoring_point(point_id)
);

CREATE TABLE authorized_parameter_set (
    set_id TEXT PRIMARY KEY
);

CREATE TABLE aps_version (
    set_id TEXT NOT NULL,
    version INTEGER NOT NULL CHECK (version >= 1),
    context_revision_id TEXT NOT NULL,
    PRIMARY KEY (set_id, version),
    UNIQUE (set_id, version, context_revision_id),
    FOREIGN KEY (set_id) REFERENCES authorized_parameter_set(set_id),
    FOREIGN KEY (context_revision_id) REFERENCES point_context_revision(context_revision_id)
);

CREATE TABLE aps_member (
    set_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    parameter_reference TEXT NOT NULL CHECK (length(trim(parameter_reference)) > 0),
    PRIMARY KEY (set_id, version, parameter_reference),
    FOREIGN KEY (set_id, version) REFERENCES aps_version(set_id, version)
);

CREATE TABLE authority_reference (
    authority_reference_id TEXT PRIMARY KEY,
    locator TEXT NOT NULL CHECK (length(trim(locator)) > 0),
    content_hash TEXT
);

CREATE TABLE evidence_reference (
    evidence_reference_id TEXT PRIMARY KEY,
    locator TEXT NOT NULL CHECK (length(trim(locator)) > 0),
    content_hash TEXT
);

CREATE TABLE authorization_basis (
    basis_id TEXT PRIMARY KEY,
    set_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    UNIQUE (basis_id, set_id, version),
    FOREIGN KEY (set_id, version) REFERENCES aps_version(set_id, version)
);

CREATE TABLE basis_authority (
    basis_id TEXT NOT NULL,
    authority_reference_id TEXT NOT NULL,
    PRIMARY KEY (basis_id, authority_reference_id),
    FOREIGN KEY (basis_id) REFERENCES authorization_basis(basis_id),
    FOREIGN KEY (authority_reference_id) REFERENCES authority_reference(authority_reference_id)
);

CREATE TABLE basis_evidence (
    basis_id TEXT NOT NULL,
    evidence_reference_id TEXT NOT NULL,
    PRIMARY KEY (basis_id, evidence_reference_id),
    FOREIGN KEY (basis_id) REFERENCES authorization_basis(basis_id),
    FOREIGN KEY (evidence_reference_id) REFERENCES evidence_reference(evidence_reference_id)
);

CREATE TABLE member_authorization_basis (
    set_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    parameter_reference TEXT NOT NULL,
    basis_id TEXT NOT NULL,
    PRIMARY KEY (set_id, version, parameter_reference, basis_id),
    FOREIGN KEY (set_id, version, parameter_reference)
        REFERENCES aps_member(set_id, version, parameter_reference),
    FOREIGN KEY (basis_id, set_id, version)
        REFERENCES authorization_basis(basis_id, set_id, version)
);

CREATE TABLE aps_applicability (
    context_revision_id TEXT PRIMARY KEY,
    set_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    FOREIGN KEY (set_id, version, context_revision_id)
        REFERENCES aps_version(set_id, version, context_revision_id)
);

CREATE TABLE governance_event (
    event_id TEXT PRIMARY KEY,
    action TEXT NOT NULL CHECK (action IN (
        'CURRENT_CONTEXT_REFERENCE_CHANGED',
        'APPLICABILITY_ASSIGNED',
        'APPLICABILITY_CHANGED',
        'APPLICABILITY_REMOVED',
        'APS_VERSION_DISQUALIFIED',
        'APS_VERSION_REQUALIFIED'
    )),
    actor_reference TEXT NOT NULL CHECK (length(trim(actor_reference)) > 0),
    registered_at TEXT NOT NULL,
    context_revision_id TEXT,
    previous_context_revision_id TEXT,
    new_context_revision_id TEXT,
    previous_set_id TEXT,
    previous_version INTEGER,
    new_set_id TEXT,
    new_version INTEGER,
    target_set_id TEXT,
    target_version INTEGER,
    FOREIGN KEY (context_revision_id) REFERENCES point_context_revision(context_revision_id),
    FOREIGN KEY (previous_context_revision_id) REFERENCES point_context_revision(context_revision_id),
    FOREIGN KEY (new_context_revision_id) REFERENCES point_context_revision(context_revision_id),
    FOREIGN KEY (previous_set_id, previous_version) REFERENCES aps_version(set_id, version),
    FOREIGN KEY (new_set_id, new_version) REFERENCES aps_version(set_id, version),
    FOREIGN KEY (target_set_id, target_version) REFERENCES aps_version(set_id, version)
);

CREATE TABLE governance_event_resolution (
    requalification_event_id TEXT NOT NULL,
    disqualification_event_id TEXT NOT NULL,
    PRIMARY KEY (requalification_event_id, disqualification_event_id),
    FOREIGN KEY (requalification_event_id) REFERENCES governance_event(event_id),
    FOREIGN KEY (disqualification_event_id) REFERENCES governance_event(event_id)
);

CREATE TABLE schema_migration (
    migration_id TEXT PRIMARY KEY,
    checksum TEXT NOT NULL,
    applied_at TEXT NOT NULL
);
