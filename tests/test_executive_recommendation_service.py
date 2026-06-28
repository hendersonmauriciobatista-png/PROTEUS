import inspect
import unittest

from analytics.models import AnalyticsSnapshot, WaterHealthScore
from executive_recommendation import ExecutiveRecommendationService
from executive_recommendation.models import RecommendationAction, RecommendationPriority
import executive_recommendation.service as recommendation_service_module


def analytics_snapshot_with_score(score):
    return AnalyticsSnapshot(
        quality_trends=[],
        consumption_trends=[],
        alerts=[],
        water_health_score=WaterHealthScore(score=score, status="", explanations=[]),
    )


class ExecutiveRecommendationServiceTests(unittest.TestCase):
    def test_score_greater_or_equal_90_maintains_routine_monitoring(self):
        snapshot = ExecutiveRecommendationService().build_snapshot(
            analytics_snapshot=analytics_snapshot_with_score(95)
        )

        recommendation = snapshot.recommendations[0]

        self.assertEqual(RecommendationPriority.LOW, recommendation.priority)
        self.assertEqual(
            RecommendationAction.MAINTAIN_ROUTINE_MONITORING,
            recommendation.action,
        )
        self.assertEqual("Manter monitoramento rotineiro.", recommendation.recommendation)

    def test_score_between_70_and_89_increases_monitoring_frequency(self):
        snapshot = ExecutiveRecommendationService().build_snapshot(
            analytics_snapshot=analytics_snapshot_with_score(82)
        )

        recommendation = snapshot.recommendations[0]

        self.assertEqual(RecommendationPriority.MEDIUM, recommendation.priority)
        self.assertEqual(
            RecommendationAction.INCREASE_MONITORING_FREQUENCY,
            recommendation.action,
        )
        self.assertEqual("Aumentar frequencia de monitoramento.", recommendation.recommendation)

    def test_score_below_70_executes_operational_inspection(self):
        snapshot = ExecutiveRecommendationService().build_snapshot(
            analytics_snapshot=analytics_snapshot_with_score(54)
        )

        recommendation = snapshot.recommendations[0]

        self.assertEqual(RecommendationPriority.HIGH, recommendation.priority)
        self.assertEqual(
            RecommendationAction.EXECUTE_OPERATIONAL_INSPECTION,
            recommendation.action,
        )
        self.assertEqual("Executar inspecao operacional.", recommendation.recommendation)

    def test_missing_score_collects_more_data(self):
        snapshot = ExecutiveRecommendationService().build_snapshot(analytics_snapshot=None)

        recommendation = snapshot.recommendations[0]

        self.assertEqual(RecommendationPriority.UNKNOWN, recommendation.priority)
        self.assertEqual(RecommendationAction.COLLECT_MORE_DATA, recommendation.action)
        self.assertEqual(
            "Coletar mais dados antes de recomendar acao operacional.",
            recommendation.recommendation,
        )

    def test_service_preserves_pa_01_boundaries(self):
        source = inspect.getsource(recommendation_service_module)

        self.assertNotIn("import csv", source.lower())
        self.assertNotIn("from csv", source.lower())
        self.assertNotIn("from monitoramento_hidrico", source)
        self.assertNotIn("import monitoramento_hidrico", source)
        self.assertNotIn("PolicyEngine(", source)
        self.assertNotIn("AvaliacaoObservacionalService(", source)

        snapshot = ExecutiveRecommendationService().build_snapshot(
            analytics_snapshot={"water_health_score": {"score": 91}},
            governance_snapshot={"ABERTO": 0},
            observational_result={"status": "NORMAL"},
        )

        self.assertTrue(snapshot.recommendations[0].evidence)
        self.assertTrue(any("PA-01 preservado" in item for item in snapshot.explanations))


if __name__ == "__main__":
    unittest.main()
