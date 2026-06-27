from pathlib import Path
import unittest

from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.operational_reports_adapter import (
    OperationalReportsHydricMonitoringAdapter,
    REPORT_STATUS_DENTRO,
    REPORT_STATUS_FORA,
)


class OperationalReportsHydricMonitoringAdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = OperationalReportsHydricMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )

    def test_status_dentro_do_padrao_quando_avaliacoes_observacionais_normais(self):
        status = self.adapter.status_linha(
            {
                "ph": "7.2",
                "turbidez": "4.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "50.0",
                "agrotoxicos": "10.0",
            }
        )

        self.assertEqual(REPORT_STATUS_DENTRO, status)

    def test_status_fora_do_padrao_quando_motor_observacional_indica_alerta(self):
        status = self.adapter.status_linha(
            {
                "ph": "7.2",
                "turbidez": "10.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "24.0",
                "agrotoxicos": "0.0",
            }
        )

        self.assertEqual(REPORT_STATUS_FORA, status)

    def test_conta_registros_fora_do_padrao_usando_resultados_observacionais(self):
        rows = [
            {
                "ph": "7.2",
                "turbidez": "4.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "24.0",
                "agrotoxicos": "0.0",
            },
            {
                "ph": "7.2",
                "turbidez": "10.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "24.0",
                "agrotoxicos": "0.0",
            },
        ]

        self.assertEqual(1, self.adapter.contar_fora_padrao(rows))

    def test_relatorios_nao_mantem_autoridade_local_de_status(self):
        source = Path("relatorios.py").read_text(encoding="utf-8")

        self.assertNotIn("def _quality_status", source)
        self.assertNotIn("CONAMA", source)
        self.assertNotIn("QUALITY_LIMITS", source)
        self.assertIn("monitoring_adapter.status_linha", source)


if __name__ == "__main__":
    unittest.main()
