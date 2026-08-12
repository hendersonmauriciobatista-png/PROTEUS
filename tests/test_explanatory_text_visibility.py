import ast
import unittest
from pathlib import Path


class ExplanatoryTextVisibilityTests(unittest.TestCase):
    ROOT = Path(__file__).resolve().parent.parent

    def methods(self, relative_path, class_name):
        source = (self.ROOT / relative_path).read_text(encoding="utf-8")
        tree = ast.parse(source)
        page = next(
            node for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == class_name
        )
        return source, {
            node.name: node for node in page.body if isinstance(node, ast.FunctionDef)
        }

    def method_source(self, source, methods, name):
        return ast.get_source_segment(source, methods[name])

    def test_executive_tables_use_target_specific_visibility_layouts(self):
        source, methods = self.methods("painel_executivo.py", "PainelExecutivoPage")
        build = self.method_source(source, methods, "_build_ui")
        style = self.method_source(source, methods, "_style_explanatory_table")

        self.assertIn("(0, 3), (1, 2, 4)", build)
        self.assertIn("(0, 2), (1, 3, 4)", build)
        self.assertIn("(0, 1, 2), (3,)", build)
        self.assertIn("QHeaderView.ResizeToContents", style)
        self.assertIn("QHeaderView.Stretch", style)
        self.assertIn("table.setWordWrap(True)", style)

    def test_executive_loaders_resize_rows_and_keep_exact_tooltips(self):
        source, methods = self.methods("painel_executivo.py", "PainelExecutivoPage")
        expectations = {
            "_load_recommendations": ("(1, 2, 4)", "recommendations_table"),
            "_load_priorities": ("(1, 3, 4)", "priorities_table"),
            "_load_signals": ("column_index == 3", "signals_table"),
        }
        for method_name, (columns, table_name) in expectations.items():
            with self.subTest(method=method_name):
                method = self.method_source(source, methods, method_name)
                self.assertIn(columns, method)
                self.assertIn("item.setToolTip(value)", method)
                self.assertIn(f"self.{table_name}.resizeRowsToContents()", method)

    def test_governance_table_compacts_metadata_and_expands_explanatory_columns(self):
        source, methods = self.methods("governanca_operacional.py", "GovernancaOperacionalPage")
        build = self.method_source(source, methods, "_build_ui")
        load = self.method_source(source, methods, "_load_table")

        self.assertIn("for column_index in (0, 1, 2, 3, 4, 5)", build)
        self.assertIn("QHeaderView.ResizeToContents", build)
        self.assertIn("for column_index in (6, 7)", build)
        self.assertIn("QHeaderView.Stretch", build)
        self.assertIn("self.table.setWordWrap(True)", build)
        self.assertIn("if column_index in (6, 7)", load)
        self.assertIn("item.setToolTip(value)", load)
        self.assertIn("self.table.resizeRowsToContents()", load)

    def test_quality_page_remains_outside_visibility_change(self):
        quality_source = (self.ROOT / "qualidade_agua.py").read_text(encoding="utf-8")

        self.assertNotIn("_style_explanatory_table", quality_source)
        self.assertNotIn("resizeRowsToContents", quality_source)

    def test_content_sources_remain_unchanged_in_ui_loaders(self):
        executive_source = (self.ROOT / "painel_executivo.py").read_text(encoding="utf-8")
        governance_source = (self.ROOT / "governanca_operacional.py").read_text(encoding="utf-8")

        self.assertIn("recommendation.rationale", executive_source)
        self.assertIn("priority.evidence", executive_source)
        self.assertIn("f\"{alert.message} | {alert.evidence}\"", executive_source)
        self.assertIn("event.evidence", governance_source)
        self.assertIn("event.recommendation", governance_source)


if __name__ == "__main__":
    unittest.main()
