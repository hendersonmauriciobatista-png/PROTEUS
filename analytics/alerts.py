from .models import PreventiveAlert


QUALITY_LIMITS = {
    "ph": (6.0, 9.0),
    "turbidez": (0.0, 5.0),
    "oxigenio_dissolvido": (5.0, 10.0),
    "temperatura": (15.0, 30.0),
    "agrotoxicos": (0.0, 0.1),
}


class PreventiveAlertService:
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
        checks = [
            ("ph", "pH", measurement.ph, "fora da faixa 6.0-9.0", "alto"),
            ("turbidez", "Turbidez", measurement.turbidez, "acima de 5.0 NTU", "alto"),
            (
                "oxigenio_dissolvido",
                "Oxigenio dissolvido",
                measurement.oxigenio_dissolvido,
                "abaixo de 5.0 mg/L",
                "alto",
            ),
            ("temperatura", "Temperatura da agua", measurement.temperatura, "fora da faixa 15.0-30.0", "medio"),
            ("agrotoxicos", "Agrotoxicos", measurement.agrotoxicos, "acima de 0.1 mg/L", "alto"),
        ]

        for metric, label, value, condition, severity in checks:
            minimum, maximum = QUALITY_LIMITS[metric]
            if value < minimum or value > maximum:
                alerts.append(
                    PreventiveAlert(
                        severity=severity,
                        domain="qualidade_agua",
                        metric=metric,
                        message=f"Atencao preventiva: {label} {condition}.",
                        evidence=f"Valor atual {value:.4f}; limite minimo {minimum:.4f}; limite maximo {maximum:.4f}.",
                        recommendation="Revisar a medicao e acompanhar novas coletas antes de qualquer decisao operacional.",
                    )
                )

        if 0.07 <= measurement.agrotoxicos <= 0.1:
            alerts.append(
                PreventiveAlert(
                    severity="medio",
                    domain="qualidade_agua",
                    metric="agrotoxicos",
                    message="Atencao preventiva: agrotoxicos proximos do limite configurado.",
                    evidence=f"Valor atual {measurement.agrotoxicos:.4f}; limite maximo 0.1000.",
                    recommendation="Acompanhar proximas medicoes e verificar contexto da coleta.",
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
