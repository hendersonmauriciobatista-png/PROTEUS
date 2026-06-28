from .models import RecommendationAction, RecommendationPriority


class ExecutiveRecommendationRules:
    def evaluate_water_health_score(self, score):
        if score is None:
            return (
                RecommendationPriority.UNKNOWN,
                RecommendationAction.COLLECT_MORE_DATA,
                "Coletar mais dados antes de recomendar acao operacional.",
                "Water Health Score ausente ou insuficiente.",
            )

        if score >= 90:
            return (
                RecommendationPriority.LOW,
                RecommendationAction.MAINTAIN_ROUTINE_MONITORING,
                "Manter monitoramento rotineiro.",
                f"Water Health Score {score}/100 em faixa >= 90.",
            )

        if 70 <= score <= 89:
            return (
                RecommendationPriority.MEDIUM,
                RecommendationAction.INCREASE_MONITORING_FREQUENCY,
                "Aumentar frequencia de monitoramento.",
                f"Water Health Score {score}/100 em faixa entre 70 e 89.",
            )

        return (
            RecommendationPriority.HIGH,
            RecommendationAction.EXECUTE_OPERATIONAL_INSPECTION,
            "Executar inspecao operacional.",
            f"Water Health Score {score}/100 abaixo de 70.",
        )
