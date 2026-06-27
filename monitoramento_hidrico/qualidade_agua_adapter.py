from .avaliacao import STATUS_ATENCAO, STATUS_CRITICO, STATUS_NAO_AVALIAVEL
from .politicas import MOTOR_OBSERVACIONAL


STATUS_DENTRO_PADRAO = "Dentro do padrão"
STATUS_FORA_PADRAO = "Fora do padrão"

PARAMETROS_QUALIDADE_AGUA = [
    ("ph", "ph", "quimicos"),
    ("turbidez", "turbidez", "fisicos"),
    ("oxigenio_dissolvido", "oxigenio_dissolvido", "quimicos"),
    ("temperatura", "temperatura_agua", "fisicos"),
    ("agrotoxicos", "agrotoxicos", "contaminantes_agricolas"),
]


class QualidadeAguaMonitoringAdapter:
    def __init__(self, policy_engine, evaluation_service, perfil_operacional=None):
        self.policy_engine = policy_engine
        self.evaluation_service = evaluation_service
        self.perfil_operacional = perfil_operacional

    def status_medicao(self, measurement):
        resultados = self.avaliar_medicao(measurement)
        for resultado in resultados:
            if resultado.status in {STATUS_ATENCAO, STATUS_CRITICO}:
                return STATUS_FORA_PADRAO
        return STATUS_DENTRO_PADRAO

    def avaliar_medicao(self, measurement):
        resultados = []
        for field_name, parametro_id, categoria in PARAMETROS_QUALIDADE_AGUA:
            policy = self.policy_engine.selecionar_politica(
                perfil_operacional=self.perfil_operacional,
                categoria=categoria,
                parametro_id=parametro_id,
            )
            if policy.motor_destino != MOTOR_OBSERVACIONAL:
                continue

            resultados.append(self.evaluation_service.avaliar(parametro_id, measurement.get(field_name)))

        return resultados

    def possui_resultados_nao_avaliaveis(self, measurement):
        return any(resultado.status == STATUS_NAO_AVALIAVEL for resultado in self.avaliar_medicao(measurement))
