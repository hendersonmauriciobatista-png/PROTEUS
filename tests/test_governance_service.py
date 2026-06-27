import tempfile
import unittest
from pathlib import Path

from analytics.models import AnalyticsSnapshot, PreventiveAlert, WaterHealthScore
from governance.models import EventState
from governance.repositories import OperationalEventRepository
from governance.service import OperationalGovernanceService


class FakeAnalyticsService:
    def __init__(self, alerts):
        self.alerts = alerts

    def build_snapshot(self):
        return AnalyticsSnapshot(
            quality_trends=[],
            consumption_trends=[],
            alerts=self.alerts,
            water_health_score=WaterHealthScore(score=80, status="Bom", explanations=[]),
        )


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


if __name__ == "__main__":
    unittest.main()
