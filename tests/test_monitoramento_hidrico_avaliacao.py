import unittest
import json
import tempfile
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

    def test_familia_fora_do_escopo_nao_e_avaliada(self):
        for parametro_id in ("agrotoxicos", "herbicidas", "fungicidas", "inseticidas"):
            with self.subTest(parametro_id=parametro_id):
                resultado = self.service.avaliar(parametro_id, 999999)

                self.assertEqual("NAO_AVALIAVEL", resultado.status)
                self.assertEqual("nenhuma", resultado.severidade)
                self.assertEqual("catalogo:parametro_fora_escopo_operacional", resultado.origem_limite)
                self.assertIn("fora do escopo operacional", resultado.mensagem)

    def test_status_fora_do_escopo_prevalece_sobre_limite_numerico(self):
        catalogo = json.loads(CATALOGO_PATH.read_text(encoding="utf-8"))
        for parametro in catalogo["parametros_hidricos"]:
            if parametro["codigo"] == "agrotoxicos":
                parametro["limite_observacional"] = {"min": 0.0, "max": 1000000.0}
                break

        with tempfile.TemporaryDirectory() as temp_dir:
            catalogo_path = Path(temp_dir) / "catalogo.json"
            catalogo_path.write_text(json.dumps(catalogo), encoding="utf-8")
            resultado = AvaliacaoObservacionalService(catalogo_path).avaliar("agrotoxicos", 1.0)

        self.assertEqual("NAO_AVALIAVEL", resultado.status)
        self.assertEqual("nenhuma", resultado.severidade)
        self.assertEqual("catalogo:parametro_fora_escopo_operacional", resultado.origem_limite)

    def test_parametros_ativos_e_desconhecido_preservam_comportamento(self):
        casos_ativos = (
            ("ph", 7.0, "NORMAL"),
            ("turbidez", 10.0, "CRITICO"),
            ("oxigenio_dissolvido", 4.0, "ATENCAO"),
        )
        for parametro_id, valor, status in casos_ativos:
            with self.subTest(parametro_id=parametro_id):
                self.assertEqual(status, self.service.avaliar(parametro_id, valor).status)

        desconhecido = self.service.avaliar("parametro_desconhecido", 1.0)
        self.assertEqual("NAO_AVALIAVEL", desconhecido.status)
        self.assertEqual("catalogo:parametro_inexistente", desconhecido.origem_limite)

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
