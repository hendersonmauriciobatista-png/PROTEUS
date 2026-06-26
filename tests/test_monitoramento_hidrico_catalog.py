import unittest

from monitoramento_hidrico import (
    load_categorias_parametros,
    load_parametros_hidricos,
    load_perfis_operacionais,
)
from monitoramento_hidrico.catalog import load_catalog


class MonitoramentoHidricoCatalogTests(unittest.TestCase):
    def test_todos_os_perfis_operacionais_existem(self):
        perfis = load_perfis_operacionais()
        nomes = {perfil.nome for perfil in perfis}

        self.assertEqual(
            {
                "Rural",
                "Industrial",
                "Urbano/Saneamento",
                "Ambiental/Rio",
                "ETA",
                "ETE",
            },
            nomes,
        )

    def test_todas_as_categorias_existem(self):
        categorias = load_categorias_parametros()
        nomes = {categoria.nome for categoria in categorias}

        self.assertEqual(
            {
                "Fisicos",
                "Quimicos",
                "Metais Pesados",
                "Contaminantes Agricolas",
                "Contaminantes Industriais",
                "Biologicos",
                "Contaminantes Emergentes",
            },
            nomes,
        )

    def test_parametros_possuem_nome_categoria_e_unidade(self):
        categorias = {categoria.codigo for categoria in load_categorias_parametros()}
        parametros = load_parametros_hidricos()

        self.assertGreaterEqual(len(parametros), 42)
        for parametro in parametros:
            self.assertTrue(parametro.nome)
            self.assertIn(parametro.categoria, categorias)
            self.assertTrue(parametro.unidade)

    def test_catalogo_pode_ser_carregado_sem_erro(self):
        catalogo = load_catalog()

        self.assertIn("perfis_operacionais", catalogo)
        self.assertIn("categorias_parametros", catalogo)
        self.assertIn("parametros_hidricos", catalogo)


if __name__ == "__main__":
    unittest.main()
