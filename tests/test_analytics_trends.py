import unittest

from analytics.models import ConsumptionMeasurement, QualityMeasurement
from analytics.trends import TrendAnalyzer


class TrendAnalyzerTests(unittest.TestCase):
    def test_quality_trend_detects_rising_turbidity(self):
        measurements = [
            QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0),
            QualityMeasurement(None, 7.0, 1.2, 6.0, 25.0, 0.0),
            QualityMeasurement(None, 7.0, 3.0, 6.0, 25.0, 0.0),
            QualityMeasurement(None, 7.0, 3.2, 6.0, 25.0, 0.0),
        ]

        trends = TrendAnalyzer().quality_trends(measurements)
        turbidity = next(trend for trend in trends if trend.metric == "turbidez")

        self.assertEqual("subindo", turbidity.direction)
        self.assertAlmostEqual(1.1, turbidity.previous_average)
        self.assertAlmostEqual(3.1, turbidity.recent_average)
        self.assertIn("media anterior", turbidity.explanation)

    def test_consumption_trend_reports_insufficient_data(self):
        measurements = [
            ConsumptionMeasurement(None, 10.0, 300.0, 350.0, 5.0),
        ]

        trends = TrendAnalyzer().consumption_trends(measurements)
        daily = next(trend for trend in trends if trend.metric == "consumo_diario")

        self.assertEqual("dados_insuficientes", daily.direction)
        self.assertIsNone(daily.delta)
        self.assertIn("minimo de 2", daily.explanation)

    def test_quality_trend_detects_stable_values(self):
        measurements = [
            QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0),
            QualityMeasurement(None, 7.01, 1.0, 6.0, 25.0, 0.0),
        ]

        trends = TrendAnalyzer().quality_trends(measurements)
        ph = next(trend for trend in trends if trend.metric == "ph")

        self.assertEqual("estavel", ph.direction)


if __name__ == "__main__":
    unittest.main()
