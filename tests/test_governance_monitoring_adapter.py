import unittest

from analytics.models import PreventiveAlert
from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.governance_adapter import (
    OperationalGovernanceHydricMonitoringAdapter,
    decidir_reavaliacao_controlada,
)
from monitoramento_hidrico.models import PoliticaAvaliacao


class OperationalGovernanceHydricMonitoringAdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = OperationalGovernanceHydricMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )

    def test_quality_alert_is_enriched_with_observational_result(self):
        signal = self.adapter.enriquecer_alerta(
            PreventiveAlert(
                severity="alto",
                domain="qualidade_agua",
                metric="ph",
                message="Atencao preventiva: pH com avaliacao observacional ATENCAO.",
                evidence="Valor atual 5.5000; origem catalogo:limite_observacional.",
                recommendation="Acompanhar novas coletas.",
            )
        )

        self.assertEqual("ATENCAO", signal.observational_status)
        self.assertEqual("media", signal.observational_severity)
        self.assertEqual("medio", signal.severity)
        self.assertEqual("catalogo:limite_observacional", signal.limit_origin)
        self.assertTrue(signal.policy_id)
        self.assertIn("reavaliacao_controlada=executada", signal.explainability)
        self.assertIn("finalidade=enriquecimento_governanca", signal.explainability)

    def test_non_quality_alert_is_preserved_without_observational_result(self):
        signal = self.adapter.enriquecer_alerta(
            PreventiveAlert(
                severity="alto",
                domain="consumo_distribuicao",
                metric="perdas_estimadas",
                message="Atencao preventiva: perdas elevadas.",
                evidence="Perdas atuais 35.00%.",
                recommendation="Verificar registros.",
            )
        )

        self.assertEqual("alto", signal.severity)
        self.assertEqual("", signal.observational_status)
        self.assertEqual("", signal.policy_id)

    def test_quality_alert_without_numeric_value_is_not_reevaluated(self):
        signal = self.adapter.enriquecer_alerta(
            PreventiveAlert(
                severity="alto",
                domain="qualidade_agua",
                metric="ph",
                message="Atencao preventiva: pH com avaliacao observacional ATENCAO.",
                evidence="Sem valor atual estruturado.",
                recommendation="Acompanhar novas coletas.",
            )
        )

        self.assertEqual("alto", signal.severity)
        self.assertEqual("", signal.observational_status)
        self.assertTrue(signal.policy_id)
        self.assertIn("reavaliacao_controlada=nao_executada", signal.explainability)
        self.assertIn("decisao=sem_valor_numerico", signal.explainability)

    def test_unmapped_quality_metric_is_not_reevaluated(self):
        signal = self.adapter.enriquecer_alerta(
            PreventiveAlert(
                severity="alto",
                domain="qualidade_agua",
                metric="cloro",
                message="Atencao preventiva: cloro.",
                evidence="Valor atual 1.0000.",
                recommendation="Acompanhar novas coletas.",
            )
        )

        self.assertEqual("alto", signal.severity)
        self.assertEqual("", signal.observational_status)
        self.assertEqual("", signal.policy_id)

    def test_non_observational_policy_is_not_reevaluated(self):
        policy_engine = PolicyEngine(
            politicas=[
                PoliticaAvaliacao(
                    identificador="politica_teste",
                    nome="Politica Teste",
                    tipo="interna_futura",
                    motor_destino="motor_futuro",
                    parametro_id="ph",
                )
            ]
        )
        adapter = OperationalGovernanceHydricMonitoringAdapter(
            policy_engine=policy_engine,
            evaluation_service=AvaliacaoObservacionalService(),
        )

        signal = adapter.enriquecer_alerta(
            PreventiveAlert(
                severity="alto",
                domain="qualidade_agua",
                metric="ph",
                message="Atencao preventiva: pH.",
                evidence="Valor atual 5.5000.",
                recommendation="Acompanhar novas coletas.",
            )
        )

        self.assertEqual("alto", signal.severity)
        self.assertEqual("", signal.observational_status)
        self.assertEqual("politica_teste", signal.policy_id)
        self.assertIn("decisao=motor_nao_observacional", signal.explainability)

    def test_controlled_reevaluation_decision_is_deterministic(self):
        alert = PreventiveAlert(
            severity="alto",
            domain="qualidade_agua",
            metric="ph",
            message="Atencao preventiva: pH.",
            evidence="Valor atual 5.5000.",
            recommendation="Acompanhar novas coletas.",
        )

        first = decidir_reavaliacao_controlada(alert, self.adapter.policy_engine)
        second = decidir_reavaliacao_controlada(alert, self.adapter.policy_engine)

        self.assertEqual(first, second)
        self.assertTrue(first.should_reevaluate)


if __name__ == "__main__":
    unittest.main()
