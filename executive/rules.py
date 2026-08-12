from .models import (
    EXECUTIVE_ATTENTION,
    EXECUTIVE_CRITICAL,
    EXECUTIVE_NORMAL,
    ExecutivePriority,
    ExecutiveTrendSummary,
)
from monitoramento_hidrico.status_semantics import WATER_HEALTH_SCORE_NO_DATA


ACTIVE_EVENT_STATES = {"ABERTO", "MONITORAMENTO"}
RISK_TRENDS = {
    "turbidez": "subindo",
    "agrotoxicos": "subindo",
    "oxigenio_dissolvido": "caindo",
    "perdas_estimadas": "subindo",
}
SEVERITY_ORDER = {"alto": 0, "medio": 1, "baixo": 2}


class ExecutiveRules:
    def classify_status(self, analytics_snapshot, events):
        score = analytics_snapshot.water_health_score.score
        score_status = analytics_snapshot.water_health_score.status
        active_events = [event for event in events if event.state in ACTIVE_EVENT_STATES]
        high_active_events = [event for event in active_events if event.severity == "alto"]
        high_alerts = [alert for alert in analytics_snapshot.alerts if alert.severity == "alto"]

        explanations = []
        if score_status == WATER_HEALTH_SCORE_NO_DATA:
            return EXECUTIVE_ATTENTION, [
                "Water Health Score sem dados; coletar mais medicoes antes da classificacao executiva."
            ]

        if score < 50:
            explanations.append(f"Water Health Score {score}/100 abaixo de 50.")
        if high_active_events:
            explanations.append(f"{len(high_active_events)} evento(s) ativo(s) com severidade alto.")
        if len(active_events) >= 3:
            explanations.append(f"{len(active_events)} evento(s) ativo(s) em acompanhamento.")
        if len(high_alerts) >= 2:
            explanations.append(f"{len(high_alerts)} alerta(s) preventivo(s) alto.")

        if explanations:
            return EXECUTIVE_CRITICAL, explanations

        medium_or_high_alerts = [
            alert for alert in analytics_snapshot.alerts if alert.severity in ("medio", "alto")
        ]
        risk_trends = self.select_key_trends(analytics_snapshot)

        if 50 <= score <= 69:
            explanations.append(f"Water Health Score {score}/100 em faixa de atencao.")
        if active_events:
            explanations.append(f"{len(active_events)} evento(s) ativo(s) para acompanhamento.")
        if medium_or_high_alerts:
            explanations.append(f"{len(medium_or_high_alerts)} alerta(s) preventivo(s) medio/alto.")
        if risk_trends:
            explanations.append(f"{len(risk_trends)} tendencia(s) de risco observacional.")

        if explanations:
            return EXECUTIVE_ATTENTION, explanations

        return EXECUTIVE_NORMAL, ["Estado geral observacional sem sinais executivos prioritarios."]

    def executive_message(self, executive_status):
        if executive_status == EXECUTIVE_CRITICAL:
            return "Ha concentracao de sinais preventivos relevantes para acompanhamento prioritario."
        if executive_status == EXECUTIVE_ATTENTION:
            return "Ha sinais preventivos que merecem acompanhamento."
        return "Estado geral observacional dentro do esperado."

    def select_relevant_alerts(self, alerts, limit=5):
        ordered = sorted(alerts, key=lambda alert: SEVERITY_ORDER.get(alert.severity, 9))
        return ordered[:limit]

    def select_key_trends(self, analytics_snapshot, limit=5):
        trends = analytics_snapshot.quality_trends + analytics_snapshot.consumption_trends
        selected = []
        for trend in trends:
            if trend.direction == RISK_TRENDS.get(trend.metric):
                selected.append(
                    ExecutiveTrendSummary(
                        domain=trend.domain,
                        metric=trend.metric,
                        direction=trend.direction,
                        explanation=trend.explanation,
                    )
                )
        return selected[:limit]

    def build_priorities(self, analytics_snapshot, events, relevant_alerts, key_trends, limit=6):
        priorities = []
        active_events = [event for event in events if event.state in ACTIVE_EVENT_STATES]
        ordered_events = sorted(active_events, key=lambda event: SEVERITY_ORDER.get(event.severity, 9))

        for event in ordered_events:
            priorities.append(
                ExecutivePriority(
                    level=event.severity,
                    title=f"Evento em acompanhamento: {event.metric}",
                    evidence=event.evidence,
                    recommendation=event.recommendation,
                    source="governance",
                )
            )

        for alert in relevant_alerts:
            priorities.append(
                ExecutivePriority(
                    level=alert.severity,
                    title=f"Alerta preventivo: {alert.metric}",
                    evidence=alert.evidence,
                    recommendation=alert.recommendation,
                    source="analytics",
                )
            )

        for trend in key_trends:
            priorities.append(
                ExecutivePriority(
                    level="baixo",
                    title=f"Tendencia observacional: {trend.metric}",
                    evidence=trend.explanation,
                    recommendation="Acompanhar se a tendencia permanece nas proximas medicoes.",
                    source="analytics",
                )
            )

        return priorities[:limit]
