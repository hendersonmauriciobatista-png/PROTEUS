import unittest
from pathlib import Path

from monitoramento_hidrico import AvaliacaoObservacionalService, avaliar_parametro_observacional


BASE_DIR = Path(__file__).resolve().parent.parent
CATALOGO_PATH = BASE_DIR / "data" / "monitoramento_hidrico_catalogo.json"
CONFIGURACOES_PATH = BASE_DIR / "data" / "monitoramento_hidrico_configuracoes.json"
QUALIDADE_CSV = BASE_DIR / "data" / "qualidade_agua_medicoes.csv"
AMBIENTE_CSV = BASE_DIR / "data" / "dados_ambientais_medicoes.csv"
CONSUMO_CSV = BASE_DIR / "data" / "consumo_distribuicao_medicoes.csv"


class MonitoramentoHidricoAvaliacaoTests(unittest.TestCase):
    def setUp(self):
        self.service = AvaliacaoObservacionalService()

    def test_limites_operacionais_observados_sem_inferencia_normativa(self):
        casos = (
            ("ph", 6.0, "NORMAL"),
            ("ph", 9.5, "NORMAL"),
            ("turbidez", 5.0, "NORMAL"),
            ("turbidez", 6.0, "ATENCAO"),
            ("oxigenio_dissolvido", 5.0, "NORMAL"),
            ("oxigenio_dissolvido", 4.0, "ATENCAO"),
        )

        for parametro_id, valor, status_operacional_esperado in casos:
            with self.subTest(parametro_id=parametro_id, valor=valor):
                resultado = self.service.avaliar(parametro_id, valor)

                self.assertEqual(status_operacional_esperado, resultado.status)
                self.assertEqual("catalogo:limite_observacional", resultado.origem_limite)
                self.assertIn("nao representa conformidade legal ou normativa", resultado.observacoes)

    def test_valor_dentro_do_limite_retorna_normal(self):
        resultado = self.service.avaliar("ph", 7.2)

        self.assertEqual("NORMAL", resultado.status)
        self.assertEqual("baixa", resultado.severidade)
        self.assertEqual("catalogo:limite_observacional", resultado.origem_limite)

    def test_valor_fora_do_limite_proximo_retorna_atencao(self):
        resultado = self.service.avaliar("turbidez", 5.5)

        self.assertEqual("ATENCAO", resultado.status)
        self.assertEqual("media", resultado.severidade)

    def test_valor_muito_fora_do_limite_retorna_critico(self):
        resultado = self.service.avaliar("turbidez", 10.0)

        self.assertEqual("CRITICO", resultado.status)
        self.assertEqual("alta", resultado.severidade)

    def test_parametro_sem_limite_retorna_nao_avaliavel(self):
        resultado = self.service.avaliar("temperatura_agua", 24.0)

        self.assertEqual("NAO_AVALIAVEL", resultado.status)
        self.assertEqual("nenhuma", resultado.severidade)
        self.assertEqual("catalogo:sem_limite_observacional", resultado.origem_limite)

    def test_valor_invalido_retorna_nao_avaliavel(self):
        resultado = avaliar_parametro_observacional("ph", "valor_invalido")

        self.assertEqual("NAO_AVALIAVEL", resultado.status)
        self.assertEqual("nenhuma", resultado.severidade)
        self.assertIn("nao e numerico", resultado.mensagem)

    def test_motor_nao_altera_catalogo_configuracoes_ou_csvs(self):
        paths = [
            CATALOGO_PATH,
            CONFIGURACOES_PATH,
            QUALIDADE_CSV,
            AMBIENTE_CSV,
            CONSUMO_CSV,
        ]
        antes = {path: path.read_bytes() for path in paths}

        self.service.avaliar("ph", 7.0)
        self.service.avaliar("turbidez", 10.0)
        self.service.avaliar("temperatura_agua", 24.0)

        depois = {path: path.read_bytes() for path in paths}
        self.assertEqual(antes, depois)


if __name__ == "__main__":
    unittest.main()
