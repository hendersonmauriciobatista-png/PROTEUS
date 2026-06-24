import unittest
from datetime import datetime

from analytics.models import AnalyticsSnapshot, PreventiveAlert, TrendResult, WaterHealthScore
from executive.models import EXECUTIVE_ATTENTION, EXECUTIVE_CRITICAL, EXECUTIVE_NORMAL
from executive.rules import ExecutiveRules
from governance.models import EventState, OperationalEvent


def make_snapshot(score=85, alerts=None, quality_trends=None, consumption_trends=None):
    return AnalyticsSnapshot(
        quality_trends=quality_trends or [],
        consumption_trends=consumption_trends or [],
        alerts=alerts or [],
        water_health_score=WaterHealthScore(score=score, status="Bom", explanations=[]),
    )


def make_event(state=EventState.ABERTO.value, severity="medio"):
    now = datetime(2026, 6, 23, 20, 0, 0)
    return OperationalEvent(
        event_id="evt-1",
        created_at=now,
        updated_at=now,
        closed_at=None,
        state=state,
        severity=severity,
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


class ExecutiveRulesTests(unittest.TestCase):
    def test_classifies_normal_when_no_priority_signal_exists(self):
        status, explanations = ExecutiveRules().classify_status(make_snapshot(score=90), [])

        self.assertEqual(EXECUTIVE_NORMAL, status)
        self.assertTrue(explanations)

    def test_classifies_critical_for_low_score(self):
        status, explanations = ExecutiveRules().classify_status(make_snapshot(score=49), [])

        self.assertEqual(EXECUTIVE_CRITICAL, status)
        self.assertIn("49/100", explanations[0])

    def test_classifies_critical_for_high_active_event(self):
        status, explanations = ExecutiveRules().classify_status(make_snapshot(score=90), [make_event(severity="alto")])

        self.assertEqual(EXECUTIVE_CRITICAL, status)
        self.assertIn("severidade alto", explanations[0])

    def test_classifies_attention_for_medium_alert(self):
        alert = PreventiveAlert(
            severity="medio",
            domain="qualidade_agua",
            metric="agrotoxicos",
            message="Atencao preventiva",
            evidence="Valor atual 0.0800",
            recommendation="Acompanhar novas medicoes.",
        )

        status, explanations = ExecutiveRules().classify_status(make_snapshot(score=90, alerts=[alert]), [])

        self.assertEqual(EXECUTIVE_ATTENTION, status)
        self.assertTrue(any("alerta" in explanation for explanation in explanations))

    def test_classifies_attention_for_risk_trend(self):
        trend = TrendResult(
            domain="qualidade_agua",
            metric="turbidez",
            direction="subindo",
            previous_average=1.0,
            recent_average=2.0,
            delta=1.0,
            explanation="Turbidez: media anterior 1.0000, media recente 2.0000.",
        )

        status, explanations = ExecutiveRules().classify_status(make_snapshot(score=90, quality_trends=[trend]), [])

        self.assertEqual(EXECUTIVE_ATTENTION, status)
        self.assertTrue(any("tendencia" in explanation for explanation in explanations))


if __name__ == "__main__":
    unittest.main()
