from dataclasses import dataclass

from .avaliacao import AvaliacaoObservacionalService
from .configuracoes import ConfiguracaoOperacionalService
from .politicas import PolicyEngine


@dataclass(frozen=True)
class HydricApplicationContext:
    configuracao_operacional: object
    policy_engine: object
    evaluation_service: object

    @property
    def perfil_operacional(self):
        return self.configuracao_operacional.perfil_operacional_base

    @classmethod
    def from_active_profile(
        cls,
        perfil_operacional_ativo,
        configuration_service=None,
        policy_engine_factory=PolicyEngine,
        evaluation_service_factory=AvaliacaoObservacionalService,
    ):
        service = configuration_service or ConfiguracaoOperacionalService()
        configuracao = service.resolver_configuracao_por_perfil_ativo(perfil_operacional_ativo)
        return cls(
            configuracao_operacional=configuracao,
            policy_engine=policy_engine_factory(),
            evaluation_service=evaluation_service_factory(),
        )

    def build_policy_adapter(self, adapter_class, **kwargs):
        return adapter_class(
            policy_engine=self.policy_engine,
            evaluation_service=self.evaluation_service,
            perfil_operacional=self.perfil_operacional,
            **kwargs,
        )
