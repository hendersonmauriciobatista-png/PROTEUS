import re
from dataclasses import dataclass

from .avaliacao import SEVERIDADE_ALTA, SEVERIDADE_BAIXA, SEVERIDADE_MEDIA, SEVERIDADE_NENHUMA
from .politicas import MOTOR_OBSERVACIONAL


GOVERNANCE_QUALITY_PARAMETERS = {
    "ph": ("ph", "quimicos"),
    "turbidez": ("turbidez", "fisicos"),
    "oxigenio_dissolvido": ("oxigenio_dissolvido", "quimicos"),
    "temperatura": ("temperatura_agua", "fisicos"),
    "agrotoxicos": ("agrotoxicos", "contaminantes_agricolas"),
}


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


class OperationalGovernanceHydricMonitoringAdapter:
    def __init__(self, policy_engine, evaluation_service, perfil_operacional=None):
        self.policy_engine = policy_engine
        self.evaluation_service = evaluation_service
        self.perfil_operacional = perfil_operacional

    def enriquecer_alertas(self, alerts):
        return [self.enriquecer_alerta(alert) for alert in alerts]

    def enriquecer_alerta(self, alert):
        if alert.domain != "qualidade_agua" or alert.metric not in GOVERNANCE_QUALITY_PARAMETERS:
            return self._from_alert(alert)

        parametro_id, categoria = GOVERNANCE_QUALITY_PARAMETERS[alert.metric]
        policy = self.policy_engine.selecionar_politica(
            perfil_operacional=self.perfil_operacional,
            categoria=categoria,
            parametro_id=parametro_id,
        )
        valor = _extract_current_value(alert.evidence)
        if valor is None or policy.motor_destino != MOTOR_OBSERVACIONAL:
            return self._from_alert(
                alert,
                policy_id=policy.identificador,
                policy_name=policy.nome,
                explainability="Alerta de qualidade sem valor numerico reavaliavel pela Governanca.",
            )

        resultado = self.evaluation_service.avaliar(parametro_id, valor)
        explainability = (
            f"Politica {policy.identificador}; motor {policy.motor_destino}; "
            f"resultado {resultado.status}; origem {resultado.origem_limite}."
        )
        evidence = f"{alert.evidence} | {resultado.mensagem}"
        return self._from_alert(
            alert,
            severity=_severity_from_observational_result(resultado.severidade, alert.severity),
            evidence=evidence,
            policy_id=policy.identificador,
            policy_name=policy.nome,
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


def _severity_from_observational_result(observational_severity, fallback):
    mapping = {
        SEVERIDADE_ALTA: "alto",
        SEVERIDADE_MEDIA: "medio",
        SEVERIDADE_BAIXA: "baixo",
        SEVERIDADE_NENHUMA: fallback,
    }
    return mapping.get(observational_severity, fallback)
