import json
import os
import shutil
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PyQt5.QtWidgets import QApplication

from governed_core.desktop_bootstrap import (
    DesktopGovernedStartupError,
    GOVERNED_DATABASE_NAME,
    initialize_desktop_governed_repository,
    resolve_user_data_root,
)
from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreRepository
from governed_entry_page import GovernedEntryPage


class DesktopGovernedPersistenceBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qt_app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.local_app_data = Path(self.temp.name) / "LocalAppData"
        self.migrations = Path(__file__).resolve().parents[1] / "migrations"

    def tearDown(self):
        self.temp.cleanup()

    def _database_path(self):
        return self.local_app_data / "Sistema de Monitoramento de Águas" / "data" / GOVERNED_DATABASE_NAME

    def test_fresh_user_root_creates_and_migrates_governed_database(self):
        repository = initialize_desktop_governed_repository(
            self.local_app_data, self.migrations
        )

        self.assertEqual(self._database_path(), repository.path)
        self.assertTrue(repository.path.is_file())
        connection = sqlite3.connect(repository.path)
        try:
            self.assertEqual(20, connection.execute("PRAGMA user_version").fetchone()[0])
            migration_ids = {
                row[0]
                for row in connection.execute("SELECT migration_id FROM schema_migration")
            }
        finally:
            connection.close()
        self.assertIn("019_mcm_wq_evaluation_authority_snapshot.sql", migration_ids)
        self.assertIn("020_mcm_wq_normalized_geo.sql", migration_ids)

    def test_persisted_database_and_repeated_startup_are_idempotent(self):
        first = initialize_desktop_governed_repository(self.local_app_data, self.migrations)
        connection = sqlite3.connect(first.path)
        try:
            connection.execute(
                "CREATE TABLE startup_probe (probe_id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )
            connection.execute(
                "INSERT INTO startup_probe VALUES (?, ?)", ("one", json.dumps({"legacy": True}))
            )
            connection.commit()
        finally:
            connection.close()

        second = initialize_desktop_governed_repository(self.local_app_data, self.migrations)
        self.assertEqual(first.path, second.path)
        connection = sqlite3.connect(second.path)
        try:
            self.assertEqual(
                (json.dumps({"legacy": True}),),
                connection.execute("SELECT payload FROM startup_probe WHERE probe_id='one'").fetchone(),
            )
            self.assertEqual(
                20, connection.execute("PRAGMA user_version").fetchone()[0]
            )
        finally:
            connection.close()

    def test_persisted_migration_019_advances_only_to_pending_020(self):
        legacy_migrations = Path(self.temp.name) / "migrations-019"
        legacy_migrations.mkdir()
        for migration in self.migrations.glob("*.sql"):
            if not migration.name.startswith("020_"):
                shutil.copy2(migration, legacy_migrations / migration.name)

        database_path = self._database_path()
        GovernedCoreRepository(database_path, legacy_migrations).initialize()
        connection = sqlite3.connect(database_path)
        try:
            self.assertEqual(19, connection.execute("PRAGMA user_version").fetchone()[0])
        finally:
            connection.close()

        repository = initialize_desktop_governed_repository(
            self.local_app_data, self.migrations
        )
        self.assertEqual(database_path, repository.path)
        connection = sqlite3.connect(database_path)
        try:
            self.assertEqual(20, connection.execute("PRAGMA user_version").fetchone()[0])
        finally:
            connection.close()

    def test_initialization_failure_is_typed_and_does_not_fallback(self):
        class FailingRepository:
            def __init__(self, *_args):
                pass

            def initialize(self):
                raise sqlite3.DatabaseError("migration preflight failed")

        with self.assertRaises(DesktopGovernedStartupError) as raised:
            initialize_desktop_governed_repository(
                self.local_app_data, self.migrations, FailingRepository
            )

        self.assertEqual("GOVERNED_DATABASE_INITIALIZATION_FAILED", raised.exception.reason_code)
        self.assertFalse((self.local_app_data / "quality_water.csv").exists())

    def test_missing_user_data_root_is_typed(self):
        with patch.dict(os.environ, {"LOCALAPPDATA": ""}, clear=False):
            with self.assertRaises(DesktopGovernedStartupError) as raised:
                resolve_user_data_root()

        self.assertEqual("USER_DATA_ROOT_UNRESOLVED", raised.exception.reason_code)

    def test_governed_entry_requires_startup_owned_repository(self):
        with self.assertRaises(ValueError):
            GovernedEntryPage()

    def test_legacy_files_are_not_imported_or_rewritten_by_startup(self):
        legacy_root = self.local_app_data / "Sistema de Monitoramento de Águas" / "data"
        legacy_root.mkdir(parents=True)
        legacy_file = legacy_root / "qualidade_agua_medicoes.csv"
        legacy_file.write_text("timestamp,ph\n2026-01-01T00:00:00Z,7.2\n", encoding="utf-8")
        before = legacy_file.read_bytes()

        initialize_desktop_governed_repository(self.local_app_data, self.migrations)

        self.assertEqual(before, legacy_file.read_bytes())
        connection = sqlite3.connect(self._database_path())
        try:
            self.assertEqual(
                0, connection.execute("SELECT COUNT(*) FROM governed_measurement").fetchone()[0]
            )
        finally:
            connection.close()

    def test_governed_write_is_sqlite_only(self):
        repository = initialize_desktop_governed_repository(
            self.local_app_data, self.migrations
        )
        state = FirstRealAPSBootstrap(repository).execute()
        receipt = ExplicitGovernedEntryService(repository).submit(
            state.point_id,
            "PH",
            7.2,
            datetime(2026, 1, 1, tzinfo=timezone.utc),
        )

        self.assertTrue(receipt.measurement_id)
        self.assertFalse(
            (self.local_app_data / "Sistema de Monitoramento de Águas" / "data" / "qualidade_agua_medicoes.csv").exists()
        )
        connection = sqlite3.connect(self._database_path())
        try:
            self.assertEqual(
                1, connection.execute("SELECT COUNT(*) FROM governed_measurement").fetchone()[0]
            )
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
