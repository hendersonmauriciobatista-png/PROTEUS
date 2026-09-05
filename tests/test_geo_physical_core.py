import os
import shutil
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from pyproj import Transformer
from pyproj.exceptions import ProjError
from pyproj.network import is_network_enabled, set_network_enabled

import governed_core.geo_crs as geo_crs
from governed_core.geo_crs import CRSResolver, CoordinateTransformer
from governed_core.geo_models import GeoAvailabilityState, LocationProvenance, SourceAxisOrder
from governed_core.geo_service import GeoReferenceResolutionError, GeoService
from governed_core.identifiers import IdentifierFactory
from governed_core.repository import GovernedConflictError, GovernedCoreRepository
from governed_core.services import PointContextService
from governed_core.temporal_state import TemporalStateService


class GeoPhysicalCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = GovernedCoreRepository(Path(self.temp.name) / "geo.sqlite3").initialize()
        self.points = PointContextService(self.repo, IdentifierFactory())
        self.geo = GeoService(self.repo, IdentifierFactory())

    def tearDown(self):
        self.temp.cleanup()

    def _point(self, **kwargs):
        return self.points.create_point_with_initial_context(
            "geo-project", kwargs.pop("name", "GEO point"),
            "ENVIRONMENTAL_CONDITION_MONITORING", "FLOWING_SURFACE_WATER", "GENERAL",
            "ACTOR", effective_from=datetime(2020, 1, 1, tzinfo=timezone.utc), **kwargs
        )

    def _provenance(self, provenance_id="prv-test", latitude=20.0, longitude=-40.0):
        return LocationProvenance(
            provenance_id, "survey://one", str(latitude), str(longitude), latitude, longitude,
            SourceAxisOrder.LATITUDE_LONGITUDE.value, "EPSG:4326", "GPS",
            "2020-01-01T00:00:00.000000Z", "KNOWN", None, None, None,
            None, None, None, "2020-01-01T00:00:00.000000Z",
        )

    def _available_data(self, provenance_id="prv-test", latitude=20.0, longitude=-40.0):
        return {
            "availability_state": GeoAvailabilityState.AVAILABLE.value,
            "latitude": latitude,
            "longitude": longitude,
            "crs_identifier": "EPSG:4326",
            "location_provenance_id": provenance_id,
            "provenance": self._provenance(provenance_id, latitude, longitude),
        }

    def test_fresh_migration_creates_normalized_tables_and_no_legacy_rows(self):
        with self.repo._optional_connection(None) as cx:
            self.assertEqual(1, cx.execute("SELECT COUNT(*) FROM schema_migration WHERE migration_id LIKE '020_%'").fetchone()[0])
            self.assertEqual(0, cx.execute("SELECT COUNT(*) FROM geo_reference").fetchone()[0])
            self.assertEqual(0, cx.execute("SELECT COUNT(*) FROM location_provenance").fetchone()[0])

    def test_persisted_legacy_database_is_classified_without_backfill(self):
        legacy_dir = Path(self.temp.name) / "legacy-migrations"
        legacy_dir.mkdir()
        source = Path(__file__).resolve().parents[1] / "migrations"
        for migration in source.glob("*.sql"):
            if int(migration.name[:3]) <= 19:
                shutil.copy2(migration, legacy_dir / migration.name)
        database = Path(self.temp.name) / "legacy.sqlite3"
        legacy_repo = GovernedCoreRepository(database, legacy_dir).initialize()
        legacy_point = PointContextService(legacy_repo).create_point_with_initial_context(
            "legacy", "Legacy", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR", geo_reference="opaque-bytes"
        )
        GovernedCoreRepository(database).initialize()
        geo = GovernedCoreRepository(database).fetch_geo_reference(legacy_point.current_context_revision_id)
        self.assertEqual(GeoAvailabilityState.LEGACY_UNCLASSIFIED.value, geo.availability_state)
        cx = sqlite3.connect(database)
        try:
            self.assertEqual("opaque-bytes", cx.execute(
                "SELECT geo_reference FROM point_context_revision WHERE context_revision_id=?",
                (legacy_point.current_context_revision_id,),
            ).fetchone()[0])
        finally:
            cx.close()

    def test_migration_020_failure_rolls_back_schema_and_registration(self):
        migration_dir = Path(self.temp.name) / "failing-migrations"
        migration_dir.mkdir()
        source = Path(__file__).resolve().parents[1] / "migrations"
        for migration in source.glob("*.sql"):
            shutil.copy2(migration, migration_dir / migration.name)
        migration = migration_dir / "020_mcm_wq_normalized_geo.sql"
        migration.write_text(migration.read_text(encoding="utf-8") + "\nTHIS IS INVALID SQL;\n", encoding="utf-8")
        database = Path(self.temp.name) / "rollback.sqlite3"
        with self.assertRaises(sqlite3.Error):
            GovernedCoreRepository(database, migration_dir).initialize()
        cx = sqlite3.connect(database)
        try:
            self.assertEqual(19, cx.execute("PRAGMA user_version").fetchone()[0])
            self.assertIsNone(cx.execute("SELECT 1 FROM sqlite_master WHERE name='geo_reference'").fetchone())
            self.assertEqual(0, cx.execute("SELECT COUNT(*) FROM schema_migration WHERE migration_id LIKE '020_%'").fetchone()[0])
        finally:
            cx.close()

    def test_migration_020_preflight_and_postcheck_fail_closed(self):
        source = Path(__file__).resolve().parents[1] / "migrations"
        preflight_dir = Path(self.temp.name) / "preflight-migrations"
        preflight_dir.mkdir()
        for migration in source.glob("*.sql"):
            shutil.copy2(migration, preflight_dir / migration.name)
        migration_019 = preflight_dir / "019_mcm_wq_evaluation_authority_snapshot.sql"
        migration_019.write_text(migration_019.read_text(encoding="utf-8") + "\n-- tampered\n", encoding="utf-8")
        with self.assertRaises(GovernedConflictError):
            GovernedCoreRepository(Path(self.temp.name) / "preflight.sqlite3", preflight_dir).initialize()
        cx = sqlite3.connect(Path(self.temp.name) / "preflight.sqlite3")
        try:
            self.assertIsNone(cx.execute("SELECT 1 FROM sqlite_master WHERE name='geo_reference'").fetchone())
        finally:
            cx.close()

        postcheck_dir = Path(self.temp.name) / "postcheck-migrations"
        postcheck_dir.mkdir()
        for migration in source.glob("*.sql"):
            shutil.copy2(migration, postcheck_dir / migration.name)
        postcheck_database = Path(self.temp.name) / "postcheck.sqlite3"
        legacy_dir = Path(self.temp.name) / "postcheck-legacy-migrations"
        legacy_dir.mkdir()
        for migration in source.glob("*.sql"):
            if int(migration.name[:3]) <= 19:
                shutil.copy2(migration, legacy_dir / migration.name)
        legacy_repo = GovernedCoreRepository(postcheck_database, legacy_dir).initialize()
        PointContextService(legacy_repo).create_point_with_initial_context(
            "postcheck", "Postcheck", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR",
        )
        migration_020 = postcheck_dir / "020_mcm_wq_normalized_geo.sql"
        sql = migration_020.read_text(encoding="utf-8").replace(
            "SET geo_reference_id = 'legacy-geo-' || context_revision_id;",
            "SET geo_reference_id = 'legacy-geo-' || context_revision_id, geo_reference = 'tampered';",
        )
        migration_020.write_text(sql, encoding="utf-8")
        shutil.copy2(migration_020, legacy_dir / migration_020.name)
        with self.assertRaises(sqlite3.IntegrityError):
            GovernedCoreRepository(postcheck_database, legacy_dir).initialize()
        cx = sqlite3.connect(postcheck_database)
        self.assertIsNone(cx.execute("SELECT 1 FROM sqlite_master WHERE name='geo_reference'").fetchone())
        cx.close()

    def _legacy_database_for_migration_020(self, name):
        source = Path(__file__).resolve().parents[1] / "migrations"
        migration_dir = Path(self.temp.name) / f"{name}-migrations"
        migration_dir.mkdir()
        for migration in source.glob("*.sql"):
            if int(migration.name[:3]) <= 19:
                shutil.copy2(migration, migration_dir / migration.name)
        database = Path(self.temp.name) / f"{name}.sqlite3"
        GovernedCoreRepository(database, migration_dir).initialize()
        shutil.copy2(source / "020_mcm_wq_normalized_geo.sql", migration_dir)
        return database, migration_dir

    def test_migration_020_preflight_rejects_missing_table_column_and_legacy_read(self):
        database, migration_dir = self._legacy_database_for_migration_020("missing-table")
        cx = sqlite3.connect(database)
        cx.execute("ALTER TABLE point_context_revision RENAME TO point_context_revision_old")
        cx.close()
        with self.assertRaises(GovernedConflictError):
            GovernedCoreRepository(database, migration_dir).initialize()
        cx = sqlite3.connect(database)
        self.assertIsNone(cx.execute("SELECT 1 FROM sqlite_master WHERE name='geo_reference'").fetchone())
        cx.close()

        database, migration_dir = self._legacy_database_for_migration_020("missing-column")
        migration = migration_dir / "020_mcm_wq_normalized_geo.sql"
        sql = migration.read_text(encoding="utf-8").replace(
            "WHERE name = 'created_at'", "WHERE name = 'missing_created_at'", 1
        )
        migration.write_text(sql, encoding="utf-8")
        with self.assertRaises(sqlite3.IntegrityError):
            GovernedCoreRepository(database, migration_dir).initialize()

        database, migration_dir = self._legacy_database_for_migration_020("unreadable-legacy")
        migration = migration_dir / "020_mcm_wq_normalized_geo.sql"
        sql = migration.read_text(encoding="utf-8").replace(
            "SELECT context_revision_id, geo_reference FROM point_context_revision",
            "SELECT context_revision_id, missing_legacy FROM point_context_revision",
            1,
        )
        migration.write_text(sql, encoding="utf-8")
        with self.assertRaises(sqlite3.Error):
            GovernedCoreRepository(database, migration_dir).initialize()

    def test_migration_020_preflight_rejects_incompatible_index_and_trigger(self):
        for kind, statement, error in (
            ("index", "CREATE INDEX geo_reference_context_unique ON point_context_revision(context_revision_id)", GovernedConflictError),
            ("trigger", "CREATE TRIGGER geo_context_link_guard BEFORE INSERT ON point_context_revision BEGIN SELECT RAISE(ABORT, 'occupied'); END", GovernedConflictError),
        ):
            database, migration_dir = self._legacy_database_for_migration_020(f"occupied-{kind}")
            cx = sqlite3.connect(database)
            cx.execute(statement)
            cx.close()
            with self.assertRaises(error):
                GovernedCoreRepository(database, migration_dir).initialize()
            cx = sqlite3.connect(database)
            self.assertIsNone(cx.execute("SELECT 1 FROM sqlite_master WHERE name='geo_reference'").fetchone())
            cx.close()

    def test_migration_020_preflight_rejects_existing_link_and_all_geo_name_collisions(self):
        cases = (
            (
                "existing-link-column",
                lambda cx: cx.execute(
                    "ALTER TABLE point_context_revision ADD COLUMN geo_reference_id TEXT"
                ),
            ),
            (
                "geo-reference-view",
                lambda cx: cx.execute("CREATE VIEW geo_reference AS SELECT 1 AS occupied"),
            ),
            (
                "geo-reference-index",
                lambda cx: cx.execute(
                    "CREATE INDEX geo_reference ON point_context_revision(context_revision_id)"
                ),
            ),
            (
                "geo-reference-trigger",
                lambda cx: cx.execute(
                    "CREATE TRIGGER geo_reference BEFORE INSERT ON point_context_revision BEGIN SELECT RAISE(ABORT, 'occupied'); END"
                ),
            ),
            (
                "location-provenance-view",
                lambda cx: cx.execute("CREATE VIEW location_provenance AS SELECT 1 AS occupied"),
            ),
            (
                "location-provenance-index",
                lambda cx: cx.execute(
                    "CREATE INDEX location_provenance ON point_context_revision(context_revision_id)"
                ),
            ),
            (
                "location-provenance-trigger",
                lambda cx: cx.execute(
                    "CREATE TRIGGER location_provenance BEFORE INSERT ON point_context_revision BEGIN SELECT RAISE(ABORT, 'occupied'); END"
                ),
            ),
        )
        for name, prepare in cases:
            database, migration_dir = self._legacy_database_for_migration_020(name)
            cx = sqlite3.connect(database)
            prepare(cx)
            cx.close()
            with self.assertRaises(GovernedConflictError):
                GovernedCoreRepository(database, migration_dir).initialize()
            cx = sqlite3.connect(database)
            try:
                self.assertIsNone(
                    cx.execute("SELECT 1 FROM sqlite_master WHERE name='geo_reference' AND type='table'").fetchone()
                )
                self.assertIsNone(
                    cx.execute("SELECT 1 FROM sqlite_master WHERE name='location_provenance' AND type='table'").fetchone()
                )
            finally:
                cx.close()

    def test_new_context_without_coordinates_is_unavailable(self):
        point = self._point()
        geo = self.repo.fetch_geo_reference(point.current_context_revision_id)
        self.assertEqual(GeoAvailabilityState.UNAVAILABLE.value, geo.availability_state)
        self.assertEqual("NO_COORDINATE_SUPPLIED", geo.state_reason)

    def test_available_coordinates_require_provenance_and_preserve_zero_zero(self):
        point = self._point(name="Available", geo_reference_data=self._available_data("prv-zero", 0.0, 0.0))
        geo = self.repo.fetch_geo_reference(point.current_context_revision_id)
        self.assertEqual((0.0, 0.0), (geo.latitude, geo.longitude))
        self.assertEqual("EPSG:4326", geo.crs_identifier)
        self.assertEqual("prv-zero", geo.location_provenance_id)
        self.assertEqual("0.0", self.repo.fetch_location_provenance("prv-zero").source_coordinate_1_raw)

    def test_unverified_and_legacy_states_are_explicit(self):
        point = self._point(name="Opaque", geo_reference="opaque-legacy")
        geo = self.repo.fetch_geo_reference(point.current_context_revision_id)
        self.assertEqual(GeoAvailabilityState.LEGACY_UNCLASSIFIED.value, geo.availability_state)
        with self.repo._optional_connection(None) as cx:
            self.assertEqual("opaque-legacy", cx.execute(
                "SELECT geo_reference FROM point_context_revision WHERE context_revision_id=?",
                (point.current_context_revision_id,),
            ).fetchone()[0])
        point2 = self._point(name="Unverified", geo_reference_data={
            "availability_state": "UNVERIFIED", "state_reason": "SOURCE_NOT_ACCEPTED",
            "location_provenance_id": "prv-unverified", "provenance": self._provenance("prv-unverified"),
        })
        self.assertEqual("UNVERIFIED", self.repo.fetch_geo_reference(point2.current_context_revision_id).availability_state)

    def test_direct_sql_missing_link_and_cross_link_are_rejected(self):
        point = self._point()
        second = self._point(name="Second")
        first_geo = self.repo.fetch_geo_reference(point.current_context_revision_id)
        with self.repo.transaction() as cx:
            cx.execute("SAVEPOINT missing_geo")
            with self.assertRaises(sqlite3.IntegrityError):
                cx.execute("INSERT INTO point_context_revision (context_revision_id,point_id,revision,purpose,water_context,point_type,created_at,effective_from) VALUES ('bad',?,?,?,?,?,?,?)", (point.point_id, 2, "ENVIRONMENTAL_CONDITION_MONITORING", "FLOWING_SURFACE_WATER", "GENERAL", "2020-01-01T00:00:00Z", "2021-01-01T00:00:00Z"))
            cx.execute("ROLLBACK TO missing_geo")
            cx.execute("RELEASE missing_geo")
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as cx:
                cx.execute(
                    "INSERT INTO geo_reference VALUES (?,?,?,?,?,?,?,?,?)",
                    ("cross-linked", point.current_context_revision_id, "UNAVAILABLE", None, None, None, None, "test", "2020-01-01T00:00:00Z"),
                )
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as cx:
                cx.execute(
                    "INSERT INTO geo_reference VALUES (?,?,?,?,?,?,?,?,?)",
                    ("duplicate", second.current_context_revision_id, "UNAVAILABLE", None, None, None, None, "test", "2020-01-01T00:00:00Z"),
                )
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as cx:
                cx.execute(
                    "INSERT INTO geo_reference VALUES (?,?,?,?,?,?,?,?,?)",
                    ("orphan", "missing-context", "UNAVAILABLE", None, None, None, None, "test", "2020-01-01T00:00:00Z"),
                )
        self.assertIsNotNone(first_geo)

    def test_unverified_coordinates_and_invalid_timestamp_are_typed_failures(self):
        point = self._point(name="Typed failures")
        with self.assertRaises(GeoReferenceResolutionError) as error:
            self.geo.create_reference(
                point.current_context_revision_id, "UNVERIFIED", latitude=1.0,
                location_provenance_id="missing", state_reason="not accepted",
            )
        self.assertEqual("GEO_REFERENCE_INVALID", error.exception.reason_code)
        with self.assertRaises(GeoReferenceResolutionError) as error:
            self.geo.register_provenance(replace(
                self._provenance("bad-time"), registered_at="2020-01-01T00:00:00+00:00"
            ))
        self.assertEqual("GEO_PROVENANCE_INVALID", error.exception.reason_code)

    def test_direct_sql_rejects_invalid_numeric_type_and_nonfinite_value(self):
        values = ("direct-invalid", "source://direct", "1", "2", "not-a-number", 2.0,
                  "LATITUDE_LONGITUDE", "EPSG:4326", None, None, "UNKNOWN", None, None,
                  None, None, None, None, "2020-01-01T00:00:00Z")
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as cx:
                cx.execute("INSERT INTO location_provenance VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", values)
        nonfinite = list(values)
        nonfinite[0] = "direct-infinite"
        nonfinite[4] = float("inf")
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as cx:
                cx.execute("INSERT INTO location_provenance VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", nonfinite)
        invalid_time = list(values)
        invalid_time[0] = "direct-invalid-time"
        invalid_time[4] = 1.0
        invalid_time[-1] = "2020-01-01T00:00:00+00:00"
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as cx:
                cx.execute("INSERT INTO location_provenance VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", invalid_time)
        invalid_calendar = list(values)
        invalid_calendar[0] = "direct-invalid-calendar"
        invalid_calendar[4] = 1.0
        invalid_calendar[-1] = "2021-02-29T00:00:00Z"
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repo.transaction() as cx:
                cx.execute("INSERT INTO location_provenance VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", invalid_calendar)

    def test_provenance_and_geo_are_immutable(self):
        point = self._point(geo_reference_data=self._available_data())
        with self.repo.transaction() as cx:
            geo_id = self.repo.fetch_geo_reference(point.current_context_revision_id, cx).geo_reference_id
            with self.assertRaises(sqlite3.IntegrityError):
                cx.execute("UPDATE geo_reference SET state_reason='changed' WHERE geo_reference_id=?", (geo_id,))
            with self.assertRaises(sqlite3.IntegrityError):
                cx.execute("DELETE FROM location_provenance WHERE provenance_id='prv-test'")

    def test_crs_resolution_and_transform_are_offline_and_fail_safe(self):
        os.environ["PROJ_NETWORK"] = "OFF"
        self.assertEqual("RESOLVED_CRS", CRSResolver().resolve("EPSG:4326").state)
        transformed = CoordinateTransformer().transform(
            "EPSG:4326", (-40.0, 20.0), SourceAxisOrder.LONGITUDE_LATITUDE.value
        )
        self.assertEqual("TRANSFORMED_COORDINATE", transformed.state)
        self.assertEqual((20.0, -40.0), (transformed.latitude, transformed.longitude))
        self.assertEqual("CRS_UNRESOLVED", CRSResolver().resolve("EPSG:does-not-exist").reason_code)
        self.assertEqual("CRS_AXIS_ORDER_UNRESOLVED", CoordinateTransformer().transform(
            "EPSG:4326", (-40.0, 20.0), SourceAxisOrder.UNKNOWN.value
        ).reason_code)
        with self.assertRaises(GeoReferenceResolutionError) as error:
            point = self._point(name="3D CRS")
            self.geo.create_reference(
                point.current_context_revision_id, "AVAILABLE", latitude=20.0,
                longitude=-40.0, crs_identifier="EPSG:4979", location_provenance_id="missing",
            )
        self.assertEqual("CRS_NOT_GEOGRAPHIC_LATLON", error.exception.reason_code)

    def test_crs_operations_reassert_network_off(self):
        set_network_enabled(True)
        self.assertTrue(is_network_enabled())
        self.assertEqual("RESOLVED_CRS", CRSResolver().resolve("EPSG:4326").state)
        self.assertFalse(is_network_enabled())

    def test_non_identity_transform_is_persisted_with_provenance(self):
        forward = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
        x, y = forward.transform(-40.0, 20.0)
        transformed = CoordinateTransformer().transform(
            "EPSG:3857", (x, y), SourceAxisOrder.LONGITUDE_LATITUDE.value
        )
        self.assertEqual("TRANSFORMED_COORDINATE", transformed.state)
        provenance = LocationProvenance(
            "prv-projected", "survey://projected", str(x), str(y), x, y,
            SourceAxisOrder.LONGITUDE_LATITUDE.value, "EPSG:3857", "SURVEY",
            "2020-01-01T00:00:00.000000Z", "KNOWN", "PROJ", "{}",
            transformed.operation, None, None, None, "2020-01-01T00:00:00.000000Z",
        )
        point = self._point(name="Projected", geo_reference_data={
            "availability_state": "AVAILABLE", "latitude": transformed.latitude,
            "longitude": transformed.longitude, "crs_identifier": "EPSG:4326",
            "location_provenance_id": "prv-projected", "provenance": provenance,
        })
        persisted = self.repo.fetch_location_provenance("prv-projected")
        self.assertEqual("PROJ", persisted.transformation_method)
        self.assertEqual(transformed.operation, persisted.transformation_provenance)
        self.assertEqual("AVAILABLE", self.repo.fetch_geo_reference(point.current_context_revision_id).availability_state)

    def test_manifest_mismatch_and_grid_failure_fail_safe(self):
        original = geo_crs.EXPECTED_PROJ_DB_SHA256
        try:
            geo_crs.EXPECTED_PROJ_DB_SHA256 = "0" * 64
            self.assertEqual("GEO_MANIFEST_MISMATCH", geo_crs.verify_runtime_manifest())
        finally:
            geo_crs.EXPECTED_PROJ_DB_SHA256 = original
        with patch("governed_core.geo_crs.Transformer.from_crs", side_effect=ProjError("grid unavailable")):
            result = CoordinateTransformer().transform(
                "EPSG:4326", (-40.0, 20.0), SourceAxisOrder.LONGITUDE_LATITUDE.value
            )
        self.assertEqual("TRANSFORMATION_UNAVAILABLE", result.state)

    def test_runtime_failure_rolls_back_point_and_provenance(self):
        data = self._available_data("prv-rollback")
        data["latitude"] = 21.0
        with self.assertRaises(GeoReferenceResolutionError):
            self._point(name="Rollback", geo_reference_data=data)
        with self.repo._optional_connection(None) as cx:
            self.assertEqual(0, cx.execute("SELECT COUNT(*) FROM governed_monitoring_point WHERE display_name='Rollback'").fetchone()[0])
            self.assertEqual(0, cx.execute("SELECT COUNT(*) FROM location_provenance WHERE provenance_id='prv-rollback'").fetchone()[0])

    def test_historical_geo_is_resolved_from_context_revision(self):
        point = self._point(name="Historical", geo_reference_data=self._available_data("prv-old", 10.0, -30.0))
        with self.repo.transaction() as cx:
            cx.execute("INSERT INTO authority_reference VALUES ('a-geo','a-geo',NULL)")
            cx.execute("INSERT INTO evidence_reference VALUES ('e-geo','e-geo',NULL)")
            cx.execute("INSERT INTO authorized_parameter_set VALUES ('aps-geo')")
            cx.execute("INSERT INTO aps_version VALUES ('aps-geo',1,?)", (point.current_context_revision_id,))
            cx.execute("INSERT INTO aps_member VALUES ('aps-geo',1,'PH')")
            cx.execute("INSERT INTO authorization_basis VALUES ('bas-geo','aps-geo',1)")
            cx.execute("INSERT INTO basis_authority VALUES ('bas-geo','a-geo')")
            cx.execute("INSERT INTO basis_evidence VALUES ('bas-geo','e-geo')")
        successor = TemporalStateService(self.repo).append_successor(
            "POINT_CONTEXT_REVISION", point.current_context_revision_id,
            {"effective_from": datetime(2021, 1, 1, tzinfo=timezone.utc), "revision": 2,
             "purpose": "ENVIRONMENTAL_CONDITION_MONITORING", "water_context": "FLOWING_SURFACE_WATER",
             "point_type": "GENERAL", "geo_reference_data": self._available_data("prv-new", 11.0, -31.0)},
            "ACTOR", "bas-geo")
        old_geo = self.repo.fetch_geo_reference(point.current_context_revision_id)
        new_geo = self.repo.fetch_geo_reference(successor)
        self.assertEqual((10.0, -30.0), (old_geo.latitude, old_geo.longitude))
        self.assertEqual((11.0, -31.0), (new_geo.latitude, new_geo.longitude))
        old = SimpleNamespace(point_id=point.point_id, context_revision_id=point.current_context_revision_id, measured_at="2020-06-01T00:00:00.000000Z")
        self.assertEqual(old_geo.geo_reference_id, self.geo.resolve_for_measurement(old).geo_reference_id)


if __name__ == "__main__":
    unittest.main()
