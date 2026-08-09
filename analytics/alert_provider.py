from typing import Protocol

from .models import (
    ConsumptionMeasurement,
    EnvironmentMeasurement,
    PreventiveAlert,
    QualityMeasurement,
    TrendResult,
)


class AlertProvider(Protocol):
    def build_alerts(
        self,
        quality: list[QualityMeasurement],
        environment: list[EnvironmentMeasurement],
        consumption: list[ConsumptionMeasurement],
        quality_trends: list[TrendResult],
        consumption_trends: list[TrendResult],
    ) -> list[PreventiveAlert]: ...
