from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from executive_recommendation.models import RecommendationSnapshot
from monitoramento_hidrico.status_semantics import (
    EXECUTIVE_STATUS_OBSERVATIONAL_ATTENTION,
    EXECUTIVE_STATUS_OBSERVATIONAL_CRITICAL,
    EXECUTIVE_STATUS_OBSERVATIONAL_NORMAL,
)


EXECUTIVE_NORMAL = EXECUTIVE_STATUS_OBSERVATIONAL_NORMAL
EXECUTIVE_ATTENTION = EXECUTIVE_STATUS_OBSERVATIONAL_ATTENTION
EXECUTIVE_CRITICAL = EXECUTIVE_STATUS_OBSERVATIONAL_CRITICAL


@dataclass(frozen=True)
class ExecutivePriority:
    level: str
    title: str
    evidence: str
    recommendation: str
    source: str


@dataclass(frozen=True)
class ExecutiveTrendSummary:
    domain: str
    metric: str
    direction: str
    explanation: str


@dataclass(frozen=True)
class ExecutiveSnapshot:
    generated_at: datetime
    water_health_score: int
    water_health_status: str
    executive_status: str
    open_events: int
    monitoring_events: int
    resolved_events: int
    archived_events: int
    relevant_alerts: list
    key_trends: list[ExecutiveTrendSummary]
    executive_message: str
    observational_priorities: list[ExecutivePriority]
    explanations: list[str] = field(default_factory=list)
    recommendation_snapshot: Optional[RecommendationSnapshot] = None
