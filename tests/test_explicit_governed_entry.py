import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreRepository, GovernedReferenceError


class ExplicitGovernedEntryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repository = GovernedCoreRepository(Path(self.temp.name) / "entry.sqlite3").initialize()
        self.bootstrap = FirstRealAPSBootstrap(self.repository)
        self.state = self.bootstrap.execute()
        self.service = ExplicitGovernedEntryService(self.repository)

    def tearDown(self):
        self.temp.cleanup()

    def count(self, table):
        with self.repository._optional_connection(None) as connection:
            return connection.execute("SELECT COUNT(*) FROM " + table).fetchone()[0]

    def test_explicit_entry_returns_complete_receipt_and_no_legacy_write(self):
        self.assertEqual(("PH", "TURBIDITY", "DISSOLVED_OXYGEN"), self.service.canonical_parameters(self.state.point_id))
        measured_at = datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc)
        receipt = self.service.submit(self.state.point_id, "PH", 7.2, measured_at)
        self.assertEqual(self.state.point_id, receipt.point_id)
        self.assertEqual("PH", receipt.parameter_reference)
        self.assertEqual("MANUAL_ENTRY", receipt.provenance)
        self.assertTrue(receipt.measurement_id)
        self.assertTrue(receipt.registered_at)
        self.assertTrue(receipt.measured_at.endswith("Z"))
        self.assertEqual(1, self.count("governed_measurement"))

    def test_explicit_entry_rejects_naive_time_and_non_member(self):
        before = self.count("governed_measurement")
        with self.assertRaises(ValueError):
            self.service.submit(self.state.point_id, "PH", 7.2, datetime(2026, 8, 30, 12, 0))
        with self.assertRaises(ValueError):
            self.service.submit(self.state.point_id, "TEMPERATURE", 20.0, datetime.now(timezone.utc))
        self.assertEqual(before, self.count("governed_measurement"))

    def test_application_seam_rejects_non_canonical_parameter(self):
        before = self.count("governed_measurement")
        with self.assertRaises(ValueError):
            self.service.submit(
                self.state.point_id,
                "TEMPERATURE",
                20.0,
                datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc),
            )
        self.assertEqual(before, self.count("governed_measurement"))

    def test_no_point_selection_is_not_accepted(self):
        with self.assertRaises(GovernedReferenceError):
            self.service.canonical_parameters("pnt_missing")


if __name__ == "__main__":
    unittest.main()
