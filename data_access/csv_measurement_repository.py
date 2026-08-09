import csv
from pathlib import Path
from typing import Mapping, Protocol, Sequence


class MeasurementRepository(Protocol):
    def read_all(self) -> list[dict[str, str]]:
        ...

    def append(self, measurement: Mapping[str, object]) -> None:
        ...

    def clear(self) -> None:
        ...


class CSVMeasurementRepository:
    def __init__(self, path, fieldnames: Sequence[str]):
        self.path = Path(path)
        self.fieldnames = tuple(fieldnames)
        if not self.fieldnames:
            raise ValueError("O repositorio CSV exige ao menos um campo.")

    def read_all(self):
        if not self.path.exists():
            return []

        with self.path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def append(self, measurement):
        self._ensure_storage()
        with self.path.open("a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writerow(dict(measurement))

    def clear(self):
        self._write_header()

    def _ensure_storage(self):
        if not self.path.exists():
            self._write_header()

    def _write_header(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
