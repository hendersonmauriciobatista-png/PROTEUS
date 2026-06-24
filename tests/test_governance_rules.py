import unittest
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


if __name__ == "__main__":
    unittest.main()
