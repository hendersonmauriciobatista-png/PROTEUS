import hashlib
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.repository import GovernedCoreRepository, GovernedReferenceError
from governed_core.services import APSService, ApplicabilityService, PointContextService
from governed_core.measurement_service import GovernedMeasurementService
from governed_core.measurement_models import GovernedMeasurementRequest, DataProvenance
from governed_core.evaluation_service import GovernedEvaluationService
from governed_core.rule_service import RuleService
from governed_core.authority_service import AuthorityService


class TemporalMeasurementContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = GovernedCoreRepository(Path(self.temp.name) / "temporal.sqlite3").initialize()
        self.point = PointContextService(self.repo).create_point_with_initial_context(
            "p", "Temporal", "ENVIRONMENTAL_CONDITION_MONITORING", "FLOWING_SURFACE_WATER", "GENERAL", "A",
            effective_from=datetime(2020, 1, 1, tzinfo=timezone.utc))
        with self.repo.transaction() as cx:
            cx.execute("INSERT INTO authority_reference VALUES ('a','a',NULL)")
            cx.execute("INSERT INTO evidence_reference VALUES ('e','e',NULL)")
        basis = APSService(self.repo).make_basis(("a",), ("e",), ("PH",))
        self.aps = APSService(self.repo).create_version(self.point.current_context_revision_id, ("PH",), (basis,))
        ApplicabilityService(self.repo).assign_temporal(self.point.current_context_revision_id, self.aps, datetime(2020, 1, 1, tzinfo=timezone.utc), actor_reference="A")
        with self.repo._optional_connection(None) as cx:
            self.app_id = cx.execute("SELECT aps_applicability_id FROM aps_temporal_applicability").fetchone()[0]
        artifact = b"temporal-authority"
        AuthorityService(self.repo).create_authority(
            "urn:test:temporal-authority",
            hashlib.sha256(artifact).hexdigest(),
            self.point.current_context_revision_id,
            "PH",
            datetime(2020, 1, 1, tzinfo=timezone.utc),
            authority_id="authority-temporal",
            effective_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:published",
            artifact_bytes=artifact,
            artifact_locator_reference="urn:test:temporal-authority",
            verification_provenance="test:verification",
        )
        AuthorityService(self.repo).create_applicability(
            "authority-temporal",
            1,
            self.point.current_context_revision_id,
            "PH",
            datetime(2020, 1, 1, tzinfo=timezone.utc),
            "A",
            "test applicability",
        )

    def tearDown(self): self.temp.cleanup()

    def test_measured_at_resolves_context_aps_and_member(self):
        context = self.repo.fetch_temporal_context(self.point.point_id, "2020-01-01T00:00:00Z")
        aps = self.repo.fetch_temporal_aps(context.context_revision_id, "2020-01-01T00:00:00Z")
        self.assertEqual(self.aps, aps)
        self.repo.resolve_member_authorization(aps, "PH")

    def test_accept_temporal_persists_temporal_references(self):
        measurement = GovernedMeasurementService(self.repo).accept_temporal(
            GovernedMeasurementRequest(self.point.point_id, "PH", 7.2,
                                       datetime(2020, 1, 1, tzinfo=timezone.utc),
                                       DataProvenance.MANUAL_ENTRY))
        self.assertEqual(self.point.current_context_revision_id, measurement.context_revision_id)
        self.assertEqual(self.aps.set_id, measurement.aps_set_id)
        self.assertEqual(self.aps.version, measurement.aps_version)

    def test_temporal_evaluation_persists_zero_and_one_rule(self):
        measurement = GovernedMeasurementService(self.repo).accept_temporal(
            GovernedMeasurementRequest(self.point.point_id, "PH", 7.2, datetime(2020, 1, 1, tzinfo=timezone.utc), DataProvenance.MANUAL_ENTRY))
        evaluator = GovernedEvaluationService(self.repo)
        zero = evaluator.evaluate_temporal(measurement.measurement_id)
        self.assertEqual("NAO_AVALIAVEL", zero.status)
        RuleService(self.repo).create_version(self.point.current_context_revision_id, "PH", datetime(2020, 1, 1, tzinfo=timezone.utc), "test", {"operator": "RANGE_INCLUSIVE", "min": "6", "max": "9"}, "pH", ("a",), ("e",), rule_id="r-temporal")
        one = evaluator.evaluate_temporal(measurement.measurement_id)
        self.assertEqual("NORMAL", one.status)

    def test_boundaries_are_start_inclusive_end_exclusive(self):
        self.assertIsNotNone(self.repo.fetch_temporal_context(self.point.point_id, "2020-01-01T00:00:00Z"))
        with self.repo.transaction() as cx:
            cx.execute("UPDATE point_context_revision SET effective_until=? WHERE context_revision_id=?", ("2021-01-01T00:00:00Z", self.point.current_context_revision_id))
            cx.execute("UPDATE aps_temporal_applicability SET effective_until=? WHERE aps_applicability_id=?", ("2021-01-01T00:00:00Z", self.app_id))
        with self.assertRaises(GovernedReferenceError):
            self.repo.fetch_temporal_context(self.point.point_id, "2021-01-01T00:00:00Z")
        with self.assertRaises(GovernedReferenceError):
            self.repo.fetch_temporal_aps(self.point.current_context_revision_id, "2021-01-01T00:00:00Z")

    def test_zero_temporal_aps_and_missing_member_block(self):
        point = PointContextService(self.repo).create_point_with_initial_context(
            "p2", "No APS", "ENVIRONMENTAL_CONDITION_MONITORING", "FLOWING_SURFACE_WATER", "GENERAL", "A",
            effective_from=datetime(2020, 1, 1, tzinfo=timezone.utc))
        with self.repo.transaction() as cx:
            pass
        with self.assertRaises(GovernedReferenceError):
            context = self.repo.fetch_temporal_context(point.point_id, "2020-01-01T00:00:00Z")
            self.repo.fetch_temporal_aps(context.context_revision_id, "2020-01-01T00:00:00Z")
        with self.assertRaises(GovernedReferenceError):
            self.repo.resolve_member_authorization(self.aps, "MISSING")

    def test_overlapping_context_and_multiple_aps_are_prevented_at_write(self):
        with self.repo.transaction() as cx:
            cx.execute("SAVEPOINT overlapping_context")
            cx.execute("INSERT INTO geo_reference (geo_reference_id, context_revision_id, availability_state, state_reason, registered_at) VALUES ('geo-c2','c2','UNAVAILABLE','test','2020-01-01T00:00:00Z')")
            try:
                with self.assertRaises(sqlite3.IntegrityError):
                    cx.execute("INSERT INTO point_context_revision (context_revision_id,point_id,revision,purpose,water_context,point_type,geo_reference,created_at,effective_from,effective_until,geo_reference_id) VALUES ('c2',?,?,?,?,?,?,?,?,?,?)", (self.point.point_id, 2, "ENVIRONMENTAL_CONDITION_MONITORING", "FLOWING_SURFACE_WATER", "GENERAL", None, "2020", "2020-06-01T00:00:00Z", None, "geo-c2"))
            finally:
                cx.execute("ROLLBACK TO overlapping_context")
                cx.execute("RELEASE overlapping_context")
            with self.assertRaises(sqlite3.IntegrityError):
                cx.execute("INSERT INTO aps_temporal_applicability VALUES ('a2',?,?,?,?,?)", (self.point.current_context_revision_id, self.aps.set_id, self.aps.version, "2020-06-01T00:00:00Z", None))


if __name__ == "__main__": unittest.main()
