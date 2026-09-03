import math
import shutil
import sqlite3
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from governed_core.identifiers import IdentifierFactory
from governed_core.measurement_models import DataProvenance, GovernedMeasurementRequest
from governed_core.measurement_service import (
    GovernedMeasurementService,
    serialize_utc_instant,
)
from governed_core.repository import (
    GovernedConflictError,
    GovernedCoreRepository,
    GovernedReferenceError,
)
from governed_core.services import APSService, ApplicabilityService, PointContextService


TEST_ACTOR = "test-data:actor:wave-02a"
TEST_PROJECT = "test-data:project:wave-02a"
TEST_AUTHORITY = "test-data://authority/wave-02a"
TEST_EVIDENCE = "test-data://evidence/wave-02a"
TEST_PARAMETER = "test_parameter_ph"
FIXED_NOW = datetime(2026, 8, 29, 15, 30, 45, 123456, tzinfo=timezone.utc)
FIXED_MEASURED_AT = datetime(
    2026,
    8,
    29,
    12,
    15,
    30,
    654321,
    tzinfo=timezone(timedelta(hours=-3)),
)


class GovernedMeasurementTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.database_path = self.root / "test-data-governed-core.sqlite3"
        self.repository = GovernedCoreRepository(self.database_path).initialize()
        self.identifiers = IdentifierFactory()
        self.points = PointContextService(self.repository, self.identifiers)
        self.aps = APSService(self.repository, self.identifiers)
        self.applicability = ApplicabilityService(self.repository, self.identifiers)
        self.service = GovernedMeasurementService(
            self.repository,
            self.identifiers,
            clock=lambda: FIXED_NOW,
        )
        self.point = self._create_point()
        self.reference = self._create_aps(self.point.current_context_revision_id)
        self.applicability.assign(
            self.point.current_context_revision_id,
            self.reference,
            TEST_ACTOR,
        )
        self.applicability.assign_temporal(
            self.point.current_context_revision_id, self.reference,
            datetime(2020, 1, 1, tzinfo=timezone.utc), actor_reference=TEST_ACTOR,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_point(self, point_type="SPRING"):
        return self.points.create_point_with_initial_context(
            project_reference=TEST_PROJECT,
            display_name="TEST DATA - Wave 02A point",
            purpose="ENVIRONMENTAL_CONDITION_MONITORING",
            water_context="FLOWING_SURFACE_WATER",
            point_type=point_type,
            actor_reference=TEST_ACTOR,
            effective_from=datetime(2020, 1, 1, tzinfo=timezone.utc),
        )

    def _create_aps(self, context_revision_id, parameters=(TEST_PARAMETER,), set_id=None):
        authority_id = self.aps.register_authority_reference(TEST_AUTHORITY)
        evidence_id = self.aps.register_evidence_reference(TEST_EVIDENCE)
        basis = self.aps.make_basis(
            (authority_id,),
            (evidence_id,),
            parameters,
        )
        return self.aps.create_version(
            context_revision_id,
            parameters,
            (basis,),
            set_id=set_id,
        )

    def _request(self, **overrides):
        values = {
            "point_id": self.point.point_id,
            "parameter_reference": TEST_PARAMETER,
            "value": 7.25,
            "measured_at": FIXED_MEASURED_AT,
            "provenance": DataProvenance.MANUAL_ENTRY,
        }
        values.update(overrides)
        return GovernedMeasurementRequest(**values)

    def _count_measurements(self):
        with self.repository._optional_connection(None) as connection:
            return connection.execute(
                "SELECT COUNT(*) FROM governed_measurement"
            ).fetchone()[0]

    def _corrupt(self, statements):
        connection = sqlite3.connect(self.database_path)
        try:
            connection.execute("PRAGMA foreign_keys = OFF")
            for statement, parameters in statements:
                connection.execute(statement, parameters)
            connection.commit()
        finally:
            connection.close()

    def test_nominal_acceptance_persists_exact_governed_references(self):
        measurement = self.service.accept(self._request())

        self.assertEqual(self.point.point_id, measurement.point_id)
        self.assertEqual(self.point.current_context_revision_id, measurement.context_revision_id)
        self.assertEqual(self.reference.set_id, measurement.aps_set_id)
        self.assertEqual(self.reference.version, measurement.aps_version)
        self.assertEqual(TEST_PARAMETER, measurement.parameter_reference)
        self.assertNotIn("project", measurement.__dataclass_fields__)

    def test_measurement_identifier_uses_non_semantic_core_pattern(self):
        first = self.service.accept(self._request())
        second = self.service.accept(self._request())

        self.assertTrue(self.identifiers.validate("measurement", first.measurement_id))
        self.assertTrue(first.measurement_id.startswith("mea_"))
        self.assertNotEqual(first.measurement_id, second.measurement_id)

    def test_registered_at_is_system_assigned_and_measured_at_is_preserved(self):
        measurement = self.service.accept(self._request())

        self.assertEqual("2026-08-29T15:30:45.123456Z", measurement.registered_at)
        self.assertEqual("2026-08-29T15:15:30.654321Z", measurement.measured_at)

    def test_utc_serialization_is_deterministic_and_rejects_naive_time(self):
        self.assertEqual(
            "2026-08-29T15:15:30.654321Z",
            serialize_utc_instant(FIXED_MEASURED_AT),
        )
        with self.assertRaises(ValueError):
            serialize_utc_instant(datetime(2026, 8, 29, 12, 15, 30))

    def test_every_explicit_provenance_value_is_persisted(self):
        for provenance in DataProvenance:
            with self.subTest(provenance=provenance):
                measurement = self.service.accept(self._request(provenance=provenance))
                self.assertEqual(provenance.value, measurement.provenance)

    def test_invalid_or_missing_provenance_rolls_back(self):
        for provenance in (None, "", "INFER_FROM_UI"):
            with self.subTest(provenance=provenance):
                before = self._count_measurements()
                with self.assertRaises(ValueError):
                    self.service.accept(self._request(provenance=provenance))
                self.assertEqual(before, self._count_measurements())

    def test_unknown_provenance_must_be_explicit(self):
        measurement = self.service.accept(
            self._request(provenance=DataProvenance.UNKNOWN)
        )
        self.assertEqual("UNKNOWN", measurement.provenance)

    def test_value_accepts_only_finite_non_boolean_numeric(self):
        self.assertEqual(7.25, self.service.accept(self._request()).value)
        for invalid in (None, "7.25", True, math.nan, math.inf, -math.inf):
            with self.subTest(value=invalid):
                before = self._count_measurements()
                with self.assertRaises(ValueError):
                    self.service.accept(self._request(value=invalid))
                self.assertEqual(before, self._count_measurements())

    def test_missing_measured_at_rolls_back(self):
        with self.assertRaises(ValueError):
            self.service.accept(self._request(measured_at=None))
        self.assertEqual(0, self._count_measurements())

    def test_missing_point_fails_safe(self):
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request(point_id="pnt_missing"))
        self.assertEqual(0, self._count_measurements())

    def test_inactive_point_fails_at_operational_gate(self):
        self.points.update_status(self.point.point_id, "INACTIVE")
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())
        self.assertEqual(0, self._count_measurements())

    def test_missing_current_context_fails_safe(self):
        self._corrupt(
            [("UPDATE governed_monitoring_point SET current_context_revision_id = NULL", ())]
        )
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())

    def test_cross_point_context_fails_safe(self):
        other = self._create_point("WELL")
        self._corrupt(
            [(
                "UPDATE governed_monitoring_point SET current_context_revision_id = ? "
                "WHERE point_id = ?",
                (other.current_context_revision_id, self.point.point_id),
            )]
        )
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())

    def test_zero_applicability_fails_safe(self):
        self.applicability.remove(self.point.current_context_revision_id, TEST_ACTOR)
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())

    def test_multiple_applicability_fails_safe(self):
        second = self._create_aps(
            self.point.current_context_revision_id,
            set_id=self.reference.set_id,
        )
        self._corrupt(
            [
                ("DROP TABLE aps_applicability", ()),
                (
                    "CREATE TABLE aps_applicability "
                    "(context_revision_id TEXT, set_id TEXT, version INTEGER)",
                    (),
                ),
                (
                    "INSERT INTO aps_applicability VALUES (?, ?, ?)",
                    (self.point.current_context_revision_id, self.reference.set_id, self.reference.version),
                ),
                (
                    "INSERT INTO aps_applicability VALUES (?, ?, ?)",
                    (self.point.current_context_revision_id, second.set_id, second.version),
                ),
            ]
        )
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())

    def test_aps_context_mismatch_fails_safe(self):
        other = self._create_point("WELL")
        other_reference = self._create_aps(other.current_context_revision_id)
        self._corrupt(
            [
                ("DELETE FROM aps_applicability", ()),
                (
                    "INSERT INTO aps_applicability VALUES (?, ?, ?)",
                    (
                        self.point.current_context_revision_id,
                        other_reference.set_id,
                        other_reference.version,
                    ),
                ),
            ]
        )
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())

    def test_parameter_not_member_fails_safe(self):
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(
                self._request(parameter_reference="test_parameter_not_authorized")
            )

    def test_member_specific_resolution_returns_exact_basis_authority_and_evidence(self):
        resolution = self.repository.resolve_member_authorization(
            self.reference,
            TEST_PARAMETER,
        )
        self.assertEqual(self.reference, resolution.aps_reference)
        self.assertEqual(TEST_PARAMETER, resolution.parameter_reference)
        self.assertEqual(1, len(resolution.bases))
        self.assertEqual(1, len(resolution.bases[0].authority_reference_ids))
        self.assertEqual(1, len(resolution.bases[0].evidence_reference_ids))

    def test_missing_member_basis_fails_safe(self):
        self._corrupt(
            [
                ("DROP TRIGGER member_authorization_basis_immutable_delete", ()),
                ("DELETE FROM member_authorization_basis", ()),
            ]
        )
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())

    def test_cross_version_basis_fails_safe(self):
        second = self._create_aps(
            self.point.current_context_revision_id,
            set_id=self.reference.set_id,
        )
        with self.repository._optional_connection(None) as connection:
            second_basis = connection.execute(
                "SELECT basis_id FROM authorization_basis WHERE set_id = ? AND version = ?",
                (second.set_id, second.version),
            ).fetchone()[0]
        self._corrupt(
            [
                ("DROP TRIGGER member_authorization_basis_immutable_update", ()),
                (
                    "UPDATE member_authorization_basis SET basis_id = ? "
                    "WHERE set_id = ? AND version = ?",
                    (second_basis, self.reference.set_id, self.reference.version),
                ),
            ]
        )
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())

    def test_missing_authority_or_evidence_fails_safe(self):
        cases = (
            ("basis_authority_immutable_delete", "basis_authority"),
            ("basis_evidence_immutable_delete", "basis_evidence"),
        )
        for trigger, table in cases:
            with self.subTest(table=table):
                isolated_path = self.root / f"test-data-{table}.sqlite3"
                shutil.copy2(self.database_path, isolated_path)
                repository = GovernedCoreRepository(isolated_path)
                service = GovernedMeasurementService(repository, clock=lambda: FIXED_NOW)
                connection = sqlite3.connect(isolated_path)
                try:
                    connection.execute(f"DROP TRIGGER {trigger}")
                    connection.execute(f"DELETE FROM {table}")
                    connection.commit()
                finally:
                    connection.close()
                with self.assertRaises(GovernedReferenceError):
                    service.accept(self._request())

    def test_unresolved_disqualification_and_exact_requalification(self):
        first = self.applicability.disqualify(self.reference, TEST_ACTOR)
        second = self.applicability.disqualify(self.reference, TEST_ACTOR)
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())
        self.applicability.requalify(self.reference, (first,), TEST_ACTOR)
        with self.assertRaises(GovernedReferenceError):
            self.service.accept(self._request())
        self.applicability.requalify(self.reference, (second,), TEST_ACTOR)
        self.assertEqual(TEST_PARAMETER, self.service.accept(self._request()).parameter_reference)

    def test_measurement_update_and_delete_are_blocked(self):
        measurement = self.service.accept(self._request())
        for statement in (
            "UPDATE governed_measurement SET value = 8 WHERE measurement_id = ?",
            "DELETE FROM governed_measurement WHERE measurement_id = ?",
        ):
            with self.subTest(statement=statement):
                with self.assertRaises(sqlite3.IntegrityError):
                    with self.repository.transaction() as connection:
                        connection.execute(statement, (measurement.measurement_id,))

    def test_registered_at_is_immutable(self):
        measurement = self.service.accept(self._request())
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repository.transaction() as connection:
                connection.execute(
                    "UPDATE governed_measurement SET registered_at = ? WHERE measurement_id = ?",
                    ("2027-01-01T00:00:00.000000Z", measurement.measurement_id),
                )

    def test_authorization_history_links_are_immutable(self):
        for table in (
            "authority_reference",
            "evidence_reference",
            "basis_authority",
            "basis_evidence",
            "member_authorization_basis",
        ):
            with self.subTest(table=table):
                with self.assertRaises(sqlite3.IntegrityError):
                    with self.repository.transaction() as connection:
                        connection.execute(f"DELETE FROM {table}")

    def test_no_csv_write_or_legacy_history_change(self):
        legacy = self.root / "test-data-legacy.csv"
        original = b"timestamp,ph\nlegacy,7.0\n"
        legacy.write_bytes(original)
        self.service.accept(self._request())
        self.assertEqual(original, legacy.read_bytes())
        self.assertEqual([], list(self.root.glob("*measurements*.csv")))

    def test_schema_has_no_aps_status_or_eligibility_boolean(self):
        with self.repository._optional_connection(None) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            columns = {
                row[1]
                for row in connection.execute("PRAGMA table_info(governed_measurement)")
            }
        self.assertNotIn("eligibility_relation", tables)
        self.assertNotIn("eligible", columns)
        self.assertNotIn("aps_status", columns)


class GovernedMeasurementMigrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.source_migrations = Path(__file__).resolve().parent.parent / "migrations"

    def tearDown(self):
        self.temp_dir.cleanup()

    def _copy_migration(self, name, target):
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.source_migrations / name, target / name)

    def test_empty_database_applies_001_002_003_without_bootstrap(self):
        database = self.root / "test-data-empty.sqlite3"
        repository = GovernedCoreRepository(database).initialize()
        with repository._optional_connection(None) as connection:
            self.assertEqual(17, connection.execute("PRAGMA user_version").fetchone()[0])
            self.assertEqual(0, connection.execute("SELECT COUNT(*) FROM governed_measurement").fetchone()[0])
            self.assertEqual(0, connection.execute("SELECT COUNT(*) FROM governed_monitoring_point").fetchone()[0])

    def test_fresh_bootstrap_reaches_historical_temporal_extension(self):
        database = self.root / "test-data-fresh-017.sqlite3"
        repository = GovernedCoreRepository(database).initialize()
        with repository._optional_connection(None) as connection:
            self.assertEqual(17, connection.execute("PRAGMA user_version").fetchone()[0])
            columns = {row[1] for row in connection.execute("PRAGMA table_info(authority_event)")}
        self.assertIn("effective_at", columns)
        self.assertIn("effective_at_source", columns)
        self.assertIn("effective_at_provenance", columns)

    def test_persisted_016_database_upgrades_to_017_without_backfill(self):
        migrations = self.root / "test-data-016-to-017"
        migrations.mkdir()
        for source in self.source_migrations.glob("*.sql"):
            if source.name.startswith("017_"):
                continue
            shutil.copy2(source, migrations / source.name)
        database = self.root / "test-data-upgrade-017.sqlite3"
        GovernedCoreRepository(database, migrations).initialize()
        connection = sqlite3.connect(database)
        try:
            connection.execute(
                "INSERT INTO governed_authority VALUES (?,?,?,?,?)",
                ("legacy", 1, "urn:legacy", "hash", "2026-01-01T00:00:00.000000Z"),
            )
            connection.execute(
                "INSERT INTO authority_scope VALUES (?,?,?,?)",
                ("legacy", 1, "ctx", "parameter"),
            )
            connection.execute(
                "INSERT INTO authority_state VALUES (?,?,?,?,?)",
                ("legacy", 1, "PUBLISHED", "2026-01-01T00:00:00.000000Z", "event-legacy"),
            )
            connection.execute(
                "INSERT INTO authority_temporal_boundary VALUES (?,?,?,?)",
                ("legacy", 1, "2026-01-01T00:00:00.000000Z", None),
            )
            connection.execute(
                "INSERT INTO authority_event VALUES (?,?,?,?,?,?,?,?,?)",
                ("event-legacy", "legacy", 1, "PUBLISHED", "actor", "legacy", None, None,
                 "2026-01-01T00:00:00.000000Z"),
            )
            connection.commit()
        finally:
            connection.close()
        self._copy_migration("017_mcm_wq_historical_authority_temporal_extension.sql", migrations)
        repository = GovernedCoreRepository(database, migrations).initialize()
        with repository._optional_connection(None) as connection:
            self.assertEqual(17, connection.execute("PRAGMA user_version").fetchone()[0])
            row = connection.execute(
                "SELECT effective_at,effective_at_source,effective_at_provenance "
                "FROM authority_event WHERE event_id='event-legacy'"
            ).fetchone()
        self.assertEqual((None, None, None), tuple(row))

    def test_wave_01_database_upgrades_only_with_003(self):
        migrations = self.root / "test-data-migrations"
        self._copy_migration("001_dfa02_core_v1.sql", migrations)
        self._copy_migration("002_dfa02_core_v1_guards.sql", migrations)
        database = self.root / "test-data-wave-01.sqlite3"
        GovernedCoreRepository(database, migrations).initialize()
        self._copy_migration("003_dfa02_governed_measurement.sql", migrations)
        repository = GovernedCoreRepository(database, migrations).initialize()
        with repository._optional_connection(None) as connection:
            applied = connection.execute(
                "SELECT migration_id FROM schema_migration ORDER BY migration_id"
            ).fetchall()
        self.assertEqual(
            [
                ("001_dfa02_core_v1.sql",),
                ("002_dfa02_core_v1_guards.sql",),
                ("003_dfa02_governed_measurement.sql",),
            ],
            applied,
        )

    def test_checksum_divergence_fails_safe(self):
        migrations = self.root / "test-data-migrations"
        migrations.mkdir(exist_ok=True)
        for source in self.source_migrations.glob("*.sql"):
            shutil.copy2(source, migrations / source.name)
        database = self.root / "test-data-checksum.sqlite3"
        GovernedCoreRepository(database, migrations).initialize()
        migration = migrations / "003_dfa02_governed_measurement.sql"
        migration.write_text(migration.read_text(encoding="utf-8") + "\n-- changed\n", encoding="utf-8")
        with self.assertRaises(GovernedConflictError):
            GovernedCoreRepository(database, migrations).initialize()

    def test_failed_migration_rolls_back_schema_and_registration_atomically(self):
        migrations = self.root / "test-data-migrations"
        self._copy_migration("001_dfa02_core_v1.sql", migrations)
        self._copy_migration("002_dfa02_core_v1_guards.sql", migrations)
        failing = migrations / "003_test-data_failure.sql"
        failing.write_text(
            "CREATE TABLE test_data_partial(id TEXT);\n"
            "THIS IS NOT VALID SQL;\n",
            encoding="utf-8",
        )
        database = self.root / "test-data-failure.sqlite3"
        with self.assertRaises(sqlite3.Error):
            GovernedCoreRepository(database, migrations).initialize()
        connection = sqlite3.connect(database)
        try:
            partial = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE name = 'test_data_partial'"
            ).fetchone()
            registered = connection.execute(
                "SELECT 1 FROM schema_migration WHERE migration_id = ?",
                (failing.name,),
            ).fetchone()
        finally:
            connection.close()
        self.assertIsNone(partial)
        self.assertIsNone(registered)


if __name__ == "__main__":
    unittest.main()
