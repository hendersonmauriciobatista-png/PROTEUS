import unittest

from monitoramento_hidrico import (
    listar_parametros_por_categoria,
    listar_parametros_por_perfil,
    obter_metadados_parametro,
    validar_metadados_parametros,
)
from monitoramento_hidrico.catalog import load_parametros_hidricos


class MonitoramentoHidricoCatalogoInteligenteTests(unittest.TestCase):
    def test_todos_os_parametros_possuem_tipo_valor(self):
        parametros = load_parametros_hidricos()

        for parametro in parametros:
            self.assertIn(parametro.tipo_valor, {"numerico", "texto", "booleano", "observacional"})

    def test_parametros_numericos_possuem_unidade_quando_aplicavel(self):
        parametros = load_parametros_hidricos()

        for parametro in parametros:
            if parametro.tipo_valor == "numerico":
                self.assertTrue(parametro.unidade_medida)
                self.assertEqual(parametro.unidade, parametro.unidade_medida)

    def test_parametros_podem_ser_filtrados_por_perfil(self):
        parametros_rurais = listar_parametros_por_perfil("rural")
        codigos = {parametro.codigo for parametro in parametros_rurais}

        self.assertIn("agrotoxicos", codigos)
        self.assertIn("turbidez", codigos)
        self.assertNotIn("fenois", codigos)

    def test_parametros_podem_ser_filtrados_por_categoria(self):
        metais = listar_parametros_por_categoria("metais_pesados")
        codigos = {parametro.codigo for parametro in metais}

        self.assertIn("chumbo", codigos)
        self.assertIn("mercurio", codigos)
        self.assertNotIn("ph", codigos)

    def test_metadados_completos_podem_ser_carregados(self):
        metadados = obter_metadados_parametro("ph")

        self.assertEqual("ph", metadados["codigo"])
        self.assertEqual("numerico", metadados["tipo_valor"])
        self.assertEqual("unidade de pH", metadados["unidade_medida"])
        self.assertIn("eta", metadados["aplicabilidade_perfis"])
        self.assertIn("limite_observacional", metadados)

    def test_metadados_minimos_inteligentes_sao_validos(self):
        self.assertTrue(validar_metadados_parametros())


if __name__ == "__main__":
    unittest.main()
