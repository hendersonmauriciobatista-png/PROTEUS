import unittest

from analytics.models import ConsumptionMeasurement, EnvironmentMeasurement, QualityMeasurement
from analytics.scoring import QUALITY_SCORE_WEIGHTS, WaterHealthScoreCalculator
from monitoramento_hidrico.status_semantics import (
    WATER_HEALTH_SCORE_ATTENTION,
    WATER_HEALTH_SCORE_CRITICAL,
    WATER_HEALTH_SCORE_EXCELLENT,
    WATER_HEALTH_SCORE_GOOD,
    WATER_HEALTH_SCORE_NO_DATA,
    WATER_HEALTH_SCORE_VERY_CRITICAL,
)


class WaterHealthScoreCalculatorTests(unittest.TestCase):
    def test_no_measurements_returns_zero_with_no_data_semantics(self):
        score = WaterHealthScoreCalculator().calculate([], [], [])

        self.assertEqual(0, score.score)
        self.assertEqual(WATER_HEALTH_SCORE_NO_DATA, score.status)

    def test_score_is_high_when_latest_quality_is_within_limits(self):
        score = WaterHealthScoreCalculator().calculate(
            [QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0)],
            [],
            [],
        )

        self.assertEqual(100, score.score)
        self.assertEqual(WATER_HEALTH_SCORE_EXCELLENT, score.status)
        self.assertTrue(score.explanations)
        self.assertTrue(any("avaliacao observacional" in explanation for explanation in score.explanations))

    def test_score_stays_between_zero_and_one_hundred(self):
        score = WaterHealthScoreCalculator().calculate(
            [QualityMeasurement(None, 0.0, 100.0, 0.0, 60.0, 10.0)],
            [EnvironmentMeasurement(None, 25.0, 90.0, 100.0, 1010.0)],
            [ConsumptionMeasurement(None, 10.0, 300.0, 350.0, 80.0)],
        )

        self.assertGreaterEqual(score.score, 0)
        self.assertLessEqual(score.score, 100)
        self.assertIn(
            score.status,
            [
                WATER_HEALTH_SCORE_EXCELLENT,
                WATER_HEALTH_SCORE_GOOD,
                WATER_HEALTH_SCORE_ATTENTION,
                WATER_HEALTH_SCORE_CRITICAL,
                WATER_HEALTH_SCORE_VERY_CRITICAL,
            ],
        )

    def test_score_uses_observational_results_for_quality_penalties(self):
        score = WaterHealthScoreCalculator().calculate(
            [QualityMeasurement(None, 7.0, 100.0, 6.0, 25.0, 0.0)],
            [],
            [],
        )

        self.assertLess(score.score, 100)
        self.assertTrue(any("avaliacao observacional critica" in explanation for explanation in score.explanations))
        self.assertFalse(any("faixa configurada" in explanation for explanation in score.explanations))

    def test_score_exclui_parametro_descontinuado(self):
        calculator = WaterHealthScoreCalculator()
        measurement_a = QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 0.0)
        measurement_b = QualityMeasurement(None, 7.0, 1.0, 6.0, 25.0, 999999.0)

        resultados = {
            item["parametro_id"]: item["resultado"].status
            for item in calculator.monitoring_adapter.avaliar_qualidade(measurement_a)
        }
        score_a = calculator.calculate([measurement_a], [], [])
        score_b = calculator.calculate([measurement_b], [], [])

        self.assertEqual("NAO_AVALIAVEL", resultados["temperatura_agua"])
        self.assertNotIn("agrotoxicos", resultados)
        self.assertNotIn("agrotoxicos", QUALITY_SCORE_WEIGHTS)
        self.assertEqual(score_a.score, score_b.score)
        self.assertEqual(score_a.explanations, score_b.explanations)
        self.assertTrue(
            any("Temperatura da agua sem avaliacao observacional aplicavel ao score" in item for item in score_a.explanations)
        )
        self.assertFalse(any("Agrotoxicos" in item for item in score_a.explanations))


if __name__ == "__main__":
    unittest.main()
