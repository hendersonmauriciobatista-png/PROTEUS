import unittest
from unittest.mock import patch

from monitoramento_hidrico import (
    PolicyEngine,
    PoliticaAvaliacao,
    listar_politicas_disponiveis,
    selecionar_politica_avaliacao,
)


class MonitoramentoHidricoPolicyEngineTests(unittest.TestCase):
    def test_politicas_disponiveis_podem_ser_listadas(self):
        politicas = listar_politicas_disponiveis()
        identificadores = {politica.identificador for politica in politicas}

        self.assertIn("politica_observacional_padrao", identificadores)
        self.assertIn("politica_observacional_industrial", identificadores)
        self.assertIn("politica_observacional_eta", identificadores)
        self.assertIn("politica_observacional_ete", identificadores)

    def test_politica_padrao_e_retornada(self):
        politica = selecionar_politica_avaliacao(
            perfil_operacional="rural",
            categoria="fisicos",
            parametro_id="temperatura_agua",
        )

        self.assertEqual("politica_observacional_padrao", politica.identificador)
        self.assertEqual("observacional", politica.tipo)
        self.assertEqual("avaliacao_observacional", politica.motor_destino)

    def test_politica_especifica_por_perfil_tem_prioridade(self):
        politica = selecionar_politica_avaliacao(
            perfil_operacional="industrial",
            categoria="quimicos",
            parametro_id="ph",
        )

        self.assertEqual("politica_observacional_industrial", politica.identificador)

    def test_politica_especifica_por_parametro_tem_prioridade_maior(self):
        politicas = [
            PoliticaAvaliacao(
                identificador="padrao",
                nome="Padrao",
                tipo="observacional",
                motor_destino="avaliacao_observacional",
                prioridade=0,
            ),
            PoliticaAvaliacao(
                identificador="perfil_industrial",
                nome="Perfil Industrial",
                tipo="observacional",
                motor_destino="avaliacao_observacional",
                perfil_operacional="industrial",
                prioridade=100,
            ),
            PoliticaAvaliacao(
                identificador="parametro_ph",
                nome="Parametro pH",
                tipo="observacional",
                motor_destino="avaliacao_observacional",
                parametro_id="ph",
                prioridade=1,
            ),
        ]

        politica = PolicyEngine(politicas=politicas).selecionar_politica(
            perfil_operacional="industrial",
            categoria="quimicos",
            parametro_id="ph",
        )

        self.assertEqual("parametro_ph", politica.identificador)

    def test_policy_engine_nao_chama_motor_observacional(self):
        with patch("monitoramento_hidrico.avaliacao.AvaliacaoObservacionalService.avaliar") as avaliar:
            politica = selecionar_politica_avaliacao(
                perfil_operacional="eta",
                categoria="quimicos",
                parametro_id="cloro_residual",
            )

        avaliar.assert_not_called()
        self.assertEqual("politica_observacional_eta", politica.identificador)


if __name__ == "__main__":
    unittest.main()
