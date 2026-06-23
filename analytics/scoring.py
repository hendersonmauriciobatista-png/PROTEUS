from .alerts import QUALITY_LIMITS
from .models import WaterHealthScore


class WaterHealthScoreCalculator:
    def calculate(self, quality, environment, consumption):
        score = 100.0
        explanations = []

        if not quality:
            return WaterHealthScore(
                score=0,
                status="Sem dados",
                explanations=["Sem registros de qualidade da agua para calcular o score."],
            )

        latest_quality = quality[-1]
        score -= self._quality_penalty("ph", "pH", latest_quality.ph, explanations, 18)
        score -= self._quality_penalty("turbidez", "Turbidez", latest_quality.turbidez, explanations, 18)
        score -= self._quality_penalty(
            "oxigenio_dissolvido",
            "Oxigenio dissolvido",
            latest_quality.oxigenio_dissolvido,
            explanations,
            20,
        )
        score -= self._quality_penalty("temperatura", "Temperatura da agua", latest_quality.temperatura, explanations, 10)
        score -= self._quality_penalty("agrotoxicos", "Agrotoxicos", latest_quality.agrotoxicos, explanations, 22)

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

    def _quality_penalty(self, metric, label, value, explanations, max_penalty):
        minimum, maximum = QUALITY_LIMITS[metric]
        if minimum <= value <= maximum:
            explanations.append(
                f"{label} {value:.4f} dentro da faixa configurada {minimum:.4f}-{maximum:.4f}; sem penalidade."
            )
            return 0.0

        if value < minimum:
            distance = minimum - value
            reference = max(abs(minimum), 1.0)
            direction = "abaixo"
        else:
            distance = value - maximum
            reference = max(abs(maximum), 1.0)
            direction = "acima"

        penalty = min(max_penalty, max_penalty * (distance / reference))
        explanations.append(
            f"{label} {value:.4f} {direction} da faixa {minimum:.4f}-{maximum:.4f}; reduz {penalty:.2f} pontos."
        )
        return penalty

    def _status(self, score):
        if score >= 85:
            return "Excelente"
        if score >= 70:
            return "Bom"
        if score >= 50:
            return "Atencao"
        if score >= 30:
            return "Critico"
        return "Muito critico"
