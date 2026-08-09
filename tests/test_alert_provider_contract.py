import inspect
import unittest
from pathlib import Path

from analytics import AlertProvider, AnalyticsService
from analytics.alerts import PreventiveAlertService
from analytics.models import (
    ConsumptionMeasurement,
    EnvironmentMeasurement,
    PreventiveAlert,
    QualityMeasurement,
    TrendResult,
    WaterHealthScore,
)
from analytics.trends import TrendAnalyzer


class FixedRepository:
    def __init__(self, quality, environment, consumption):
        self.quality = quality
        self.environment = environment
        self.consumption = consumption

    def load_quality(self):
        return self.quality

    def load_environment(self):
        return self.environment

    def load_consumption(self):
        return self.consumption


class FixedTrendAnalyzer:
    def __init__(self, quality_trends, consumption_trends):
        self._quality_trends = quality_trends
        self._consumption_trends = consumption_trends

    def quality_trends(self, quality):
        return self._quality_trends

    def consumption_trends(self, consumption):
        return self._consumption_trends


class FixedScoreCalculator:
    def calculate(self, quality, environment, consumption):
        return WaterHealthScore(score=100, status="EXCELENTE", explanations=[])


class RecordingAlertProvider:
    def __init__(self, alerts):
        self.alerts = alerts
        self.calls = []

    def build_alerts(self, quality, environment, consumption, quality_trends, consumption_trends):
        self.calls.append((quality, environment, consumption, quality_trends, consumption_trends))
        return list(self.alerts)


class AlertProviderContractTests(unittest.TestCase):
    def test_contract_forwards_inputs_and_invokes_provider_once(self):
        quality = [QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0)]
        environment = [EnvironmentMeasurement(None, 25.0, 70.0, 0.0, 1013.25)]
        consumption = [ConsumptionMeasurement(None, 10.0, 300.0, 350.0, 5.0)]
        quality_trends = [TrendResult("qualidade_agua", "ph", "estavel", 7.0, 7.0, 0.0, "estavel")]
        consumption_trends = [
            TrendResult("consumo_distribuicao", "consumo_diario", "estavel", 10.0, 10.0, 0.0, "estavel")
        ]
        alert = PreventiveAlert("baixo", "qualidade_agua", "ph", "mensagem", "evidencia", "recomendacao")
        provider = RecordingAlertProvider([alert])
        service = AnalyticsService(
            repository=FixedRepository(quality, environment, consumption),
            trend_analyzer=FixedTrendAnalyzer(quality_trends, consumption_trends),
            alert_service=provider,
            score_calculator=FixedScoreCalculator(),
        )

        snapshot = service.build_snapshot()

        self.assertEqual(1, len(provider.calls))
        self.assertEqual((quality, environment, consumption, quality_trends, consumption_trends), provider.calls[0])
        self.assertEqual([alert], snapshot.alerts)

    def test_default_provider_output_is_equivalent_to_direct_generation(self):
        quality = [
            QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0),
            QualityMeasurement(None, 7.0, 4.0, 6.0, 25.0, 0.0),
        ]
        environment = [EnvironmentMeasurement(None, 25.0, 90.0, 25.0, 1010.0)]
        consumption = [ConsumptionMeasurement(None, 10.0, 300.0, 350.0, 15.0)]
        trends = TrendAnalyzer()
        quality_trends = trends.quality_trends(quality)
        consumption_trends = trends.consumption_trends(consumption)
        expected = PreventiveAlertService().build_alerts(
            quality,
            environment,
            consumption,
            quality_trends,
            consumption_trends,
        )
        service = AnalyticsService(
            repository=FixedRepository(quality, environment, consumption),
            trend_analyzer=trends,
            score_calculator=FixedScoreCalculator(),
        )

        self.assertEqual(expected, service.build_snapshot().alerts)

    def test_protocol_has_only_generation_boundary(self):
        public_methods = {
            name
            for name, member in inspect.getmembers(AlertProvider, inspect.isfunction)
            if not name.startswith("_")
        }

        self.assertEqual({"build_alerts"}, public_methods)

    def test_analytics_service_has_no_parallel_provider_generation(self):
        source = Path("analytics/service.py").read_text(encoding="utf-8")

        self.assertEqual(1, source.count(".build_alerts("))
        self.assertEqual(1, source.count("PreventiveAlertService()"))

    def test_downstream_consumers_keep_analytics_snapshot_alerts_boundary(self):
        governance_source = Path("governance/service.py").read_text(encoding="utf-8")
        executive_source = Path("executive/service.py").read_text(encoding="utf-8")
        recommendation_source = Path("executive_recommendation/service.py").read_text(encoding="utf-8")
        administration_source = Path("administracao.py").read_text(encoding="utf-8")

        self.assertIn("snapshot.alerts", governance_source)
        self.assertIn("analytics_snapshot.alerts", executive_source)
        self.assertIn('self._read_list(analytics_snapshot, "alerts")', recommendation_source)
        self.assertIn("snapshot.alerts", administration_source)


if __name__ == "__main__":
    unittest.main()
