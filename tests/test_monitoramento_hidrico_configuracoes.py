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
        self.assertNotIn(
            "agrotoxicos",
            {
                parametro
                for configuracao in configuracoes
                for parametro in configuracao.parametros_habilitados
            },
        )

    def test_parametro_fora_do_escopo_nao_pode_ser_habilitado(self):
        configuracao = self.service.criar_a_partir_de_perfil(
            "teste_rural",
            "Teste Rural",
            "rural",
        )

        with self.assertRaisesRegex(ValueError, "Parametro inexistente no catalogo"):
            self.service.habilitar_parametro(configuracao, "agrotoxicos")

    def test_perfil_ativo_resolve_exatamente_uma_configuracao(self):
        configuracao = self.service.resolver_configuracao_por_perfil_ativo("eta")

        self.assertEqual("config_eta_base", configuracao.identificador)
        self.assertEqual("eta", configuracao.perfil_operacional_base)

    def test_perfil_ativo_sem_configuracao_falha_explicitamente(self):
        with self.assertRaisesRegex(ValueError, "Nenhuma configuracao operacional"):
            self.service.resolver_configuracao_por_perfil_ativo("perfil_sem_configuracao", [])

    def test_perfil_ativo_com_multiplas_configuracoes_falha_explicitamente(self):
        configuracoes = [
            ConfiguracaoOperacional("eta_1", "ETA 1", "eta"),
            ConfiguracaoOperacional("eta_2", "ETA 2", "eta"),
        ]

        with self.assertRaisesRegex(ValueError, "Mais de uma configuracao operacional"):
            self.service.resolver_configuracao_por_perfil_ativo("eta", configuracoes)


if __name__ == "__main__":
    unittest.main()
