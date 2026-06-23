import csv
from datetime import datetime
from pathlib import Path

from .models import ConsumptionMeasurement, EnvironmentMeasurement, QualityMeasurement


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
QUALIDADE_CSV = DATA_DIR / "qualidade_agua_medicoes.csv"
AMBIENTE_CSV = DATA_DIR / "dados_ambientais_medicoes.csv"
CONSUMO_CSV = DATA_DIR / "consumo_distribuicao_medicoes.csv"


def _to_float(value):
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def _to_datetime(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


class AnalyticsRepository:
    def __init__(
        self,
        quality_path=QUALIDADE_CSV,
        environment_path=AMBIENTE_CSV,
        consumption_path=CONSUMO_CSV,
    ):
        self.quality_path = Path(quality_path)
        self.environment_path = Path(environment_path)
        self.consumption_path = Path(consumption_path)

    def load_quality(self):
        return [
            QualityMeasurement(
                timestamp=_to_datetime(row.get("timestamp")),
                ph=_to_float(row.get("ph")),
                turbidez=_to_float(row.get("turbidez")),
                oxigenio_dissolvido=_to_float(row.get("oxigenio_dissolvido")),
                temperatura=_to_float(row.get("temperatura")),
                agrotoxicos=_to_float(row.get("agrotoxicos")),
            )
            for row in self._read_csv(self.quality_path)
        ]

    def load_environment(self):
        return [
            EnvironmentMeasurement(
                timestamp=_to_datetime(row.get("timestamp")),
                temperatura_ambiente=_to_float(row.get("temperatura_ambiente")),
                umidade_relativa=_to_float(row.get("umidade_relativa")),
                chuva=_to_float(row.get("chuva")),
                pressao_atmosferica=_to_float(row.get("pressao_atmosferica")),
                observacao=row.get("observacao", ""),
            )
            for row in self._read_csv(self.environment_path)
        ]

    def load_consumption(self):
        return [
            ConsumptionMeasurement(
                timestamp=_to_datetime(row.get("timestamp")),
                consumo_diario=_to_float(row.get("consumo_diario")),
                consumo_mensal=_to_float(row.get("consumo_mensal")),
                volume_distribuido=_to_float(row.get("volume_distribuido")),
                perdas_estimadas=_to_float(row.get("perdas_estimadas")),
                observacao=row.get("observacao", ""),
            )
            for row in self._read_csv(self.consumption_path)
        ]

    def _read_csv(self, path):
        if not path.exists():
            return []

        with path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
