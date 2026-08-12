import ast
import unittest
from pathlib import Path


class AnalyticsMessageVisibilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parent.parent
        cls.source = (cls.root / "previsao_analitica.py").read_text(encoding="utf-8")
        tree = ast.parse(cls.source)
        page = next(
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "PrevisaoAnaliticaPage"
        )
        cls.methods = {
            node.name: node
            for node in page.body
            if isinstance(node, ast.FunctionDef)
        }

    def method_source(self, name):
        return ast.get_source_segment(self.source, self.methods[name])

    def test_alerts_table_wraps_text_and_uses_content_aware_columns(self):
        style_source = self.method_source("_style_alerts_table")

        self.assertIn("self.alerts_table.setWordWrap(True)", style_source)
        self.assertIn("for column_index in (0, 1, 2)", style_source)
        self.assertIn("QHeaderView.ResizeToContents", style_source)
        self.assertIn("for column_index in (3, 4)", style_source)
        self.assertIn("QHeaderView.Stretch", style_source)

    def test_message_and_evidence_keep_exact_tooltip_text(self):
        load_source = self.method_source("_load_alerts")

        self.assertIn("if column_index in (3, 4)", load_source)
        self.assertIn("item.setToolTip(value)", load_source)
        self.assertNotIn("value[:", load_source)
        self.assertNotIn("...", load_source)

    def test_alert_rows_resize_after_population(self):
        load_alerts = self.methods["_load_alerts"]
        last_statement = load_alerts.body[-1]

        self.assertIsInstance(last_statement, ast.Expr)
        call = last_statement.value
        self.assertIsInstance(call, ast.Call)
        self.assertEqual("resizeRowsToContents", call.func.attr)

    def test_trends_table_keeps_shared_style_only(self):
        build_source = self.method_source("_build_ui")

        self.assertIn("self._style_table(self.trends_table)", build_source)
        self.assertNotIn("self._style_alerts_table(self.trends_table)", build_source)

    def test_analytics_modules_are_unchanged_consumers(self):
        self.assertIn("snapshot = self.analytics_service.build_snapshot()", self.method_source("refresh"))
        self.assertEqual(
            ["executive", "governance", "monitoramento_hidrico"],
            sorted([path.name for path in self.root.iterdir() if path.name in {"executive", "governance", "monitoramento_hidrico"}]),
        )


if __name__ == "__main__":
    unittest.main()
