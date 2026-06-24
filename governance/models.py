from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class EventState(str, Enum):
    ABERTO = "ABERTO"
    MONITORAMENTO = "MONITORAMENTO"
    RESOLVIDO = "RESOLVIDO"
    ARQUIVADO = "ARQUIVADO"


@dataclass
class OperationalEvent:
    event_id: str
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime]
    state: str
    severity: str
    domain: str
    metric: str
    fingerprint: str
    title: str
    description: str
    evidence: str
    recommendation: str
    source: str
    occurrence_count: int
    last_seen_at: datetime
    resolution_note: str = ""
    archived_reason: str = ""

    def to_dict(self):
        return {
            "event_id": self.event_id,
            "created_at": self.created_at.isoformat(timespec="seconds"),
            "updated_at": self.updated_at.isoformat(timespec="seconds"),
            "closed_at": self.closed_at.isoformat(timespec="seconds") if self.closed_at else None,
            "state": self.state,
            "severity": self.severity,
            "domain": self.domain,
            "metric": self.metric,
            "fingerprint": self.fingerprint,
            "title": self.title,
            "description": self.description,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "source": self.source,
            "occurrence_count": self.occurrence_count,
            "last_seen_at": self.last_seen_at.isoformat(timespec="seconds"),
            "resolution_note": self.resolution_note,
            "archived_reason": self.archived_reason,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            event_id=data.get("event_id", ""),
            created_at=_parse_datetime(data.get("created_at")),
            updated_at=_parse_datetime(data.get("updated_at")),
            closed_at=_parse_optional_datetime(data.get("closed_at")),
            state=data.get("state", EventState.ABERTO.value),
            severity=data.get("severity", ""),
            domain=data.get("domain", ""),
            metric=data.get("metric", ""),
            fingerprint=data.get("fingerprint", ""),
            title=data.get("title", ""),
            description=data.get("description", ""),
            evidence=data.get("evidence", ""),
            recommendation=data.get("recommendation", ""),
            source=data.get("source", "analytics"),
            occurrence_count=int(data.get("occurrence_count") or 0),
            last_seen_at=_parse_datetime(data.get("last_seen_at")),
            resolution_note=data.get("resolution_note", ""),
            archived_reason=data.get("archived_reason", ""),
        )


def _parse_datetime(value):
    if not value:
        return datetime.now()
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return datetime.now()


def _parse_optional_datetime(value):
    if not value:
        return None
    return _parse_datetime(value)
