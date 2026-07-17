from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class RecommendationPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNKNOWN = "UNKNOWN"
    LOW_CONTROLLED = "LOW_CONTROLLED"


class RecommendationAction(str, Enum):
    MAINTAIN_ROUTINE_MONITORING = "MAINTAIN_ROUTINE_MONITORING"
    INCREASE_MONITORING_FREQUENCY = "INCREASE_MONITORING_FREQUENCY"
    EXECUTE_OPERATIONAL_INSPECTION = "EXECUTE_OPERATIONAL_INSPECTION"
    COLLECT_MORE_DATA = "COLLECT_MORE_DATA"


@dataclass(frozen=True)
class RecommendationEvidence:
    source: str
    metric: str
    value: Optional[float]
    description: str
    origin_layer: str = ""
    origin_artifact: str = ""
    origin_reference: str = ""


@dataclass(frozen=True)
class ExecutiveRecommendation:
    recommendation_id: str
    priority: RecommendationPriority
    action: RecommendationAction
    recommendation: str
    rationale: str
    confidence: Optional[float] = None
    evidence: list[RecommendationEvidence] = field(default_factory=list)


@dataclass(frozen=True)
class RecommendationSnapshot:
    generated_at: datetime
    recommendations: list[ExecutiveRecommendation]
    explanations: list[str] = field(default_factory=list)
