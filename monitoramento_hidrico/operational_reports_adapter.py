from .avaliacao import STATUS_ATENCAO, STATUS_CRITICO, STATUS_NAO_AVALIAVEL
from .politicas import MOTOR_OBSERVACIONAL


REPORT_STATUS_DENTRO = "Dentro do padrão"
REPORT_STATUS_FORA = "Fora do padrão"

REPORT_QUALITY_PARAMETERS = [
    ("ph", "ph", "quimicos"),
    ("turbidez", "turbidez", "fisicos"),
    ("oxigenio_dissolvido", "oxigenio_dissolvido", "quimicos"),
    ("temperatura", "temperatura_agua", "fisicos"),
    ("agrotoxicos", "agrotoxicos", "contaminantes_agricolas"),
]


class OperationalReportsHydricMonitoringAdapter:
    def __init__(self, policy_engine, evaluation_service, perfil_operacional=None):
        self.policy_engine = policy_engine
        self.evaluation_service = evaluation_service
        self.perfil_operacional = perfil_operacional

    def status_linha(self, row):
        resultados = self.avaliar_linha(row)
        for resultado in resultados:
            if resultado.status in {STATUS_ATENCAO, STATUS_CRITICO}:
                return REPORT_STATUS_FORA
        return REPORT_STATUS_DENTRO

    def avaliar_linha(self, row):
        resultados = []
        for field_name, parametro_id, categoria in REPORT_QUALITY_PARAMETERS:
            policy = self.policy_engine.selecionar_politica(
                perfil_operacional=self.perfil_operacional,
                categoria=categoria,
                parametro_id=parametro_id,
            )
            if policy.motor_destino != MOTOR_OBSERVACIONAL:
                continue

            resultados.append(self.evaluation_service.avaliar(parametro_id, row.get(field_name)))

        return resultados

    def contar_fora_padrao(self, rows):
        return sum(1 for row in rows if self.status_linha(row) == REPORT_STATUS_FORA)

    def possui_resultados_nao_avaliaveis(self, row):
        return any(resultado.status == STATUS_NAO_AVALIAVEL for resultado in self.avaliar_linha(row))
