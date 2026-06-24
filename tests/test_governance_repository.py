import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from governance.models import EventState, OperationalEvent
from governance.repositories import OperationalEventRepository


class OperationalEventRepositoryTests(unittest.TestCase):
    def test_save_and_load_events_without_deleting_history(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "eventos_operacionais.json"
            now = datetime(2026, 6, 23, 20, 0, 0)
            event = OperationalEvent(
                event_id="evt-1",
                created_at=now,
                updated_at=now,
                closed_at=None,
                state=EventState.ABERTO.value,
                severity="medio",
                domain="qualidade_agua",
                metric="turbidez",
                fingerprint="abc",
                title="Acompanhamento preventivo: turbidez",
                description="Atencao preventiva",
                evidence="Valor atual 4.0000",
                recommendation="Acompanhar novas medicoes.",
                source="analytics",
                occurrence_count=1,
                last_seen_at=now,
            )

            repository = OperationalEventRepository(path)
            repository.save_events([event])
            loaded = repository.load_events()

            self.assertEqual(1, len(loaded))
            self.assertEqual("evt-1", loaded[0].event_id)
            self.assertEqual(EventState.ABERTO.value, loaded[0].state)
            self.assertTrue(path.exists())
            self.assertFalse(path.with_suffix(".json.tmp").exists())


if __name__ == "__main__":
    unittest.main()
