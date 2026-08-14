import ast
import unittest
from dataclasses import MISSING, fields, replace
from pathlib import Path

from normative_water_foundation import (
    EvaluationScope,
    RefusalReason,
    SamplingPointType,
    StructuralResult,
    WaterMeasurementContext,
    WaterPurpose,
    WaterStateOrStage,
    validate_context,
)


BASE_DIR = Path(__file__).resolve().parents[1]
PACKAGE_DIR = BASE_DIR / "normative_water_foundation"


def complete_context(**changes):
    context = WaterMeasurementContext(
        measurement_parameter="ph",
        water_purpose=WaterPurpose.WATER_BODY_QUALITY,
        water_state_or_stage=WaterStateOrStage.AMBIENT_WATER_BODY,
        sampling_point_reference="sampling-point-01",
        sampling_point_type=SamplingPointType.AMBIENT_WATER_BODY_POINT,
        evaluation_scope=EvaluationScope.NORMATIVE,
    )
    return replace(context, **changes)


class NormativeWaterFoundationTests(unittest.TestCase):
    def test_approved_controlled_values_are_represented(self):
        self.assertEqual(
            {
                "HUMAN_CONSUMPTION",
                "WATER_BODY_QUALITY",
                "TREATMENT_AND_SUPPLY_OPERATION",
                "EFFLUENT_DISCHARGE",
                "OTHER_GOVERNED",
            },
            {item.value for item in WaterPurpose},
        )
        self.assertEqual(
            {
                "RAW_WATER",
                "IN_TREATMENT",
                "TREATED_WATER",
                "DISTRIBUTED_WATER",
                "POINT_OF_USE_WATER",
                "AMBIENT_WATER_BODY",
                "EFFLUENT",
                "OTHER_GOVERNED",
            },
            {item.value for item in WaterStateOrStage},
        )
        self.assertEqual(
            {
                "SOURCE_ABSTRACTION",
                "TREATMENT_INLET",
                "TREATMENT_PROCESS_POINT",
                "FILTER_OUTLET",
                "TREATMENT_OUTLET",
                "STORAGE_POINT",
                "DISTRIBUTION_NETWORK_POINT",
                "POINT_OF_USE",
                "AMBIENT_WATER_BODY_POINT",
                "EFFLUENT_POINT",
                "RECEIVING_WATER_POINT",
                "OTHER_GOVERNED",
            },
            {item.value for item in SamplingPointType},
        )
        self.assertEqual(
            {"NORMATIVE", "OBSERVATIONAL_NON_NORMATIVE", "RECORD_ONLY"},
            {item.value for item in EvaluationScope},
        )

    def test_result_and_refusal_reason_members_are_exact(self):
        self.assertEqual(
            {"STRUCTURALLY_ACCEPTABLE", "STRUCTURALLY_REFUSED"},
            {item.value for item in StructuralResult},
        )
        self.assertEqual(
            {"CONTEXT_INSUFFICIENT", "INVALID_CONTROLLED_VALUE"},
            {item.value for item in RefusalReason},
        )

    def test_required_core_field_set_is_exact(self):
        required = {
            field.name
            for field in fields(WaterMeasurementContext)
            if field.default is MISSING and field.default_factory is MISSING
        }
        self.assertEqual(
            {
                "measurement_parameter",
                "water_purpose",
                "water_state_or_stage",
                "sampling_point_reference",
                "evaluation_scope",
            },
            required,
        )

    def test_complete_required_core_is_acceptable(self):
        result = validate_context(complete_context())
        self.assertEqual(StructuralResult.STRUCTURALLY_ACCEPTABLE, result.result)
        self.assertIsNone(result.reason)

    def test_optional_sampling_point_type_can_be_omitted(self):
        result = validate_context(complete_context(sampling_point_type=None))
        self.assertEqual(StructuralResult.STRUCTURALLY_ACCEPTABLE, result.result)
        self.assertIsNone(result.reason)

    def test_each_missing_required_core_field_is_refused(self):
        required_fields = {
            "measurement_parameter": "",
            "water_purpose": None,
            "water_state_or_stage": None,
            "sampling_point_reference": " ",
            "evaluation_scope": None,
        }
        self.assertTrue(required_fields.keys() <= {field.name for field in fields(WaterMeasurementContext)})
        for field_name, missing_value in required_fields.items():
            with self.subTest(field=field_name):
                result = validate_context(complete_context(**{field_name: missing_value}))
                self.assertEqual(StructuralResult.STRUCTURALLY_REFUSED, result.result)
                self.assertEqual(RefusalReason.CONTEXT_INSUFFICIENT, result.reason)
                self.assertIn(field_name, result.fields)

    def test_unresolved_other_governed_is_context_insufficient(self):
        cases = (
            {"water_purpose": WaterPurpose.OTHER_GOVERNED},
            {"water_state_or_stage": WaterStateOrStage.OTHER_GOVERNED},
            {"sampling_point_type": SamplingPointType.OTHER_GOVERNED},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                result = validate_context(complete_context(**changes))
                self.assertEqual(StructuralResult.STRUCTURALLY_REFUSED, result.result)
                self.assertEqual(RefusalReason.CONTEXT_INSUFFICIENT, result.reason)

    def test_unknown_free_text_and_cross_dimension_values_are_refused(self):
        cases = (
            {"water_purpose": "CUSTOM_PURPOSE"},
            {"water_state_or_stage": "UNKNOWN"},
            {"evaluation_scope": "NORMATIVE"},
            {"water_purpose": WaterStateOrStage.RAW_WATER},
            {"sampling_point_type": WaterPurpose.HUMAN_CONSUMPTION},
            {"measurement_parameter": "UNKNOWN"},
            {"sampling_point_reference": "unknown"},
        )
        for changes in cases:
            with self.subTest(changes=changes):
                result = validate_context(complete_context(**changes))
                self.assertEqual(StructuralResult.STRUCTURALLY_REFUSED, result.result)
                self.assertEqual(RefusalReason.INVALID_CONTROLLED_VALUE, result.reason)

    def test_non_string_identifiers_are_refused(self):
        unexpected_values = (123, True, [], {}, object())
        for field_name in ("measurement_parameter", "sampling_point_reference"):
            for value in unexpected_values:
                with self.subTest(field=field_name, value_type=type(value).__name__):
                    result = validate_context(complete_context(**{field_name: value}))
                    self.assertEqual(StructuralResult.STRUCTURALLY_REFUSED, result.result)
                    self.assertEqual(RefusalReason.INVALID_CONTROLLED_VALUE, result.reason)
                    self.assertIn(field_name, result.fields)

    def test_non_context_input_is_refused(self):
        for value in (None, 123, True, [], {}, object()):
            with self.subTest(value_type=type(value).__name__):
                result = validate_context(value)
                self.assertEqual(StructuralResult.STRUCTURALLY_REFUSED, result.result)
                self.assertEqual(RefusalReason.INVALID_CONTROLLED_VALUE, result.reason)
                self.assertEqual(("context",), result.fields)

    def test_package_has_no_observational_or_legacy_dependencies(self):
        allowed_roots = {"ast", "dataclasses", "enum", "typing"}
        for path in PACKAGE_DIR.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        self.assertIn(alias.name.split(".")[0], allowed_roots)
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    self.assertIn((node.module or "").split(".")[0], allowed_roots)

    def test_package_exposes_no_normative_evaluation_or_numeric_comparison(self):
        prohibited_names = {
            "RESOLVED",
            "COMPLIANT",
            "NON_COMPLIANT",
            "INDETERMINATE",
            "NOT_EVALUATED",
            "NORMAL",
            "ATENCAO",
            "CRITICO",
        }
        package_source = "\n".join(
            path.read_text(encoding="utf-8") for path in PACKAGE_DIR.glob("*.py")
        )
        for prohibited_name in prohibited_names:
            self.assertNotIn(prohibited_name, package_source)

        validation_tree = ast.parse((PACKAGE_DIR / "validation.py").read_text(encoding="utf-8"))
        numeric_comparisons = [
            node
            for node in ast.walk(validation_tree)
            if isinstance(node, ast.Compare)
            and any(isinstance(operator, (ast.Lt, ast.LtE, ast.Gt, ast.GtE)) for operator in node.ops)
        ]
        self.assertEqual([], numeric_comparisons)


if __name__ == "__main__":
    unittest.main()
