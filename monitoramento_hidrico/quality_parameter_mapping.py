from dataclasses import dataclass


@dataclass(frozen=True)
class QualityParameterMapping:
    field_name: str
    parametro_id: str
    categoria: str
    label: str


QUALITY_PARAMETER_MAPPINGS = (
    QualityParameterMapping("ph", "ph", "quimicos", "pH"),
    QualityParameterMapping("turbidez", "turbidez", "fisicos", "Turbidez"),
    QualityParameterMapping(
        "oxigenio_dissolvido",
        "oxigenio_dissolvido",
        "quimicos",
        "Oxigenio dissolvido",
    ),
    QualityParameterMapping("temperatura", "temperatura_agua", "fisicos", "Temperatura da agua"),
)


def quality_parameter_triples():
    return tuple((item.field_name, item.parametro_id, item.categoria) for item in QUALITY_PARAMETER_MAPPINGS)


def quality_parameter_analytics_entries():
    return tuple(
        (item.field_name, item.parametro_id, item.categoria, item.label)
        for item in QUALITY_PARAMETER_MAPPINGS
    )


def quality_parameter_governance_mapping():
    return {
        item.field_name: (item.parametro_id, item.categoria)
        for item in QUALITY_PARAMETER_MAPPINGS
    }
