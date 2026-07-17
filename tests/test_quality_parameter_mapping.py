from dataclasses import FrozenInstanceError
from pathlib import Path
import unittest

from monitoramento_hidrico.quality_parameter_mapping import (
    QUALITY_PARAMETER_MAPPINGS,
    quality_parameter_analytics_entries,
    quality_parameter_governance_mapping,
    quality_parameter_triples,
)


EXPECTED_TRIPLES = (
    ("ph", "ph", "quimicos"),
    ("turbidez", "turbidez", "fisicos"),
    ("oxigenio_dissolvido", "oxigenio_dissolvido", "quimicos"),
    ("temperatura", "temperatura_agua", "fisicos"),
    ("agrotoxicos", "agrotoxicos", "contaminantes_agricolas"),
)

EXPECTED_ANALYTICS_ENTRIES = (
    ("ph", "ph", "quimicos", "pH"),
    ("turbidez", "turbidez", "fisicos", "Turbidez"),
    ("oxigenio_dissolvido", "oxigenio_dissolvido", "quimicos", "Oxigenio dissolvido"),
    ("temperatura", "temperatura_agua", "fisicos", "Temperatura da agua"),
    ("agrotoxicos", "agrotoxicos", "contaminantes_agricolas", "Agrotoxicos"),
)

EXPECTED_GOVERNANCE_MAPPING = {
    "ph": ("ph", "quimicos"),
    "turbidez": ("turbidez", "fisicos"),
    "oxigenio_dissolvido": ("oxigenio_dissolvido", "quimicos"),
    "temperatura": ("temperatura_agua", "fisicos"),
    "agrotoxicos": ("agrotoxicos", "contaminantes_agricolas"),
}

ADAPTER_AUTHORITY_NAMES = (
    "PARAMETROS_QUALIDADE_AGUA",
    "QUALITY_PARAMETER_FIELDS",
    "REPORT_QUALITY_PARAMETERS",
    "QUALITY_ANALYTICS_PARAMETERS",
    "GOVERNANCE_QUALITY_PARAMETERS",
)

ADAPTERS = (
    Path("monitoramento_hidrico/qualidade_agua_adapter.py"),
    Path("monitoramento_hidrico/dashboard_adapter.py"),
    Path("monitoramento_hidrico/operational_reports_adapter.py"),
    Path("monitoramento_hidrico/analytics_adapter.py"),
    Path("monitoramento_hidrico/governance_adapter.py"),
)


class QualityParameterMappingTests(unittest.TestCase):
    def test_contract_preserves_field_parameter_category_order(self):
        self.assertEqual(EXPECTED_TRIPLES, quality_parameter_triples())

    def test_contract_preserves_analytics_labels(self):
        self.assertEqual(EXPECTED_ANALYTICS_ENTRIES, quality_parameter_analytics_entries())

    def test_contract_preserves_governance_lookup_shape(self):
        self.assertEqual(EXPECTED_GOVERNANCE_MAPPING, quality_parameter_governance_mapping())

    def test_source_is_immutable_for_consumers(self):
        with self.assertRaises(FrozenInstanceError):
            QUALITY_PARAMETER_MAPPINGS[0].field_name = "campo_alterado"

    def test_governance_lookup_returns_copy(self):
        quality_parameters = quality_parameter_governance_mapping()
        quality_parameters["ph"] = ("parametro_alterado", "categoria_alterada")

        self.assertEqual(EXPECTED_GOVERNANCE_MAPPING, quality_parameter_governance_mapping())

    def test_adapters_no_longer_define_local_parameter_authorities(self):
        for path in ADAPTERS:
            with self.subTest(path=str(path)):
                source = path.read_text(encoding="utf-8")
                for authority_name in ADAPTER_AUTHORITY_NAMES:
                    self.assertNotIn(f"{authority_name} =", source)
                self.assertIn("quality_parameter_", source)


if __name__ == "__main__":
    unittest.main()
