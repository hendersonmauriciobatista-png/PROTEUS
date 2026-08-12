import shutil
from dataclasses import dataclass
from datetime import datetime

from analytics import AnalyticsService
from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.governance_adapter import (
    OperationalGovernanceHydricMonitoringAdapter,
    decidir_reavaliacao_controlada,
)

from .models import EventState
from .repositories import OperationalEventRepository
from .rules import OperationalGovernanceRules


TERMINAL_EVENT_STATES = {EventState.RESOLVIDO.value, EventState.ARQUIVADO.value}


@dataclass(frozen=True)
class GovernanceHistoryStatus:
    open_events: int
    monitoring_events: int
    resolved_events: int
    archived_events: int

    @property
    def active_events(self):
        return self.open_events + self.monitoring_events

    @property
    def terminal_events(self):
        return self.resolved_events + self.archived_events


@dataclass(frozen=True)
class GovernanceHistoryResetResult:
    cleared: bool
    status: GovernanceHistoryStatus
    removed_events: int = 0
    backup_path: str = ""
    confirmation_required: bool = False
    error: str = ""


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
        decisions = [self._decidir_reavaliacao_controlada(alert) for alert in snapshot.alerts]
        signals = self.monitoring_adapter.enriquecer_alertas(snapshot.alerts, decisions)
        created, updated = self.rules.sync_alerts(events, signals)
        self.repository.save_events(events)
        return {
            "created": created,
            "updated": updated,
            "total": len(events),
            "alerts": len(signals),
        }

    def _decidir_reavaliacao_controlada(self, alert):
        policy_engine = getattr(self.monitoring_adapter, "policy_engine", PolicyEngine())
        perfil_operacional = getattr(self.monitoring_adapter, "perfil_operacional", None)
        return decidir_reavaliacao_controlada(
            alert,
            policy_engine,
            perfil_operacional,
        )

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

    def governance_history_status(self):
        summary = self.summarize_by_state()
        return GovernanceHistoryStatus(
            open_events=summary.get(EventState.ABERTO.value, 0),
            monitoring_events=summary.get(EventState.MONITORAMENTO.value, 0),
            resolved_events=summary.get(EventState.RESOLVIDO.value, 0),
            archived_events=summary.get(EventState.ARQUIVADO.value, 0),
        )

    def reset_terminal_history(self, confirmed=False):
        events = self.repository.load_events()
        status = self.governance_history_status()
        if status.active_events:
            return GovernanceHistoryResetResult(False, status)
        if status.terminal_events and not confirmed:
            return GovernanceHistoryResetResult(
                False,
                status,
                confirmation_required=True,
            )
        if not status.terminal_events:
            return GovernanceHistoryResetResult(True, status)

        source_path = self.repository.path
        backup_path = source_path.with_name(
            f"{source_path.stem}.backup-{datetime.now().strftime('%Y%m%d%H%M%S%f')}{source_path.suffix}"
        )
        try:
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, backup_path)
        except (OSError, shutil.Error) as error:
            return GovernanceHistoryResetResult(False, status, error=str(error))

        remaining_events = [
            event for event in events if event.state not in TERMINAL_EVENT_STATES
        ]
        self.repository.save_events(remaining_events)
        return GovernanceHistoryResetResult(
            True,
            status,
            removed_events=status.terminal_events,
            backup_path=str(backup_path),
        )

    def _transition(self, event_id, target_state, note=""):
        events = self.repository.load_events()
        for event in events:
            if event.event_id == event_id:
                changed = self.rules.transition_event(event, target_state, note)
                if changed:
                    self.repository.save_events(events)
                return changed
        return False
