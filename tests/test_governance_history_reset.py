import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from governance.models import EventState, OperationalEvent
from governance.repositories import OperationalEventRepository
from governance.service import OperationalGovernanceService


def make_event(event_id, state):
    now = datetime(2026, 8, 11, 10, 0, 0)
    return OperationalEvent(
        event_id=event_id,
        created_at=now,
        updated_at=now,
        closed_at=now if state in {EventState.RESOLVIDO.value, EventState.ARQUIVADO.value} else None,
        state=state,
        severity="baixo",
        domain="qualidade_agua",
        metric="ph",
        fingerprint=event_id,
        title="Evento",
        description="Descricao",
        evidence="Evidencia",
        recommendation="Acompanhar",
        source="analytics",
        occurrence_count=1,
        last_seen_at=now,
    )


class GovernanceHistoryResetTests(unittest.TestCase):
    def make_service(self, directory, events):
        repository = OperationalEventRepository(Path(directory) / "eventos_operacionais.json")
        repository.save_events(events)
        return OperationalGovernanceService(repository=repository), repository

    def test_active_events_block_reset_even_when_confirmed(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service, repository = self.make_service(
                temp_dir,
                [
                    make_event("active", EventState.ABERTO.value),
                    make_event("terminal", EventState.ARQUIVADO.value),
                ],
            )

            result = service.reset_terminal_history(confirmed=True)

            self.assertFalse(result.cleared)
            self.assertEqual(1, result.status.active_events)
            self.assertEqual(2, len(repository.load_events()))
            self.assertEqual([], list(Path(temp_dir).glob("*.backup-*.json")))

    def test_confirmation_is_required_before_terminal_reset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service, repository = self.make_service(
                temp_dir,
                [make_event("resolved", EventState.RESOLVIDO.value)],
            )

            result = service.reset_terminal_history()

            self.assertFalse(result.cleared)
            self.assertTrue(result.confirmation_required)
            self.assertEqual(1, len(repository.load_events()))

    def test_confirmed_reset_creates_backup_then_persists_valid_empty_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service, repository = self.make_service(
                temp_dir,
                [
                    make_event("resolved", EventState.RESOLVIDO.value),
                    make_event("archived", EventState.ARQUIVADO.value),
                ],
            )
            original_payload = repository.path.read_text(encoding="utf-8")

            result = service.reset_terminal_history(confirmed=True)

            self.assertTrue(result.cleared)
            self.assertEqual(2, result.removed_events)
            backup_path = Path(result.backup_path)
            self.assertTrue(backup_path.exists())
            self.assertEqual(original_payload, backup_path.read_text(encoding="utf-8"))
            self.assertEqual([], repository.load_events())
            self.assertEqual([], json.loads(repository.path.read_text(encoding="utf-8")))

    def test_backup_failure_blocks_reset_and_preserves_source(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            service, repository = self.make_service(
                temp_dir,
                [make_event("archived", EventState.ARQUIVADO.value)],
            )
            original_payload = repository.path.read_text(encoding="utf-8")

            with patch("governance.service.shutil.copy2", side_effect=OSError("backup indisponivel")):
                result = service.reset_terminal_history(confirmed=True)

            self.assertFalse(result.cleared)
            self.assertIn("backup indisponivel", result.error)
            self.assertEqual(original_payload, repository.path.read_text(encoding="utf-8"))
            self.assertEqual(1, len(repository.load_events()))

    def test_reset_does_not_change_unrelated_project_configuration_or_measurements(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            base = Path(temp_dir)
            unrelated = {
                base / "projeto.json": "projeto-preservado",
                base / "configuracao.json": "configuracao-preservada",
                base / "medicoes.csv": "cabecalho\nmedicao\n",
            }
            for path, content in unrelated.items():
                path.write_text(content, encoding="utf-8")
            service, _repository = self.make_service(
                temp_dir,
                [make_event("resolved", EventState.RESOLVIDO.value)],
            )

            result = service.reset_terminal_history(confirmed=True)

            self.assertTrue(result.cleared)
            for path, content in unrelated.items():
                self.assertEqual(content, path.read_text(encoding="utf-8"))

    def test_governance_and_executive_pages_preserve_navigation_refresh_contract(self):
        root = Path(__file__).resolve().parent.parent
        governance_source = (root / "governanca_operacional.py").read_text(encoding="utf-8")
        executive_source = (root / "painel_executivo.py").read_text(encoding="utf-8")

        self.assertIn("def refresh(self):", governance_source)
        self.assertIn("self.events = self.service.list_events()", governance_source)
        self.assertIn("def refresh(self):", executive_source)
        self.assertIn("snapshot = self.service.build_snapshot()", executive_source)


if __name__ == "__main__":
    unittest.main()
