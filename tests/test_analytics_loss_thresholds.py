from pathlib import Path
import unittest

from analytics.alerts import PreventiveAlertService
from analytics.loss_thresholds import LOSS_HIGH_THRESHOLD, LOSS_MONITORING_THRESHOLD
from analytics.models import ConsumptionMeasurement, QualityMeasurement
from analytics.scoring import WaterHealthScoreCalculator


class AnalyticsLossThresholdTests(unittest.TestCase):
    def setUp(self):
        self.quality = [QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0)]

    def _consumption(self, loss):
        return [ConsumptionMeasurement(None, 10.0, 300.0, 350.0, loss)]

    def test_loss_thresholds_have_one_analytics_domain_source(self):
        self.assertEqual(15.0, LOSS_MONITORING_THRESHOLD)
        self.assertEqual(30.0, LOSS_HIGH_THRESHOLD)

        for consumer in ("analytics/scoring.py", "analytics/alerts.py"):
            source = Path(consumer).read_text(encoding="utf-8")
            self.assertNotIn(">= 15.0", source)
            self.assertNotIn(">= 30.0", source)

    def test_scoring_behavior_is_preserved_at_loss_boundaries(self):
        calculator = WaterHealthScoreCalculator()

        self.assertEqual(100, calculator.calculate(self.quality, [], self._consumption(14.99)).score)
        self.assertEqual(94, calculator.calculate(self.quality, [], self._consumption(15.0)).score)
        self.assertEqual(88, calculator.calculate(self.quality, [], self._consumption(30.0)).score)

    def test_alert_behavior_is_preserved_at_loss_boundaries(self):
        service = PreventiveAlertService()

        below = service.build_alerts([], [], self._consumption(14.99), [], [])
        monitoring = service.build_alerts([], [], self._consumption(15.0), [], [])
        high = service.build_alerts([], [], self._consumption(30.0), [], [])

        self.assertEqual([], below)
        self.assertEqual("medio", monitoring[0].severity)
        self.assertIn("15.00%", monitoring[0].evidence)
        self.assertEqual("alto", high[0].severity)
        self.assertIn("30.00%", high[0].evidence)

    def test_policy_engine_scope_is_not_expanded(self):
        source = Path("analytics/loss_thresholds.py").read_text(encoding="utf-8")

        self.assertNotIn("PolicyEngine", source)
        self.assertNotIn("monitoramento_hidrico", source)


if __name__ == "__main__":
    unittest.main()
