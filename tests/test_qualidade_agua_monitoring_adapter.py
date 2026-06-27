from pathlib import Path
import unittest

from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.qualidade_agua_adapter import (
    STATUS_DENTRO_PADRAO,
    STATUS_FORA_PADRAO,
    QualidadeAguaMonitoringAdapter,
)


class QualidadeAguaMonitoringAdapterTests(unittest.TestCase):
    def setUp(self):
        self.adapter = QualidadeAguaMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )

    def test_status_dentro_do_padrao_quando_avaliacoes_observacionais_normais(self):
        status = self.adapter.status_medicao(
            {
                "ph": "7.2",
                "turbidez": "4.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "50.0",
                "agrotoxicos": "10.0",
            }
        )

        self.assertEqual(STATUS_DENTRO_PADRAO, status)

    def test_status_fora_do_padrao_quando_motor_observacional_indica_alerta(self):
        status = self.adapter.status_medicao(
            {
                "ph": "7.2",
                "turbidez": "10.0",
                "oxigenio_dissolvido": "6.0",
                "temperatura": "24.0",
                "agrotoxicos": "0.0",
            }
        )

        self.assertEqual(STATUS_FORA_PADRAO, status)

    def test_valor_invalido_usa_resultado_nao_avaliavel_sem_quebrar_status(self):
        measurement = {
            "ph": "valor_invalido",
            "turbidez": "4.0",
            "oxigenio_dissolvido": "6.0",
            "temperatura": "24.0",
            "agrotoxicos": "0.0",
        }

        resultados = self.adapter.avaliar_medicao(measurement)

        self.assertIn("NAO_AVALIAVEL", {resultado.status for resultado in resultados})
        self.assertEqual(STATUS_DENTRO_PADRAO, self.adapter.status_medicao(measurement))

    def test_tela_qualidade_agua_nao_mantem_autoridade_local_de_status(self):
        source = Path("qualidade_agua.py").read_text(encoding="utf-8")

        self.assertNotIn("CONAMA", source)
        self.assertNotIn("def check_status", source)
        self.assertIn("monitoring_adapter.status_medicao", source)


if __name__ == "__main__":
    unittest.main()
