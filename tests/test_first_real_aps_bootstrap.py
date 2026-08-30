import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path

from governed_core.first_real_aps_bootstrap import (
    ACTOR_REFERENCE,
    APS_MEMBERS,
    AUTHORITY_LOCATORS,
    DISPLAY_NAME,
    EVIDENCE_LOCATOR,
    EXTERNAL_STATION_REFERENCE,
    FirstRealAPSBootstrap,
    PROJECT_REFERENCE,
)
from governed_core.repository import GovernedCoreRepository
from governed_core.services import PointContextService


class FirstRealAPSBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Path(self.temp_dir.name) / "core.sqlite3"
        self.repository = GovernedCoreRepository(self.database).initialize()
        self.bootstrap = FirstRealAPSBootstrap(self.repository)

    def tearDown(self):
        self.temp_dir.cleanup()

    def snapshot(self):
        with self.repository._optional_connection(None) as connection:
            tables = (
                "governed_monitoring_point",
                "point_context_revision",
                "authority_reference",
                "evidence_reference",
                "authorized_parameter_set",
                "aps_version",
                "aps_member",
                "authorization_basis",
                "basis_authority",
                "basis_evidence",
                "member_authorization_basis",
                "aps_applicability",
                "governance_event",
                "governed_measurement",
            )
            return {
                table: connection.execute(
                    f"SELECT * FROM {table} ORDER BY 1"
                ).fetchall()
                for table in tables
            }

    def test_run_two_resolves_exact_semantic_state_without_duplicates(self):
        first = self.bootstrap.execute()
        first_state = self.snapshot()
        second = self.bootstrap.execute()

        self.assertEqual(first, second)
        self.assertEqual(first_state, self.snapshot())
        self.assertEqual(
            EXTERNAL_STATION_REFERENCE,
            self.repository.fetch_point(first.point_id).external_station_reference,
        )
        self.assertNotEqual(EXTERNAL_STATION_REFERENCE, first.point_id)

    def test_exact_members_authorization_applicability_actor_and_zero_measurements(self):
        result = self.bootstrap.execute()
        with self.repository._optional_connection(None) as connection:
            members = {
                row[0]
                for row in connection.execute(
                    "SELECT parameter_reference FROM aps_member "
                    "WHERE set_id = ? AND version = ?",
                    (result.aps_reference.set_id, result.aps_reference.version),
                )
            }
            applicable = connection.execute(
                "SELECT context_revision_id, set_id, version FROM aps_applicability"
            ).fetchall()
            actors = {
                row[0]
                for row in connection.execute(
                    "SELECT actor_reference FROM governance_event"
                ).fetchall()
            }
            hashes = connection.execute(
                "SELECT content_hash FROM authority_reference "
                "UNION ALL SELECT content_hash FROM evidence_reference"
            ).fetchall()
            measurement_count = connection.execute(
                "SELECT COUNT(*) FROM governed_measurement"
            ).fetchone()[0]

        self.assertEqual(set(APS_MEMBERS), members)
        self.assertNotIn("BOD_5D_20C", members)
        self.assertEqual(
            [(result.context_revision_id, result.aps_reference.set_id, 1)],
            applicable,
        )
        self.assertEqual({ACTOR_REFERENCE}, actors)
        self.assertTrue(actors)
        self.assertTrue(all(row[0] is None for row in hashes))
        self.assertEqual(0, measurement_count)

        for member in APS_MEMBERS:
            resolution = self.repository.resolve_member_authorization(
                result.aps_reference, member
            )
            self.assertEqual(1, len(resolution.bases))
            basis = resolution.bases[0]
            with self.repository._optional_connection(None) as connection:
                authority_locators = {
                    row[0]
                    for row in connection.execute(
                        "SELECT locator FROM authority_reference WHERE "
                        "authority_reference_id IN ({})".format(
                            ",".join("?" * len(basis.authority_reference_ids))
                        ),
                        basis.authority_reference_ids,
                    )
                }
                evidence_locators = {
                    row[0]
                    for row in connection.execute(
                        "SELECT locator FROM evidence_reference WHERE "
                        "evidence_reference_id IN ({})".format(
                            ",".join("?" * len(basis.evidence_reference_ids))
                        ),
                        basis.evidence_reference_ids,
                    )
                }
            self.assertEqual(set(AUTHORITY_LOCATORS), authority_locators)
            self.assertEqual({EVIDENCE_LOCATOR}, evidence_locators)

    def test_each_injected_failure_rolls_back_all_bootstrap_state(self):
        stages = (
            "after_point",
            "after_authority",
            "during_aps",
            "during_applicability",
        )
        for stage in stages:
            with self.subTest(stage=stage):
                database = Path(self.temp_dir.name) / f"{stage}.sqlite3"
                repository = GovernedCoreRepository(database).initialize()
                bootstrap = FirstRealAPSBootstrap(repository)

                def fail(actual):
                    if actual == stage:
                        raise RuntimeError(stage)

                with self.assertRaisesRegex(RuntimeError, stage):
                    bootstrap.execute(failure_hook=fail)
                with repository._optional_connection(None) as connection:
                    counts = [
                        connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                        for table in (
                            "governed_monitoring_point",
                            "point_context_revision",
                            "authority_reference",
                            "evidence_reference",
                            "authorized_parameter_set",
                            "aps_version",
                            "aps_member",
                            "authorization_basis",
                            "aps_applicability",
                            "governance_event",
                            "governed_measurement",
                        )
                    ]
                self.assertEqual([0] * len(counts), counts)

    def test_external_reference_constraints_and_project_scope(self):
        points = PointContextService(self.repository)
        with self.assertRaises(ValueError):
            points.create_point_with_initial_context(
                "PROJECT", "Point", "ENVIRONMENTAL_CONDITION_MONITORING",
                "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR",
                external_station_reference=" ",
            )
        first = points.create_point_with_initial_context(
            "PROJECT_A", "First", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR",
            external_station_reference="STATION",
        )
        second = points.create_point_with_initial_context(
            "PROJECT_B", "Second", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR",
            external_station_reference="STATION",
        )
        self.assertNotEqual(first.point_id, second.point_id)
        with self.assertRaises(sqlite3.IntegrityError):
            points.create_point_with_initial_context(
                "PROJECT_A", "Duplicate", "ENVIRONMENTAL_CONDITION_MONITORING",
                "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR",
                external_station_reference="STATION",
            )

    def test_migration_preserves_existing_rows_and_adds_optional_identity(self):
        migration_dir = Path(self.temp_dir.name) / "migrations"
        migration_dir.mkdir()
        source = Path(__file__).resolve().parent.parent / "migrations"
        for number in ("001", "002", "003"):
            file = next(source.glob(f"{number}_*.sql"))
            shutil.copy(file, migration_dir / file.name)
        database = Path(self.temp_dir.name) / "legacy.sqlite3"
        repository = GovernedCoreRepository(database, migration_dir).initialize()
        legacy_point_id = "pnt_" + "1" * 32
        legacy_context_id = "ctx_" + "2" * 32
        with repository.transaction() as connection:
            connection.execute(
                "INSERT INTO governed_monitoring_point "
                "(point_id, project_reference, display_name, status) "
                "VALUES (?, 'LEGACY', 'Legacy', 'INACTIVE')",
                (legacy_point_id,),
            )
            connection.execute(
                "INSERT INTO point_context_revision "
                "(context_revision_id, point_id, revision, purpose, water_context, "
                "point_type, created_at) VALUES (?, ?, 1, "
                "'ENVIRONMENTAL_CONDITION_MONITORING', 'FLOWING_SURFACE_WATER', "
                "'GENERAL', '2026-01-01T00:00:00+00:00')",
                (legacy_context_id, legacy_point_id),
            )
            connection.execute(
                "UPDATE governed_monitoring_point SET status = 'ACTIVE', "
                "current_context_revision_id = ? WHERE point_id = ?",
                (legacy_context_id, legacy_point_id),
            )
        shutil.copy(source / "004_dfa02_external_station_identity.sql", migration_dir)
        repository.initialize()

        migrated = repository.fetch_point(legacy_point_id)
        self.assertEqual("Legacy", migrated.display_name)
        self.assertIsNone(migrated.external_station_reference)
        with repository._optional_connection(None) as connection:
            self.assertEqual(4, connection.execute("PRAGMA user_version").fetchone()[0])


if __name__ == "__main__":
    unittest.main()
