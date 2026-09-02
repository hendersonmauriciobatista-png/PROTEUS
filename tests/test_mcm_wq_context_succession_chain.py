import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.repository import GovernedCoreRepository, GovernedConflictError
from governed_core.services import APSService, ApplicabilityService, PointContextService
from governed_core.temporal_state import TemporalStateService


class ContextSuccessionChainTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = GovernedCoreRepository(Path(self.temp.name) / "chain.sqlite3").initialize()
        self.point = PointContextService(self.repo).create_point_with_initial_context(
            "fixture-project", "Historical point", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "ACTOR",
            effective_from=datetime(2020, 1, 1, tzinfo=timezone.utc))
        self.state = type("State", (), {"point_id": self.point.point_id,
            "context_revision_id": self.point.current_context_revision_id})()
        with self.repo.transaction() as cx:
            cx.execute("INSERT INTO authority_reference VALUES ('a-chain','a-chain',NULL)")
            cx.execute("INSERT INTO evidence_reference VALUES ('e-chain','e-chain',NULL)")
        aps = APSService(self.repo)
        basis0 = aps.make_basis(("a-chain",), ("e-chain",), ("PH",))
        self.state.aps_reference = aps.create_version(self.state.context_revision_id, ("PH",), (basis0,))
        self.app = ApplicabilityService(self.repo)
        self.app.assign_temporal(self.state.context_revision_id, self.state.aps_reference,
                                 datetime(2020, 1, 1, tzinfo=timezone.utc), actor_reference="ACTOR")
        with self.repo._optional_connection(None) as cx:
            self.app_id = cx.execute("SELECT aps_applicability_id FROM aps_temporal_applicability").fetchone()[0]
            self.basis = cx.execute("SELECT basis_id FROM authorization_basis LIMIT 1").fetchone()[0]

    def tearDown(self): self.temp.cleanup()

    def test_distinct_context_successor_has_its_own_aps_chain(self):
        instant = datetime(2025, 1, 1, tzinfo=timezone.utc)
        temporal = TemporalStateService(self.repo)
        temporal.close("APS_TEMPORAL_APPLICABILITY", self.app_id, instant, "ACTOR", self.basis)
        successor_id = temporal.append_successor(
            "POINT_CONTEXT_REVISION", self.state.context_revision_id,
            {"effective_from": instant, "revision": 2,
             "purpose": "WATER_USE_MONITORING", "water_context": "GROUNDWATER",
             "point_type": "WELL"}, "ACTOR", self.basis)
        refs = APSService(self.repo)
        basis = refs.make_basis(tuple(self._refs("authority_reference")), tuple(self._refs("evidence_reference")), ("PH",))
        new_aps = refs.create_version(successor_id, ("PH",), (basis,))
        self.app.assign_temporal(successor_id, new_aps, instant, actor_reference="ACTOR")
        old = self.repo.fetch_temporal_context(self.state.point_id, "2024-12-31T23:59:59Z")
        new = self.repo.fetch_temporal_context(self.state.point_id, "2025-01-01T00:00:00Z")
        self.assertEqual(self.state.context_revision_id, old.context_revision_id)
        self.assertEqual(successor_id, new.context_revision_id)
        self.assertEqual(self.state.aps_reference, self.repo.fetch_temporal_aps(old.context_revision_id, "2024-12-31T23:59:59Z"))
        self.assertEqual(new_aps, self.repo.fetch_temporal_aps(new.context_revision_id, "2025-01-01T00:00:00Z"))

    def _refs(self, table):
        column = "authority_reference_id" if table == "authority_reference" else "evidence_reference_id"
        with self.repo._optional_connection(None) as cx:
            return tuple(row[0] for row in cx.execute(f"SELECT {column} FROM {table}"))


if __name__ == "__main__": unittest.main()
