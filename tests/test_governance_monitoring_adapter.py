import unittest

from analytics.models import PreventiveAlert
from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.governance_adapter import OperationalGovernanceHydricMonitoringAdapter


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


if __name__ == "__main__":
    unittest.main()
