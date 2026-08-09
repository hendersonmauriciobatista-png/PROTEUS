import csv
import tempfile
import unittest
from pathlib import Path

from data_access import CSVMeasurementRepository
from monitoramento_hidrico.application_context import HydricApplicationContext
from monitoramento_hidrico.configuracoes import ConfiguracaoOperacionalService


class SharedDataAccessTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.path = Path(self.temp_dir.name) / "measurements.csv"
        self.fields = ("timestamp", "ph", "turbidez")
        self.repository = CSVMeasurementRepository(self.path, self.fields)

    def test_csv_read_write_preserves_schema(self):
        self.repository.append({"timestamp": "2026-08-08T12:00:00", "ph": 7.2, "turbidez": 4.0})

        self.assertEqual(
            [{"timestamp": "2026-08-08T12:00:00", "ph": "7.2", "turbidez": "4.0"}],
            self.repository.read_all(),
        )
        with self.path.open("r", newline="", encoding="utf-8") as file:
            self.assertEqual(list(self.fields), next(csv.reader(file)))

    def test_csv_clear_preserves_header_and_removes_rows(self):
        self.repository.append({"timestamp": "2026-08-08T12:00:00", "ph": 7.2, "turbidez": 4.0})

        self.repository.clear()

        self.assertEqual([], self.repository.read_all())
        with self.path.open("r", newline="", encoding="utf-8") as file:
            self.assertEqual([list(self.fields)], list(csv.reader(file)))

    def test_missing_csv_reads_as_empty_without_creating_storage(self):
        self.assertEqual([], self.repository.read_all())
        self.assertFalse(self.path.exists())


class ApplicationContextTests(unittest.TestCase):
    def setUp(self):
        self.configuration_service = ConfiguracaoOperacionalService()

    def test_profile_is_propagated_from_operational_configuration(self):
        context = HydricApplicationContext.from_active_profile(
            "industrial",
            configuration_service=self.configuration_service,
            policy_engine_factory=lambda: object(),
            evaluation_service_factory=lambda: object(),
        )

        class Adapter:
            def __init__(self, policy_engine, evaluation_service, perfil_operacional):
                self.policy_engine = policy_engine
                self.evaluation_service = evaluation_service
                self.perfil_operacional = perfil_operacional

        adapter = context.build_policy_adapter(Adapter)

        self.assertEqual("industrial", context.configuracao_operacional.perfil_operacional_base)
        self.assertEqual("industrial", adapter.perfil_operacional)
        self.assertIs(context.policy_engine, adapter.policy_engine)
        self.assertIs(context.evaluation_service, adapter.evaluation_service)
