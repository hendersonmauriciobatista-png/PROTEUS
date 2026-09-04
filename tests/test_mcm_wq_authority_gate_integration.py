import unittest
import shutil
from contextlib import contextmanager
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import patch

from governed_core.authority_gate import AuthorityGate, AuthorityGateBlockedError
from governed_core.authority_service import AuthorityService
from governed_core.evaluation_service import GovernedEvaluationService
from governed_core.measurement_models import DataProvenance, GovernedMeasurementRequest
from governed_core.measurement_service import GovernedMeasurementService
from governed_core.repository import GovernedCoreRepository
from governed_core.rule_service import RuleResolution, RuleService
from governed_core.authority_models import AuthorityEvent, HistoricalAuthorityResolution
from governed_core.services import APSService, ApplicabilityService, PointContextService

from tests.test_mcm_wq_temporal_measurement_contract import (
    TemporalMeasurementContractTests,
)


class TrackingRepository(GovernedCoreRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.track_optional_connections = False
        self.connection_ids = []
        self.transaction_count = 0

    @contextmanager
    def transaction(self):
        self.transaction_count += 1
        with super().transaction() as connection:
            yield connection

    @contextmanager
    def _optional_connection(self, connection):
        if self.track_optional_connections and connection is None:
            raise AssertionError("integrated path opened an optional connection")
        if self.track_optional_connections and connection is not None:
            self.connection_ids.append(id(connection))
        with super()._optional_connection(connection) as active:
            yield active


class FailingRepository(GovernedCoreRepository):
    failure_stage = None

    def insert_evaluation(self, evaluation, connection):
        super().insert_evaluation(evaluation, connection)
        if self.failure_stage == "evaluation":
            raise RuntimeError("after evaluation persistence")

    def insert_authority_snapshot_basis(self, basis, connection):
        super().insert_authority_snapshot_basis(basis, connection)
        if self.failure_stage == "basis":
            raise RuntimeError("after basis persistence")

    def insert_authority_snapshot(self, snapshot, connection):
        if self.failure_stage == "snapshot":
            raise RuntimeError("at snapshot persistence")
        super().insert_authority_snapshot(snapshot, connection)


class AuthorityGateIntegrationEvidenceTests(TemporalMeasurementContractTests):
    def measurement(self):
        return GovernedMeasurementService(self.repo).accept_temporal(
            GovernedMeasurementRequest(
                self.point.point_id,
                "PH",
                7.2,
                datetime(2020, 1, 1, tzinfo=timezone.utc),
                DataProvenance.MANUAL_ENTRY,
            )
        )

    def assert_no_final_persistence(self, measurement_id):
        self.assertEqual((), self.repo.list_evaluations_by_measurement(measurement_id))
        with self.repo._optional_connection(None) as connection:
            self.assertEqual(
                0,
                connection.execute(
                    "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot_basis"
                ).fetchone()[0],
            )
            self.assertEqual(
                0,
                connection.execute(
                    "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot"
                ).fetchone()[0],
            )

    def test_measurement_fetch_failure_is_typed_and_fail_closed(self):
        with self.assertRaises(AuthorityGateBlockedError) as raised:
            GovernedEvaluationService(self.repo).evaluate_temporal("missing-measurement")
        self.assertEqual("MEASUREMENT_UNRESOLVED", raised.exception.reason_code)
        self.assertEqual("missing-measurement", raised.exception.result.resolution_provenance["measurement_id"])

    def _new_point_with_aps(self, effective_from=datetime(2019, 1, 1, tzinfo=timezone.utc)):
        point = PointContextService(self.repo).create_point_with_initial_context(
            "p-real", "Real evidence", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "A", effective_from=effective_from,
        )
        basis = APSService(self.repo).make_basis(("a",), ("e",), ("PH",))
        aps = APSService(self.repo).create_version(
            point.current_context_revision_id, ("PH",), (basis,)
        )
        ApplicabilityService(self.repo).assign_temporal(
            point.current_context_revision_id, aps, effective_from, actor_reference="A"
        )
        return point

    def _real_measurement(self, point, measured_at):
        return GovernedMeasurementService(self.repo).accept_temporal(
            GovernedMeasurementRequest(
                point.point_id, "PH", 7.2, measured_at, DataProvenance.MANUAL_ENTRY
            )
        )

    def test_real_db_zero_authority_candidate_blocks_at_gate(self):
        point = self._new_point_with_aps()
        measurement = self._real_measurement(point, datetime(2020, 1, 1, tzinfo=timezone.utc))
        with self.assertRaises(AuthorityGateBlockedError) as raised:
            GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("NO_AUTHORITY_CANDIDATE", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)
        self.assertIsNotNone(self.repo.fetch_measurement(measurement.measurement_id))

    def test_real_db_ambiguous_applicability_history_blocks_without_winner(self):
        measurement = self.measurement()
        with self.repo.transaction() as connection:
            app_id = connection.execute(
                "SELECT applicability_id FROM authority_applicability"
            ).fetchone()[0]
            connection.execute(
                "INSERT INTO authority_applicability_event "
                "VALUES (?,?,?,?,?,?,?,?)",
                (
                    "real-ambiguous-event", app_id, "PUBLISHED",
                    "2020-01-01T00:00:00.000000Z",
                    "2020-01-01T00:00:02.000000Z", "real-test", "duplicate publication", None,
                ),
            )
        with self.assertRaises(AuthorityGateBlockedError) as raised:
            GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("INCOMPLETE_AUTHORITY_HISTORY", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def _legacy_repository(self):
        temp = __import__("tempfile").TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = __import__("pathlib").Path(temp.name)
        migration_dir = root / "migrations"
        migration_dir.mkdir()
        source_dir = __import__("pathlib").Path(__file__).resolve().parents[1] / "migrations"
        for migration in source_dir.glob("*.sql"):
            if not migration.name.startswith(("017_", "018_", "019_")):
                shutil.copy2(migration, migration_dir / migration.name)
        repo = GovernedCoreRepository(root / "legacy.sqlite3", migration_dir).initialize()
        point = PointContextService(repo).create_point_with_initial_context(
            "legacy-p", "Legacy evidence", "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER", "GENERAL", "A",
            effective_from=datetime(2020, 1, 1, tzinfo=timezone.utc),
        )
        with repo.transaction() as connection:
            connection.execute("INSERT INTO authority_reference VALUES ('a','a',NULL)")
            connection.execute("INSERT INTO evidence_reference VALUES ('e','e',NULL)")
        basis = APSService(repo).make_basis(("a",), ("e",), ("PH",))
        aps = APSService(repo).create_version(
            point.current_context_revision_id, ("PH",), (basis,)
        )
        ApplicabilityService(repo).assign_temporal(
            point.current_context_revision_id, aps,
            datetime(2020, 1, 1, tzinfo=timezone.utc), actor_reference="A"
        )
        raw = b"legacy-integrated-authority"
        digest = __import__("hashlib").sha256(raw).hexdigest()
        registered = "2020-01-01T00:00:01.000000Z"
        effective = "2020-01-01T00:00:00.000000Z"
        with repo.transaction() as connection:
            connection.execute(
                "INSERT INTO governed_authority VALUES (?,?,?,?,?)",
                ("legacy-integrated", 1, "urn:legacy", digest, registered),
            )
            connection.execute(
                "INSERT INTO authority_scope VALUES (?,?,?,?)",
                ("legacy-integrated", 1, point.current_context_revision_id, "PH"),
            )
            connection.execute(
                "INSERT INTO authority_temporal_boundary VALUES (?,?,?,?)",
                ("legacy-integrated", 1, effective, None),
            )
            connection.execute(
                "INSERT INTO authority_state VALUES (?,?,?,?,?)",
                ("legacy-integrated", 1, "PUBLISHED", registered, None),
            )
            connection.execute(
                "INSERT INTO authority_event VALUES (?,?,?,?,?,?,?,?,?)",
                ("legacy-integrated-event", "legacy-integrated", 1, "PUBLISHED",
                 "A", "legacy", None, None, registered),
            )
        AuthorityService(repo).create_applicability(
            "legacy-integrated", 1, point.current_context_revision_id, "PH",
            datetime(2020, 1, 1, tzinfo=timezone.utc), "A", "legacy applicability",
        )
        shutil.copy2(source_dir / "017_mcm_wq_historical_authority_temporal_extension.sql", migration_dir)
        repo.initialize()
        shutil.copy2(source_dir / "018_mcm_wq_authority_artifact_verification.sql", migration_dir)
        repo.initialize()
        shutil.copy2(source_dir / "019_mcm_wq_evaluation_authority_snapshot.sql", migration_dir)
        repo.initialize()
        return repo, point, raw

    def test_real_db_legacy_missing_verification_blocks_at_gate(self):
        repo, point, _ = self._legacy_repository()
        measurement = GovernedMeasurementService(repo).accept_temporal(
            GovernedMeasurementRequest(
                point.point_id, "PH", 7.2,
                datetime(2020, 1, 1, tzinfo=timezone.utc),
                DataProvenance.MANUAL_ENTRY,
            )
        )
        with self.assertRaises(AuthorityGateBlockedError) as raised:
            GovernedEvaluationService(repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("MISSING_VERIFICATION", raised.exception.reason_code)
        self.assertEqual((), repo.list_evaluations_by_measurement(measurement.measurement_id))
        with repo._optional_connection(None) as connection:
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot_basis"
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot"
            ).fetchone()[0])

    def test_real_db_legacy_incomplete_history_blocks_after_verification(self):
        repo, point, raw = self._legacy_repository()
        AuthorityService(repo).verify_authority_artifact(
            "legacy-integrated", 1, raw, "urn:legacy:artifact", "real:legacy-proof",
            verified_at=datetime(2020, 1, 1, 0, 0, 3, tzinfo=timezone.utc),
        )
        measurement = GovernedMeasurementService(repo).accept_temporal(
            GovernedMeasurementRequest(
                point.point_id, "PH", 7.2,
                datetime(2020, 1, 1, tzinfo=timezone.utc),
                DataProvenance.MANUAL_ENTRY,
            )
        )
        with self.assertRaises(AuthorityGateBlockedError) as raised:
            GovernedEvaluationService(repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("LIFECYCLE_UNDEFINED", raised.exception.reason_code)
        self.assertEqual((), repo.list_evaluations_by_measurement(measurement.measurement_id))
        with repo._optional_connection(None) as connection:
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot_basis"
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM governed_evaluation_authority_snapshot"
            ).fetchone()[0])

    def test_real_db_before_authority_boundary_is_ineligible(self):
        point = self._new_point_with_aps()
        artifact = b"before-boundary-authority"
        AuthorityService(self.repo).create_authority(
            "urn:before-boundary", __import__("hashlib").sha256(artifact).hexdigest(),
            point.current_context_revision_id, "PH",
            datetime(2020, 1, 1, tzinfo=timezone.utc), authority_id="before-boundary",
            effective_at=datetime(2020, 1, 1, tzinfo=timezone.utc),
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="real:published", artifact_bytes=artifact,
            artifact_locator_reference="urn:before-boundary:artifact",
            verification_provenance="real:verification",
        )
        AuthorityService(self.repo).create_applicability(
            "before-boundary", 1, point.current_context_revision_id, "PH",
            datetime(2019, 1, 1, tzinfo=timezone.utc), "A", "real applicability",
        )
        measurement = self._real_measurement(point, datetime(2019, 6, 1, tzinfo=timezone.utc))
        with self.assertRaises(AuthorityGateBlockedError) as raised:
            GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("LIFECYCLE_INELIGIBLE", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def test_real_db_terminal_lifecycle_blocks_at_and_after_terminal(self):
        authority = AuthorityService(self.repo)
        authority.activate(
            "authority-temporal", 1, "A", "real active",
            effective_at=datetime(2020, 6, 1, tzinfo=timezone.utc),
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="real:active",
        )
        authority.revoke(
            "authority-temporal", 1, "A", "real terminal",
            effective_at=datetime(2021, 1, 1, tzinfo=timezone.utc),
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="real:terminal",
        )
        for measured_at in (
            datetime(2021, 1, 1, tzinfo=timezone.utc),
            datetime(2021, 6, 1, tzinfo=timezone.utc),
        ):
            with self.subTest(measured_at=measured_at):
                measurement = self._real_measurement(self.point, measured_at)
                with self.assertRaises(AuthorityGateBlockedError) as raised:
                    GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
                self.assertEqual("LIFECYCLE_INELIGIBLE", raised.exception.reason_code)
                self.assert_no_final_persistence(measurement.measurement_id)

    def test_real_db_scope_mismatch_blocks_at_gate(self):
        point = self._new_point_with_aps()
        AuthorityService(self.repo).create_applicability(
            "authority-temporal", 1, point.current_context_revision_id, "PH",
            datetime(2020, 1, 1, tzinfo=timezone.utc), "A", "mismatched scope",
        )
        measurement = self._real_measurement(point, datetime(2020, 1, 1, tzinfo=timezone.utc))
        with self.assertRaises(AuthorityGateBlockedError) as raised:
            GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("AUTHORITY_SCOPE_MISMATCH", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def test_real_path_invokes_gate_and_persists_complete_zero_snapshot(self):
        measurement = self.measurement()
        called = []
        original = AuthorityGate.resolve

        def wrapped(gate, *args, **kwargs):
            called.append(True)
            return original(gate, *args, **kwargs)

        with patch.object(AuthorityGate, "resolve", wrapped):
            evaluation = GovernedEvaluationService(self.repo).evaluate_temporal(
                measurement.measurement_id
            )
        self.assertEqual([True], called)
        snapshot = self.repo.fetch_authority_snapshot(evaluation.evaluation_id)
        basis = self.repo.list_authority_snapshot_basis(evaluation.evaluation_id)
        self.assertEqual(11, len(snapshot))
        self.assertEqual("RESOLVED", snapshot[7])
        self.assertEqual("ZERO_APPLICABLE_RULE", snapshot[9])
        self.assertEqual(1, len(basis))
        self.assertEqual(
            self.repo.resolve_member_authorization(
                self.aps, "PH"
            ).bases[0].basis_id,
            basis[0][1],
        )

    def test_real_path_persists_one_rule_snapshot_and_exact_bindings(self):
        measurement = self.measurement()
        RuleService(self.repo).create_version(
            self.point.current_context_revision_id,
            "PH",
            datetime(2020, 1, 1, tzinfo=timezone.utc),
            "test",
            {"operator": "RANGE_INCLUSIVE", "min": "6", "max": "9"},
            "pH",
            ("a",),
            ("e",),
            rule_id="integration-rule",
        )
        evaluation = GovernedEvaluationService(self.repo).evaluate_temporal(
            measurement.measurement_id
        )
        snapshot = self.repo.fetch_authority_snapshot(evaluation.evaluation_id)
        self.assertEqual("ONE_APPLICABLE_RULE", snapshot[9])
        self.assertIsNotNone(snapshot[3])
        self.assertEqual("authority-temporal", snapshot[1])
        self.assertEqual(
            "authority-temporal:verification:1",
            snapshot[6],
        )
        self.assertEqual(1, len(self.repo.list_authority_snapshot_basis(evaluation.evaluation_id)))

    def test_zero_candidate_is_typed_blocked_and_retains_measurement(self):
        measurement = self.measurement()
        with patch.object(self.repo, "fetch_authority_applicability_candidates", return_value=()):
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("NO_AUTHORITY_CANDIDATE", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)
        self.assertIsNotNone(self.repo.fetch_measurement(measurement.measurement_id))

    def test_multiple_and_conflicting_candidates_are_blocked_without_selection(self):
        measurement = self.measurement()
        real = self.repo.fetch_authority_applicability_candidates(
            measurement.context_revision_id, "PH", measurement.measured_at
        )[0]
        for candidates, expected in (
            ((real, real), "MULTIPLE_AUTHORITY_CANDIDATES"),
            ((real, ("other-app", "other-authority", 2, *real[3:])), "CONFLICTING_AUTHORITY"),
        ):
            with self.subTest(expected=expected):
                with patch.object(
                    self.repo,
                    "fetch_authority_applicability_candidates",
                    return_value=candidates,
                ):
                    with self.assertRaises(AuthorityGateBlockedError) as raised:
                        GovernedEvaluationService(self.repo).evaluate_temporal(
                            measurement.measurement_id
                        )
                self.assertEqual(expected, raised.exception.reason_code)
                self.assert_no_final_persistence(measurement.measurement_id)

    def test_unknown_policy_and_undefined_history_are_typed_blocked(self):
        measurement = self.measurement()
        with self.repo.transaction() as connection:
            context = self.repo.fetch_temporal_context(
                measurement.point_id, measurement.measured_at, connection
            )
            aps = self.repo.fetch_temporal_aps(
                context.context_revision_id, measurement.measured_at, connection
            )
            member = self.repo.resolve_member_authorization(aps, "PH", connection)
            result = AuthorityGate(
                self.repo,
                policy_contract_version="unknown-policy",
            ).resolve(measurement, context, member, connection)
            self.assertEqual("BLOCKED", result.status)
            self.assertEqual("UNKNOWN_POLICY_VERSION", result.reason_code)

        with patch(
            "governed_core.authority_gate.AuthorityService.resolve_historical_authority",
            return_value=HistoricalAuthorityResolution("UNDEFINED", "insufficient history"),
        ):
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(
                    measurement.measurement_id
                )
        self.assertEqual("LIFECYCLE_UNDEFINED", raised.exception.reason_code)

    def test_multiple_applicable_rules_use_governed_reason(self):
        measurement = self.measurement()
        with patch.object(
            __import__("governed_core.evaluation_service", fromlist=["RuleResolutionService"]),
            "RuleResolutionService",
        ) as resolver:
            resolver.return_value.resolve.return_value = RuleResolution(
                "BLOCKED", reason="MULTIPLE_APPLICABLE_RULES"
            )
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("MULTIPLE_APPLICABLE_RULES", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def test_applicability_history_ambiguity_blocks_without_winner_selection(self):
        measurement = self.measurement()
        with patch.object(
            self.repo,
            "fetch_authority_applicability_event_ids",
            return_value=("event-a", "event-b"),
        ):
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(measurement.measurement_id)
        self.assertEqual("INCOMPLETE_AUTHORITY_HISTORY", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def test_missing_and_unaccepted_verification_are_typed_blocked(self):
        measurement = self.measurement()
        for verification, expected in (
            (None, "MISSING_VERIFICATION"),
            (SimpleNamespace(verification_result="REJECTED"), "VERIFICATION_NOT_ACCEPTED"),
        ):
            with self.subTest(expected=expected):
                with patch.object(
                    self.repo,
                    "fetch_authority_artifact_verification",
                    return_value=verification,
                ):
                    with self.assertRaises(AuthorityGateBlockedError) as raised:
                        GovernedEvaluationService(self.repo).evaluate_temporal(
                            measurement.measurement_id
                        )
                self.assertEqual(expected, raised.exception.reason_code)
                self.assert_no_final_persistence(measurement.measurement_id)

    def test_scope_mismatch_and_malformed_history_fail_closed(self):
        measurement = self.measurement()
        with patch.object(self.repo, "fetch_authority_scope", return_value=()):
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(
                    measurement.measurement_id
                )
        self.assertEqual("AUTHORITY_SCOPE_MISMATCH", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

        with patch(
            "governed_core.authority_gate.AuthorityService.resolve_historical_authority",
            return_value=HistoricalAuthorityResolution(
                "UNDEFINED", "AUTHORITY_HISTORY_MALFORMED"
            ),
        ):
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(
                    measurement.measurement_id
                )
        self.assertEqual("LIFECYCLE_UNDEFINED", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def test_boundary_failure_maps_to_lifecycle_ineligible(self):
        measurement = self.measurement()
        with patch(
            "governed_core.authority_gate.AuthorityService.resolve_historical_authority",
            return_value=HistoricalAuthorityResolution(
                "TECHNICALLY_INELIGIBLE", "AUTHORITY_OUT_OF_WINDOW"
            ),
        ):
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(
                    measurement.measurement_id
                )
        self.assertEqual("LIFECYCLE_INELIGIBLE", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def test_terminal_lifecycle_event_blocks_at_measured_at(self):
        measurement = self.measurement()
        event = AuthorityEvent(
            "terminal-event", "authority-temporal", 1, "REVOKED", "test",
            "terminal", None, None, "2020-01-01T00:00:01.000000Z",
            "2020-01-01T00:00:00.000000Z", "CALLER_SUPPLIED_EXPLICIT_TIME", "test",
        )
        with patch(
            "governed_core.authority_gate.AuthorityService.resolve_historical_authority",
            return_value=HistoricalAuthorityResolution("RESOLVED", event=event),
        ):
            with self.assertRaises(AuthorityGateBlockedError) as raised:
                GovernedEvaluationService(self.repo).evaluate_temporal(
                    measurement.measurement_id
                )
        self.assertEqual("LIFECYCLE_INELIGIBLE", raised.exception.reason_code)
        self.assert_no_final_persistence(measurement.measurement_id)

    def test_post_commit_provenance_reads_snapshot_and_schema_a_binding(self):
        measurement = self.measurement()
        evaluation = GovernedEvaluationService(self.repo).evaluate_temporal(
            measurement.measurement_id
        )
        snapshot_before = self.repo.fetch_authority_snapshot(evaluation.evaluation_id)
        basis_before = self.repo.list_authority_snapshot_basis(evaluation.evaluation_id)
        service = AuthorityService(self.repo)
        service.activate(
            "authority-temporal", 1, "test", "post-commit active",
            effective_at=datetime(2021, 1, 1, tzinfo=timezone.utc),
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test",
        )
        service.revoke(
            "authority-temporal", 1, "test", "post-commit revoke",
            effective_at=datetime(2022, 1, 1, tzinfo=timezone.utc),
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test",
        )
        snapshot_after = self.repo.fetch_authority_snapshot(evaluation.evaluation_id)
        basis_after = self.repo.list_authority_snapshot_basis(evaluation.evaluation_id)
        self.assertEqual(snapshot_before, snapshot_after)
        self.assertEqual(basis_before, basis_after)
        with self.repo._optional_connection(None) as connection:
            self.assertIsNotNone(
                connection.execute(
                    "SELECT 1 FROM authority_artifact_verification "
                    "WHERE verification_id=? AND verification_result='VERIFIED'",
                    (snapshot_after[6],),
                ).fetchone()
            )

    def test_integrated_path_reuses_one_connection_and_no_optional_none(self):
        measurement = self.measurement()
        tracked = TrackingRepository(self.repo.path).initialize()
        tracked.track_optional_connections = True
        GovernedEvaluationService(tracked).evaluate_temporal(measurement.measurement_id)
        self.assertEqual(1, tracked.transaction_count)
        self.assertTrue(tracked.connection_ids)
        self.assertEqual(1, len(set(tracked.connection_ids)))

    def test_integrated_failures_roll_back_evaluation_basis_and_snapshot(self):
        measurement = self.measurement()
        for stage in ("evaluation", "basis", "snapshot"):
            with self.subTest(stage=stage):
                failing = FailingRepository(self.repo.path).initialize()
                failing.failure_stage = stage
                with self.assertRaises(AuthorityGateBlockedError):
                    GovernedEvaluationService(failing).evaluate_temporal(
                        measurement.measurement_id
                    )
                self.assert_no_final_persistence(measurement.measurement_id)


if __name__ == "__main__":
    unittest.main()
