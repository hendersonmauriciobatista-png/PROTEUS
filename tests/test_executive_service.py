import unittest
from datetime import datetime

from analytics.models import AnalyticsSnapshot, PreventiveAlert, TrendResult, WaterHealthScore
from executive import ExecutiveIntelligenceService
from executive.models import EXECUTIVE_ATTENTION
from executive_recommendation.models import RecommendationPriority
from governance.models import EventState, OperationalEvent
from monitoramento_hidrico.status_semantics import WATER_HEALTH_SCORE_GOOD


class FakeAnalyticsService:
    def build_snapshot(self):
        return AnalyticsSnapshot(
            quality_trends=[
                TrendResult(
                    domain="qualidade_agua",
                    metric="turbidez",
                    direction="subindo",
                    previous_average=1.0,
                    recent_average=2.0,
                    delta=1.0,
                    explanation="Turbidez: media anterior 1.0000, media recente 2.0000.",
                )
            ],
            consumption_trends=[],
            alerts=[
                PreventiveAlert(
                    severity="medio",
                    domain="qualidade_agua",
                    metric="turbidez",
                    message="Atencao preventiva",
                    evidence="Valor atual 6.0000",
                    recommendation="Acompanhar novas medicoes.",
                )
            ],
            water_health_score=WaterHealthScore(score=82, status=WATER_HEALTH_SCORE_GOOD, explanations=[]),
        )


class FakeGovernanceService:
    def __init__(self):
        now = datetime(2026, 6, 23, 20, 0, 0)
        self.events = [
            OperationalEvent(
                event_id="evt-1",
                created_at=now,
                updated_at=now,
                closed_at=None,
                state=EventState.ABERTO.value,
                severity="medio",
                domain="qualidade_agua",
                metric="turbidez",
                fingerprint="abc",
                title="Acompanhamento preventivo",
                description="Atencao preventiva",
                evidence="Valor observado",
                recommendation="Acompanhar novas medicoes.",
                source="analytics",
                occurrence_count=1,
                last_seen_at=now,
            )
        ]

    def list_events(self):
        return list(self.events)

    def summarize_by_state(self):
        return {
            EventState.ABERTO.value: 1,
            EventState.MONITORAMENTO.value: 0,
            EventState.RESOLVIDO.value: 0,
            EventState.ARQUIVADO.value: 0,
        }


class OutOfScopeAnalyticsService:
    def __init__(self, metric):
        self.metric = metric

    def build_snapshot(self):
        return AnalyticsSnapshot(
            quality_trends=[
                TrendResult(
                    domain="qualidade_agua",
                    metric=self.metric,
                    direction="subindo",
                    previous_average=0.0,
                    recent_average=1.0,
                    delta=1.0,
                    explanation="Tendencia historica descontinuada.",
                )
            ],
            consumption_trends=[],
            alerts=[
                PreventiveAlert(
                    severity="alto",
                    domain="qualidade_agua",
                    metric=self.metric,
                    message="Alerta historico descontinuado.",
                    evidence="Evidencia historica.",
                    recommendation="Nenhuma acao operacional.",
                )
            ],
            water_health_score=WaterHealthScore(score=90, status=WATER_HEALTH_SCORE_GOOD, explanations=[]),
        )


class OutOfScopeGovernanceService:
    def __init__(self, metric):
        self.metric = metric

    def list_events(self):
        now = datetime(2026, 6, 23, 20, 0, 0)
        return [
            OperationalEvent(
                event_id="evt-out-of-scope",
                created_at=now,
                updated_at=now,
                closed_at=None,
                state=EventState.ABERTO.value,
                severity="alto",
                domain="qualidade_agua",
                metric=self.metric,
                fingerprint="out-of-scope",
                title="Sinal historico",
                description="Sinal descontinuado",
                evidence="Evidencia historica",
                recommendation="Nenhuma acao operacional.",
                source="historico",
                occurrence_count=1,
                last_seen_at=now,
            )
        ]

    def summarize_by_state(self):
        return {
            EventState.ABERTO.value: 1,
            EventState.MONITORAMENTO.value: 0,
            EventState.RESOLVIDO.value: 0,
            EventState.ARQUIVADO.value: 0,
        }


class ExecutiveIntelligenceServiceTests(unittest.TestCase):
    def test_build_snapshot_consolidates_public_services(self):
        service = ExecutiveIntelligenceService(
            analytics_service=FakeAnalyticsService(),
            governance_service=FakeGovernanceService(),
        )

        snapshot = service.build_snapshot()

        self.assertEqual(EXECUTIVE_ATTENTION, snapshot.executive_status)
        self.assertEqual(82, snapshot.water_health_score)
        self.assertEqual(1, snapshot.open_events)
        self.assertEqual(1, len(snapshot.relevant_alerts))
        self.assertEqual(1, len(snapshot.key_trends))
        self.assertTrue(snapshot.observational_priorities)
        self.assertIsNotNone(snapshot.recommendation_snapshot)
        self.assertEqual(1, len(snapshot.recommendation_snapshot.recommendations))
        self.assertEqual(
            RecommendationPriority.MEDIUM,
            snapshot.recommendation_snapshot.recommendations[0].priority,
        )
        self.assertIn("acompanhamento", snapshot.executive_message)

    def test_familia_fora_do_escopo_nao_alimenta_recomendacoes(self):
        for metric in ("agrotoxicos", "herbicidas", "fungicidas", "inseticidas"):
            with self.subTest(metric=metric):
                snapshot = ExecutiveIntelligenceService(
                    analytics_service=OutOfScopeAnalyticsService(metric),
                    governance_service=OutOfScopeGovernanceService(metric),
                ).build_snapshot()

                self.assertEqual([], snapshot.relevant_alerts)
                self.assertEqual([], snapshot.key_trends)
                self.assertEqual([], snapshot.observational_priorities)
                self.assertEqual(0, snapshot.open_events)
                recommendation = snapshot.recommendation_snapshot.recommendations[0]
                evidence_metrics = {item.metric for item in recommendation.evidence}
                self.assertNotIn(metric, evidence_metrics)
                self.assertNotIn("preventive_alerts", evidence_metrics)
                self.assertNotIn("trends", evidence_metrics)
                self.assertIn("0 evento(s) ativo(s)", recommendation.rationale)


if __name__ == "__main__":
    unittest.main()
