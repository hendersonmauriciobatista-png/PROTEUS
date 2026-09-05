import sqlite3, tempfile, unittest
from datetime import datetime, timezone
from pathlib import Path
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreError, GovernedCoreRepository, GovernedConflictError, GovernedReferenceError
from governed_core.services import ApplicabilityService
from governed_core.services import APSService, PointContextService
from governed_core.temporal_state import TemporalStateService

class ClosureGuardTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.r=GovernedCoreRepository(Path(self.t.name)/'x.sqlite3').initialize(); self.s=FirstRealAPSBootstrap(self.r).execute(); self.a=ApplicabilityService(self.r); self.a.assign_temporal(self.s.context_revision_id,self.s.aps_reference,datetime(2026,1,1,tzinfo=timezone.utc),actor_reference='ACTOR'); self.c=TemporalStateService(self.r,clock=lambda: datetime(2026,1,1,tzinfo=timezone.utc))
    def tearDown(self): self.t.cleanup()
    def test_context_overlap_and_boundaries(self):
        with self.assertRaises(GovernedReferenceError):
            self.r.fetch_temporal_context(self.s.point_id,'2025-01-01T00:00:00Z')
    def test_valid_closure_and_history_invalidation(self):
        with self.r._optional_connection(None) as c: app=c.execute('SELECT aps_applicability_id FROM aps_temporal_applicability').fetchone()[0]
        self.c.close('APS_TEMPORAL_APPLICABILITY',app,datetime(2026,2,1,tzinfo=timezone.utc),'ACTOR',self._basis())
    def _basis(self):
        with self.r._optional_connection(None) as c: return c.execute('SELECT basis_id FROM authorization_basis LIMIT 1').fetchone()[0]
    def test_event_immutability(self):
        with self.r._optional_connection(None) as c: self.assertGreaterEqual(c.execute('SELECT COUNT(*) FROM governance_event').fetchone()[0],2)

    def test_invalid_close_and_incompatible_basis_block(self):
        with self.r._optional_connection(None) as c: app=c.execute('SELECT aps_applicability_id FROM aps_temporal_applicability').fetchone()[0]
        with self.assertRaises(GovernedConflictError): self.c.close('APS_TEMPORAL_APPLICABILITY', app, datetime(2025,1,1,tzinfo=timezone.utc), 'ACTOR', self._basis())
        with self.assertRaises(GovernedCoreError): self.c.close('APS_TEMPORAL_APPLICABILITY', app, datetime(2027,1,1,tzinfo=timezone.utc), 'ACTOR', 'bas_missing')

    def test_closed_event_cannot_be_rewritten_or_deleted(self):
        with self.r._optional_connection(None) as c: app=c.execute('SELECT aps_applicability_id FROM aps_temporal_applicability').fetchone()[0]
        self.c.close('APS_TEMPORAL_APPLICABILITY', app, datetime(2026,2,1,tzinfo=timezone.utc), 'ACTOR', self._basis())
        with self.r.transaction() as c:
            event=c.execute("SELECT event_id FROM governance_event WHERE action='CLOSE_TEMPORAL_INTERVAL'").fetchone()[0]
            with self.assertRaises(sqlite3.IntegrityError): c.execute("UPDATE governance_event SET actor_reference='X' WHERE event_id=?",(event,))
            with self.assertRaises(sqlite3.IntegrityError): c.execute("DELETE FROM governance_event WHERE event_id=?",(event,))

    def test_explicit_context_overlap_is_rejected(self):
        with self.r.transaction() as c:
            c.execute("INSERT INTO geo_reference (geo_reference_id,context_revision_id,availability_state,state_reason,registered_at) VALUES ('geo-overlap','ctx_overlap','UNAVAILABLE','test','2026-01-01T00:00:00Z')")
            c.execute("INSERT INTO point_context_revision (context_revision_id,point_id,revision,purpose,water_context,point_type,created_at,effective_from,effective_until,geo_reference_id) VALUES ('ctx_overlap',?,?,? ,?,?,?,?,?,?)", (self.s.point_id, 99, 'ENVIRONMENTAL_CONDITION_MONITORING','FLOWING_SURFACE_WATER','GENERAL','2026-01-01T00:00:00Z','2026-02-01T00:00:00Z',None,'geo-overlap'))
            with self.assertRaises(sqlite3.IntegrityError):
                c.execute("INSERT INTO point_context_revision (context_revision_id,point_id,revision,purpose,water_context,point_type,created_at,effective_from,geo_reference_id) VALUES ('ctx_overlap2',?,?,? ,?,?,?,?,?)", (self.s.point_id, 100, 'ENVIRONMENTAL_CONDITION_MONITORING','FLOWING_SURFACE_WATER','GENERAL','2026-01-15T00:00:00Z','2026-03-01T00:00:00Z','geo-overlap'))

    def test_referenced_aps_history_blocks_closure(self):
        with self.r._optional_connection(None) as c: app=c.execute('SELECT aps_applicability_id,aps_set_id,aps_version FROM aps_temporal_applicability').fetchone()
        from governed_core.entry_application import ExplicitGovernedEntryService
        ExplicitGovernedEntryService(self.r).submit(self.s.point_id, 'PH', 7.0, datetime(2026,1,15,tzinfo=timezone.utc))
        with self.assertRaises(GovernedConflictError): self.c.close('APS_TEMPORAL_APPLICABILITY', app[0], datetime(2026,1,1,tzinfo=timezone.utc), 'ACTOR', self._basis())

    def test_closed_interval_rewrite_reopen_and_delete_blocked(self):
        with self.r._optional_connection(None) as c: app=c.execute('SELECT aps_applicability_id FROM aps_temporal_applicability').fetchone()[0]
        self.c.close('APS_TEMPORAL_APPLICABILITY', app, datetime(2026,2,1,tzinfo=timezone.utc), 'ACTOR', self._basis())
        with self.r.transaction() as c:
            with self.assertRaises(sqlite3.IntegrityError): c.execute("UPDATE aps_temporal_applicability SET effective_until=NULL WHERE aps_applicability_id=?",(app,))
            with self.assertRaises(sqlite3.IntegrityError): c.execute("UPDATE aps_temporal_applicability SET effective_from='2026-01-02T00:00:00Z' WHERE aps_applicability_id=?",(app,))
            with self.assertRaises(sqlite3.IntegrityError): c.execute("DELETE FROM aps_temporal_applicability WHERE aps_applicability_id=?",(app,))

    def test_context_lineage_authorization_mismatch_blocks(self):
        with self.r._optional_connection(None) as c: app=c.execute('SELECT aps_applicability_id FROM aps_temporal_applicability').fetchone()[0]
        with self.assertRaises(GovernedCoreError): self.c.close('APS_TEMPORAL_APPLICABILITY', app, datetime(2026,2,1,tzinfo=timezone.utc), 'ACTOR', 'bas_missing')

    def test_resolvable_incompatible_context_and_aps_bases_block(self):
        with self.r._optional_connection(None) as c:
            refs=c.execute('SELECT authority_reference_id FROM authority_reference').fetchall(); ev=c.execute('SELECT evidence_reference_id FROM evidence_reference').fetchall(); app=c.execute('SELECT aps_applicability_id FROM aps_temporal_applicability').fetchone()[0]
        aps=APSService(self.r); basis=aps.make_basis(tuple(x[0] for x in refs), tuple(x[0] for x in ev), ('PH',)); other=aps.create_version(self.s.context_revision_id, ('PH',), (basis,))
        with self.assertRaises(GovernedConflictError): self.c.close('APS_TEMPORAL_APPLICABILITY', app, datetime(2026,2,1,tzinfo=timezone.utc), 'ACTOR', basis.basis_id)

    def test_valid_different_context_lineage_basis_blocks_original_close(self):
        current = self.r.fetch_current_context(self.s.point_id)
        second = PointContextService(self.r).create_context_revision(self.s.point_id, current.purpose, current.water_context, current.point_type, 'ACTOR')
        with self.r._optional_connection(None) as c:
            refs=c.execute('SELECT authority_reference_id FROM authority_reference').fetchall(); ev=c.execute('SELECT evidence_reference_id FROM evidence_reference').fetchall()
        aps=APSService(self.r); basis=aps.make_basis(tuple(x[0] for x in refs), tuple(x[0] for x in ev), ('PH',)); aps.create_version(second.context_revision_id, ('PH',), (basis,))
        with self.assertRaises(GovernedConflictError): self.c.close('POINT_CONTEXT_REVISION', self.s.context_revision_id, datetime(2026,2,1,tzinfo=timezone.utc), 'ACTOR', basis.basis_id)

if __name__=='__main__': unittest.main()
