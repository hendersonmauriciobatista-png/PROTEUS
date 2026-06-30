import inspect
import tempfile
import unittest
from pathlib import Path

from monitoramento_hidrico.projeto_monitoramento import (
    PROJETO_ATIVO_ID,
    ProjetoMonitoramento,
    ProjetoMonitoramentoStore,
    projeto_monitoramento_padrao,
    validar_projeto_monitoramento,
)
import monitoramento_hidrico.projeto_monitoramento as projeto_module


class ProjetoMonitoramentoTests(unittest.TestCase):
    def test_store_cria_e_carrega_projeto_padrao_unico(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "projeto_monitoramento.json"
            store = ProjetoMonitoramentoStore(path)

            projeto = store.carregar()
            recarregado = store.carregar()

        self.assertEqual(PROJETO_ATIVO_ID, projeto.identificador)
        self.assertEqual(projeto, recarregado)
        self.assertEqual("ativo", projeto.status)

    def test_projeto_minimo_valida_apenas_conceitos_aprovados(self):
        projeto = ProjetoMonitoramento(
            identificador=PROJETO_ATIVO_ID,
            nome="Monitoramento ETA Central",
            cliente="Cliente A",
            area_operacional="urbana",
            ponto_principal_coleta="eta",
            coletor_responsavel="Operador A",
            data_criacao="2026-06-30T20:00:00",
            status="ativo",
        )

        self.assertTrue(validar_projeto_monitoramento(projeto))

    def test_rejeita_multiplos_projetos_nesta_gp(self):
        projeto = projeto_monitoramento_padrao(criado_em="2026-06-30T20:00:00")
        outro = ProjetoMonitoramento(
            identificador="outro_projeto",
            nome=projeto.nome,
            cliente=projeto.cliente,
            area_operacional=projeto.area_operacional,
            ponto_principal_coleta=projeto.ponto_principal_coleta,
            coletor_responsavel=projeto.coletor_responsavel,
            data_criacao=projeto.data_criacao,
            status=projeto.status,
        )

        with self.assertRaises(ValueError):
            validar_projeto_monitoramento(outro)

    def test_modulo_de_projeto_nao_acessa_policy_engine_ou_motor_observacional(self):
        source = inspect.getsource(projeto_module)

        self.assertNotIn("PolicyEngine", source)
        self.assertNotIn("AvaliacaoObservacionalService", source)
        self.assertNotIn("projeto_id", source)


if __name__ == "__main__":
    unittest.main()
