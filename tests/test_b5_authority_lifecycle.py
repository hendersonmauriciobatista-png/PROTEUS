import sqlite3, tempfile, unittest
from datetime import datetime, timezone
from pathlib import Path
from governed_core.repository import GovernedCoreRepository
from governed_core.authority_service import AuthorityService
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.evaluation_service import GovernedEvaluationService

T0=datetime(2026,1,1,tzinfo=timezone.utc); T1=datetime(2027,1,1,tzinfo=timezone.utc); T2=datetime(2028,1,1,tzinfo=timezone.utc)

class B5AuthorityLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.repo=GovernedCoreRepository(Path(self.tmp.name)/'db.sqlite3').initialize(); self.service=AuthorityService(self.repo)
        self.authority=self.service.create_authority('urn:test','hash','ctx','p',T0)
    def tearDown(self): self.tmp.cleanup()
    def test_create_resolve_and_state(self):
        a=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        self.assertEqual(a.applicability_id,self.service.resolve_applicability('ctx','p',T1).applicability_id)
        c=self.repo._connect()
        try: self.assertEqual('ACTIVE',c.execute("select state from authority_applicability_state where applicability_id=?",(a.applicability_id,)).fetchone()[0])
        finally: c.close()
    def test_revocation_closes_half_open_interval(self):
        a=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create'); self.service.revoke_applicability(a.applicability_id,T1,'actor','revoke')
        with self.assertRaises(ValueError): self.service.resolve_applicability('ctx','p',T1)
    def test_duplicate_terminal_and_reopen_rejected(self):
        a=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create'); self.service.revoke_applicability(a.applicability_id,T1,'actor','revoke')
        with self.assertRaises(ValueError): self.service.revoke_applicability(a.applicability_id,T2,'actor','again')
    def test_supersession_linkage_and_projection(self):
        a=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create'); b=self.service.supersede_applicability(a.applicability_id,self.authority.authority_id,1,'ctx','p',T1,'actor','replace')
        c=self.repo._connect()
        try:
            self.assertEqual(b,c.execute("select successor_applicability_id from authority_applicability_event where applicability_id=? and event_type='SUPERSEDED'",(a.applicability_id,)).fetchone()[0])
            self.assertEqual('SUPERSEDED',c.execute("select state from authority_applicability_state where applicability_id=?",(a.applicability_id,)).fetchone()[0])
            self.assertEqual('ACTIVE',c.execute("select state from authority_applicability_state where applicability_id=?",(b,)).fetchone()[0])
        finally: c.close()
    def test_unmapped_authority_blocked(self):
        with self.assertRaises(ValueError): self.service.create_applicability('missing',1,'ctx','p',T0,'actor','create')
    def test_overlap_prevented(self):
        self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        with self.assertRaises(ValueError): self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T1,'actor','create')

    def test_supersession_requires_active_predecessor_and_rolls_back(self):
        a=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create'); self.service.revoke_applicability(a.applicability_id,T1,'actor','revoke')
        with self.assertRaises(ValueError): self.service.supersede_applicability(a.applicability_id,self.authority.authority_id,1,'ctx','p',T2,'actor','replace')

    def test_terminal_time_is_explicit(self):
        a=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        self.service.revoke_applicability(a.applicability_id,T0,'actor','explicit')
        c=self.repo._connect()
        try: self.assertEqual('REVOKED', c.execute("select state from authority_applicability_state where applicability_id=?",(a.applicability_id,)).fetchone()[0])
        finally: c.close()

    def test_retroactive_terminal_event_blocked_by_persisted_evaluation(self):
        bootstrap=FirstRealAPSBootstrap(self.repo).execute()
        measurement=ExplicitGovernedEntryService(self.repo).submit(bootstrap.point_id,'PH',7.2,datetime(2026,8,30,12,0,tzinfo=timezone.utc))
        evaluation=GovernedEvaluationService(self.repo,clock=lambda:datetime(2026,8,30,12,1,tzinfo=timezone.utc)).record(measurement.measurement_id,'NORMAL','Dentro','catalogo',datetime(2026,8,30,12,0,30,tzinfo=timezone.utc))
        a=self.service.create_applicability(self.authority.authority_id,1,measurement.context_revision_id,'PH',T0,'actor','create')
        c=self.repo._connect()
        try: before=len(c.execute("select * from authority_applicability_event where applicability_id=?",(a.applicability_id,)).fetchall())
        finally: c.close()
        with self.assertRaises(ValueError): self.service.revoke_applicability(a.applicability_id,T1,'actor','retroactive')
        c=self.repo._connect()
        try:
            self.assertEqual(evaluation.evaluation_id,c.execute('select evaluation_id from governed_evaluation where evaluation_id=?',(evaluation.evaluation_id,)).fetchone()[0])
            self.assertEqual(before,c.execute("select count(*) from authority_applicability_event where applicability_id=?",(a.applicability_id,)).fetchone()[0])
            self.assertEqual('ACTIVE',c.execute("select state from authority_applicability_state where applicability_id=?",(a.applicability_id,)).fetchone()[0])
        finally: c.close()

    def test_supersession_forced_failure_rolls_back_partial_successor(self):
        predecessor=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        class FailingIds:
            def __init__(self): self.calls=0
            def new(self, kind):
                self.calls += 1
                if self.calls == 1: return 'apa_forced_successor'
                raise RuntimeError('forced test failure')
        self.service.identifiers=FailingIds()
        with self.assertRaises(RuntimeError):
            self.service.supersede_applicability(predecessor.applicability_id,self.authority.authority_id,1,'ctx','p',T1,'actor','replace')
        c=self.repo._connect()
        try:
            self.assertIsNone(c.execute("select 1 from authority_applicability where applicability_id='apa_forced_successor'").fetchone())
            self.assertIsNone(c.execute("select 1 from authority_applicability_event where applicability_id=? and event_type='SUPERSEDED'",(predecessor.applicability_id,)).fetchone())
            self.assertEqual('ACTIVE',c.execute("select state from authority_applicability_state where applicability_id=?",(predecessor.applicability_id,)).fetchone()[0])
        finally: c.close()

    def test_supersession_failure_after_predecessor_event_rolls_back(self):
        predecessor=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        def fail(stage):
            if stage == 'after_predecessor_event':
                raise RuntimeError('forced predecessor-event failure')
        self.service._test_supersession_failure_hook=fail
        with self.assertRaises(RuntimeError):
            self.service.supersede_applicability(predecessor.applicability_id,self.authority.authority_id,1,'ctx','p',T1,'actor','replace')
        c=self.repo._connect()
        try:
            self.assertIsNone(c.execute("select 1 from authority_applicability_event where applicability_id=? and event_type='SUPERSEDED'",(predecessor.applicability_id,)).fetchone())
            self.assertEqual('ACTIVE',c.execute("select state from authority_applicability_state where applicability_id=?",(predecessor.applicability_id,)).fetchone()[0])
            self.assertEqual(1,c.execute("select count(*) from authority_applicability").fetchone()[0])
        finally: c.close()

    def test_supersession_failure_after_successor_insert_rolls_back(self):
        predecessor=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        def fail(stage):
            if stage == 'after_successor_applicability':
                raise RuntimeError('forced successor-insert failure')
        self.service._test_supersession_failure_hook=fail
        with self.assertRaises(RuntimeError):
            self.service.supersede_applicability(predecessor.applicability_id,self.authority.authority_id,1,'ctx','p',T1,'actor','replace')
        c=self.repo._connect()
        try:
            self.assertIsNone(c.execute("select 1 from authority_applicability_event where applicability_id=? and event_type='SUPERSEDED'",(predecessor.applicability_id,)).fetchone())
            self.assertEqual('ACTIVE',c.execute("select state from authority_applicability_state where applicability_id=?",(predecessor.applicability_id,)).fetchone()[0])
            self.assertEqual(1,c.execute("select count(*) from authority_applicability").fetchone()[0])
        finally: c.close()

    def test_revocation_forced_failure_rolls_back_partial_event(self):
        applicability=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        self.service._test_failure_hook=lambda: (_ for _ in ()).throw(RuntimeError('forced test failure'))
        with self.assertRaises(ValueError):
            self.service.revoke_applicability(applicability.applicability_id,T1,'actor','revoke')
        c=self.repo._connect()
        try:
            self.assertIsNone(c.execute("select 1 from authority_applicability_event where applicability_id=? and event_type='REVOKED'",(applicability.applicability_id,)).fetchone())
            self.assertEqual('ACTIVE',c.execute("select state from authority_applicability_state where applicability_id=?",(applicability.applicability_id,)).fetchone()[0])
        finally: c.close()

    def test_closed_interval_overlap_rejected_and_adjacent_allowed(self):
        first=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        self.service.revoke_applicability(first.applicability_id,T1,'actor','close')
        with self.assertRaises(ValueError):
            self.service.create_applicability(self.authority.authority_id,1,'ctx','p',datetime(2026,6,1,tzinfo=timezone.utc),'actor','overlap')
        adjacent=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T1,'actor','adjacent')
        c=self.repo._connect()
        try:
            self.assertIsNotNone(c.execute('select 1 from authority_applicability where applicability_id=?',(adjacent.applicability_id,)).fetchone())
            self.assertIsNone(c.execute("select 1 from authority_applicability where context_revision_id='ctx' and parameter_reference='p' and effective_from=?",('2026-06-01T00:00:00.000000Z',)).fetchone())
        finally: c.close()

    def test_effective_at_is_distinct_from_registered_at(self):
        applicability=self.service.create_applicability(self.authority.authority_id,1,'ctx','p',T0,'actor','create')
        self.service.revoke_applicability(applicability.applicability_id,T0,'actor','historical terminal')
        c=self.repo._connect()
        try:
            effective,registered=c.execute("select effective_at,registered_at from authority_applicability_event where applicability_id=? and event_type='REVOKED'",(applicability.applicability_id,)).fetchone()
            self.assertEqual('2026-01-01T00:00:00.000000Z',effective)
            self.assertNotEqual(effective,registered)
            self.assertGreater(registered,effective)
            self.assertIsNone(c.execute("select 1 from authority_applicability_temporal where applicability_id=? and effective_from<=? and (terminal_effective_at is null or ?<terminal_effective_at)",(applicability.applicability_id,effective,effective)).fetchone())
        finally: c.close()

    def test_retroactive_guard_ignores_evaluation_from_different_context(self):
        bootstrap=FirstRealAPSBootstrap(self.repo).execute()
        measurement=ExplicitGovernedEntryService(self.repo).submit(bootstrap.point_id,'PH',7.2,datetime(2026,8,30,12,0,tzinfo=timezone.utc))
        evaluation=GovernedEvaluationService(self.repo,clock=lambda:datetime(2026,8,30,12,1,tzinfo=timezone.utc)).record(measurement.measurement_id,'NORMAL','Dentro','catalogo',datetime(2026,8,30,12,0,30,tzinfo=timezone.utc))
        applicability=self.service.create_applicability(self.authority.authority_id,1,'context-a','X',T0,'actor','create')
        self.service.revoke_applicability(applicability.applicability_id,T1,'actor','context-a terminal')
        c=self.repo._connect()
        try:
            self.assertIsNotNone(c.execute("select 1 from authority_applicability_event where applicability_id=? and event_type='REVOKED'",(applicability.applicability_id,)).fetchone())
            self.assertEqual(evaluation.evaluation_id,c.execute('select evaluation_id from governed_evaluation where evaluation_id=?',(evaluation.evaluation_id,)).fetchone()[0])
        finally: c.close()

    def test_retroactive_guard_ignores_evaluation_from_different_parameter(self):
        bootstrap=FirstRealAPSBootstrap(self.repo).execute()
        measurement=ExplicitGovernedEntryService(self.repo).submit(bootstrap.point_id,'PH',7.2,datetime(2026,8,30,12,0,tzinfo=timezone.utc))
        evaluation=GovernedEvaluationService(self.repo,clock=lambda:datetime(2026,8,30,12,1,tzinfo=timezone.utc)).record(measurement.measurement_id,'NORMAL','Dentro','catalogo',datetime(2026,8,30,12,0,30,tzinfo=timezone.utc))
        applicability=self.service.create_applicability(self.authority.authority_id,1,measurement.context_revision_id,'X',T0,'actor','create')
        self.service.revoke_applicability(applicability.applicability_id,T1,'actor','parameter-x terminal')
        c=self.repo._connect()
        try:
            self.assertIsNotNone(c.execute("select 1 from authority_applicability_event where applicability_id=? and event_type='REVOKED'",(applicability.applicability_id,)).fetchone())
            self.assertEqual(evaluation.evaluation_id,c.execute('select evaluation_id from governed_evaluation where evaluation_id=?',(evaluation.evaluation_id,)).fetchone()[0])
        finally: c.close()

    def test_retroactive_guard_ignores_evaluation_outside_affected_interval(self):
        bootstrap=FirstRealAPSBootstrap(self.repo).execute()
        measurement=ExplicitGovernedEntryService(self.repo).submit(bootstrap.point_id,'PH',7.2,datetime(2026,8,30,12,0,tzinfo=timezone.utc))
        evaluation=GovernedEvaluationService(self.repo,clock=lambda:datetime(2026,8,30,12,1,tzinfo=timezone.utc)).record(measurement.measurement_id,'NORMAL','Dentro','catalogo',datetime(2026,8,30,12,0,30,tzinfo=timezone.utc))
        applicability=self.service.create_applicability(self.authority.authority_id,1,measurement.context_revision_id,'PH',T0,'actor','create')
        self.service.revoke_applicability(applicability.applicability_id,T0,'actor','historical close')
        c=self.repo._connect()
        try:
            self.assertIsNotNone(c.execute("select 1 from authority_applicability_event where applicability_id=? and event_type='REVOKED'",(applicability.applicability_id,)).fetchone())
            self.assertEqual(evaluation.evaluation_id,c.execute('select evaluation_id from governed_evaluation where evaluation_id=?',(evaluation.evaluation_id,)).fetchone()[0])
        finally: c.close()

    def test_incomplete_applicability_linkage_fails_safe_without_event(self):
        with self.assertRaises(ValueError):
            self.service.create_applicability(self.authority.authority_id,1,'','PH',T0,'actor','incomplete')
        c=self.repo._connect()
        try:
            self.assertEqual(0,c.execute("select count(*) from authority_applicability").fetchone()[0])
            self.assertEqual(0,c.execute("select count(*) from authority_applicability_event").fetchone()[0])
        finally: c.close()

if __name__=='__main__': unittest.main()
