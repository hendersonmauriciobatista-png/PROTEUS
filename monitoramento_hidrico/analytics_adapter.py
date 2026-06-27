from .avaliacao import STATUS_ATENCAO, STATUS_CRITICO, STATUS_NAO_AVALIAVEL, STATUS_NORMAL
from .politicas import MOTOR_OBSERVACIONAL


QUALITY_ANALYTICS_PARAMETERS = [
    ("ph", "ph", "quimicos", "pH"),
    ("turbidez", "turbidez", "fisicos", "Turbidez"),
    ("oxigenio_dissolvido", "oxigenio_dissolvido", "quimicos", "Oxigenio dissolvido"),
    ("temperatura", "temperatura_agua", "fisicos", "Temperatura da agua"),
    ("agrotoxicos", "agrotoxicos", "contaminantes_agricolas", "Agrotoxicos"),
]


class AnalyticsHydricMonitoringAdapter:
    def __init__(self, policy_engine, evaluation_service, perfil_operacional=None):
        self.policy_engine = policy_engine
        self.evaluation_service = evaluation_service
        self.perfil_operacional = perfil_operacional

    def avaliar_qualidade(self, measurement):
        resultados = []
        for field_name, parametro_id, categoria, label in QUALITY_ANALYTICS_PARAMETERS:
            policy = self.policy_engine.selecionar_politica(
                perfil_operacional=self.perfil_operacional,
                categoria=categoria,
                parametro_id=parametro_id,
            )
            if policy.motor_destino != MOTOR_OBSERVACIONAL:
                continue

            resultado = self.evaluation_service.avaliar(parametro_id, getattr(measurement, field_name))
            resultados.append(
                {
                    "field_name": field_name,
                    "parametro_id": parametro_id,
                    "categoria": categoria,
                    "label": label,
                    "resultado": resultado,
                }
            )

        return resultados


def resultado_requer_atencao(resultado):
    return resultado.status in {STATUS_ATENCAO, STATUS_CRITICO}


def resultado_normal(resultado):
    return resultado.status == STATUS_NORMAL


def resultado_nao_avaliavel(resultado):
    return resultado.status == STATUS_NAO_AVALIAVEL
