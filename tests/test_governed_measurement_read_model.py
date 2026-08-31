import tempfile
import unittest
import os
from datetime import datetime, timezone
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
from PyQt5.QtWidgets import QApplication

from data_access.csv_measurement_repository import CSVMeasurementRepository
from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreRepository
from governed_core.services import APSService, ApplicabilityService, PointContextService
from governed_entry_page import GovernedEntryPage


class GovernedMeasurementReadModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.qt_app = QApplication.instance() or QApplication([])

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

    def test_multi_point_query_has_zero_cross_point_leakage(self):
        points = PointContextService(self.repository)
        other = points.create_point_with_initial_context(
            "OTHER_PROJECT", "Other", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR",
        )
        aps = APSService(self.repository)
        authority = aps.register_authority_reference("authority://other")
        evidence = aps.register_evidence_reference("evidence://other")
        basis = aps.make_basis((authority,), (evidence,), ("PH",))
        reference = aps.create_version(other.current_context_revision_id, ("PH",), (basis,))
        ApplicabilityService(self.repository).assign(other.current_context_revision_id, reference, "ACTOR")
        self.service.submit(self.state.point_id, "PH", 7.1, datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc))
        other_service = ExplicitGovernedEntryService(self.repository)
        other_service.submit(other.point_id, "PH", 8.1, datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc))
        rows = self.service.governed_history(self.state.point_id)
        self.assertEqual(1, len(rows))
        self.assertEqual(self.state.point_id, rows[0].point_id)
        self.assertNotIn(8.1, [row.value for row in rows])

    def test_qt_empty_state_is_rendered_for_selected_point(self):
        page = GovernedEntryPage(repository=self.repository)
        page.point_input.setCurrentIndex(1)
        self.assertEqual(
            "Nenhuma medição governada registrada para este ponto.",
            page.history.text(),
        )

    def test_governed_history_excludes_legacy_csv_content(self):
        legacy = Path(self.temp.name) / "legacy.csv"
        csv = CSVMeasurementRepository(legacy, ("timestamp", "ph"))
        csv.append({"timestamp": "legacy-row", "ph": "9.9"})
        self.service.submit(
            self.state.point_id, "PH", 7.1,
            datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc),
        )
        history = self.service.governed_history(self.state.point_id)
        self.assertEqual(1, len(history))
        self.assertNotIn("legacy-row", repr(history))
        self.assertNotIn("9.9", repr(history))

    def test_legacy_history_excludes_governed_rows(self):
        legacy = Path(self.temp.name) / "legacy.csv"
        csv = CSVMeasurementRepository(legacy, ("timestamp", "ph"))
        csv.append({"timestamp": "legacy-row", "ph": "9.9"})
        self.service.submit(
            self.state.point_id, "PH", 7.1,
            datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc),
        )
        rows = csv.read_all()
        self.assertEqual([{"timestamp": "legacy-row", "ph": "9.9"}], rows)
        self.assertNotIn("mea_", repr(rows))


if __name__ == "__main__":
    unittest.main()
