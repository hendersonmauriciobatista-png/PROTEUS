import re
from dataclasses import dataclass

from .avaliacao import SEVERIDADE_ALTA, SEVERIDADE_BAIXA, SEVERIDADE_MEDIA, SEVERIDADE_NENHUMA
from .politicas import MOTOR_OBSERVACIONAL
from .quality_parameter_mapping import quality_parameter_governance_mapping


@dataclass(frozen=True)
class GovernanceHydricSignal:
    severity: str
    domain: str
    metric: str
    message: str
    evidence: str
    recommendation: str
    source: str = "analytics"
    policy_id: str = ""
    policy_name: str = ""
    observational_status: str = ""
    observational_severity: str = ""
    limit_origin: str = ""
    technical_observations: str = ""
    explainability: str = ""


@dataclass(frozen=True)
class ControlledReevaluationDecision:
    should_reevaluate: bool
    reason: str
    parametro_id: str = ""
    categoria: str = ""
    value: str = ""
    policy_id: str = ""
    policy_name: str = ""
    policy_motor: str = ""


def decidir_reavaliacao_controlada(alert, policy_engine, perfil_operacional=None):
    quality_parameters = quality_parameter_governance_mapping()
    if alert.domain != "qualidade_agua":
        return ControlledReevaluationDecision(False, "fora_do_dominio_qualidade")
    if alert.metric not in quality_parameters:
        return ControlledReevaluationDecision(False, "metrica_nao_mapeada")

    parametro_id, categoria = quality_parameters[alert.metric]
    policy = policy_engine.selecionar_politica(
        perfil_operacional=perfil_operacional,
        categoria=categoria,
        parametro_id=parametro_id,
    )
    value = _extract_current_value(alert.evidence)
    if value is None:
        return ControlledReevaluationDecision(
            False,
            "sem_valor_numerico",
            parametro_id=parametro_id,
            categoria=categoria,
            policy_id=policy.identificador,
            policy_name=policy.nome,
            policy_motor=policy.motor_destino,
        )
    if policy.motor_destino != MOTOR_OBSERVACIONAL:
        return ControlledReevaluationDecision(
            False,
            "motor_nao_observacional",
            parametro_id=parametro_id,
            categoria=categoria,
            value=value,
            policy_id=policy.identificador,
            policy_name=policy.nome,
            policy_motor=policy.motor_destino,
        )

    return ControlledReevaluationDecision(
        True,
        "pre_condicoes_atendidas",
        parametro_id=parametro_id,
        categoria=categoria,
        value=value,
        policy_id=policy.identificador,
        policy_name=policy.nome,
        policy_motor=policy.motor_destino,
    )


class OperationalGovernanceHydricMonitoringAdapter:
    def __init__(self, policy_engine, evaluation_service, perfil_operacional=None):
        self.policy_engine = policy_engine
        self.evaluation_service = evaluation_service
        self.perfil_operacional = perfil_operacional

    def enriquecer_alertas(self, alerts, decisions=None):
        alerts = list(alerts)
        if decisions is None:
            decisions = [self.decidir_reavaliacao(alert) for alert in alerts]
        else:
            decisions = list(decisions)
            if len(decisions) != len(alerts):
                raise ValueError("A quantidade de decisoes deve acompanhar a quantidade de alertas.")
        return [
            self.enriquecer_alerta(alert, decision)
            for alert, decision in zip(alerts, decisions)
        ]

    def decidir_reavaliacao(self, alert):
        return decidir_reavaliacao_controlada(alert, self.policy_engine, self.perfil_operacional)

    def enriquecer_alerta(self, alert, decision=None):
        decision = decision or self.decidir_reavaliacao(alert)
        if not decision.should_reevaluate:
            if not decision.policy_id:
                return self._from_alert(alert)
            return self._from_alert(
                alert,
                policy_id=decision.policy_id,
                policy_name=decision.policy_name,
                explainability=_controlled_reevaluation_explainability(decision),
            )

        resultado = self.evaluation_service.avaliar(decision.parametro_id, decision.value)
        explainability = (
            f"reavaliacao_controlada=executada; finalidade=enriquecimento_governanca; "
            f"decisao={decision.reason}; politica {decision.policy_id}; motor {decision.policy_motor}; "
            f"resultado {resultado.status}; origem {resultado.origem_limite}."
        )
        evidence = f"{alert.evidence} | {resultado.mensagem}"
        return self._from_alert(
            alert,
            severity=_severity_from_observational_result(resultado.severidade, alert.severity),
            evidence=evidence,
            policy_id=decision.policy_id,
            policy_name=decision.policy_name,
            observational_status=resultado.status,
            observational_severity=resultado.severidade,
            limit_origin=resultado.origem_limite,
            technical_observations=resultado.observacoes,
            explainability=explainability,
        )

    def _from_alert(
        self,
        alert,
        severity=None,
        evidence=None,
        policy_id="",
        policy_name="",
        observational_status="",
        observational_severity="",
        limit_origin="",
        technical_observations="",
        explainability="",
    ):
        return GovernanceHydricSignal(
            severity=severity or alert.severity,
            domain=alert.domain,
            metric=alert.metric,
            message=alert.message,
            evidence=evidence or alert.evidence,
            recommendation=alert.recommendation,
            source="analytics",
            policy_id=policy_id,
            policy_name=policy_name,
            observational_status=observational_status,
            observational_severity=observational_severity,
            limit_origin=limit_origin,
            technical_observations=technical_observations,
            explainability=explainability,
        )


def _extract_current_value(evidence):
    match = re.search(r"Valor atual\s+(-?\d+(?:\.\d+)?)", evidence or "")
    if not match:
        return None
    return match.group(1)


def _controlled_reevaluation_explainability(decision):
    return (
        f"reavaliacao_controlada=nao_executada; finalidade=enriquecimento_governanca; "
        f"decisao={decision.reason}; politica {decision.policy_id}; motor {decision.policy_motor}."
    )


def _severity_from_observational_result(observational_severity, fallback):
    mapping = {
        SEVERIDADE_ALTA: "alto",
        SEVERIDADE_MEDIA: "medio",
        SEVERIDADE_BAIXA: "baixo",
        SEVERIDADE_NENHUMA: fallback,
    }
    return mapping.get(observational_severity, fallback)
