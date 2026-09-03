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
        self.authority=self.service.create_authority('urn:test','hash','ctx','p',T0, effective_at=T0, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME', effective_at_provenance='test:published')
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

    def test_effective_time_source_and_provenance_are_required(self):
        with self.assertRaises(ValueError):
            self.service.create_authority('urn:missing', 'hash', 'ctx', 'p', T0)
        with self.assertRaises(ValueError):
            self.service.activate(self.authority.authority_id, 1, 'actor', 'activate',
                                  effective_at=T1,
                                  effective_at_source='UNKNOWN',
                                  effective_at_provenance='test')

    def test_system_immediate_time_uses_trusted_clock(self):
        times = iter((T1, datetime(2026, 1, 1, 0, 0, 0, 1, tzinfo=timezone.utc)))
        service = AuthorityService(self.repo, clock=lambda: next(times))
        authority = service.create_authority(
            'urn:immediate', 'hash', 'ctx', 'immediate', T1,
            effective_at_source='SYSTEM_GENERATED_IMMEDIATE_TIME',
            effective_at_provenance='trusted-test-clock', immediate_effect=True,
        )
        with self.repo._optional_connection(None) as c:
            row = c.execute(
                "SELECT effective_at,effective_at_source,effective_at_provenance,registered_at "
                "FROM authority_event WHERE authority_id=?", (authority.authority_id,)
            ).fetchone()
        self.assertEqual('2027-01-01T00:00:00.000000Z', row[0])
        self.assertEqual('SYSTEM_GENERATED_IMMEDIATE_TIME', row[1])
        self.assertEqual('trusted-test-clock', row[2])
        self.assertNotEqual(row[0], row[3])

    def test_new_authority_event_rejects_noncanonical_and_equal_times(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as c:
                c.execute(
                    "INSERT INTO authority_event "
                    "(event_id,authority_id,authority_version,event_type,actor_reference,reason,"
                    "registered_at,effective_at,effective_at_source,effective_at_provenance) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?)",
                    ('bad-time', self.authority.authority_id, 1, 'ACTIVE', 'actor', 'bad',
                     '2026-01-01T00:00:00.000000Z', '2026-01-01T00:00:00Z',
                     'CALLER_SUPPLIED_EXPLICIT_TIME', 'test'),
                )
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as c:
                c.execute(
                    "INSERT INTO authority_event "
                    "(event_id,authority_id,authority_version,event_type,actor_reference,reason,"
                    "registered_at,effective_at,effective_at_source,effective_at_provenance) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?)",
                    ('duplicate-time', self.authority.authority_id, 1, 'PUBLISHED', 'actor', 'bad',
                     '2026-01-01T00:00:00.000001Z', T0.isoformat(timespec='microseconds').replace('+00:00','Z'),
                     'CALLER_SUPPLIED_EXPLICIT_TIME', 'test'),
                )

    def test_historical_authority_reconstructs_state_at_measured_at(self):
        self.service.activate(
            self.authority.authority_id, 1, 'actor', 'activate',
            effective_at=T1, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:active',
        )
        self.service.revoke(
            self.authority.authority_id, 1, 'actor', 'revoke',
            effective_at=T2, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:revoke',
        )
        before = self.service.resolve_historical_authority(
            self.authority.authority_id, 1, datetime(2025, 12, 31, tzinfo=timezone.utc), 'ctx', 'p'
        )
        at_publish = self.service.resolve_historical_authority(
            self.authority.authority_id, 1, T0, 'ctx', 'p'
        )
        between = self.service.resolve_historical_authority(
            self.authority.authority_id, 1, datetime(2026, 6, 1, tzinfo=timezone.utc), 'ctx', 'p'
        )
        at_active = self.service.resolve_historical_authority(
            self.authority.authority_id, 1, T1, 'ctx', 'p'
        )
        at_terminal = self.service.resolve_historical_authority(
            self.authority.authority_id, 1, T2, 'ctx', 'p'
        )
        self.assertEqual('UNDEFINED', before.state)
        self.assertEqual('PUBLISHED', at_publish.event.event_type)
        self.assertEqual('PUBLISHED', between.event.event_type)
        self.assertEqual('ACTIVE', at_active.event.event_type)
        self.assertEqual('REVOKED', at_terminal.event.event_type)

    def test_current_state_does_not_replace_historical_state(self):
        self.service.activate(
            self.authority.authority_id, 1, 'actor', 'activate',
            effective_at=T1, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:active',
        )
        self.service.revoke(
            self.authority.authority_id, 1, 'actor', 'revoke',
            effective_at=T2, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:revoke',
        )
        historical = self.service.resolve_historical_authority(
            self.authority.authority_id, 1, datetime(2027, 6, 1, tzinfo=timezone.utc), 'ctx', 'p'
        )
        self.assertEqual('ACTIVE', historical.event.event_type)

    def test_authority_boundary_blocks_out_of_window_resolution(self):
        authority = self.service.create_authority(
            'urn:bounded', 'hash', 'ctx', 'bounded', T0, T2,
            effective_at=T0, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:bounded',
        )
        result = self.service.resolve_historical_authority(
            authority.authority_id, 1, T2, 'ctx', 'bounded'
        )
        self.assertEqual('TECHNICALLY_INELIGIBLE', result.state)
        self.assertEqual('AUTHORITY_OUT_OF_WINDOW', result.reason)

    def test_authority_supersession_is_atomic_and_successor_is_not_active(self):
        self.service.activate(
            self.authority.authority_id, 1, 'actor', 'activate',
            effective_at=T1, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:active',
        )
        successor = self.service.supersede(
            self.authority.authority_id, 1, authority_id='successor',
            authority_version=2, effective_from=T2, effective_at=T2,
            effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:supersede', actor_reference='actor',
            reason='replace',
        )
        with self.repo._optional_connection(None) as c:
            predecessor_state = c.execute(
                "SELECT status FROM authority_state WHERE authority_id=? AND authority_version=1",
                (self.authority.authority_id,),
            ).fetchone()[0]
            successor_state = c.execute(
                "SELECT status FROM authority_state WHERE authority_id='successor' AND authority_version=2"
            ).fetchone()[0]
            linkage = c.execute(
                "SELECT successor_authority_id,successor_authority_version FROM authority_event "
                "WHERE authority_id=? AND event_type='SUPERSEDED'",
                (self.authority.authority_id,),
            ).fetchone()
        self.assertEqual('successor', successor.authority_id)
        self.assertEqual('SUPERSEDED', predecessor_state)
        self.assertEqual('PUBLISHED', successor_state)
        self.assertEqual(('successor', 2), linkage)

    def test_authority_supersession_failure_rolls_back_everything(self):
        self.service.activate(
            self.authority.authority_id, 1, 'actor', 'activate',
            effective_at=T1, effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
            effective_at_provenance='test:active',
        )
        for stage in ('before_successor_persistence', 'after_successor_published',
                      'before_predecessor_terminal_event'):
            def fail(current, expected=stage):
                if current == expected:
                    raise RuntimeError('forced authority supersession failure')
            self.service._test_supersession_failure_hook = fail
            with self.assertRaises(RuntimeError):
                self.service.supersede(
                    self.authority.authority_id, 1, authority_id='failed-' + stage,
                    authority_version=2, effective_from=T2, effective_at=T2,
                    effective_at_source='CALLER_SUPPLIED_EXPLICIT_TIME',
                    effective_at_provenance='test:failure', actor_reference='actor',
                    reason='replace',
                )
            with self.repo._optional_connection(None) as c:
                self.assertIsNone(c.execute(
                    "SELECT 1 FROM governed_authority WHERE authority_id=?", ('failed-' + stage,)
                ).fetchone())
                self.assertIsNone(c.execute(
                    "SELECT 1 FROM authority_event WHERE authority_id=? AND event_type='SUPERSEDED'",
                    (self.authority.authority_id,),
                ).fetchone())
                self.assertEqual('ACTIVE', c.execute(
                    "SELECT status FROM authority_state WHERE authority_id=? AND authority_version=1",
                    (self.authority.authority_id,),
                ).fetchone()[0])
            self.service._test_supersession_failure_hook = None

if __name__=='__main__': unittest.main()
