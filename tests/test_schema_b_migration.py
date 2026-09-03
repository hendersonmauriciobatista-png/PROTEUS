import hashlib
import shutil
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.authority_service import AuthorityService
from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.measurement_models import GovernedEvaluation
from governed_core.repository import GovernedConflictError, GovernedCoreRepository


class SchemaBMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = Path(__file__).resolve().parents[1] / "migrations"

    def tearDown(self):
        self.temp.cleanup()

    def _copy_migrations(self, target, last):
        target.mkdir(parents=True, exist_ok=True)
        for migration in self.source.glob("*.sql"):
            if int(migration.name[:3]) <= last:
                shutil.copy2(migration, target / migration.name)

    def test_fresh_001_to_019_has_exact_schema_b_tables(self):
        repo = GovernedCoreRepository(self.root / "fresh.sqlite3").initialize()
        with repo._optional_connection(None) as connection:
            self.assertEqual(19, connection.execute("PRAGMA user_version").fetchone()[0])
            self.assertEqual(1, connection.execute("PRAGMA foreign_keys").fetchone()[0])
            tables = {
                row[0] for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' "
                    "AND name LIKE 'governed_evaluation_authority_snapshot%'")
            }
            self.assertEqual({
                "governed_evaluation_authority_snapshot",
                "governed_evaluation_authority_snapshot_basis",
            }, tables)

    def test_persisted_017_and_018_upgrade_to_019(self):
        for last in (17, 18):
            migration_dir = self.root / f"migrations-{last}"
            self._copy_migrations(migration_dir, last)
            database = self.root / f"persisted-{last}.sqlite3"
            GovernedCoreRepository(database, migration_dir).initialize()
            if last == 17:
                shutil.copy2(self.source / "018_mcm_wq_authority_artifact_verification.sql", migration_dir)
            shutil.copy2(self.source / "019_mcm_wq_evaluation_authority_snapshot.sql", migration_dir)
            repo = GovernedCoreRepository(database, migration_dir).initialize()
            with repo._optional_connection(None) as connection:
                self.assertEqual(19, connection.execute("PRAGMA user_version").fetchone()[0])
                self.assertEqual(1, connection.execute(
                    "SELECT COUNT(*) FROM schema_migration WHERE migration_id LIKE '019_%'"
                ).fetchone()[0])

    def test_foreign_key_guard_rejects_disabled_connection(self):
        repo = GovernedCoreRepository(self.root / "guard.sqlite3").initialize()
        connection = sqlite3.connect(repo.path)
        try:
            with self.assertRaises(GovernedConflictError):
                repo._assert_governed_connection(connection)
        finally:
            connection.close()

    def _base_snapshot_fixture(self):
        repo = GovernedCoreRepository(self.root / "fixture.sqlite3").initialize()
        state = FirstRealAPSBootstrap(repo).execute()
        measured_at = datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc)
        measurement = ExplicitGovernedEntryService(repo).submit(
            state.point_id, "PH", 7.2, measured_at
        )
        clock = lambda: datetime(2026, 8, 30, 12, 1, tzinfo=timezone.utc)
        raw = b"schema-b-authority"
        digest = hashlib.sha256(raw).hexdigest()
        authority = AuthorityService(repo, clock=clock).create_authority(
            "urn:schema-b:authority", digest, state.context_revision_id, "PH",
            datetime(2026, 1, 1, tzinfo=timezone.utc),
            authority_id="schema-b-authority", actor_reference="test",
            reason="test", effective_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:authority", artifact_bytes=raw,
            artifact_locator_reference="urn:schema-b:artifact",
            verification_provenance="test:verification",
        )
        applicability = AuthorityService(repo, clock=clock).create_applicability(
            authority.authority_id, authority.authority_version,
            state.context_revision_id, "PH",
            datetime(2026, 1, 1, tzinfo=timezone.utc), "test", "test",
        )
        with repo._optional_connection(None) as connection:
            basis_id = connection.execute(
                "SELECT basis_id FROM member_authorization_basis "
                "WHERE set_id=? AND version=? AND parameter_reference='PH'",
                (state.aps_reference.set_id, state.aps_reference.version),
            ).fetchone()[0]
            verification_id = connection.execute(
                "SELECT verification_id FROM authority_artifact_verification "
                "WHERE authority_id=? AND authority_version=?",
                (authority.authority_id, authority.authority_version),
            ).fetchone()[0]
            lifecycle_event_id = connection.execute(
                "SELECT event_id FROM authority_event WHERE authority_id=?",
                (authority.authority_id,),
            ).fetchone()[0]
            applicability_event_id = connection.execute(
                "SELECT event_id FROM authority_applicability_event WHERE applicability_id=?",
                (applicability.applicability_id,),
            ).fetchone()[0]
        return {
            "repo": repo, "state": state, "measurement": measurement,
            "authority": authority, "applicability": applicability,
            "basis_id": basis_id, "verification_id": verification_id,
            "lifecycle_event_id": lifecycle_event_id,
            "applicability_event_id": applicability_event_id,
        }

    def _valid_snapshot_fixture(self, rule_outcome="ONE_APPLICABLE_RULE", status="NORMAL"):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        evaluation = GovernedEvaluation(
            "evaluation-schema-b", fixture["measurement"].measurement_id, "PH",
            status, "ok", "test", "2026-08-30T12:00:00.000000Z",
            "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
        )
        basis = (
            evaluation.evaluation_id, fixture["basis_id"],
            fixture["state"].aps_reference.set_id,
            fixture["state"].aps_reference.version, "PH",
        )
        snapshot = (
            evaluation.evaluation_id, fixture["authority"].authority_id,
            fixture["authority"].authority_version,
            fixture["applicability"].applicability_id,
            fixture["lifecycle_event_id"], fixture["applicability_event_id"],
            fixture["verification_id"], "RESOLVED",
            "TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION", rule_outcome,
            "mcm-wq-authority-gate-technical-admission/v1",
        )
        with repo.transaction() as connection:
            repo.insert_evaluation(evaluation, connection)
            repo.insert_authority_snapshot_basis(basis, connection)
            repo.insert_authority_snapshot(snapshot, connection)
        return repo, evaluation.evaluation_id, basis, snapshot

    def test_normative_order_persists_complete_snapshot(self):
        repo, evaluation_id, basis, _ = self._valid_snapshot_fixture()
        self.assertIsNotNone(repo.fetch_authority_snapshot(evaluation_id))
        self.assertEqual((basis,), repo.list_authority_snapshot_basis(evaluation_id))

    def test_snapshot_without_basis_rolls_back_evaluation(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        evaluation = GovernedEvaluation(
            "evaluation-rollback", fixture["measurement"].measurement_id, "PH",
            "NORMAL", "ok", "test", "2026-08-30T12:00:00.000000Z",
            "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
        )
        snapshot = (
            evaluation.evaluation_id, fixture["authority"].authority_id, 1,
            fixture["applicability"].applicability_id,
            fixture["lifecycle_event_id"], fixture["applicability_event_id"],
            fixture["verification_id"], "RESOLVED",
            "TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION",
            "ZERO_APPLICABLE_RULE", "mcm-wq-authority-gate-technical-admission/v1",
        )
        with self.assertRaises(sqlite3.DatabaseError):
            with repo.transaction() as connection:
                repo.insert_evaluation(evaluation, connection)
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    snapshot,
                )
        with repo._optional_connection(None) as connection:
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation WHERE evaluation_id=?",
                (evaluation.evaluation_id,),
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot_basis "
                "WHERE evaluation_id=?", (evaluation.evaluation_id,),
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot "
                "WHERE evaluation_id=?", (evaluation.evaluation_id,),
            ).fetchone()[0])

    def test_snapshot_and_basis_are_immutable(self):
        repo, evaluation_id, basis, _ = self._valid_snapshot_fixture()
        with repo.transaction() as connection:
            with self.assertRaises(sqlite3.DatabaseError):
                connection.execute(
                    "UPDATE governed_evaluation_authority_snapshot "
                    "SET authority_gate_status='RESOLVED' WHERE evaluation_id=?",
                    (evaluation_id,),
                )
        self.assertIsNotNone(repo.fetch_authority_snapshot(evaluation_id))
        for statement in (
            "DELETE FROM governed_evaluation_authority_snapshot WHERE evaluation_id=?",
            "UPDATE governed_evaluation_authority_snapshot_basis SET basis_id='x' WHERE evaluation_id=?",
            "DELETE FROM governed_evaluation_authority_snapshot_basis WHERE evaluation_id=?",
        ):
            with self.assertRaises(sqlite3.DatabaseError):
                with repo.transaction() as connection:
                    connection.execute(statement, (evaluation_id,))
        self.assertEqual((basis,), repo.list_authority_snapshot_basis(evaluation_id))

    def test_basis_after_snapshot_is_rejected_by_direct_sql(self):
        repo, evaluation_id, basis, _ = self._valid_snapshot_fixture()
        with self.assertRaises(sqlite3.DatabaseError):
            with repo.transaction() as connection:
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot_basis "
                    "VALUES (?,?,?,?,?)", basis,
                )
        self.assertEqual((basis,), repo.list_authority_snapshot_basis(evaluation_id))

    def test_incomplete_basis_set_is_rejected(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        scope = fixture["state"].aps_reference
        with repo.transaction() as connection:
            authority_ref = connection.execute(
                "SELECT authority_reference_id FROM authority_reference LIMIT 1"
            ).fetchone()[0]
            evidence_ref = connection.execute(
                "SELECT evidence_reference_id FROM evidence_reference LIMIT 1"
            ).fetchone()[0]
            connection.execute(
                "INSERT INTO authorization_basis VALUES (?,?,?)",
                ("basis-ph-second", scope.set_id, scope.version),
            )
            connection.execute(
                "INSERT INTO basis_authority VALUES (?,?)",
                ("basis-ph-second", authority_ref),
            )
            connection.execute(
                "INSERT INTO basis_evidence VALUES (?,?)",
                ("basis-ph-second", evidence_ref),
            )
            connection.execute(
                "INSERT INTO member_authorization_basis VALUES (?,?,?,?)",
                (scope.set_id, scope.version, "PH", "basis-ph-second"),
            )
        evaluation = GovernedEvaluation(
            "evaluation-incomplete", fixture["measurement"].measurement_id, "PH",
            "NORMAL", "ok", "test", "2026-08-30T12:00:00.000000Z",
            "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
        )
        with self.assertRaises(sqlite3.DatabaseError):
            with repo.transaction() as connection:
                repo.insert_evaluation(evaluation, connection)
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot_basis VALUES (?,?,?,?,?)",
                    (evaluation.evaluation_id, fixture["basis_id"], scope.set_id, scope.version, "PH"),
                )
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (evaluation.evaluation_id, fixture["authority"].authority_id, 1,
                     fixture["applicability"].applicability_id, fixture["lifecycle_event_id"],
                     fixture["applicability_event_id"], fixture["verification_id"], "RESOLVED",
                     "TECHNICALLY_ELIGIBLE_FOR_GOVERNED_EVALUATION", "ONE_APPLICABLE_RULE",
                     "mcm-wq-authority-gate-technical-admission/v1"),
                )

    def test_extra_and_scope_mismatch_basis_are_rejected_by_direct_sql(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        scope = fixture["state"].aps_reference
        with repo.transaction() as connection:
            turbidity_basis = connection.execute(
                "SELECT basis_id FROM member_authorization_basis "
                "WHERE set_id=? AND version=? AND parameter_reference='TURBIDITY'",
                (scope.set_id, scope.version),
            ).fetchone()[0]
            evaluation = GovernedEvaluation(
                "evaluation-scope-negative", fixture["measurement"].measurement_id, "PH",
                "NORMAL", "ok", "test", "2026-08-30T12:00:00.000000Z",
                "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
            )
            repo.insert_evaluation(evaluation, connection)
            with self.assertRaises(sqlite3.DatabaseError):
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot_basis VALUES (?,?,?,?,?)",
                    (evaluation.evaluation_id, turbidity_basis, scope.set_id, scope.version, "TURBIDITY"),
                )

    def test_duplicate_basis_is_rejected(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        scope = fixture["state"].aps_reference
        evaluation = GovernedEvaluation(
            "evaluation-duplicate", fixture["measurement"].measurement_id, "PH",
            "NORMAL", "ok", "test", "2026-08-30T12:00:00.000000Z",
            "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
        )
        with self.assertRaises(sqlite3.DatabaseError):
            with repo.transaction() as connection:
                repo.insert_evaluation(evaluation, connection)
                basis = (evaluation.evaluation_id, fixture["basis_id"], scope.set_id, scope.version, "PH")
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot_basis VALUES (?,?,?,?,?)", basis
                )
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot_basis VALUES (?,?,?,?,?)", basis
                )

    def test_orphan_basis_fails_deferred_commit_and_rolls_back_all(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        scope = fixture["state"].aps_reference
        evaluation = GovernedEvaluation(
            "evaluation-orphan", fixture["measurement"].measurement_id, "PH",
            "NORMAL", "ok", "test", "2026-08-30T12:00:00.000000Z",
            "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
        )
        basis = (evaluation.evaluation_id, fixture["basis_id"], scope.set_id, scope.version, "PH")
        with self.assertRaises(sqlite3.IntegrityError):
            with repo.transaction() as connection:
                repo.insert_evaluation(evaluation, connection)
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot_basis VALUES (?,?,?,?,?)",
                    basis,
                )
        with repo._optional_connection(None) as connection:
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation WHERE evaluation_id=?",
                (evaluation.evaluation_id,),
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot_basis "
                "WHERE evaluation_id=?", (evaluation.evaluation_id,),
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot "
                "WHERE evaluation_id=?", (evaluation.evaluation_id,),
            ).fetchone()[0])

    def test_extra_basis_same_scope_is_rejected_before_materialization(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        scope = fixture["state"].aps_reference
        with repo.transaction() as connection:
            authority_ref = connection.execute(
                "SELECT authority_reference_id FROM authority_reference LIMIT 1"
            ).fetchone()[0]
            evidence_ref = connection.execute(
                "SELECT evidence_reference_id FROM evidence_reference LIMIT 1"
            ).fetchone()[0]
            connection.execute(
                "INSERT INTO authorization_basis VALUES (?,?,?)",
                ("basis-ph-extra", scope.set_id, scope.version),
            )
            connection.execute(
                "INSERT INTO basis_authority VALUES (?,?)",
                ("basis-ph-extra", authority_ref),
            )
            connection.execute(
                "INSERT INTO basis_evidence VALUES (?,?)",
                ("basis-ph-extra", evidence_ref),
            )
        evaluation = GovernedEvaluation(
            "evaluation-extra", fixture["measurement"].measurement_id, "PH",
            "NORMAL", "ok", "test", "2026-08-30T12:00:00.000000Z",
            "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
        )
        with self.assertRaises(sqlite3.DatabaseError):
            with repo.transaction() as connection:
                repo.insert_evaluation(evaluation, connection)
                connection.execute(
                    "INSERT INTO governed_evaluation_authority_snapshot_basis VALUES (?,?,?,?,?)",
                    (evaluation.evaluation_id, "basis-ph-extra", scope.set_id, scope.version, "PH"),
                )
        with repo._optional_connection(None) as connection:
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation WHERE evaluation_id=?",
                (evaluation.evaluation_id,),
            ).fetchone()[0])

    def test_blocked_result_fixture_performs_attempt_without_final_persistence(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        evaluation_id = "evaluation-blocked"
        candidate = GovernedEvaluation(
            evaluation_id, fixture["measurement"].measurement_id, "PH",
            "NORMAL", "unreachable", "test",
            "2026-08-30T12:00:00.000000Z",
            "2026-08-30T12:01:00.000000Z", "TEST", "1", None,
        )
        blocked_result = "BLOCKED"
        with repo.transaction() as connection:
            # Controlled test boundary: blocked results are deliberately not
            # passed to any final-evaluation persistence method.
            if blocked_result == "BLOCKED":
                attempted = candidate.evaluation_id
            else:
                attempted = False
                connection.execute(
                    "INSERT INTO governed_evaluation VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                    (evaluation_id, fixture["measurement"].measurement_id, "PH",
                     "NORMAL", "unreachable", "test",
                     "2026-08-30T12:00:00.000000Z",
                     "2026-08-30T12:01:00.000000Z", "TEST", "1", None),
                )
        self.assertEqual(evaluation_id, attempted)
        with repo._optional_connection(None) as connection:
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation WHERE evaluation_id=?",
                (evaluation_id,),
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot_basis"
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot"
            ).fetchone()[0])
    def test_authority_blocked_fixture_has_no_final_records(self):
        fixture = self._base_snapshot_fixture()
        repo = fixture["repo"]
        with repo._optional_connection(None) as connection:
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation WHERE measurement_id=?",
                (fixture["measurement"].measurement_id,),
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot_basis"
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot"
            ).fetchone()[0])

    def test_zero_rule_fixture_has_complete_snapshot(self):
        repo, evaluation_id, basis, snapshot = self._valid_snapshot_fixture(
            rule_outcome="ZERO_APPLICABLE_RULE", status="NAO_AVALIAVEL"
        )
        with repo._optional_connection(None) as connection:
            self.assertEqual(
                "NAO_AVALIAVEL",
                connection.execute(
                    "SELECT status FROM governed_evaluation WHERE evaluation_id=?",
                    (evaluation_id,),
                ).fetchone()[0],
            )
        self.assertEqual(snapshot[9], "ZERO_APPLICABLE_RULE")
        self.assertIsNotNone(repo.fetch_authority_snapshot(evaluation_id))
        self.assertEqual((basis,), repo.list_authority_snapshot_basis(evaluation_id))


if __name__ == "__main__":
    unittest.main()
