from .avaliacao import STATUS_NAO_AVALIAVEL
from .politicas import MOTOR_OBSERVACIONAL
from .quality_parameter_mapping import quality_parameter_triples
from .status_semantics import (
    QUALITY_STATUS_OBSERVATIONAL_ATTENTION,
    QUALITY_STATUS_OBSERVATIONAL_CRITICAL,
    QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE,
    QUALITY_STATUS_OBSERVATIONAL_NORMAL,
    aggregate_observational_status,
)


STATUS_QUALIDADE_OBSERVACIONAL_NORMAL = QUALITY_STATUS_OBSERVATIONAL_NORMAL
STATUS_QUALIDADE_OBSERVACIONAL_ATENCAO = QUALITY_STATUS_OBSERVATIONAL_ATTENTION
STATUS_QUALIDADE_OBSERVACIONAL_CRITICO = QUALITY_STATUS_OBSERVATIONAL_CRITICAL
STATUS_QUALIDADE_OBSERVACIONAL_NAO_AVALIAVEL = QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE


class QualidadeAguaApplicationService:
    def __init__(self, repository, monitoring_adapter):
        self.repository = repository
        self.monitoring_adapter = monitoring_adapter

    def salvar_medicao(self, measurement):
        self.repository.append(measurement)

    def listar_medicoes(self):
        return self.repository.read_all()

    def status_medicao(self, measurement):
        return self.monitoring_adapter.status_medicao(measurement)


class QualidadeAguaMonitoringAdapter:
    def __init__(self, policy_engine, evaluation_service, perfil_operacional=None):
        if not perfil_operacional:
            raise ValueError("QualidadeAguaMonitoringAdapter exige perfil operacional autoritativo.")
        self.policy_engine = policy_engine
        self.evaluation_service = evaluation_service
        self.perfil_operacional = perfil_operacional

    def status_medicao(self, measurement):
        resultados = self.avaliar_medicao(measurement)
        return aggregate_observational_status(resultado.status for resultado in resultados)

    def avaliar_medicao(self, measurement):
        resultados = []
        for field_name, parametro_id, categoria in quality_parameter_triples():
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
