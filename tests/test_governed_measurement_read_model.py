import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreRepository


class GovernedMeasurementReadModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repository = GovernedCoreRepository(Path(self.temp.name) / "read.sqlite3").initialize()
        self.state = FirstRealAPSBootstrap(self.repository).execute()
        self.service = ExplicitGovernedEntryService(self.repository)

    def tearDown(self):
        self.temp.cleanup()

    def test_point_scoping_persisted_values_and_po60_ties(self):
        instant = datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc)
        first = self.service.submit(self.state.point_id, "PH", 7.1, instant)
        second = self.service.submit(self.state.point_id, "TURBIDITY", 2.0, instant)
        rows = self.service.governed_history(self.state.point_id)
        expected = sorted(
            (first, second),
            key=lambda row: (row.measured_at, row.registered_at, row.measurement_id),
            reverse=True,
        )
        self.assertEqual([row.measurement_id for row in expected], [row.measurement_id for row in rows])
        self.assertEqual(second.value, rows[0].value)
        self.assertTrue(all(row.point_id == self.state.point_id for row in rows))
        before = [(row.measurement_id, row.value) for row in rows]
        after = [(row.measurement_id, row.value) for row in self.service.governed_history(self.state.point_id)]
        self.assertEqual(before, after)

    def test_empty_history_is_explicit_and_other_point_isolated(self):
        self.assertEqual((), self.service.governed_history(self.state.point_id))
        with self.repository._optional_connection(None) as connection:
            self.assertEqual(
                0,
                connection.execute("SELECT COUNT(*) FROM governed_measurement").fetchone()[0],
            )


if __name__ == "__main__":
    unittest.main()
