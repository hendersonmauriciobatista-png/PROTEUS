from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class QualityMeasurement:
    timestamp: Optional[datetime]
    ph: float
    turbidez: float
    oxigenio_dissolvido: float
    temperatura: float
    agrotoxicos: float


@dataclass(frozen=True)
class EnvironmentMeasurement:
    timestamp: Optional[datetime]
    temperatura_ambiente: float
    umidade_relativa: float
    chuva: float
    pressao_atmosferica: float
    observacao: str = ""


@dataclass(frozen=True)
class ConsumptionMeasurement:
    timestamp: Optional[datetime]
    consumo_diario: float
    consumo_mensal: float
    volume_distribuido: float
    perdas_estimadas: float
    observacao: str = ""


@dataclass(frozen=True)
class TrendResult:
    domain: str
    metric: str
    direction: str
    previous_average: Optional[float]
    recent_average: Optional[float]
    delta: Optional[float]
    explanation: str


@dataclass(frozen=True)
class PreventiveAlert:
    severity: str
    domain: str
    metric: str
    message: str
    evidence: str
    recommendation: str


@dataclass(frozen=True)
class WaterHealthScore:
    score: int
    status: str
    explanations: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class AnalyticsSnapshot:
    quality_trends: list[TrendResult]
    consumption_trends: list[TrendResult]
    alerts: list[PreventiveAlert]
    water_health_score: WaterHealthScore
