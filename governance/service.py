from analytics import AnalyticsService
from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.governance_adapter import OperationalGovernanceHydricMonitoringAdapter

from .models import EventState
from .repositories import OperationalEventRepository
from .rules import OperationalGovernanceRules


class OperationalGovernanceService:
    def __init__(self, repository=None, analytics_service=None, rules=None, monitoring_adapter=None):
        self.repository = repository or OperationalEventRepository()
        self.analytics_service = analytics_service or AnalyticsService()
        self.rules = rules or OperationalGovernanceRules()
        self.monitoring_adapter = monitoring_adapter or OperationalGovernanceHydricMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )

    def list_events(self):
        return self.repository.load_events()

    def sync_from_analytics(self):
        events = self.repository.load_events()
        snapshot = self.analytics_service.build_snapshot()
        signals = self.monitoring_adapter.enriquecer_alertas(snapshot.alerts)
        created, updated = self.rules.sync_alerts(events, signals)
        self.repository.save_events(events)
        return {
            "created": created,
            "updated": updated,
            "total": len(events),
            "alerts": len(signals),
        }

    def move_to_monitoring(self, event_id):
        return self._transition(event_id, EventState.MONITORAMENTO.value)

    def resolve_event(self, event_id, note="Resolucao observacional registrada pelo operador."):
        return self._transition(event_id, EventState.RESOLVIDO.value, note)

    def archive_event(self, event_id, reason="Arquivamento observacional registrado pelo operador."):
        return self._transition(event_id, EventState.ARQUIVADO.value, reason)

    def summarize_by_state(self):
        summary = {state.value: 0 for state in EventState}
        for event in self.repository.load_events():
            summary[event.state] = summary.get(event.state, 0) + 1
        return summary

    def _transition(self, event_id, target_state, note=""):
        events = self.repository.load_events()
        for event in events:
            if event.event_id == event_id:
                changed = self.rules.transition_event(event, target_state, note)
                if changed:
                    self.repository.save_events(events)
                return changed
        return False
