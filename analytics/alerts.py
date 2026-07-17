from .models import PreventiveAlert
from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.analytics_adapter import (
    AnalyticsHydricMonitoringAdapter,
    resultado_requer_atencao,
)
from monitoramento_hidrico.status_semantics import observational_status_label


class PreventiveAlertService:
    def __init__(self, monitoring_adapter=None):
        self.monitoring_adapter = monitoring_adapter or AnalyticsHydricMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )

    def build_alerts(self, quality, environment, consumption, quality_trends, consumption_trends):
        alerts = []
        latest_quality = quality[-1] if quality else None
        latest_environment = environment[-1] if environment else None
        latest_consumption = consumption[-1] if consumption else None

        if latest_quality:
            alerts.extend(self._quality_limit_alerts(latest_quality))
            alerts.extend(self._quality_trend_alerts(quality_trends))

        if latest_consumption:
            alerts.extend(self._consumption_alerts(latest_consumption, consumption_trends))

        if latest_environment:
            alerts.extend(self._environment_context_alerts(latest_environment, quality_trends))

        return alerts

    def _quality_limit_alerts(self, measurement):
        alerts = []
        for item in self.monitoring_adapter.avaliar_qualidade(measurement):
            resultado = item["resultado"]
            if not resultado_requer_atencao(resultado):
                continue

            alerts.append(
                PreventiveAlert(
                    severity=_severity_from_observational_status(resultado.status),
                    domain="qualidade_agua",
                    metric=item["field_name"],
                    message=(
                        f"Atencao preventiva: {item['label']} com "
                        f"{observational_status_label(resultado.status).lower()}."
                    ),
                    evidence=(
                        f"Valor atual {float(resultado.valor_avaliado):.4f}; "
                        f"{resultado.mensagem}; origem {resultado.origem_limite}."
                    ),
                    recommendation="Revisar a medicao e acompanhar novas coletas antes de qualquer decisao operacional.",
                )
            )

        return alerts

    def _quality_trend_alerts(self, trends):
        alerts = []
        risk_directions = {
            "turbidez": "subindo",
            "agrotoxicos": "subindo",
            "oxigenio_dissolvido": "caindo",
        }
        for trend in trends:
            if trend.direction == risk_directions.get(trend.metric):
                alerts.append(
                    PreventiveAlert(
                        severity="baixo",
                        domain=trend.domain,
                        metric=trend.metric,
                        message=f"Atencao preventiva: tendencia de risco em {trend.metric}.",
                        evidence=trend.explanation,
                        recommendation="Observar se a tendencia se repete nas proximas medicoes.",
                    )
                )
        return alerts

    def _consumption_alerts(self, measurement, trends):
        alerts = []
        if measurement.perdas_estimadas >= 30.0:
            alerts.append(
                PreventiveAlert(
                    severity="alto",
                    domain="consumo_distribuicao",
                    metric="perdas_estimadas",
                    message="Atencao preventiva: perdas estimadas elevadas.",
                    evidence=f"Perdas atuais {measurement.perdas_estimadas:.2f}%; referencia preventiva 30.00%.",
                    recommendation="Verificar registros de distribuicao e possiveis inconsistencias operacionais.",
                )
            )
        elif measurement.perdas_estimadas >= 15.0:
            alerts.append(
                PreventiveAlert(
                    severity="medio",
                    domain="consumo_distribuicao",
                    metric="perdas_estimadas",
                    message="Atencao preventiva: perdas estimadas acima do patamar de acompanhamento.",
                    evidence=f"Perdas atuais {measurement.perdas_estimadas:.2f}%; referencia preventiva 15.00%.",
                    recommendation="Acompanhar evolucao das perdas nas proximas medicoes.",
                )
            )

        for trend in trends:
            if trend.metric in ("consumo_diario", "perdas_estimadas") and trend.direction == "subindo":
                alerts.append(
                    PreventiveAlert(
                        severity="baixo",
                        domain=trend.domain,
                        metric=trend.metric,
                        message=f"Atencao preventiva: {trend.metric} em tendencia de alta.",
                        evidence=trend.explanation,
                        recommendation="Comparar a tendencia com operacao planejada e contexto ambiental.",
                    )
                )
        return alerts

    def _environment_context_alerts(self, measurement, quality_trends):
        turbidity_trend = next((trend for trend in quality_trends if trend.metric == "turbidez"), None)
        if measurement.chuva >= 20.0 and turbidity_trend and turbidity_trend.direction == "subindo":
            return [
                PreventiveAlert(
                    severity="medio",
                    domain="dados_ambientais",
                    metric="chuva",
                    message="Atencao preventiva: chuva elevada combinada com turbidez em alta.",
                    evidence=f"Chuva atual {measurement.chuva:.2f} mm; {turbidity_trend.explanation}",
                    recommendation="Observar novas medicoes de turbidez apos o evento de chuva.",
                )
            ]
        return []


def _severity_from_observational_status(status):
    if status == "CRITICO":
        return "alto"
    if status == "ATENCAO":
        return "medio"
    return "baixo"
