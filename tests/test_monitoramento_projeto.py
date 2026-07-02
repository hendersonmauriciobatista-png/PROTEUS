import inspect
import tempfile
import unittest
from pathlib import Path

from monitoramento_hidrico.projeto_monitoramento import (
    DOSSIE_FINAL_ID,
    PERFIS_OPERACIONAIS,
    PROJETO_ATIVO_ID,
    STATUS_ARQUIVADO,
    STATUS_ATIVO,
    STATUS_ENCERRADO,
    STATUS_PROJETO,
    DossierFinalStore,
    ProjetoMonitoramento,
    ProjetoMonitoramentoStore,
    arquivar_projeto,
    derivar_perfil_operacional,
    dossier_final_do_projeto,
    encerrar_projeto,
    projeto_monitoramento_padrao,
    validar_dossier_final,
    validar_transicao_status,
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
        self.assertEqual("urbano_saneamento", projeto.perfil_operacional)
        self.assertEqual((STATUS_ATIVO, STATUS_ENCERRADO, STATUS_ARQUIVADO), STATUS_PROJETO)

    def test_projeto_minimo_valida_apenas_conceitos_aprovados(self):
        projeto = ProjetoMonitoramento(
            identificador=PROJETO_ATIVO_ID,
            nome="Monitoramento ETA Central",
            cliente="Cliente A",
            area_operacional="urbana",
            ponto_principal_coleta="eta",
            coletor_responsavel="Operador A",
            data_criacao="2026-06-30T20:00:00",
            perfil_operacional="urbano_saneamento",
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
            perfil_operacional=projeto.perfil_operacional,
            status=projeto.status,
        )

        with self.assertRaises(ValueError):
            validar_projeto_monitoramento(outro)

    def test_contexto_operacional_deriva_perfil_aprovado(self):
        self.assertEqual("urbano_saneamento", derivar_perfil_operacional("urbana"))
        self.assertEqual("rural", derivar_perfil_operacional("rural"))
        self.assertEqual("industrial", derivar_perfil_operacional("industrial"))
        self.assertEqual("rural", derivar_perfil_operacional("agricola"))
        self.assertNotIn("agricola", PERFIS_OPERACIONAIS)

    def test_rejeita_perfil_operacional_inconsistente_com_contexto(self):
        projeto = ProjetoMonitoramento(
            identificador=PROJETO_ATIVO_ID,
            nome="Monitoramento Agricola",
            cliente="Cliente A",
            area_operacional="agricola",
            ponto_principal_coleta="rio",
            coletor_responsavel="Operador A",
            data_criacao="2026-06-30T20:00:00",
            perfil_operacional="industrial",
            status="ativo",
        )

        with self.assertRaises(ValueError):
            validar_projeto_monitoramento(projeto)

    def test_encerrar_e_arquivar_respeitam_transicoes_minimas(self):
        projeto = projeto_monitoramento_padrao(criado_em="2026-06-30T20:00:00")

        encerrado = encerrar_projeto(projeto)
        arquivado = arquivar_projeto(encerrado)

        self.assertEqual(STATUS_ENCERRADO, encerrado.status)
        self.assertEqual(STATUS_ARQUIVADO, arquivado.status)

    def test_rejeita_arquivamento_direto_de_projeto_ativo(self):
        projeto = projeto_monitoramento_padrao(criado_em="2026-06-30T20:00:00")

        with self.assertRaises(ValueError):
            arquivar_projeto(projeto)

        with self.assertRaises(ValueError):
            validar_transicao_status(STATUS_ATIVO, STATUS_ARQUIVADO)

    def test_store_persiste_estado_e_bloqueia_salto_direto_para_arquivado(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "projeto_monitoramento.json"
            store = ProjetoMonitoramentoStore(path)
            projeto = store.carregar()

            direto_arquivado = ProjetoMonitoramento(
                identificador=projeto.identificador,
                nome=projeto.nome,
                cliente=projeto.cliente,
                area_operacional=projeto.area_operacional,
                ponto_principal_coleta=projeto.ponto_principal_coleta,
                coletor_responsavel=projeto.coletor_responsavel,
                data_criacao=projeto.data_criacao,
                perfil_operacional=projeto.perfil_operacional,
                status=STATUS_ARQUIVADO,
            )

            with self.assertRaises(ValueError):
                store.salvar(direto_arquivado)

            encerrado = store.salvar(encerrar_projeto(projeto))
            arquivado = store.salvar(arquivar_projeto(encerrado))
            recarregado = store.carregar()

        self.assertEqual(STATUS_ENCERRADO, encerrado.status)
        self.assertEqual(STATUS_ARQUIVADO, arquivado.status)
        self.assertEqual(STATUS_ARQUIVADO, recarregado.status)

    def test_dossie_final_estrutura_projeto_encerrado_com_campos_finais_opcionais(self):
        projeto = encerrar_projeto(projeto_monitoramento_padrao(criado_em="2026-06-30T20:00:00"))

        dossie = dossier_final_do_projeto(projeto)

        self.assertEqual(DOSSIE_FINAL_ID, dossie.identificador)
        self.assertEqual(PROJETO_ATIVO_ID, dossie.identificador_projeto)
        self.assertEqual(projeto.nome, dossie.projeto_nome)
        self.assertEqual(projeto.cliente, dossie.cliente)
        self.assertEqual(projeto.area_operacional, dossie.contexto_operacional)
        self.assertEqual(projeto.perfil_operacional, dossie.perfil_operacional)
        self.assertEqual(STATUS_ENCERRADO, dossie.status_projeto)
        self.assertEqual("", dossie.periodo_inicio)
        self.assertEqual("", dossie.periodo_fim)
        self.assertEqual("", dossie.data_encerramento)
        self.assertTrue(validar_dossier_final(dossie))

    def test_dossie_final_rejeita_projeto_ativo(self):
        projeto = projeto_monitoramento_padrao(criado_em="2026-06-30T20:00:00")

        with self.assertRaises(ValueError):
            dossier_final_do_projeto(projeto)

    def test_store_persiste_dossie_final_associado_ao_projeto_encerrado(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "dossie_final_projeto.json"
            store = DossierFinalStore(path)
            projeto = encerrar_projeto(projeto_monitoramento_padrao(criado_em="2026-06-30T20:00:00"))
            dossie = dossier_final_do_projeto(
                projeto,
                periodo_inicio="2026-06-01",
                periodo_fim="2026-06-30",
                data_encerramento="2026-07-01T10:00:00",
            )

            salvo = store.salvar(dossie)
            recarregado = store.carregar()

        self.assertEqual(salvo, recarregado)
        self.assertEqual(PROJETO_ATIVO_ID, recarregado.identificador_projeto)
        self.assertEqual("2026-06-01", recarregado.periodo_inicio)
        self.assertEqual("2026-06-30", recarregado.periodo_fim)
        self.assertEqual("2026-07-01T10:00:00", recarregado.data_encerramento)

    def test_modulo_de_projeto_nao_acessa_policy_engine_ou_motor_observacional(self):
        source = inspect.getsource(projeto_module)

        self.assertNotIn("PolicyEngine", source)
        self.assertNotIn("AvaliacaoObservacionalService", source)
        self.assertNotIn("projeto_id", source)


if __name__ == "__main__":
    unittest.main()
