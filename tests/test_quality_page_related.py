import ast
import unittest
from pathlib import Path


class QualityPageRelatedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parent.parent
        cls.quality_source = (cls.root / "qualidade_agua.py").read_text(encoding="utf-8")
        cls.quality_tree = ast.parse(cls.quality_source)
        cls.quality_class = next(
            node
            for node in cls.quality_tree.body
            if isinstance(node, ast.ClassDef) and node.name == "QualidadeAguaPage"
        )
        cls.methods = {
            node.name: node
            for node in cls.quality_class.body
            if isinstance(node, ast.FunctionDef)
        }

    def test_refresh_contract_delegates_to_load_history(self):
        refresh = self.methods["refresh"]

        self.assertEqual(1, len(refresh.body))
        call = refresh.body[0].value
        self.assertIsInstance(call, ast.Call)
        self.assertIsInstance(call.func, ast.Attribute)
        self.assertEqual("load_history", call.func.attr)

    def test_empty_repository_clears_table_rows(self):
        load_history_source = ast.get_source_segment(
            self.quality_source,
            self.methods["load_history"],
        )

        self.assertIn("rows = self.quality_service.listar_medicoes()", load_history_source)
        self.assertIn("self.table.setRowCount(len(rows))", load_history_source)

    def test_navigation_uses_page_refresh_contract(self):
        main_source = (self.root / "main.py").read_text(encoding="utf-8")

        self.assertIn('hasattr(current_page, "refresh")', main_source)
        self.assertIn("current_page.refresh()", main_source)

    def test_save_still_reloads_history(self):
        save_source = ast.get_source_segment(
            self.quality_source,
            self.methods["save_measurement"],
        )

        self.assertIn("self.quality_service.salvar_medicao(measurement)", save_source)
        self.assertIn("self.load_history()", save_source)


if __name__ == "__main__":
    unittest.main()
