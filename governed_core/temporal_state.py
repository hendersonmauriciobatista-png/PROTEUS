from datetime import datetime, timezone
from .identifiers import IdentifierFactory
from .repository import GovernedConflictError, GovernedReferenceError
from .measurement_service import serialize_utc_instant
from .geo_models import GeoAvailabilityState, LocationProvenance
from .geo_service import GeoService

class TemporalStateService:
    ACTIONS = {"CLOSE_TEMPORAL_INTERVAL", "CLOSE_AND_APPEND_SUCCESSOR"}
    TYPES = {"POINT_CONTEXT_REVISION", "APS_TEMPORAL_APPLICABILITY"}
    def __init__(self, repository, identifiers=None, clock=None):
        self.repository = repository; self.identifiers = identifiers or IdentifierFactory(); self.clock = clock or (lambda: datetime.now(timezone.utc)); self.geo = GeoService(repository, self.identifiers, self.clock)

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

    def append_successor(self, record_type, record_id, successor, actor_reference, authorization_basis_id):
        if record_type not in self.TYPES or not isinstance(successor, dict):
            raise ValueError("invalid temporal successor")
        start = successor.get("effective_from")
        if start is None: raise ValueError("successor effective_from is required")
        start = serialize_utc_instant(start)
        with self.repository.transaction() as c:
            basis = c.execute("SELECT set_id, version FROM authorization_basis WHERE basis_id=?", (authorization_basis_id,)).fetchone()
            if basis is None: raise GovernedReferenceError("authorization basis not resolvable")
            if record_type == "APS_TEMPORAL_APPLICABILITY":
                row = c.execute("SELECT context_revision_id, aps_set_id, aps_version, effective_from, effective_until FROM aps_temporal_applicability WHERE aps_applicability_id=?", (record_id,)).fetchone()
                if row is None or row[4] is not None: raise GovernedConflictError("interval is not open")
                if (row[1], row[2]) != basis: raise GovernedConflictError("authorization basis incompatible with APS lineage")
                ref = successor.get("reference")
                if ref is None or self.repository.fetch_aps_version(ref, c) != row[0]: raise GovernedReferenceError("successor APS context mismatch")
                c.execute("UPDATE aps_temporal_applicability SET effective_until=? WHERE aps_applicability_id=?", (start, record_id))
                successor_id = self.identifiers.new("aps_applicability")
                c.execute("INSERT INTO aps_temporal_applicability VALUES (?,?,?,?,?,NULL)", (successor_id, row[0], ref.set_id, ref.version, start))
            else:
                row = c.execute("SELECT point_id, effective_from, effective_until FROM point_context_revision WHERE context_revision_id=?", (record_id,)).fetchone()
                if row is None or row[2] is not None: raise GovernedConflictError("interval is not open")
                if c.execute("SELECT set_id,version FROM aps_version WHERE context_revision_id=? ORDER BY version LIMIT 1", (record_id,)).fetchone() not in (basis, None): raise GovernedConflictError("authorization basis incompatible with context lineage")
                successor_id = self.identifiers.new("context_revision")
                c.execute("UPDATE point_context_revision SET effective_until=? WHERE context_revision_id=?", (start, record_id))
                legacy_value = successor.get("geo_reference")
                geo_id = None
                if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='geo_reference'").fetchone():
                    data = successor.get("geo_reference_data")
                    if isinstance(data, dict):
                        data = dict(data)
                        provenance = data.pop("provenance", None)
                        if isinstance(provenance, dict):
                            provenance = LocationProvenance(**provenance)
                        if provenance is not None:
                            self.geo.register_provenance(provenance, c)
                        geo_id = self.geo.create_reference(successor_id, connection=c, **data).geo_reference_id
                    else:
                        state = (GeoAvailabilityState.LEGACY_UNCLASSIFIED.value
                                 if legacy_value is not None else GeoAvailabilityState.UNAVAILABLE.value)
                        reason = ("LEGACY_OPAQUE_VALUE_NOT_SEMANTICALLY_PROVEN"
                                  if legacy_value is not None else "NO_COORDINATE_SUPPLIED")
                        geo_id = self.geo.create_reference(successor_id, state, state_reason=reason, connection=c).geo_reference_id
                columns = "context_revision_id,point_id,revision,purpose,water_context,point_type,geo_reference,created_at,effective_from"
                values = [successor_id, row[0], successor["revision"], successor["purpose"], successor["water_context"], successor["point_type"], legacy_value, serialize_utc_instant(self.clock()), start]
                if geo_id is not None:
                    columns += ",geo_reference_id"; values.append(geo_id)
                c.execute(f"INSERT INTO point_context_revision ({columns}) VALUES ({','.join('?' for _ in values)})", values)
                c.execute("UPDATE governed_monitoring_point SET current_context_revision_id=? WHERE point_id=?", (successor_id, row[0]))
            c.execute("INSERT INTO governance_event (event_id,action,actor_reference,registered_at,authorization_basis_id,decision_timestamp,affected_record_type,affected_record_id,previous_effective_until,new_effective_until,successor_record_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)", (self.identifiers.new("event"), "CLOSE_AND_APPEND_SUCCESSOR", actor_reference, serialize_utc_instant(self.clock()), authorization_basis_id, start, record_type, record_id, None, start, successor_id))
        return successor_id
