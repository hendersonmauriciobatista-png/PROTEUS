from pathlib import Path

from .csv_measurement_repository import CSVMeasurementRepository


BASE_DIR = Path(__file__).resolve().parent.parent
QUALITY_WATER_CSV_PATH = BASE_DIR / "data" / "qualidade_agua_medicoes.csv"
QUALITY_WATER_FIELDS = (
    "timestamp",
    "ph",
    "turbidez",
    "oxigenio_dissolvido",
    "temperatura",
    "agrotoxicos",
)


def build_quality_water_repository(path=QUALITY_WATER_CSV_PATH):
    return CSVMeasurementRepository(path, QUALITY_WATER_FIELDS)
