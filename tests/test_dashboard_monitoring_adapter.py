import unittest

from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.dashboard_adapter import (
    DASHBOARD_STATUS_OBSERVACIONAL_ATENCAO,
    DASHBOARD_STATUS_OBSERVACIONAL_NORMAL,
    DashboardMonitoringAdapter,
)


class DashboardMonitoringAdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = DashboardMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
            perfil_operacional="urbano_saneamento",
        )

    def test_adapter_exige_perfil_operacional_autoritativo(self):
        with self.assertRaises(ValueError):
            DashboardMonitoringAdapter(
                policy_engine=PolicyEngine(),
                evaluation_service=AvaliacaoObservacionalService(),
            )

    def test_status_dentro_do_padrao_quando_avaliacoes_observacionais_normais(self):
        status = self.adapter.quality_status(
            {
                "ph": "7.2",
                "turbidez": "4.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "50.0",
                "agrotoxicos": "10.0",
            }
        )

        self.assertEqual(DASHBOARD_STATUS_OBSERVACIONAL_NORMAL, status)

    def test_status_fora_do_padrao_quando_motor_observacional_indica_alerta(self):
        status = self.adapter.quality_status(
            {
                "ph": "7.2",
                "turbidez": "10.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "24.0",
                "agrotoxicos": "0.0",
            }
        )

        self.assertEqual(DASHBOARD_STATUS_OBSERVACIONAL_ATENCAO, status)

    def test_valor_invalido_usa_fallback_nao_avaliavel_sem_quebrar_dashboard(self):
        resultados = self.adapter.evaluate_quality_row(
            {
                "ph": "valor_invalido",
                "turbidez": "4.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "24.0",
                "agrotoxicos": "0.0",
            }
        )

        self.assertIn("NAO_AVALIAVEL", {resultado.status for resultado in resultados})
        self.assertEqual(
            DASHBOARD_STATUS_OBSERVACIONAL_NORMAL,
            self.adapter.quality_status(
                {
                    "ph": "valor_invalido",
                    "turbidez": "4.0",
                    "oxigenio_dissolvido": "6.0",
                    "temperatura": "24.0",
                    "agrotoxicos": "0.0",
                }
            ),
        )


if __name__ == "__main__":
    unittest.main()
