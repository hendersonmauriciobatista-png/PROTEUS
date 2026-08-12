import csv
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from administracao import HistoryMaintenanceService
from governance.models import EventState


FIELDS = {
    "qualidade_agua": ["timestamp", "ph"],
    "consumo_distribuicao": ["timestamp", "consumo_diario"],
    "dados_ambientais": ["timestamp", "chuva"],
}


class FakeAnalyticsService:
    def __init__(self, alerts=None):
        self.alerts = alerts or []

    def build_snapshot(self):
        return SimpleNamespace(alerts=self.alerts)


class FakeGovernanceService:
    def __init__(self, events=None):
        self.events = events or []

    def list_events(self):
        return self.events


class FakeMonitoringAdapter:
    def __init__(self, nonconformities=0):
        self.nonconformities = nonconformities

    def contar_observacional_atencao(self, _rows):
        return self.nonconformities


class HistoryMaintenanceServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        base = Path(self.temp_dir.name)
        self.modules = {}
        for module_id, fields in FIELDS.items():
            path = base / f"{module_id}.csv"
            self.modules[module_id] = {
                "label": module_id,
                "path": path,
                "fields": fields,
            }
            with path.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                writer.writerow({fields[0]: "2026-01-01", fields[1]: "1"})

    def tearDown(self):
        self.temp_dir.cleanup()

    def make_service(self, alerts=None, events=None, nonconformities=0):
        return HistoryMaintenanceService(
            modules=self.modules,
            analytics_service=FakeAnalyticsService(alerts),
            governance_service=FakeGovernanceService(events),
            monitoring_adapter=FakeMonitoringAdapter(nonconformities),
        )

    def test_clears_each_module_individually_and_preserves_other_histories(self):
        service = self.make_service()
        for module_id in self.modules:
            with self.subTest(module=module_id):
                result = service.clear_history(module_id)
                self.assertTrue(result.cleared)
                self.assertEqual(1, result.removed_records)
                self.assertEqual(0, service.record_count(module_id))
                for other_id in self.modules:
                    if other_id != module_id:
                        self.assertEqual(1, service.record_count(other_id))
                self._restore_row(module_id)

    def test_quality_nonconformity_requires_confirmation_but_does_not_block(self):
        service = self.make_service(nonconformities=1)
        result = service.clear_history("qualidade_agua")
        self.assertFalse(result.cleared)
        self.assertTrue(result.confirmation_required)
        self.assertEqual(1, service.record_count("qualidade_agua"))

        confirmed = service.clear_history("qualidade_agua", confirmed=True)
        self.assertTrue(confirmed.cleared)
        self.assertEqual(0, service.record_count("qualidade_agua"))

    def test_quality_alert_requires_confirmation_but_does_not_block(self):
        alert = SimpleNamespace(domain="qualidade_agua")
        service = self.make_service(alerts=[alert])

        pending = service.clear_history("qualidade_agua")
        confirmed = service.clear_history("qualidade_agua", confirmed=True)

        self.assertTrue(pending.confirmation_required)
        self.assertFalse(pending.cleared)
        self.assertTrue(confirmed.cleared)

    def test_blocks_cleaning_for_active_alert_in_same_module(self):
        alert = SimpleNamespace(domain="dados_ambientais")
        service = self.make_service(alerts=[alert])
        result = service.clear_history("dados_ambientais")
        self.assertFalse(result.cleared)
        self.assertEqual(1, service.record_count("dados_ambientais"))

    def test_blocks_cleaning_for_active_event_in_same_module(self):
        event = SimpleNamespace(
            domain="consumo_distribuicao",
            state=EventState.MONITORAMENTO.value,
        )
        service = self.make_service(events=[event])
        result = service.clear_history("consumo_distribuicao")
        self.assertFalse(result.cleared)
        self.assertEqual(1, service.record_count("consumo_distribuicao"))

    def test_active_quality_event_cannot_be_bypassed_by_confirmation(self):
        event = SimpleNamespace(
            domain="qualidade_agua",
            state=EventState.MONITORAMENTO.value,
        )
        service = self.make_service(events=[event], nonconformities=1)

        result = service.clear_history("qualidade_agua", confirmed=True)

        self.assertFalse(result.cleared)
        self.assertFalse(result.confirmation_required)
        self.assertEqual(1, service.record_count("qualidade_agua"))

    def test_quality_confirmation_displays_counts_and_irreversible_warning(self):
        source = (Path(__file__).resolve().parent.parent / "administracao.py").read_text(encoding="utf-8")

        self.assertIn("Medições que serão removidas", source)
        self.assertIn("Não conformidades derivadas", source)
        self.assertIn("Alertas analíticos ativos", source)
        self.assertIn("Esta operação é irreversível", source)
        self.assertIn("clear_history(module_id, confirmed=True)", source)

    def test_governance_reset_ui_requires_counts_confirmation_and_backup_result(self):
        source = (Path(__file__).resolve().parent.parent / "administracao.py").read_text(encoding="utf-8")

        self.assertIn('QPushButton("Limpar histórico de Governança")', source)
        self.assertIn("Eventos resolvidos que serão removidos", source)
        self.assertIn("Eventos arquivados que serão removidos", source)
        self.assertIn("Esta operação é irreversível", source)
        self.assertIn("reset_terminal_history(confirmed=True)", source)
        self.assertIn("Backup: {result.backup_path}", source)

    def test_ignores_resolved_events_and_dependencies_from_other_modules(self):
        alerts = [SimpleNamespace(domain="dados_ambientais")]
        events = [
            SimpleNamespace(
                domain="qualidade_agua",
                state=EventState.RESOLVIDO.value,
            ),
            SimpleNamespace(
                domain="dados_ambientais",
                state=EventState.ABERTO.value,
            ),
        ]
        service = self.make_service(alerts=alerts, events=events)
        result = service.clear_history("consumo_distribuicao")
        self.assertTrue(result.cleared)
        self.assertEqual(1, service.record_count("qualidade_agua"))
        self.assertEqual(1, service.record_count("dados_ambientais"))

    def _restore_row(self, module_id):
        module = self.modules[module_id]
        with Path(module["path"]).open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=module["fields"])
            writer.writerow(
                {
                    module["fields"][0]: "2026-01-01",
                    module["fields"][1]: "1",
                }
            )


if __name__ == "__main__":
    unittest.main()
