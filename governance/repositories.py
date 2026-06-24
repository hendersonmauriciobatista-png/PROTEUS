import json
import os
from pathlib import Path

from .models import OperationalEvent


BASE_DIR = Path(__file__).resolve().parent.parent
EVENTS_FILE = BASE_DIR / "data" / "eventos_operacionais.json"


class OperationalEventRepository:
    def __init__(self, path=EVENTS_FILE):
        self.path = Path(path)

    def load_events(self):
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            return []

        return [OperationalEvent.from_dict(item) for item in data if isinstance(item, dict)]

    def save_events(self, events):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = [event.to_dict() for event in events]
        temp_path = self.path.with_suffix(self.path.suffix + ".tmp")

        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, ensure_ascii=False, indent=2)
            file.write("\n")

        os.replace(temp_path, self.path)
