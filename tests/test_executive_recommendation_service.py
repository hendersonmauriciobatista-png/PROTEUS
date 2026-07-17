import inspect
import unittest

from analytics.models import AnalyticsSnapshot, PreventiveAlert, TrendResult, WaterHealthScore
from executive_recommendation import ExecutiveRecommendationService
from executive_recommendation.models import RecommendationAction, RecommendationPriority
import executive_recommendation.service as recommendation_service_module
from monitoramento_hidrico.status_semantics import WATER_HEALTH_SCORE_GOOD


def analytics_snapshot_with_score(score, alerts=None, trends=None, explanations=None):
    trends = trends or []
    return AnalyticsSnapshot(
        quality_trends=trends,
        consumption_trends=[],
        alerts=alerts or [],
        water_health_score=WaterHealthScore(score=score, status=WATER_HEALTH_SCORE_GOOD, explanations=explanations or []),
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
        self.assertIsNotNone(recommendation.confidence)

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

    def test_recommendation_uses_consolidated_alerts_trends_and_governance_as_context(self):
        alerts = [
            PreventiveAlert(
                severity="medio",
                domain="qualidade_agua",
                metric="turbidez",
                message="Atencao preventiva",
                evidence="Valor atual 2.0000",
                recommendation="Acompanhar novas medicoes.",
            )
        ]
        trends = [
            TrendResult(
                domain="qualidade_agua",
                metric="turbidez",
                direction="subindo",
                previous_average=1.0,
                recent_average=2.0,
                delta=1.0,
                explanation="Turbidez em tendencia de alta ja consolidada.",
            )
        ]

        snapshot = ExecutiveRecommendationService().build_snapshot(
            analytics_snapshot=analytics_snapshot_with_score(
                82,
                alerts=alerts,
                trends=trends,
                explanations=["Score calculado com sinais consolidados."],
            ),
            governance_snapshot={"ABERTO": 1, "MONITORAMENTO": 1, "RESOLVIDO": 0, "ARQUIVADO": 0},
        )

        recommendation = snapshot.recommendations[0]
        evidence_metrics = [evidence.metric for evidence in recommendation.evidence]

        self.assertEqual(RecommendationPriority.MEDIUM, recommendation.priority)
        self.assertEqual(RecommendationAction.INCREASE_MONITORING_FREQUENCY, recommendation.action)
        self.assertIn("alerta(s) preventivo(s)", recommendation.rationale)
        self.assertIn("evento(s) ativo(s)", recommendation.rationale)
        self.assertIn("preventive_alerts", evidence_metrics)
        self.assertIn("trends", evidence_metrics)
        self.assertIn("governance_snapshot", evidence_metrics)
        self.assertGreaterEqual(recommendation.confidence, 0.95)

    def test_recommendation_evidence_has_traceability_to_consolidated_origins(self):
        alerts = [
            PreventiveAlert(
                severity="alto",
                domain="qualidade_agua",
                metric="ph",
                message="Atencao preventiva",
                evidence="Valor atual 5.5000",
                recommendation="Acompanhar novas medicoes.",
            )
        ]
        trends = [
            TrendResult(
                domain="qualidade_agua",
                metric="ph",
                direction="descendo",
                previous_average=7.0,
                recent_average=5.5,
                delta=-1.5,
                explanation="pH em tendencia de queda ja consolidada.",
            )
        ]

        snapshot = ExecutiveRecommendationService().build_snapshot(
            analytics_snapshot=analytics_snapshot_with_score(
                64,
                alerts=alerts,
                trends=trends,
                explanations=["Score penalizado por sinal observacional consolidado."],
            ),
            governance_snapshot={"ABERTO": 1, "MONITORAMENTO": 0},
            observational_result={
                "policy_id": "politica-ph",
                "observational_status": "ATENCAO",
                "observational_severity": "media",
                "limit_origin": "catalogo:limite_observacional",
                "explainability": "resultado ATENCAO ja consolidado",
            },
        )

        evidence = snapshot.recommendations[0].evidence
        trace_pairs = {(item.origin_layer, item.origin_artifact) for item in evidence}

        self.assertIn(("Analytics", "WaterHealthScore"), trace_pairs)
        self.assertIn(("Analytics", "PreventiveAlert"), trace_pairs)
        self.assertIn(("Analytics", "TrendResult"), trace_pairs)
        self.assertIn(("Operational Governance", "governance_snapshot"), trace_pairs)
        self.assertIn(("Nucleo Hidrologico", "observational_result"), trace_pairs)
        self.assertTrue(all(item.origin_reference for item in evidence))
        self.assertTrue(
            any("policy_id" in item.origin_reference for item in evidence if item.source == "observational_core_result")
        )

    def test_recommendation_evidence_traceability_is_contractual_and_backward_compatible(self):
        snapshot = ExecutiveRecommendationService().build_snapshot(
            analytics_snapshot=analytics_snapshot_with_score(91)
        )

        evidence = snapshot.recommendations[0].evidence[0]

        self.assertEqual("analytics", evidence.source)
        self.assertEqual("water_health_score", evidence.metric)
        self.assertEqual(91, evidence.value)
        self.assertEqual("Analytics", evidence.origin_layer)
        self.assertEqual("WaterHealthScore", evidence.origin_artifact)
        self.assertEqual("analytics_snapshot.water_health_score.score", evidence.origin_reference)


if __name__ == "__main__":
    unittest.main()
