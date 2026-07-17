from .models import WaterHealthScore
from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.analytics_adapter import (
    AnalyticsHydricMonitoringAdapter,
    resultado_nao_avaliavel,
    resultado_normal,
)
from monitoramento_hidrico.status_semantics import (
    WATER_HEALTH_SCORE_ATTENTION,
    WATER_HEALTH_SCORE_CRITICAL,
    WATER_HEALTH_SCORE_EXCELLENT,
    WATER_HEALTH_SCORE_GOOD,
    WATER_HEALTH_SCORE_NO_DATA,
    WATER_HEALTH_SCORE_VERY_CRITICAL,
    observational_status_label,
)


QUALITY_SCORE_WEIGHTS = {
    "ph": 18,
    "turbidez": 18,
    "oxigenio_dissolvido": 20,
    "temperatura": 10,
    "agrotoxicos": 22,
}


class WaterHealthScoreCalculator:
    def __init__(self, monitoring_adapter=None):
        self.monitoring_adapter = monitoring_adapter or AnalyticsHydricMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )

    def calculate(self, quality, environment, consumption):
        score = 100.0
        explanations = []

        if not quality:
            return WaterHealthScore(
                score=0,
                status=WATER_HEALTH_SCORE_NO_DATA,
                explanations=["Sem registros de qualidade da agua para calcular o score."],
            )

        latest_quality = quality[-1]
        score -= self._quality_penalties_from_observational_results(latest_quality, explanations)

        if consumption:
            latest_consumption = consumption[-1]
            if latest_consumption.perdas_estimadas >= 30.0:
                score -= 12
                explanations.append(
                    f"Perdas estimadas {latest_consumption.perdas_estimadas:.2f}% reduzem 12 pontos."
                )
            elif latest_consumption.perdas_estimadas >= 15.0:
                score -= 6
                explanations.append(
                    f"Perdas estimadas {latest_consumption.perdas_estimadas:.2f}% reduzem 6 pontos."
                )

        if environment:
            latest_environment = environment[-1]
            if latest_environment.chuva >= 50.0:
                score -= 5
                explanations.append(f"Chuva {latest_environment.chuva:.2f} mm reduz 5 pontos como contexto preventivo.")
            elif latest_environment.chuva >= 20.0:
                score -= 3
                explanations.append(f"Chuva {latest_environment.chuva:.2f} mm reduz 3 pontos como contexto preventivo.")

        final_score = max(0, min(100, round(score)))
        if not explanations:
            explanations.append("Ultima medicao de qualidade dentro dos limites configurados; sem penalidades aplicadas.")

        return WaterHealthScore(score=final_score, status=self._status(final_score), explanations=explanations)

    def _quality_penalties_from_observational_results(self, measurement, explanations):
        total_penalty = 0.0
        for item in self.monitoring_adapter.avaliar_qualidade(measurement):
            resultado = item["resultado"]
            max_penalty = QUALITY_SCORE_WEIGHTS[item["field_name"]]

            if resultado_normal(resultado):
                explanations.append(
                    f"{item['label']} {float(resultado.valor_avaliado):.4f} normal na avaliacao observacional; sem penalidade."
                )
                continue

            if resultado_nao_avaliavel(resultado):
                explanations.append(
                    f"{item['label']} sem avaliacao observacional aplicavel ao score: {resultado.mensagem}"
                )
                continue

            penalty = max_penalty if resultado.status == "CRITICO" else max_penalty * 0.5
            total_penalty += penalty
            explanations.append(
                f"{item['label']} {float(resultado.valor_avaliado):.4f} com "
                f"{observational_status_label(resultado.status).lower()}; "
                f"reduz {penalty:.2f} pontos."
            )

        return total_penalty

    def _status(self, score):
        if score >= 85:
            return WATER_HEALTH_SCORE_EXCELLENT
        if score >= 70:
            return WATER_HEALTH_SCORE_GOOD
        if score >= 50:
            return WATER_HEALTH_SCORE_ATTENTION
        if score >= 30:
            return WATER_HEALTH_SCORE_CRITICAL
        return WATER_HEALTH_SCORE_VERY_CRITICAL
