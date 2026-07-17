import ast
import unittest
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from analytics.dashboard_snapshot import DashboardAnalyticsSnapshotService
from analytics.models import ConsumptionMeasurement, EnvironmentMeasurement, QualityMeasurement


@dataclass(frozen=True)
class FakeScore:
    score: int
    status: str


class FakeRepository:
    def __init__(self, quality=None, environment=None, consumption=None):
        self.quality = quality or []
        self.environment = environment or []
        self.consumption = consumption or []

    def load_quality(self):
        return list(self.quality)

    def load_environment(self):
        return list(self.environment)

    def load_consumption(self):
        return list(self.consumption)


class RecordingScoreCalculator:
    def __init__(self):
        self.calls = []

    def calculate(self, quality, environment, consumption):
        self.calls.append((list(quality), list(environment), list(consumption)))
        return FakeScore(score=60 + len(quality), status=f"status-{len(quality)}")


class DashboardAnalyticsSnapshotServiceTests(unittest.TestCase):
    def test_series_is_empty_when_quality_history_is_insufficient(self):
        repository = FakeRepository(
            quality=[QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0)]
        )
        calculator = RecordingScoreCalculator()

        points = DashboardAnalyticsSnapshotService(repository, calculator).water_health_score_series()

        self.assertEqual([], points)
        self.assertEqual([], calculator.calls)

    def test_series_is_ready_for_water_health_score_chart(self):
        repository = FakeRepository(
            quality=[
                QualityMeasurement(datetime(2026, 7, 1, 8, 0), 7.0, 1.0, 6.0, 25.0, 0.0),
                QualityMeasurement(datetime(2026, 7, 2, 8, 0), 7.1, 1.0, 6.0, 25.0, 0.0),
            ],
        )
        calculator = RecordingScoreCalculator()

        points = DashboardAnalyticsSnapshotService(repository, calculator).water_health_score_series()

        self.assertEqual(
            [
                {"label": "01/07", "score": 61, "status": "status-1"},
                {"label": "02/07", "score": 62, "status": "status-2"},
            ],
            points,
        )
        self.assertEqual({"label", "score", "status"}, set(points[0]))

    def test_series_filters_environment_and_consumption_until_quality_timestamp(self):
        quality = [
            QualityMeasurement(datetime(2026, 7, 1, 8, 0), 7.0, 1.0, 6.0, 25.0, 0.0),
            QualityMeasurement(datetime(2026, 7, 3, 8, 0), 7.1, 1.0, 6.0, 25.0, 0.0),
        ]
        environment = [
            EnvironmentMeasurement(datetime(2026, 7, 1, 7, 0), 20.0, 70.0, 0.0, 1010.0),
            EnvironmentMeasurement(datetime(2026, 7, 4, 7, 0), 21.0, 72.0, 0.0, 1010.0),
            EnvironmentMeasurement(None, 22.0, 73.0, 0.0, 1010.0),
        ]
        consumption = [
            ConsumptionMeasurement(datetime(2026, 7, 2, 7, 0), 10.0, 300.0, 350.0, 4.0),
            ConsumptionMeasurement(datetime(2026, 7, 5, 7, 0), 11.0, 330.0, 360.0, 5.0),
        ]
        calculator = RecordingScoreCalculator()

        DashboardAnalyticsSnapshotService(
            FakeRepository(quality, environment, consumption),
            calculator,
        ).water_health_score_series()

        first_call = calculator.calls[0]
        second_call = calculator.calls[1]
        self.assertEqual(2, len(first_call[1]))
        self.assertEqual(0, len(first_call[2]))
        self.assertEqual(2, len(second_call[1]))
        self.assertEqual(1, len(second_call[2]))

    def test_series_returns_only_last_twelve_points(self):
        quality = [
            QualityMeasurement(datetime(2026, 7, day, 8, 0), 7.0, 1.0, 6.0, 25.0, 0.0)
            for day in range(1, 15)
        ]

        points = DashboardAnalyticsSnapshotService(
            FakeRepository(quality=quality),
            RecordingScoreCalculator(),
        ).water_health_score_series()

        self.assertEqual(12, len(points))
        self.assertEqual("03/07", points[0]["label"])
        self.assertEqual("14/07", points[-1]["label"])

    def test_dashboard_page_has_no_direct_analytics_dependencies(self):
        source = Path("main.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        dashboard_class = next(
            node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "DashboardPage"
        )
        dashboard_source = ast.get_source_segment(source, dashboard_class)

        forbidden_terms = [
            "AnalyticsRepository",
            "WaterHealthScoreCalculator",
            "_water_health_score_series",
            "_measurements_until",
        ]
        for term in forbidden_terms:
            self.assertNotIn(term, dashboard_source)

        imports = [
            node
            for node in tree.body
            if isinstance(node, (ast.Import, ast.ImportFrom))
        ]
        imported_modules = {
            node.module
            for node in imports
            if isinstance(node, ast.ImportFrom) and node.module is not None
        }
        self.assertNotIn("analytics.repositories", imported_modules)
        self.assertNotIn("analytics.scoring", imported_modules)
        self.assertIn("analytics.dashboard_snapshot", imported_modules)


if __name__ == "__main__":
    unittest.main()
