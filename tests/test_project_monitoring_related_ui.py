import ast
import tempfile
import unittest
from pathlib import Path

from monitoramento_hidrico.projeto_monitoramento import (
    STATUS_ATIVO,
    ProjetoMonitoramentoStore,
    arquivar_projeto,
    encerrar_projeto,
    reativar_monitoramento,
)


class ProjectMonitoringRelatedUiTests(unittest.TestCase):
    def test_reactivation_persists_only_status_change(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = ProjetoMonitoramentoStore(Path(temp_dir) / "projeto_monitoramento.json")
            ativo = store.carregar()
            encerrado = store.salvar(encerrar_projeto(ativo))
            arquivado = store.salvar(arquivar_projeto(encerrado))
            reativado = store.salvar(reativar_monitoramento(arquivado))

            self.assertEqual(STATUS_ATIVO, reativado.status)
            self.assertEqual(arquivado.__dict__ | {"status": STATUS_ATIVO}, reativado.__dict__)

    def test_ui_exposes_reactivate_action_only_for_archived_status(self):
        page_path = Path(__file__).resolve().parent.parent / "projeto_monitoramento_page.py"
        source = page_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        methods = {
            node.name: node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        self.assertIn('QPushButton("Reativar Monitoramento")', source)
        self.assertIn("reactivate_monitoring", methods)
        apply_status_source = ast.get_source_segment(source, methods["_apply_status_state"])
        self.assertIn("self.reactivate_button.setEnabled(projeto_arquivado)", apply_status_source)


if __name__ == "__main__":
    unittest.main()
