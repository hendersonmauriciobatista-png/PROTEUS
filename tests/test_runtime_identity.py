import ast
import unittest
from pathlib import Path


class RuntimeIdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parent.parent
        cls.main_path = cls.root / "main.py"
        cls.main_source = cls.main_path.read_text(encoding="utf-8")
        cls.main_tree = ast.parse(cls.main_source)

    def test_current_identity_replaces_legacy_visible_branding(self):
        self.assertIn(
            'CURRENT_IDENTITY = "Sistema de Monitoramento de Águas"',
            self.main_source,
        )
        self.assertIn("self.setWindowTitle(CURRENT_IDENTITY)", self.main_source)
        for legacy in (
            "PROTEUS",
            "Sistema de Análise de Água",
            "AquaAnalysis",
            "SISTEMA DE ANALISE",
        ):
            self.assertNotIn(legacy, self.main_source)

    def test_official_asset_is_loaded_without_source_mutation(self):
        self.assertIn('"sistema_monitoramento_aguas.png"', self.main_source)
        self.assertIn("QPixmap(str(OFFICIAL_IDENTITY_ASSET))", self.main_source)
        self.assertIn("Qt.KeepAspectRatio", self.main_source)
        self.assertNotIn("save(", self.main_source)

    def test_navigation_items_and_order_are_preserved(self):
        main_window = next(
            node
            for node in self.main_tree.body
            if isinstance(node, ast.ClassDef) and node.name == "MainWindow"
        )
        build_ui = next(
            node
            for node in main_window.body
            if isinstance(node, ast.FunctionDef) and node.name == "_build_ui"
        )
        nav_assignment = next(
            node
            for node in ast.walk(build_ui)
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "nav_items"
                for target in node.targets
            )
        )
        self.assertEqual(
            [
                ("Projeto de Monitoramento", 0),
                ("Dashboard", 1),
                ("Painel Executivo", 2),
                ("Qualidade da Água", 2),
                ("Consumo e Distribuição", 3),
                ("Dados Ambientais", 4),
                ("Relatórios", 5),
                ("Previsao Analitica", 7),
                ("Governanca Operacional", 8),
                ("Administração", 9),
                ("Entrada Governada", 10),
            ],
            ast.literal_eval(nav_assignment.value),
        )


if __name__ == "__main__":
    unittest.main()
