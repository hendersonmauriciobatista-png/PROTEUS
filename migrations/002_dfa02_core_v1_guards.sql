CREATE TRIGGER point_project_reference_immutable
BEFORE UPDATE OF project_reference ON governed_monitoring_point
BEGIN
    SELECT RAISE(ABORT, 'project_reference is immutable');
END;

CREATE TRIGGER context_revision_immutable_update
BEFORE UPDATE ON point_context_revision
BEGIN
    SELECT RAISE(ABORT, 'point_context_revision is immutable');
END;

CREATE TRIGGER context_revision_immutable_delete
BEFORE DELETE ON point_context_revision
BEGIN
    SELECT RAISE(ABORT, 'point_context_revision is immutable');
END;

CREATE TRIGGER aps_set_immutable_update
BEFORE UPDATE ON authorized_parameter_set
BEGIN
    SELECT RAISE(ABORT, 'authorized_parameter_set is immutable');
END;

CREATE TRIGGER aps_set_immutable_delete
BEFORE DELETE ON authorized_parameter_set
BEGIN
    SELECT RAISE(ABORT, 'authorized_parameter_set is immutable');
END;

CREATE TRIGGER aps_version_immutable_update
BEFORE UPDATE ON aps_version
BEGIN
    SELECT RAISE(ABORT, 'aps_version is immutable');
END;

CREATE TRIGGER aps_version_immutable_delete
BEFORE DELETE ON aps_version
BEGIN
    SELECT RAISE(ABORT, 'aps_version is immutable');
END;

CREATE TRIGGER aps_member_immutable_update
BEFORE UPDATE ON aps_member
BEGIN
    SELECT RAISE(ABORT, 'aps_member is immutable');
END;

CREATE TRIGGER aps_member_immutable_delete
BEFORE DELETE ON aps_member
BEGIN
    SELECT RAISE(ABORT, 'aps_member is immutable');
END;

CREATE TRIGGER authorization_basis_immutable_update
BEFORE UPDATE ON authorization_basis
BEGIN
    SELECT RAISE(ABORT, 'authorization_basis is immutable');
END;

CREATE TRIGGER authorization_basis_immutable_delete
BEFORE DELETE ON authorization_basis
BEGIN
    SELECT RAISE(ABORT, 'authorization_basis is immutable');
END;

CREATE TRIGGER governance_event_append_only_update
BEFORE UPDATE ON governance_event
BEGIN
    SELECT RAISE(ABORT, 'governance_event is append-only');
END;

CREATE TRIGGER governance_event_append_only_delete
BEFORE DELETE ON governance_event
BEGIN
    SELECT RAISE(ABORT, 'governance_event is append-only');
END;

CREATE TRIGGER governance_event_resolution_append_only_update
BEFORE UPDATE ON governance_event_resolution
BEGIN
    SELECT RAISE(ABORT, 'governance_event_resolution is append-only');
END;

CREATE TRIGGER governance_event_resolution_append_only_delete
BEFORE DELETE ON governance_event_resolution
BEGIN
    SELECT RAISE(ABORT, 'governance_event_resolution is append-only');
END;
