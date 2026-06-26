import tempfile
import unittest
from pathlib import Path

from monitoramento_hidrico import ConfiguracaoOperacionalService
from monitoramento_hidrico.models import ConfiguracaoOperacional


class MonitoramentoHidricoConfiguracoesTests(unittest.TestCase):
    def setUp(self):
        self.service = ConfiguracaoOperacionalService()

    def test_configuracao_pode_ser_criada_a_partir_de_perfil(self):
        configuracao = self.service.criar_a_partir_de_perfil(
            identificador="teste_rural",
            nome="Teste Rural",
            perfil_operacional_base="rural",
        )

        self.assertEqual("rural", configuracao.perfil_operacional_base)
        self.assertEqual([], configuracao.categorias_habilitadas)
        self.assertEqual([], configuracao.parametros_habilitados)

    def test_categorias_podem_ser_habilitadas_e_desabilitadas(self):
        configuracao = self.service.criar_a_partir_de_perfil(
            "teste_eta",
            "Teste ETA",
            "eta",
        )

        self.service.habilitar_categoria(configuracao, "fisicos")
        self.service.habilitar_categoria(configuracao, "quimicos")
        self.service.habilitar_categoria(configuracao, "fisicos")
        self.service.desabilitar_categoria(configuracao, "fisicos")

        self.assertEqual(["quimicos"], configuracao.categorias_habilitadas)

    def test_parametros_podem_ser_habilitados_e_desabilitados(self):
        configuracao = self.service.criar_a_partir_de_perfil(
            "teste_industrial",
            "Teste Industrial",
            "industrial",
        )

        self.service.habilitar_parametro(configuracao, "ph")
        self.service.habilitar_parametro(configuracao, "dbo")
        self.service.habilitar_parametro(configuracao, "ph")
        self.service.desabilitar_parametro(configuracao, "dbo")

        self.assertEqual(["ph"], configuracao.parametros_habilitados)

    def test_configuracoes_invalidas_sao_rejeitadas(self):
        with self.assertRaises(ValueError):
            self.service.criar_a_partir_de_perfil(
                "teste_invalido",
                "Teste Invalido",
                "perfil_inexistente",
            )

        configuracao = ConfiguracaoOperacional(
            identificador="teste_parametro_invalido",
            nome="Teste Parametro Invalido",
            perfil_operacional_base="rural",
            categorias_habilitadas=["fisicos"],
            parametros_habilitados=["parametro_inexistente"],
        )

        with self.assertRaises(ValueError):
            self.service.validar_configuracao(configuracao)

    def test_configuracoes_podem_ser_salvas_e_carregadas(self):
        configuracao = self.service.criar_a_partir_de_perfil(
            identificador="teste_ambiental",
            nome="Teste Ambiental",
            perfil_operacional_base="ambiental_rio",
            categorias_habilitadas=["fisicos", "quimicos"],
            parametros_habilitados=["temperatura_agua", "oxigenio_dissolvido"],
            observacoes="Amostra de teste.",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "configuracoes.json"
            self.service.salvar_configuracoes([configuracao], path)
            carregadas = self.service.carregar_configuracoes(path)

        self.assertEqual(1, len(carregadas))
        self.assertEqual(configuracao, carregadas[0])

    def test_configuracoes_iniciais_podem_ser_carregadas(self):
        configuracoes = self.service.carregar_configuracoes()
        perfis = {configuracao.perfil_operacional_base for configuracao in configuracoes}

        self.assertEqual(
            {
                "rural",
                "industrial",
                "urbano_saneamento",
                "ambiental_rio",
                "eta",
                "ete",
            },
            perfis,
        )


if __name__ == "__main__":
    unittest.main()
