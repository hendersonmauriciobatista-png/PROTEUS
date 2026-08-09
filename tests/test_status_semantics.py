from pathlib import Path
import unittest

from monitoramento_hidrico.status_semantics import (
    EXECUTIVE_STATUS_OBSERVATIONAL_ATTENTION,
    EXECUTIVE_STATUS_OBSERVATIONAL_CRITICAL,
    EXECUTIVE_STATUS_OBSERVATIONAL_NORMAL,
    QUALITY_STATUS_OBSERVATIONAL_ATTENTION,
    QUALITY_STATUS_OBSERVATIONAL_NORMAL,
    STATUS_CONTEXT_ANALYTICAL_SCORE,
    STATUS_CONTEXT_EXECUTIVE,
    STATUS_CONTEXT_OBSERVATIONAL,
    STATUS_SEMANTICS,
    WATER_HEALTH_SCORE_ATTENTION,
    WATER_HEALTH_SCORE_CRITICAL,
    WATER_HEALTH_SCORE_EXCELLENT,
    WATER_HEALTH_SCORE_GOOD,
    WATER_HEALTH_SCORE_NO_DATA,
    WATER_HEALTH_SCORE_VERY_CRITICAL,
    observational_status_label,
    aggregate_observational_status,
    QUALITY_STATUS_OBSERVATIONAL_ATTENTION,
    QUALITY_STATUS_OBSERVATIONAL_CRITICAL,
    QUALITY_STATUS_OBSERVATIONAL_NORMAL,
    QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE,
)


class StatusSemanticsTests(unittest.TestCase):
    def test_agregacao_nao_avaliavel_permanece_informativa(self):
        self.assertEqual(
            QUALITY_STATUS_OBSERVATIONAL_NOT_EVALUABLE,
            aggregate_observational_status(["NAO_AVALIAVEL"]),
        )

    def test_normal_com_nao_avaliavel_nao_promove_risco(self):
        self.assertEqual(
            QUALITY_STATUS_OBSERVATIONAL_NORMAL,
            aggregate_observational_status(["NORMAL", "NAO_AVALIAVEL"]),
        )

    def test_atencao_tem_precedencia_sobre_nao_avaliavel(self):
        self.assertEqual(
            QUALITY_STATUS_OBSERVATIONAL_ATTENTION,
            aggregate_observational_status(["ATENCAO", "NAO_AVALIAVEL"]),
        )

    def test_critico_tem_precedencia_sobre_demais_status(self):
        self.assertEqual(
            QUALITY_STATUS_OBSERVATIONAL_CRITICAL,
            aggregate_observational_status(["NORMAL", "ATENCAO", "CRITICO", "NAO_AVALIAVEL"]),
        )
    def test_official_status_vocabulary_has_context_and_non_normative_boundary(self):
        expected_labels = {
            QUALITY_STATUS_OBSERVATIONAL_NORMAL,
            QUALITY_STATUS_OBSERVATIONAL_ATTENTION,
            WATER_HEALTH_SCORE_NO_DATA,
            WATER_HEALTH_SCORE_EXCELLENT,
            WATER_HEALTH_SCORE_GOOD,
            WATER_HEALTH_SCORE_ATTENTION,
            WATER_HEALTH_SCORE_CRITICAL,
            WATER_HEALTH_SCORE_VERY_CRITICAL,
            EXECUTIVE_STATUS_OBSERVATIONAL_NORMAL,
            EXECUTIVE_STATUS_OBSERVATIONAL_ATTENTION,
            EXECUTIVE_STATUS_OBSERVATIONAL_CRITICAL,
        }

        self.assertTrue(expected_labels.issubset(set(STATUS_SEMANTICS)))
        for label in expected_labels:
            semantic = STATUS_SEMANTICS[label]
            self.assertIn(
                semantic["context"],
                {STATUS_CONTEXT_OBSERVATIONAL, STATUS_CONTEXT_ANALYTICAL_SCORE, STATUS_CONTEXT_EXECUTIVE},
            )
            self.assertTrue(semantic["origin"])
            self.assertTrue(semantic["meaning"])
            self.assertTrue(semantic["not_meaning"])

    def test_observational_engine_codes_are_translated_before_communication(self):
        self.assertEqual("Avaliacao observacional normal", observational_status_label("NORMAL"))
        self.assertEqual("Avaliacao observacional em atencao", observational_status_label("ATENCAO"))
        self.assertEqual("Avaliacao observacional critica", observational_status_label("CRITICO"))
        self.assertEqual("Avaliacao observacional nao avaliavel", observational_status_label("NAO_AVALIAVEL"))

    def test_ambiguous_quality_labels_do_not_return_to_runtime_components(self):
        runtime_files = [
            Path("monitoramento_hidrico/qualidade_agua_adapter.py"),
            Path("monitoramento_hidrico/dashboard_adapter.py"),
            Path("monitoramento_hidrico/operational_reports_adapter.py"),
            Path("analytics/scoring.py"),
            Path("analytics/alerts.py"),
            Path("painel_executivo.py"),
            Path("relatorios.py"),
        ]
        forbidden_fragments = [
            "Dentro do padrao",
            "Dentro do padrão",
            "Fora do padrao",
            "Fora do padrão",
            "Status Executivo",
            "status CRITICO",
        ]

        for runtime_file in runtime_files:
            source = runtime_file.read_text(encoding="utf-8")
            for fragment in forbidden_fragments:
                self.assertNotIn(fragment, source, runtime_file)


if __name__ == "__main__":
    unittest.main()
