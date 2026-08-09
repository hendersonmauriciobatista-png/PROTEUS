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


DASHBOARD_STATUS_OBSERVACIONAL_NORMAL = QUALITY_STATUS_OBSERVATIONAL_NORMAL
DASHBOARD_STATUS_OBSERVACIONAL_ATENCAO = QUALITY_STATUS_OBSERVATIONAL_ATTENTION
DASHBOARD_STATUS_OBSERVACIONAL_CRITICO = QUALITY_STATUS_OBSERVATIONAL_CRITICAL
DASHBOARD_STATUS_OBSERVACIONAL_NAO_AVALIAVEL = QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE


class DashboardMonitoringAdapter:
    def __init__(self, policy_engine, evaluation_service, perfil_operacional=None):
        if not perfil_operacional:
            raise ValueError("O perfil operacional autoritativo e obrigatorio.")
        self.policy_engine = policy_engine
        self.evaluation_service = evaluation_service
        self.perfil_operacional = perfil_operacional

    def quality_status(self, row):
        resultados = self.evaluate_quality_row(row)
        return aggregate_observational_status(resultado.status for resultado in resultados)

    def evaluate_quality_row(self, row):
        resultados = []
        for field_name, parametro_id, categoria in quality_parameter_triples():
            policy = self.policy_engine.selecionar_politica(
                perfil_operacional=self.perfil_operacional,
                categoria=categoria,
                parametro_id=parametro_id,
            )
            if policy.motor_destino != MOTOR_OBSERVACIONAL:
                continue

            resultados.append(self.evaluation_service.avaliar(parametro_id, row.get(field_name)))

        return resultados

    def has_non_evaluable_results(self, row):
        return any(resultado.status == STATUS_NAO_AVALIAVEL for resultado in self.evaluate_quality_row(row))
