"""Minimum context value used only for structural validation."""

from dataclasses import dataclass
from typing import Optional

from .vocabulary import EvaluationScope, SamplingPointType, WaterPurpose, WaterStateOrStage


@dataclass(frozen=True)
class WaterMeasurementContext:
    measurement_parameter: str
    water_purpose: WaterPurpose
    water_state_or_stage: WaterStateOrStage
    sampling_point_reference: str
    evaluation_scope: EvaluationScope
    sampling_point_type: Optional[SamplingPointType] = None
