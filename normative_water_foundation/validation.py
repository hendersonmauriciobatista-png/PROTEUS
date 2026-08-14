"""Fail-safe structural validation with no authority or rule evaluation."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Tuple

from .context import WaterMeasurementContext
from .vocabulary import EvaluationScope, SamplingPointType, WaterPurpose, WaterStateOrStage


class StructuralResult(str, Enum):
    STRUCTURALLY_ACCEPTABLE = "STRUCTURALLY_ACCEPTABLE"
    STRUCTURALLY_REFUSED = "STRUCTURALLY_REFUSED"


class RefusalReason(str, Enum):
    CONTEXT_INSUFFICIENT = "CONTEXT_INSUFFICIENT"
    INVALID_CONTROLLED_VALUE = "INVALID_CONTROLLED_VALUE"


@dataclass(frozen=True)
class StructuralValidation:
    result: StructuralResult
    reason: Optional[RefusalReason] = None
    fields: Tuple[str, ...] = ()


_CONTROLLED_FIELDS = (
    ("water_purpose", WaterPurpose),
    ("water_state_or_stage", WaterStateOrStage),
    ("evaluation_scope", EvaluationScope),
)


def validate_context(context: WaterMeasurementContext) -> StructuralValidation:
    """Validate only completeness and governed vocabulary membership."""
    if not isinstance(context, WaterMeasurementContext):
        return StructuralValidation(
            StructuralResult.STRUCTURALLY_REFUSED,
            RefusalReason.INVALID_CONTROLLED_VALUE,
            ("context",),
        )

    missing = tuple(
        field_name
        for field_name in (
            "measurement_parameter",
            "water_purpose",
            "water_state_or_stage",
            "sampling_point_reference",
            "evaluation_scope",
        )
        if _is_missing(getattr(context, field_name, None))
    )
    if missing:
        return StructuralValidation(
            StructuralResult.STRUCTURALLY_REFUSED,
            RefusalReason.CONTEXT_INSUFFICIENT,
            missing,
        )

    invalid = tuple(
        field_name
        for field_name, expected_type in _CONTROLLED_FIELDS
        if not isinstance(getattr(context, field_name), expected_type)
    )
    if context.sampling_point_type is not None and not isinstance(
        context.sampling_point_type, SamplingPointType
    ):
        invalid += ("sampling_point_type",)
    identifier_fields = tuple(
        field_name
        for field_name in ("measurement_parameter", "sampling_point_reference")
        if not isinstance(getattr(context, field_name), str)
        or _is_unknown_identifier(getattr(context, field_name))
    )
    if invalid or identifier_fields:
        return StructuralValidation(
            StructuralResult.STRUCTURALLY_REFUSED,
            RefusalReason.INVALID_CONTROLLED_VALUE,
            invalid + identifier_fields,
        )

    unresolved = tuple(
        field_name
        for field_name in ("water_purpose", "water_state_or_stage", "sampling_point_type")
        if getattr(context, field_name, None) is not None
        and getattr(context, field_name).value == "OTHER_GOVERNED"
    )
    if unresolved:
        return StructuralValidation(
            StructuralResult.STRUCTURALLY_REFUSED,
            RefusalReason.CONTEXT_INSUFFICIENT,
            unresolved,
        )

    return StructuralValidation(StructuralResult.STRUCTURALLY_ACCEPTABLE)


def _is_missing(value: object) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def _is_unknown_identifier(value: object) -> bool:
    return isinstance(value, str) and value.strip().upper() == "UNKNOWN"
