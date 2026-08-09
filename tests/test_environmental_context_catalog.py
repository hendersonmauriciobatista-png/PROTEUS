import csv
import unittest
from dataclasses import fields
from pathlib import Path

from analytics.alerts import PreventiveAlertService
from analytics.models import EnvironmentMeasurement, QualityMeasurement
from analytics.rain_thresholds import RAIN_CONTEXT_HIGH_THRESHOLD, RAIN_CONTEXT_MONITORING_THRESHOLD
from analytics.scoring import WaterHealthScoreCalculator
from analytics.trends import TrendAnalyzer
from monitoramento_hidrico import load_parametros_ambientais_contextuais, load_parametros_hidricos


ENVIRONMENTAL_CONTEXT_CODES = {
    "temperatura_ambiente",
    "umidade_relativa",
    "chuva",
    "pressao_atmosferica",
}


class EnvironmentalContextCatalogTests(unittest.TestCase):
    def _quality(self):
        return [QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0)]

    def _environment(self, rain):
        return [EnvironmentMeasurement(None, 25.0, 70.0, rain, 1013.25)]

    def test_environmental_catalog_maps_numeric_csv_schema(self):
        parameters = load_parametros_ambientais_contextuais()
        codes = {parameter.codigo for parameter in parameters}
        model_fields = {item.name for item in fields(EnvironmentMeasurement)}

        with Path("data/dados_ambientais_medicoes.csv").open(newline="", encoding="utf-8") as file:
            csv_fields = set(next(csv.reader(file)))

        self.assertEqual(ENVIRONMENTAL_CONTEXT_CODES, codes)
        self.assertTrue(codes.issubset(model_fields))
        self.assertTrue(codes.issubset(csv_fields))
        self.assertIn("timestamp", model_fields & csv_fields)
        self.assertIn("observacao", model_fields & csv_fields)
        self.assertTrue(all(parameter.autoridade == "contexto" for parameter in parameters))

    def test_environmental_and_hydric_codes_do_not_duplicate(self):
        environmental_codes = {item.codigo for item in load_parametros_ambientais_contextuais()}
        hydric_codes = {item.codigo for item in load_parametros_hidricos()}

        self.assertFalse(environmental_codes & hydric_codes)

    def test_environmental_parameters_have_no_hydric_limit_or_policy_fields(self):
        catalog_source = Path("monitoramento_hidrico/catalog.py").read_text(encoding="utf-8")
        policy_source = Path("monitoramento_hidrico/politicas.py").read_text(encoding="utf-8")
        environmental_fields = {item.name for item in fields(load_parametros_ambientais_contextuais()[0])}

        self.assertNotIn("limite_observacional", environmental_fields)
        self.assertNotIn("categoria", environmental_fields)
        self.assertNotIn("aplicabilidade_perfis", environmental_fields)
        self.assertNotIn("load_parametros_ambientais_contextuais", policy_source)
        self.assertNotIn("PolicyEngine", catalog_source)

    def test_rain_monitoring_boundary_controls_context_alert(self):
        quality = [
            QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0),
            QualityMeasurement(None, 7.0, 4.0, 6.0, 25.0, 0.0),
        ]
        trends = TrendAnalyzer().quality_trends(quality)
        service = PreventiveAlertService()

        below = service.build_alerts(quality, self._environment(19.99), [], trends, [])
        boundary = service.build_alerts(quality, self._environment(20.0), [], trends, [])

        self.assertEqual(20.0, RAIN_CONTEXT_MONITORING_THRESHOLD)
        self.assertFalse(any(alert.domain == "dados_ambientais" for alert in below))
        self.assertTrue(any(alert.domain == "dados_ambientais" for alert in boundary))

    def test_rain_score_boundaries_are_centralized(self):
        calculator = WaterHealthScoreCalculator()

        below = calculator.calculate(self._quality(), self._environment(19.99), [])
        monitoring = calculator.calculate(self._quality(), self._environment(20.0), [])
        below_high = calculator.calculate(self._quality(), self._environment(49.99), [])
        high = calculator.calculate(self._quality(), self._environment(50.0), [])

        self.assertEqual(50.0, RAIN_CONTEXT_HIGH_THRESHOLD)
        self.assertEqual(100, below.score)
        self.assertEqual(97, monitoring.score)
        self.assertEqual(97, below_high.score)
        self.assertEqual(95, high.score)


if __name__ == "__main__":
    unittest.main()
