from datetime import datetime, timezone
from .identifiers import IdentifierFactory
from .repository import GovernedConflictError, GovernedReferenceError
from .measurement_service import serialize_utc_instant

class TemporalStateService:
    ACTIONS = {"CLOSE_TEMPORAL_INTERVAL", "CLOSE_AND_APPEND_SUCCESSOR"}
    TYPES = {"POINT_CONTEXT_REVISION", "APS_TEMPORAL_APPLICABILITY"}
    def __init__(self, repository, identifiers=None, clock=None):
        self.repository = repository; self.identifiers = identifiers or IdentifierFactory(); self.clock = clock or (lambda: datetime.now(timezone.utc))

    def close(self, record_type, record_id, effective_until, actor_reference, authorization_basis_id, successor=None):
        if record_type not in self.TYPES: raise ValueError("invalid affected record type")
        if not actor_reference or not authorization_basis_id: raise ValueError("actor and authorization basis are required")
        end = serialize_utc_instant(effective_until)
        action = "CLOSE_AND_APPEND_SUCCESSOR" if successor else "CLOSE_TEMPORAL_INTERVAL"
        with self.repository.transaction() as c:
            basis = c.execute("SELECT set_id, version FROM authorization_basis WHERE basis_id = ?", (authorization_basis_id,)).fetchone()
            if basis is None: raise GovernedReferenceError("authorization basis not resolvable")
            table = "point_context_revision" if record_type == "POINT_CONTEXT_REVISION" else "aps_temporal_applicability"
            row = c.execute(f"SELECT effective_from, effective_until FROM {table} WHERE {'context_revision_id' if record_type == 'POINT_CONTEXT_REVISION' else 'aps_applicability_id'} = ?", (record_id,)).fetchone()
            if row is None or row[1] is not None: raise GovernedConflictError("interval is not open")
            if record_type == "APS_TEMPORAL_APPLICABILITY":
                lineage = c.execute("SELECT aps_set_id, aps_version FROM aps_temporal_applicability WHERE aps_applicability_id=?", (record_id,)).fetchone()
                if lineage != basis: raise GovernedConflictError("authorization basis incompatible with APS lineage")
            else:
                lineage = c.execute("SELECT set_id, version FROM aps_version WHERE context_revision_id=? ORDER BY version LIMIT 1", (record_id,)).fetchone()
                if lineage is not None and lineage != basis: raise GovernedConflictError("authorization basis incompatible with context lineage")
            if end <= row[0]: raise GovernedConflictError("invalid interval closure")
            if record_type == "POINT_CONTEXT_REVISION":
                if c.execute("SELECT 1 FROM governed_measurement WHERE context_revision_id=? AND measured_at>=?", (record_id,end)).fetchone(): raise GovernedConflictError("closure invalidates history")
                c.execute("UPDATE point_context_revision SET effective_until=? WHERE context_revision_id=?", (end,record_id))
            else:
                lineage = c.execute("SELECT aps_set_id, aps_version FROM aps_temporal_applicability WHERE aps_applicability_id=?", (record_id,)).fetchone()
                if c.execute("SELECT 1 FROM governed_measurement WHERE aps_set_id=? AND aps_version=? AND measured_at>=?", (lineage[0], lineage[1], end)).fetchone(): raise GovernedConflictError("closure invalidates history")
                c.execute("UPDATE aps_temporal_applicability SET effective_until=? WHERE aps_applicability_id=?", (end,record_id))
            c.execute("INSERT INTO governance_event (event_id,action,actor_reference,registered_at,authorization_basis_id,decision_timestamp,affected_record_type,affected_record_id,previous_effective_until,new_effective_until,successor_record_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (self.identifiers.new('event'),action,actor_reference,serialize_utc_instant(self.clock()),authorization_basis_id,serialize_utc_instant(self.clock()),record_type,record_id,None,end,successor))
