import ast
import unittest
from pathlib import Path


class PostResetRefreshContractTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def _class_methods(self, relative_path, class_name):
        source = (self.ROOT / relative_path).read_text(encoding="utf-8")
        tree = ast.parse(source)
        page_class = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == class_name
        )
        methods = {
            node.name: node
            for node in page_class.body
            if isinstance(node, ast.FunctionDef)
        }
        return source, methods

    def _assert_refresh_contract(self, relative_path, class_name):
        source, methods = self._class_methods(relative_path, class_name)
        refresh = methods["refresh"]
        self.assertEqual(1, len(refresh.body))
        call = refresh.body[0].value
        self.assertIsInstance(call, ast.Call)
        self.assertIsInstance(call.func, ast.Attribute)
        self.assertEqual("load_history", call.func.attr)

        load_history_source = ast.get_source_segment(source, methods["load_history"])
        self.assertIn("self.table.setRowCount(len(rows))", load_history_source)

        save_source = ast.get_source_segment(source, methods["save_measurement"])
        self.assertIn("self.load_history()", save_source)

    def test_consumption_refresh_delegates_and_preserves_empty_state_contract(self):
        self._assert_refresh_contract(
            "consumo_distribuicao.py",
            "ConsumoDistribuicaoPage",
        )

    def test_environment_refresh_delegates_and_preserves_empty_state_contract(self):
        self._assert_refresh_contract(
            "dados_ambientais.py",
            "DadosAmbientaisPage",
        )

    def test_navigation_refresh_contract_remains_centralized(self):
        main_source = (self.ROOT / "main.py").read_text(encoding="utf-8")
        self.assertIn('hasattr(current_page, "refresh")', main_source)
        self.assertIn("current_page.refresh()", main_source)

    def test_derived_pages_keep_their_refresh_contracts(self):
        for relative_path, class_name in (
            ("painel_executivo.py", "PainelExecutivoPage"),
            ("previsao_analitica.py", "PrevisaoAnaliticaPage"),
        ):
            with self.subTest(page=relative_path):
                _source, methods = self._class_methods(relative_path, class_name)
                self.assertIn("refresh", methods)


if __name__ == "__main__":
    unittest.main()
