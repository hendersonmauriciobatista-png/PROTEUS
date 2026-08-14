"""Isolated structural foundation for future normative water capabilities."""

from .context import WaterMeasurementContext
from .validation import RefusalReason, StructuralResult, StructuralValidation, validate_context
from .vocabulary import EvaluationScope, SamplingPointType, WaterPurpose, WaterStateOrStage

__all__ = [
    "EvaluationScope",
    "RefusalReason",
    "SamplingPointType",
    "StructuralResult",
    "StructuralValidation",
    "WaterMeasurementContext",
    "WaterPurpose",
    "WaterStateOrStage",
    "validate_context",
]
