from datetime import datetime

from .models import ExecutiveRecommendation, RecommendationEvidence, RecommendationSnapshot
from .rules import ExecutiveRecommendationRules


class ExecutiveRecommendationService:
    """
    Deterministic recommendation layer.

    PA-01 is preserved here by consuming only consolidated signals. This service
    does not select policies, execute observational evaluations, read CSV files,
    or recalculate hydric observational status.
    """

    def __init__(self, rules=None):
        self.rules = rules or ExecutiveRecommendationRules()

    def build_snapshot(
        self,
        analytics_snapshot=None,
        governance_snapshot=None,
        observational_result=None,
    ):
        score = self._extract_water_health_score(analytics_snapshot)
        score_status = self._extract_water_health_status(analytics_snapshot)
        priority, action, recommendation_text, rationale = self.rules.evaluate_water_health_score(
            score,
            score_status,
        )
        evidence = self._build_evidence(score, analytics_snapshot, governance_snapshot, observational_result)
        rationale = self._enrich_rationale(rationale, analytics_snapshot, governance_snapshot)
        confidence = self._calculate_confidence(score, analytics_snapshot, governance_snapshot, observational_result)

        recommendation = ExecutiveRecommendation(
            recommendation_id="water-health-score-primary",
            priority=priority,
            action=action,
            recommendation=recommendation_text,
            rationale=rationale,
            confidence=confidence,
            evidence=evidence,
        )

        return RecommendationSnapshot(
            generated_at=datetime.now(),
            recommendations=[recommendation],
            explanations=[
                "PA-01 preservado: recomendacao gerada apenas a partir de sinais consolidados.",
                "Nenhum CSV, PolicyEngine, AvaliacaoObservacionalService ou Nucleo de Monitoramento Hidrico foi acessado.",
            ],
        )

    def _extract_water_health_score(self, analytics_snapshot):
        if analytics_snapshot is None:
            return None

        water_health_score = self._read_field(analytics_snapshot, "water_health_score")
        if water_health_score is None:
            return self._coerce_score(self._read_field(analytics_snapshot, "score"))

        if isinstance(water_health_score, (int, float)):
            return self._coerce_score(water_health_score)

        return self._coerce_score(self._read_field(water_health_score, "score"))

    def _extract_water_health_status(self, analytics_snapshot):
        water_health_score = self._read_field(analytics_snapshot, "water_health_score")
        return self._read_field(water_health_score, "status")

    def _build_evidence(self, score, analytics_snapshot, governance_snapshot, observational_result):
        evidence = []
        water_health_score = self._read_field(analytics_snapshot, "water_health_score")

        if score is not None:
            evidence.append(
                RecommendationEvidence(
                    source="analytics",
                    metric="water_health_score",
                    value=score,
                    description=f"Water Health Score consolidado: {score}/100.",
                    origin_layer="Analytics",
                    origin_artifact="WaterHealthScore",
                    origin_reference="analytics_snapshot.water_health_score.score",
                )
            )
            status = self._read_field(water_health_score, "status")
            if status:
                evidence.append(
                    RecommendationEvidence(
                        source="analytics",
                        metric="water_health_status",
                        value=None,
                        description=f"Status consolidado do Water Health Score: {status}.",
                        origin_layer="Analytics",
                        origin_artifact="WaterHealthScore",
                        origin_reference="analytics_snapshot.water_health_score.status",
                    )
                )
            for index, explanation in enumerate(self._read_list(water_health_score, "explanations")[:3]):
                evidence.append(
                    RecommendationEvidence(
                        source="analytics",
                        metric="water_health_score_explanation",
                        value=None,
                        description=explanation,
                        origin_layer="Analytics",
                        origin_artifact="WaterHealthScore",
                        origin_reference=f"analytics_snapshot.water_health_score.explanations[{index}]",
                    )
                )
        else:
            evidence.append(
                RecommendationEvidence(
                    source="analytics",
                    metric="water_health_score",
                    value=None,
                    description="Water Health Score nao disponivel em sinal consolidado.",
                    origin_layer="Analytics",
                    origin_artifact="AnalyticsSnapshot",
                    origin_reference="analytics_snapshot.water_health_score",
                )
            )

        alerts = self._read_list(analytics_snapshot, "alerts")
        if alerts:
            severities = self._count_by_field(alerts, "severity")
            evidence.append(
                RecommendationEvidence(
                    source="analytics",
                    metric="preventive_alerts",
                    value=len(alerts),
                    description=f"{len(alerts)} alerta(s) preventivo(s) consolidado(s): {self._format_counts(severities)}.",
                    origin_layer="Analytics",
                    origin_artifact="AnalyticsSnapshot.alerts",
                    origin_reference="analytics_snapshot.alerts",
                )
            )
            for index, alert in enumerate(alerts[:3]):
                evidence.append(
                    RecommendationEvidence(
                        source="analytics",
                        metric=self._read_field(alert, "metric") or "alert",
                        value=None,
                        description=self._format_alert_evidence(alert),
                        origin_layer="Analytics",
                        origin_artifact="PreventiveAlert",
                        origin_reference=f"analytics_snapshot.alerts[{index}]",
                    )
                )

        quality_trends = self._read_list(analytics_snapshot, "quality_trends")
        consumption_trends = self._read_list(analytics_snapshot, "consumption_trends")
        trends = quality_trends + consumption_trends
        if trends:
            directions = self._count_by_field(trends, "direction")
            evidence.append(
                RecommendationEvidence(
                    source="analytics",
                    metric="trends",
                    value=len(trends),
                    description=f"{len(trends)} tendencia(s) consolidada(s): {self._format_counts(directions)}.",
                    origin_layer="Analytics",
                    origin_artifact="AnalyticsSnapshot.trends",
                    origin_reference="analytics_snapshot.quality_trends + analytics_snapshot.consumption_trends",
                )
            )
            trend_entries = [
                (trend, f"analytics_snapshot.quality_trends[{index}]")
                for index, trend in enumerate(quality_trends)
            ] + [
                (trend, f"analytics_snapshot.consumption_trends[{index}]")
                for index, trend in enumerate(consumption_trends)
            ]
            for trend, origin_reference in trend_entries[:3]:
                evidence.append(
                    RecommendationEvidence(
                        source="analytics",
                        metric=self._read_field(trend, "metric") or "trend",
                        value=None,
                        description=self._read_field(trend, "explanation")
                        or "Tendencia consolidada sem explicacao textual.",
                        origin_layer="Analytics",
                        origin_artifact="TrendResult",
                        origin_reference=origin_reference,
                    )
                )

        if governance_snapshot is not None:
            active_events = self._governance_count(governance_snapshot, "ABERTO") + self._governance_count(
                governance_snapshot, "MONITORAMENTO"
            )
            evidence.append(
                RecommendationEvidence(
                    source="governance",
                    metric="governance_snapshot",
                    value=active_events,
                    description=(
                        "Resumo de governanca consolidado recebido: "
                        f"{self._format_governance_snapshot(governance_snapshot)}."
                    ),
                    origin_layer="Operational Governance",
                    origin_artifact="governance_snapshot",
                    origin_reference="governance_snapshot",
                )
            )

        if observational_result is not None:
            observational_status = self._read_field(observational_result, "observational_status")
            if observational_status is None:
                observational_status = self._read_field(observational_result, "status")
            description = "Resultado observacional recebido como contexto consolidado."
            if observational_status:
                description = f"Resultado observacional consolidado recebido: {observational_status}."
            evidence.append(
                RecommendationEvidence(
                    source="observational_core_result",
                    metric="observational_status",
                    value=None,
                    description=description,
                    origin_layer="Nucleo Hidrologico",
                    origin_artifact="observational_result",
                    origin_reference=self._observational_origin_reference(observational_result),
                )
            )

        return evidence

    def _observational_origin_reference(self, observational_result):
        references = []
        for field_name in (
            "policy_id",
            "policy_name",
            "observational_status",
            "status",
            "observational_severity",
            "severity",
            "limit_origin",
            "explainability",
        ):
            if self._read_field(observational_result, field_name):
                references.append(field_name)
        if not references:
            return "observational_result"
        return "observational_result." + "|".join(references)

    def _enrich_rationale(self, rationale, analytics_snapshot, governance_snapshot):
        details = []
        alerts = self._read_list(analytics_snapshot, "alerts")
        trends = self._read_list(analytics_snapshot, "quality_trends") + self._read_list(
            analytics_snapshot, "consumption_trends"
        )

        if alerts:
            details.append(f"{len(alerts)} alerta(s) preventivo(s) ja consolidado(s)")
        if trends:
            details.append(f"{len(trends)} tendencia(s) ja consolidada(s)")
        if governance_snapshot is not None:
            active_events = self._governance_count(governance_snapshot, "ABERTO") + self._governance_count(
                governance_snapshot, "MONITORAMENTO"
            )
            details.append(f"{active_events} evento(s) ativo(s) em governanca")

        if not details:
            return rationale

        return f"{rationale} Contexto executivo considerado: {', '.join(details)}."

    def _calculate_confidence(self, score, analytics_snapshot, governance_snapshot, observational_result):
        confidence = 0.35
        if score is not None:
            confidence += 0.30
        if self._read_list(self._read_field(analytics_snapshot, "water_health_score"), "explanations"):
            confidence += 0.10
        if self._read_list(analytics_snapshot, "alerts"):
            confidence += 0.10
        if self._read_list(analytics_snapshot, "quality_trends") or self._read_list(
            analytics_snapshot, "consumption_trends"
        ):
            confidence += 0.10
        if governance_snapshot is not None:
            confidence += 0.05
        if observational_result is not None:
            confidence += 0.05

        return min(0.95, round(confidence, 2))

    def _read_field(self, source, field_name):
        if isinstance(source, dict):
            return source.get(field_name)
        return getattr(source, field_name, None)

    def _read_list(self, source, field_name):
        value = self._read_field(source, field_name)
        if value is None:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, tuple):
            return list(value)
        if isinstance(value, set):
            return sorted(value)
        return [value]

    def _coerce_score(self, value):
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    def _count_by_field(self, items, field_name):
        counts = {}
        for item in items:
            value = self._read_field(item, field_name) or "desconhecido"
            counts[value] = counts.get(value, 0) + 1
        return counts

    def _format_counts(self, counts):
        return ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))

    def _format_alert_evidence(self, alert):
        severity = self._read_field(alert, "severity") or "sem severidade"
        message = self._read_field(alert, "message") or "Alerta preventivo consolidado."
        evidence = self._read_field(alert, "evidence") or "Sem evidencia textual."
        return f"{severity}: {message} Evidencia: {evidence}"

    def _governance_count(self, governance_snapshot, state):
        return self._coerce_score(self._read_field(governance_snapshot, state)) or 0

    def _format_governance_snapshot(self, governance_snapshot):
        if isinstance(governance_snapshot, dict):
            return self._format_counts(governance_snapshot)
        return str(governance_snapshot)
