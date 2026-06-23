from .models import TrendResult


QUALITY_TOLERANCES = {
    "ph": 0.05,
    "turbidez": 0.05,
    "oxigenio_dissolvido": 0.05,
    "temperatura": 0.1,
    "agrotoxicos": 0.001,
}

CONSUMPTION_TOLERANCES = {
    "consumo_diario": 0.1,
    "consumo_mensal": 1.0,
    "volume_distribuido": 1.0,
    "perdas_estimadas": 0.1,
}


class TrendAnalyzer:
    def quality_trends(self, measurements):
        metrics = [
            ("ph", "pH"),
            ("turbidez", "Turbidez"),
            ("oxigenio_dissolvido", "Oxigenio dissolvido"),
            ("temperatura", "Temperatura da agua"),
            ("agrotoxicos", "Agrotoxicos"),
        ]
        return [
            self._calculate("qualidade_agua", attr, label, measurements, QUALITY_TOLERANCES[attr])
            for attr, label in metrics
        ]

    def consumption_trends(self, measurements):
        metrics = [
            ("consumo_diario", "Consumo diario"),
            ("consumo_mensal", "Consumo mensal"),
            ("volume_distribuido", "Volume distribuido"),
            ("perdas_estimadas", "Perdas estimadas"),
        ]
        return [
            self._calculate("consumo_distribuicao", attr, label, measurements, CONSUMPTION_TOLERANCES[attr])
            for attr, label in metrics
        ]

    def _calculate(self, domain, attr, label, measurements, tolerance):
        values = [getattr(item, attr) for item in measurements if getattr(item, attr) is not None]
        if len(values) < 2:
            return TrendResult(
                domain=domain,
                metric=attr,
                direction="dados_insuficientes",
                previous_average=None,
                recent_average=None,
                delta=None,
                explanation=f"{label}: apenas {len(values)} registro(s), minimo de 2 para tendencia.",
            )

        midpoint = len(values) // 2
        previous_values = values[:midpoint]
        recent_values = values[midpoint:]
        previous_average = sum(previous_values) / len(previous_values)
        recent_average = sum(recent_values) / len(recent_values)
        delta = recent_average - previous_average

        if delta > tolerance:
            direction = "subindo"
        elif delta < -tolerance:
            direction = "caindo"
        else:
            direction = "estavel"

        return TrendResult(
            domain=domain,
            metric=attr,
            direction=direction,
            previous_average=previous_average,
            recent_average=recent_average,
            delta=delta,
            explanation=(
                f"{label}: media anterior {previous_average:.4f}, "
                f"media recente {recent_average:.4f}, variacao {delta:.4f}."
            ),
        )
