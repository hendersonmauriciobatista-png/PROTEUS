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
                    metric="agrotoxicos",
                    message="Atencao preventiva",
                    evidence="Valor atual 0.0800",
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


if __name__ == "__main__":
    unittest.main()
