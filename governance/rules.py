import hashlib
import uuid
from datetime import datetime

from .models import EventState, OperationalEvent


ACTIVE_STATES = {EventState.ABERTO.value, EventState.MONITORAMENTO.value}
VALID_TRANSITIONS = {
    EventState.ABERTO.value: {EventState.MONITORAMENTO.value, EventState.RESOLVIDO.value},
    EventState.MONITORAMENTO.value: {EventState.RESOLVIDO.value},
    EventState.RESOLVIDO.value: {EventState.ARQUIVADO.value},
    EventState.ARQUIVADO.value: set(),
}


def build_alert_fingerprint(alert):
    raw = f"{alert.severity}|{alert.domain}|{alert.metric}|{alert.message}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


class OperationalGovernanceRules:
    def sync_alerts(self, events, alerts, now=None):
        now = now or datetime.now()
        by_fingerprint = {
            event.fingerprint: event
            for event in events
            if event.state in ACTIVE_STATES
        }
        created = 0
        updated = 0

        for alert in alerts:
            fingerprint = build_alert_fingerprint(alert)
            existing = by_fingerprint.get(fingerprint)
            if existing:
                self.update_existing_event(existing, alert, now)
                updated += 1
                continue

            event = self.create_event_from_alert(alert, fingerprint, now)
            events.append(event)
            by_fingerprint[fingerprint] = event
            created += 1

        return created, updated

    def create_event_from_alert(self, alert, fingerprint=None, now=None):
        now = now or datetime.now()
        fingerprint = fingerprint or build_alert_fingerprint(alert)
        event_hash = uuid.uuid4().hex[:8]
        return OperationalEvent(
            event_id=f"evt-{now.strftime('%Y%m%d%H%M%S')}-{event_hash}",
            created_at=now,
            updated_at=now,
            closed_at=None,
            state=EventState.ABERTO.value,
            severity=alert.severity,
            domain=alert.domain,
            metric=alert.metric,
            fingerprint=fingerprint,
            title=f"Acompanhamento preventivo: {alert.metric}",
            description=alert.message,
            evidence=alert.evidence,
            recommendation=alert.recommendation,
            source="analytics",
            occurrence_count=1,
            last_seen_at=now,
        )

    def update_existing_event(self, event, alert, now=None):
        now = now or datetime.now()
        event.updated_at = now
        event.last_seen_at = now
        event.occurrence_count += 1
        event.severity = alert.severity
        event.evidence = alert.evidence
        event.recommendation = alert.recommendation
        event.description = alert.message
        return event

    def transition_event(self, event, target_state, note="", now=None):
        now = now or datetime.now()
        if target_state not in VALID_TRANSITIONS.get(event.state, set()):
            return False

        event.state = target_state
        event.updated_at = now

        if target_state == EventState.RESOLVIDO.value:
            event.closed_at = now
            event.resolution_note = note

        if target_state == EventState.ARQUIVADO.value:
            event.archived_reason = note

        return True
