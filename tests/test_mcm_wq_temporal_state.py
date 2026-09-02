import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreRepository, GovernedReferenceError
from governed_core.services import ApplicabilityService, PointContextService


class MCMWQTemporalStateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repository = GovernedCoreRepository(Path(self.temp.name) / "temporal.sqlite3").initialize()
        state = FirstRealAPSBootstrap(self.repository).execute()
        self.state = state

    def tearDown(self):
        self.temp.cleanup()

    def test_new_context_requires_explicit_effective_from_and_preserves_created_at(self):
        point = self.repository.fetch_point(self.state.point_id)
        context = self.repository.fetch_current_context(point.point_id)
        service = PointContextService(self.repository)
        created = service.create_context_revision(
            point.point_id, context.purpose, context.water_context, context.point_type,
            "ACTOR", effective_from=datetime(2026, 9, 1, tzinfo=timezone.utc),
        )
        self.assertEqual("2026-09-01T00:00:00.000000Z", created.effective_from)
        self.assertNotEqual(created.created_at, created.effective_from)

    def test_temporal_aps_start_is_inclusive_and_zero_match_blocks(self):
        service = ApplicabilityService(self.repository)
        service.assign_temporal(self.state.context_revision_id, self.state.aps_reference,
                                datetime(2026, 9, 1, tzinfo=timezone.utc), actor_reference="ACTOR")
        self.assertEqual(self.state.aps_reference, self.repository.fetch_temporal_aps(
            self.state.context_revision_id, "2026-09-01T00:00:00.000000Z"))
        with self.assertRaises(GovernedReferenceError):
            self.repository.fetch_temporal_aps(self.state.context_revision_id, "2026-08-31T23:59:59.000000Z")


if __name__ == "__main__":
    unittest.main()
