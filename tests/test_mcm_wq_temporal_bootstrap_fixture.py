import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.repository import GovernedCoreRepository, GovernedReferenceError
from governed_core.services import APSService, ApplicabilityService, PointContextService


class TemporalBootstrapFixtureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = GovernedCoreRepository(Path(self.temp.name) / "fixture.sqlite3").initialize()
        self.point = PointContextService(self.repo).create_point_with_initial_context(
            "fixture-project", "Fixture point", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "FIXTURE_ACTOR",
            effective_from=datetime(2020, 1, 1, tzinfo=timezone.utc),
        )
        self._register_refs()
        aps = APSService(self.repo)
        basis = aps.make_basis((self.authority,), (self.evidence,), ("PH",))
        self.reference = aps.create_version(self.point.current_context_revision_id, ("PH",), (basis,))
        ApplicabilityService(self.repo).assign_temporal(
            self.point.current_context_revision_id, self.reference,
            datetime(2020, 1, 1, tzinfo=timezone.utc), actor_reference="FIXTURE_ACTOR",
        )

    def tearDown(self):
        self.temp.cleanup()

    def _register_refs(self):
        with self.repo.transaction() as cx:
            cx.execute("INSERT INTO authority_reference VALUES ('fixture-authority','fixture-authority',NULL)")
            cx.execute("INSERT INTO evidence_reference VALUES ('fixture-evidence','fixture-evidence',NULL)")
        self.authority, self.evidence = "fixture-authority", "fixture-evidence"

    def test_explicit_initial_intervals_resolve_historical_time(self):
        context = self.repo.fetch_temporal_context(self.point.point_id, "2020-01-01T00:00:00.000000Z")
        aps = self.repo.fetch_temporal_aps(context.context_revision_id, "2020-01-01T00:00:00.000000Z")
        self.assertEqual(self.point.current_context_revision_id, context.context_revision_id)
        self.assertEqual(self.reference, aps)
        with self.assertRaises(GovernedReferenceError):
            self.repo.fetch_temporal_context(self.point.point_id, "2019-12-31T23:59:59.999999Z")

    def test_open_ended_intervals_remain_resolvable_after_current_state_changes(self):
        before = self.repo.fetch_temporal_aps(self.point.current_context_revision_id, "2021-01-01T00:00:00Z")
        self.assertEqual(self.reference, before)
        with self.repo.transaction() as cx:
            cx.execute("UPDATE governed_monitoring_point SET display_name='Later name' WHERE point_id=?", (self.point.point_id,))
        after = self.repo.fetch_temporal_aps(self.point.current_context_revision_id, "2021-01-01T00:00:00Z")
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
