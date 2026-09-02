import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.models import APSReference
from governed_core.repository import GovernedCoreRepository, GovernedConflictError, GovernedReferenceError
from governed_core.services import APSService, ApplicabilityService
from governed_core.temporal_state import TemporalStateService


class TemporalSuccessionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = GovernedCoreRepository(Path(self.temp.name) / "succession.sqlite3").initialize()
        self.state = FirstRealAPSBootstrap(self.repo).execute()
        self.app = ApplicabilityService(self.repo)
        self.app.assign_temporal(self.state.context_revision_id, self.state.aps_reference,
                                 datetime(2020, 1, 1, tzinfo=timezone.utc), actor_reference="ACTOR")
        with self.repo._optional_connection(None) as cx:
            self.app_id = cx.execute("SELECT aps_applicability_id FROM aps_temporal_applicability").fetchone()[0]
            self.basis = cx.execute("SELECT basis_id FROM authorization_basis LIMIT 1").fetchone()[0]
        self.temporal = TemporalStateService(self.repo)

    def tearDown(self): self.temp.cleanup()

    def test_aps_before_and_at_successor_boundary(self):
        successor = APSReference(self.state.aps_reference.set_id, self.state.aps_reference.version)
        new_id = self.temporal.append_successor("APS_TEMPORAL_APPLICABILITY", self.app_id,
            {"effective_from": datetime(2025, 1, 1, tzinfo=timezone.utc), "reference": successor}, "ACTOR", self.basis)
        self.assertTrue(new_id)
        self.assertEqual(self.state.aps_reference, self.repo.fetch_temporal_aps(self.state.context_revision_id, "2024-12-31T23:59:59.999999Z"))
        self.assertEqual(successor, self.repo.fetch_temporal_aps(self.state.context_revision_id, "2025-01-01T00:00:00Z"))
        self.assertEqual(successor, self.repo.fetch_temporal_aps(self.state.context_revision_id, "2030-01-01T00:00:00Z"))

    def test_invalid_successor_rolls_back_and_closed_interval_cannot_reopen(self):
        with self.assertRaises(GovernedReferenceError):
            self.temporal.append_successor("APS_TEMPORAL_APPLICABILITY", self.app_id,
                {"effective_from": datetime(2025, 1, 1, tzinfo=timezone.utc), "reference": APSReference("missing", 1)}, "ACTOR", self.basis)
        with self.repo._optional_connection(None) as cx:
            self.assertIsNone(cx.execute("SELECT effective_until FROM aps_temporal_applicability WHERE aps_applicability_id=?", (self.app_id,)).fetchone()[0])
        self.temporal.close("APS_TEMPORAL_APPLICABILITY", self.app_id, datetime(2025, 1, 1, tzinfo=timezone.utc), "ACTOR", self.basis)
        with self.assertRaises(GovernedConflictError):
            self.temporal.append_successor("APS_TEMPORAL_APPLICABILITY", self.app_id,
                {"effective_from": datetime(2026, 1, 1, tzinfo=timezone.utc), "reference": self.state.aps_reference}, "ACTOR", self.basis)

    def test_overlap_and_backdating_are_rejected(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.app.assign_temporal(self.state.context_revision_id, self.state.aps_reference,
                datetime(2020, 6, 1, tzinfo=timezone.utc), actor_reference="ACTOR")
        with self.assertRaises(GovernedConflictError):
            self.temporal.close("APS_TEMPORAL_APPLICABILITY", self.app_id,
                datetime(2019, 1, 1, tzinfo=timezone.utc), "ACTOR", self.basis)


if __name__ == "__main__": unittest.main()
