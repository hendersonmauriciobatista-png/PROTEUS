import unittest
from copy import deepcopy
from datetime import datetime

from analytics.models import PreventiveAlert
from governance.models import EventState
from governance.rules import OperationalGovernanceRules, build_alert_fingerprint


class OperationalGovernanceRulesTests(unittest.TestCase):
    def test_sync_creates_event_for_new_alert(self):
        alert = PreventiveAlert(
            severity="baixo",
            domain="qualidade_agua",
            metric="turbidez",
            message="Atencao preventiva: turbidez em alta.",
            evidence="media anterior 1.0000, media recente 2.0000",
            recommendation="Observar novas medicoes.",
        )
        events = []
        rules = OperationalGovernanceRules()

        created, updated = rules.sync_alerts(events, [alert], datetime(2026, 6, 23, 20, 0, 0))

        self.assertEqual(1, created)
        self.assertEqual(0, updated)
        self.assertEqual(1, len(events))
        self.assertEqual(EventState.ABERTO.value, events[0].state)
        self.assertEqual(build_alert_fingerprint(alert), events[0].fingerprint)

    def test_sync_does_not_duplicate_active_fingerprint(self):
        alert = PreventiveAlert(
            severity="baixo",
            domain="qualidade_agua",
            metric="turbidez",
            message="Atencao preventiva: turbidez em alta.",
            evidence="media anterior 1.0000, media recente 2.0000",
            recommendation="Observar novas medicoes.",
        )
        rules = OperationalGovernanceRules()
        events = []

        rules.sync_alerts(events, [alert], datetime(2026, 6, 23, 20, 0, 0))
        created, updated = rules.sync_alerts(events, [alert], datetime(2026, 6, 23, 21, 0, 0))

        self.assertEqual(0, created)
        self.assertEqual(1, updated)
        self.assertEqual(1, len(events))
        self.assertEqual(2, events[0].occurrence_count)
        self.assertIn("2.0000", events[0].evidence)

    def test_manual_transitions_follow_allowed_path(self):
        alert = PreventiveAlert(
            severity="medio",
            domain="consumo_distribuicao",
            metric="perdas_estimadas",
            message="Atencao preventiva: perdas elevadas.",
            evidence="Perdas atuais 20.00%",
            recommendation="Acompanhar evolucao.",
        )
        rules = OperationalGovernanceRules()
        event = rules.create_event_from_alert(alert, now=datetime(2026, 6, 23, 20, 0, 0))

        self.assertTrue(rules.transition_event(event, EventState.MONITORAMENTO.value))
        self.assertTrue(rules.transition_event(event, EventState.RESOLVIDO.value, "Observado pelo operador."))
        self.assertTrue(rules.transition_event(event, EventState.ARQUIVADO.value, "Historico preservado."))
        self.assertFalse(rules.transition_event(event, EventState.ABERTO.value))
        self.assertEqual("Historico preservado.", event.archived_reason)

    def test_archived_event_returns_to_monitoring_with_data_preserved_and_terminal_fields_cleared(self):
        alert = PreventiveAlert(
            severity="medio",
            domain="consumo_distribuicao",
            metric="perdas_estimadas",
            message="Atencao preventiva: perdas elevadas.",
            evidence="Perdas atuais 20.00%",
            recommendation="Acompanhar evolucao.",
        )
        rules = OperationalGovernanceRules()
        event = rules.create_event_from_alert(alert, now=datetime(2026, 6, 23, 20, 0, 0))
        rules.transition_event(event, EventState.RESOLVIDO.value, "Resolvido.", datetime(2026, 6, 23, 21, 0, 0))
        rules.transition_event(event, EventState.ARQUIVADO.value, "Arquivado.", datetime(2026, 6, 23, 22, 0, 0))
        archived = deepcopy(event)
        reactivated_at = datetime(2026, 6, 24, 8, 0, 0)

        self.assertTrue(rules.transition_event(event, EventState.MONITORAMENTO.value, now=reactivated_at))

        self.assertEqual(EventState.MONITORAMENTO.value, event.state)
        self.assertEqual(reactivated_at, event.updated_at)
        self.assertIsNone(event.closed_at)
        self.assertEqual("", event.resolution_note)
        self.assertEqual("", event.archived_reason)
        for field_name in (
            "event_id", "domain", "metric", "severity", "occurrence_count",
            "evidence", "recommendation", "created_at",
        ):
            self.assertEqual(getattr(archived, field_name), getattr(event, field_name))

    def test_archived_event_denies_other_new_transitions(self):
        alert = PreventiveAlert(
            severity="baixo",
            domain="qualidade_agua",
            metric="turbidez",
            message="Atencao preventiva.",
            evidence="Evidencia.",
            recommendation="Acompanhar.",
        )
        rules = OperationalGovernanceRules()
        event = rules.create_event_from_alert(alert)
        rules.transition_event(event, EventState.RESOLVIDO.value)
        rules.transition_event(event, EventState.ARQUIVADO.value)

        self.assertFalse(rules.transition_event(event, EventState.ABERTO.value))
        self.assertFalse(rules.transition_event(event, EventState.RESOLVIDO.value))


if __name__ == "__main__":
    unittest.main()
