import tempfile
import unittest
from pathlib import Path

from data_access import CSVMeasurementRepository, QUALITY_WATER_FIELDS
from monitoramento_hidrico.application_context import HydricApplicationContext
from monitoramento_hidrico.configuracoes import ConfiguracaoOperacionalService
from monitoramento_hidrico.qualidade_agua_adapter import (
    QualidadeAguaApplicationService,
    QualidadeAguaMonitoringAdapter,
)


class RecordingPolicyEngine:
    def __init__(self, delegate):
        self.delegate = delegate
        self.calls = []

    def selecionar_politica(self, perfil_operacional=None, categoria=None, parametro_id=None):
        self.calls.append((perfil_operacional, categoria, parametro_id))
        return self.delegate.selecionar_politica(perfil_operacional, categoria, parametro_id)


class AI02Phase2IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.repository = CSVMeasurementRepository(
            Path(self.temp_dir.name) / "qualidade.csv",
            QUALITY_WATER_FIELDS,
        )
        base_context = HydricApplicationContext.from_active_profile(
            "urbano_saneamento",
            configuration_service=ConfiguracaoOperacionalService(),
        )
        self.recording_policy_engine = RecordingPolicyEngine(base_context.policy_engine)
        self.context = HydricApplicationContext(
            configuracao_operacional=base_context.configuracao_operacional,
            policy_engine=self.recording_policy_engine,
            evaluation_service=base_context.evaluation_service,
        )
        self.monitoring_adapter = self.context.build_policy_adapter(
            QualidadeAguaMonitoringAdapter
        )
        self.quality_service = QualidadeAguaApplicationService(
            repository=self.repository,
            monitoring_adapter=self.monitoring_adapter,
        )

    def test_save_and_read_use_shared_repository_with_unchanged_schema(self):
        measurement = {
            "timestamp": "2026-08-08T12:00:00",
            "ph": 7.2,
            "turbidez": 4.0,
            "oxigenio_dissolvido": 6.0,
            "temperatura": 24.0,
            "agrotoxicos": 0.0,
        }

        self.quality_service.salvar_medicao(measurement)

        rows = self.quality_service.listar_medicoes()
        self.assertEqual(1, len(rows))
        self.assertEqual(list(QUALITY_WATER_FIELDS), list(rows[0]))

    def test_profile_from_configuration_reaches_every_policy_selection(self):
        measurement = {
            "ph": 7.2,
            "turbidez": 4.0,
            "oxigenio_dissolvido": 6.0,
            "temperatura": 24.0,
            "agrotoxicos": 0.0,
        }

        self.quality_service.status_medicao(measurement)

        self.assertTrue(self.recording_policy_engine.calls)
        self.assertEqual(
            {"urbano_saneamento"},
            {call[0] for call in self.recording_policy_engine.calls},
        )

    def test_same_measurement_produces_same_core_result(self):
        measurement = {
            "ph": 7.2,
            "turbidez": 10.0,
            "oxigenio_dissolvido": 6.0,
            "temperatura": 24.0,
            "agrotoxicos": 0.0,
        }
        comparison_adapter = self.context.build_policy_adapter(QualidadeAguaMonitoringAdapter)

        page_result = self.quality_service.status_medicao(measurement)
        comparison_result = comparison_adapter.status_medicao(measurement)

        self.assertEqual(page_result, comparison_result)

    def test_quality_page_has_no_direct_csv_access(self):
        source = Path("qualidade_agua.py").read_text(encoding="utf-8")

        self.assertNotIn("import csv", source)
        self.assertNotIn("DictReader", source)
        self.assertNotIn("DictWriter", source)
        self.assertNotIn(".open(", source)


if __name__ == "__main__":
    unittest.main()
