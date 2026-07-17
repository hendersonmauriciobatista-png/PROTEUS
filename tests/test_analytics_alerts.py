import unittest

from analytics.alerts import PreventiveAlertService
from analytics.models import ConsumptionMeasurement, EnvironmentMeasurement, QualityMeasurement
from analytics.trends import TrendAnalyzer


class PreventiveAlertServiceTests(unittest.TestCase):
    def test_alerts_use_preventive_language_for_out_of_range_quality(self):
        quality = [QualityMeasurement(None, 5.5, 1.0, 6.0, 25.0, 0.0)]
        environment = []
        consumption = []
        trends = TrendAnalyzer().quality_trends(quality)

        alerts = PreventiveAlertService().build_alerts(quality, environment, consumption, trends, [])

        self.assertTrue(alerts)
        self.assertEqual("medio", alerts[0].severity)
        self.assertIn("Atencao preventiva", alerts[0].message)
        self.assertIn("Valor atual 5.5000", alerts[0].evidence)
        self.assertIn("catalogo:limite_observacional", alerts[0].evidence)

    def test_alerts_report_critical_status_from_observational_engine(self):
        quality = [QualityMeasurement(None, 7.0, 100.0, 6.0, 25.0, 0.0)]
        trends = TrendAnalyzer().quality_trends(quality)

        alerts = PreventiveAlertService().build_alerts(quality, [], [], trends, [])

        turbidity_alert = next(alert for alert in alerts if alert.metric == "turbidez")
        self.assertEqual("alto", turbidity_alert.severity)
        self.assertIn("avaliacao observacional critica", turbidity_alert.message)

    def test_alerts_combine_rain_and_rising_turbidity(self):
        quality = [
            QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0),
            QualityMeasurement(None, 7.0, 4.0, 6.0, 25.0, 0.0),
        ]
        environment = [EnvironmentMeasurement(None, 25.0, 90.0, 25.0, 1010.0)]
        consumption = [ConsumptionMeasurement(None, 10.0, 300.0, 350.0, 5.0)]
        quality_trends = TrendAnalyzer().quality_trends(quality)
        consumption_trends = TrendAnalyzer().consumption_trends(consumption)

        alerts = PreventiveAlertService().build_alerts(
            quality,
            environment,
            consumption,
            quality_trends,
            consumption_trends,
        )

        rain_alert = next(alert for alert in alerts if alert.domain == "dados_ambientais")
        self.assertEqual("medio", rain_alert.severity)
        self.assertIn("25.00 mm", rain_alert.evidence)


if __name__ == "__main__":
    unittest.main()
