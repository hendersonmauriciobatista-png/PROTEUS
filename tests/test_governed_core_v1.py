import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from governed_core.identifiers import IdentifierFactory
from governed_core.models import APSReference
from governed_core.reference_resolver import GovernedReferenceResolver
from governed_core.repository import (
    GovernedConflictError,
    GovernedCoreRepository,
    GovernedReferenceError,
)
from governed_core.services import APSService, ApplicabilityService, PointContextService


TEST_ACTOR = "test-data:actor:product-owner-fixture"
TEST_PROJECT = "test-data:project:rio-azul"
TEST_AUTHORITY = "test-data://authority/po-fixture"
TEST_EVIDENCE = "test-data://evidence/document-fixture"


class GovernedCoreV1Tests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "governed-core-test.sqlite3"
        self.repository = GovernedCoreRepository(self.database_path).initialize()
        self.identifiers = IdentifierFactory()
        self.points = PointContextService(self.repository, self.identifiers)
        self.aps = APSService(self.repository, self.identifiers)
        self.applicability = ApplicabilityService(self.repository, self.identifiers)

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_point(self, point_type="SPRING"):
        return self.points.create_point_with_initial_context(
            project_reference=TEST_PROJECT,
            display_name="TEST DATA - Ponto Rio Azul",
            purpose="ENVIRONMENTAL_CONDITION_MONITORING",
            water_context="FLOWING_SURFACE_WATER",
            point_type=point_type,
            actor_reference=TEST_ACTOR,
        )

    def create_aps(self, context_revision_id, parameters=("test_parameter_ph",), set_id=None):
        authority_id = self.aps.register_authority_reference(TEST_AUTHORITY)
        evidence_id = self.aps.register_evidence_reference(TEST_EVIDENCE)
        basis = self.aps.make_basis(
            authority_references=(authority_id,),
            evidence_references=(evidence_id,),
            member_references=parameters,
        )
        return self.aps.create_version(
            context_revision_id=context_revision_id,
            parameter_references=parameters,
            bases=(basis,),
            set_id=set_id,
        )

    def test_identifiers_are_non_semantic_and_validate_by_kind(self):
        point_id = self.identifiers.new("point")
        event_id = self.identifiers.new("event")

        self.assertTrue(self.identifiers.validate("point", point_id))
        self.assertTrue(self.identifiers.validate("event", event_id))
        self.assertNotEqual(point_id, self.identifiers.new("point"))
        with self.assertRaises(ValueError):
            self.identifiers.validate("point", event_id)

    def test_schema_has_no_generic_aps_status_or_eligibility_relation(self):
        with closing(sqlite3.connect(self.database_path)) as connection:
            aps_columns = {
                row[1] for row in connection.execute("PRAGMA table_info(authorized_parameter_set)")
            }
            version_columns = {
                row[1] for row in connection.execute("PRAGMA table_info(aps_version)")
            }
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }

        self.assertNotIn("status", aps_columns)
        self.assertNotIn("status", version_columns)
        self.assertNotIn("eligible", aps_columns | version_columns)
        self.assertNotIn("eligibility_relation", tables)

    def test_point_is_created_with_explicit_initial_context(self):
        point = self.create_point()
        current = self.repository.fetch_current_context(point.point_id)

        self.assertEqual("ACTIVE", point.status)
        self.assertEqual(point.current_context_revision_id, current.context_revision_id)
        self.assertEqual(1, current.revision)
        self.assertEqual("SPRING", current.point_type)
        self.assertEqual(TEST_PROJECT, point.project_reference)

    def test_context_change_creates_new_immutable_revision(self):
        point = self.create_point()
        original = self.repository.fetch_current_context(point.point_id)

        changed = self.points.create_context_revision(
            point_id=point.point_id,
            purpose="ENVIRONMENTAL_CONDITION_MONITORING",
            water_context="FLOWING_SURFACE_WATER",
            point_type="GENERAL",
            actor_reference=TEST_ACTOR,
        )

        self.assertEqual(2, changed.revision)
        self.assertEqual("GENERAL", changed.point_type)
        self.assertEqual("SPRING", self.repository.fetch_context_revision(original.context_revision_id).point_type)
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repository.transaction() as connection:
                connection.execute(
                    "UPDATE point_context_revision SET point_type = 'GENERAL' "
                    "WHERE context_revision_id = ?",
                    (original.context_revision_id,),
                )

    def test_return_to_previous_values_creates_next_revision(self):
        point = self.create_point("SPRING")
        self.points.create_context_revision(
            point.point_id,
            "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER",
            "GENERAL",
            TEST_ACTOR,
        )
        returned = self.points.create_context_revision(
            point.point_id,
            "ENVIRONMENTAL_CONDITION_MONITORING",
            "FLOWING_SURFACE_WATER",
            "SPRING",
            TEST_ACTOR,
        )

        self.assertEqual(3, returned.revision)
        self.assertNotEqual(point.current_context_revision_id, returned.context_revision_id)

    def test_display_name_and_status_do_not_create_context_revision(self):
        point = self.create_point()
        revision_id = point.current_context_revision_id

        renamed = self.points.update_display_name(point.point_id, "TEST DATA - Renomeado")
        inactive = self.points.update_status(point.point_id, "INACTIVE")

        self.assertEqual(revision_id, renamed.current_context_revision_id)
        self.assertEqual(revision_id, inactive.current_context_revision_id)

    def test_cross_point_current_reference_fails_safe(self):
        first = self.create_point()
        second = self.create_point("WELL")

        with self.assertRaises(GovernedConflictError):
            with self.repository.transaction() as connection:
                connection.execute(
                    "UPDATE governed_monitoring_point SET current_context_revision_id = ? "
                    "WHERE point_id = ?",
                    (second.current_context_revision_id, first.point_id),
                )

        self.assertEqual(
            first.current_context_revision_id,
            self.repository.fetch_point(first.point_id).current_context_revision_id,
        )

    def test_aps_requires_members_and_complete_authorization_path(self):
        point = self.create_point()

        with self.assertRaises(GovernedConflictError):
            self.aps.create_version(point.current_context_revision_id, (), ())

        authority_id = self.aps.register_authority_reference(TEST_AUTHORITY)
        evidence_id = self.aps.register_evidence_reference(TEST_EVIDENCE)
        incomplete_basis = self.aps.make_basis(
            (authority_id,),
            (evidence_id,),
            ("different_parameter",),
        )
        with self.assertRaises(GovernedConflictError):
            self.aps.create_version(
                point.current_context_revision_id,
                ("test_parameter_ph",),
                (incomplete_basis,),
            )

    def test_aps_versions_are_set_scoped_monotonic_and_immutable(self):
        point = self.create_point()
        first = self.create_aps(point.current_context_revision_id)
        second = self.create_aps(
            point.current_context_revision_id,
            parameters=("test_parameter_ph", "test_parameter_turbidity"),
            set_id=first.set_id,
        )

        self.assertEqual(1, first.version)
        self.assertEqual(2, second.version)
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repository.transaction() as connection:
                connection.execute(
                    "UPDATE aps_version SET version = 9 WHERE set_id = ? AND version = 1",
                    (first.set_id,),
                )

    def test_cross_version_basis_trace_fails_safe(self):
        point = self.create_point()
        first = self.create_aps(point.current_context_revision_id)
        second = self.create_aps(
            point.current_context_revision_id,
            parameters=("test_parameter_ph",),
            set_id=first.set_id,
        )

        with closing(sqlite3.connect(self.database_path)) as connection:
            basis_id = connection.execute(
                "SELECT basis_id FROM authorization_basis WHERE set_id = ? AND version = 1",
                (first.set_id,),
            ).fetchone()[0]
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repository.transaction() as connection:
                connection.execute(
                    "INSERT INTO member_authorization_basis "
                    "(set_id, version, parameter_reference, basis_id) VALUES (?, ?, ?, ?)",
                    (second.set_id, second.version, "test_parameter_ph", basis_id),
                )

    def test_applicability_requires_exact_matching_context(self):
        first_point = self.create_point()
        second_point = self.create_point("WELL")
        reference = self.create_aps(first_point.current_context_revision_id)

        with self.assertRaises(GovernedReferenceError):
            self.applicability.assign(
                second_point.current_context_revision_id,
                reference,
                TEST_ACTOR,
            )

        assigned = self.applicability.assign(
            first_point.current_context_revision_id,
            reference,
            TEST_ACTOR,
        )
        self.assertEqual(reference, assigned)

    def test_zero_applicability_blocks_future_use(self):
        point = self.create_point()

        with self.assertRaises(GovernedReferenceError):
            self.applicability.assert_future_use_allowed(point.point_id)

    def test_unresolved_disqualification_blocks_and_exact_requalification_restores(self):
        point = self.create_point()
        reference = self.create_aps(point.current_context_revision_id)
        self.applicability.assign(point.current_context_revision_id, reference, TEST_ACTOR)
        first = self.applicability.disqualify(reference, TEST_ACTOR)
        second = self.applicability.disqualify(reference, TEST_ACTOR)

        with self.assertRaises(GovernedReferenceError):
            self.applicability.assert_future_use_allowed(point.point_id)

        self.applicability.requalify(reference, (first,), TEST_ACTOR)
        with self.assertRaises(GovernedReferenceError):
            self.applicability.assert_future_use_allowed(point.point_id)

        self.applicability.requalify(reference, (second,), TEST_ACTOR)
        self.assertEqual(
            reference,
            self.applicability.assert_future_use_allowed(point.point_id),
        )

    def test_requalification_rejects_missing_or_cross_target_event(self):
        first_point = self.create_point()
        second_point = self.create_point("WELL")
        first_aps = self.create_aps(first_point.current_context_revision_id)
        second_aps = self.create_aps(second_point.current_context_revision_id)
        disqualification = self.applicability.disqualify(first_aps, TEST_ACTOR)

        with self.assertRaises(GovernedReferenceError):
            self.applicability.requalify(first_aps, ("gev_missing",), TEST_ACTOR)
        with self.assertRaises(GovernedConflictError):
            self.applicability.requalify(second_aps, (disqualification,), TEST_ACTOR)

    def test_governance_events_are_append_only_and_not_timestamp_identity(self):
        point = self.create_point()
        reference = self.create_aps(point.current_context_revision_id)
        self.applicability.assign(point.current_context_revision_id, reference, TEST_ACTOR)
        first = self.applicability.disqualify(reference, TEST_ACTOR)
        second = self.applicability.disqualify(reference, TEST_ACTOR)

        self.assertNotEqual(first, second)
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repository.transaction() as connection:
                connection.execute(
                    "UPDATE governance_event SET actor_reference = 'changed' WHERE event_id = ?",
                    (first,),
                )

    def test_broken_authorization_reference_fails_safe(self):
        point = self.create_point()
        reference = self.create_aps(point.current_context_revision_id)
        resolver = GovernedReferenceResolver(self.repository)
        self.applicability.assign(point.current_context_revision_id, reference, TEST_ACTOR)

        self.assertEqual(reference, resolver.resolve_operational_aps(point.point_id))
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repository.transaction() as connection:
                connection.execute("PRAGMA foreign_keys = OFF")
                connection.execute("DELETE FROM authority_reference")


if __name__ == "__main__":
    unittest.main()
