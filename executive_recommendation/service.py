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
        priority, action, recommendation_text, rationale = self.rules.evaluate_water_health_score(score)
        evidence = self._build_evidence(score, analytics_snapshot, governance_snapshot, observational_result)

        recommendation = ExecutiveRecommendation(
            recommendation_id="water-health-score-primary",
            priority=priority,
            action=action,
            recommendation=recommendation_text,
            rationale=rationale,
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

    def _build_evidence(self, score, analytics_snapshot, governance_snapshot, observational_result):
        evidence = []

        if score is not None:
            evidence.append(
                RecommendationEvidence(
                    source="analytics",
                    metric="water_health_score",
                    value=score,
                    description=f"Water Health Score consolidado: {score}/100.",
                )
            )
        else:
            evidence.append(
                RecommendationEvidence(
                    source="analytics",
                    metric="water_health_score",
                    value=None,
                    description="Water Health Score nao disponivel em sinal consolidado.",
                )
            )

        if governance_snapshot is not None:
            evidence.append(
                RecommendationEvidence(
                    source="governance",
                    metric="governance_snapshot",
                    value=None,
                    description="Snapshot de governanca recebido como contexto consolidado.",
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
                )
            )

        return evidence

    def _read_field(self, source, field_name):
        if isinstance(source, dict):
            return source.get(field_name)
        return getattr(source, field_name, None)

    def _coerce_score(self, value):
        if value is None:
            return None
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
