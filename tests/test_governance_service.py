import tempfile
import unittest
from pathlib import Path

from analytics.models import AnalyticsSnapshot, PreventiveAlert, WaterHealthScore
from governance.models import EventState
from governance.repositories import OperationalEventRepository
from governance.service import OperationalGovernanceService
from monitoramento_hidrico.status_semantics import WATER_HEALTH_SCORE_GOOD


class FakeAnalyticsService:
    def __init__(self, alerts):
        self.alerts = alerts

    def build_snapshot(self):
        return AnalyticsSnapshot(
            quality_trends=[],
            consumption_trends=[],
            alerts=self.alerts,
            water_health_score=WaterHealthScore(score=80, status=WATER_HEALTH_SCORE_GOOD, explanations=[]),
        )


class RecordingMonitoringAdapter:
    def __init__(self, wrapped):
        self.wrapped = wrapped
        self.policy_engine = wrapped.policy_engine
        self.perfil_operacional = wrapped.perfil_operacional
        self.received_decisions = None

    def enriquecer_alertas(self, alerts, decisions=None):
        self.received_decisions = list(decisions or [])
        return self.wrapped.enriquecer_alertas(alerts, decisions)


class OperationalGovernanceServiceTests(unittest.TestCase):
    def test_sync_from_analytics_persists_events(self):
        alert = PreventiveAlert(
            severity="alto",
            domain="qualidade_agua",
            metric="ph",
            message="Atencao preventiva: pH fora da faixa.",
            evidence="Valor atual 5.5000",
            recommendation="Acompanhar novas coletas.",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = OperationalEventRepository(Path(temp_dir) / "eventos.json")
            service = OperationalGovernanceService(
                repository=repository,
                analytics_service=FakeAnalyticsService([alert]),
            )

            result = service.sync_from_analytics()
            events = service.list_events()

            self.assertEqual(1, result["created"])
            self.assertEqual(1, len(events))
            self.assertEqual(EventState.ABERTO.value, events[0].state)
            self.assertEqual("ATENCAO", events[0].observational_status)
            self.assertEqual("catalogo:limite_observacional", events[0].limit_origin)
            self.assertTrue(events[0].policy_id)
            self.assertIn("resultado ATENCAO", events[0].explainability)
            self.assertIn("reavaliacao_controlada=executada", events[0].explainability)

    def test_manual_actions_update_state(self):
        alert = PreventiveAlert(
            severity="alto",
            domain="qualidade_agua",
            metric="ph",
            message="Atencao preventiva: pH fora da faixa.",
            evidence="Valor atual 5.5000",
            recommendation="Acompanhar novas coletas.",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = OperationalEventRepository(Path(temp_dir) / "eventos.json")
            service = OperationalGovernanceService(
                repository=repository,
                analytics_service=FakeAnalyticsService([alert]),
            )
            service.sync_from_analytics()
            event_id = service.list_events()[0].event_id

            self.assertTrue(service.move_to_monitoring(event_id))
            self.assertTrue(service.resolve_event(event_id, "Resolvido por observacao."))
            self.assertTrue(service.archive_event(event_id, "Arquivo historico."))

            event = service.list_events()[0]
            self.assertEqual(EventState.ARQUIVADO.value, event.state)
            self.assertEqual("Resolvido por observacao.", event.resolution_note)
            self.assertEqual("Arquivo historico.", event.archived_reason)

    def test_archived_event_returns_to_monitoring_and_persists_cleared_terminal_fields(self):
        alert = PreventiveAlert(
            severity="alto",
            domain="qualidade_agua",
            metric="ph",
            message="Atencao preventiva: pH fora da faixa.",
            evidence="Valor atual 5.5000",
            recommendation="Acompanhar novas coletas.",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = OperationalEventRepository(Path(temp_dir) / "eventos.json")
            service = OperationalGovernanceService(
                repository=repository,
                analytics_service=FakeAnalyticsService([alert]),
            )
            service.sync_from_analytics()
            original = service.list_events()[0]
            event_id = original.event_id
            service.resolve_event(event_id, "Resolvido por observacao.")
            service.archive_event(event_id, "Arquivo historico.")
            archived = service.list_events()[0]

            self.assertTrue(service.move_to_monitoring(event_id))
            reloaded = OperationalEventRepository(repository.path).load_events()[0]

            self.assertEqual(EventState.MONITORAMENTO.value, reloaded.state)
            self.assertIsNone(reloaded.closed_at)
            self.assertEqual("", reloaded.resolution_note)
            self.assertEqual("", reloaded.archived_reason)
            for field_name in (
                "event_id", "domain", "metric", "severity", "occurrence_count",
                "evidence", "recommendation", "created_at",
            ):
                self.assertEqual(getattr(archived, field_name), getattr(reloaded, field_name))

    def test_monitoring_ui_action_is_enabled_only_for_open_or_archived_events(self):
        source = (Path(__file__).resolve().parent.parent / "governanca_operacional.py").read_text(encoding="utf-8")

        self.assertIn("self.monitor_button.clicked.connect(self.move_selected_to_monitoring)", source)
        self.assertIn("self.table.itemSelectionChanged.connect(self._update_action_states)", source)
        self.assertIn(
            "event.state in {EventState.ABERTO.value, EventState.ARQUIVADO.value}",
            source,
        )

    def test_sync_decides_controlled_reevaluation_before_enrichment(self):
        alert = PreventiveAlert(
            severity="alto",
            domain="qualidade_agua",
            metric="ph",
            message="Atencao preventiva: pH fora da faixa.",
            evidence="Valor atual 5.5000",
            recommendation="Acompanhar novas coletas.",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = OperationalEventRepository(Path(temp_dir) / "eventos.json")
            wrapped = OperationalGovernanceService(
                repository=repository,
                analytics_service=FakeAnalyticsService([alert]),
            ).monitoring_adapter
            recording_adapter = RecordingMonitoringAdapter(wrapped)
            service = OperationalGovernanceService(
                repository=repository,
                analytics_service=FakeAnalyticsService([alert]),
                monitoring_adapter=recording_adapter,
            )

            service.sync_from_analytics()

            self.assertEqual(1, len(recording_adapter.received_decisions))
            self.assertTrue(recording_adapter.received_decisions[0].should_reevaluate)
            self.assertEqual("pre_condicoes_atendidas", recording_adapter.received_decisions[0].reason)

    def test_repeated_sync_updates_existing_event_without_duplicate(self):
        alert = PreventiveAlert(
            severity="alto",
            domain="qualidade_agua",
            metric="ph",
            message="Atencao preventiva: pH fora da faixa.",
            evidence="Valor atual 5.5000",
            recommendation="Acompanhar novas coletas.",
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            repository = OperationalEventRepository(Path(temp_dir) / "eventos.json")
            service = OperationalGovernanceService(
                repository=repository,
                analytics_service=FakeAnalyticsService([alert]),
            )

            first = service.sync_from_analytics()
            second = service.sync_from_analytics()
            events = service.list_events()

            self.assertEqual(1, first["created"])
            self.assertEqual(0, second["created"])
            self.assertEqual(1, second["updated"])
            self.assertEqual(1, len(events))
            self.assertEqual(2, events[0].occurrence_count)
            self.assertIn("reavaliacao_controlada=executada", events[0].explainability)


if __name__ == "__main__":
    unittest.main()
