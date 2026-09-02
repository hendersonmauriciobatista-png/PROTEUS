import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.evaluation_service import GovernedEvaluationService
from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreError, GovernedCoreRepository, GovernedReferenceError


class GovernedEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repository = GovernedCoreRepository(Path(self.temp.name) / "a6.sqlite3").initialize()
        state = FirstRealAPSBootstrap(self.repository).execute()
        self.measurement = ExplicitGovernedEntryService(self.repository).submit(
            state.point_id, "PH", 7.2,
            datetime(2026, 8, 30, 12, 0, tzinfo=timezone.utc),
        )
        self.service = GovernedEvaluationService(
            self.repository,
            clock=lambda: datetime(2026, 8, 30, 12, 1, tzinfo=timezone.utc),
        )

    def tearDown(self):
        self.temp.cleanup()

    def record(self, **kwargs):
        values = dict(
            measurement_id=self.measurement.measurement_id,
            status="NORMAL", message="Dentro do limite", rule_origin="catalogo:limite_observacional",
            evaluated_at=datetime(2026, 8, 30, 12, 0, 30, tzinfo=timezone.utc),
        )
        values.update(kwargs)
        return self.service.record(**values)

    def test_zero_to_many_and_reevaluation_preserves_history(self):
        self.assertEqual((), self.repository.list_evaluations_by_measurement(self.measurement.measurement_id))
        first = self.record()
        second = self.record(status="ATENCAO", message="Reavaliacao")
        rows = self.repository.list_evaluations_by_measurement(self.measurement.measurement_id)
        self.assertEqual(2, len(rows))
        self.assertNotEqual(first.evaluation_id, second.evaluation_id)
        self.assertEqual({first.message, second.message}, {row.message for row in rows})

    def test_exact_references_and_temporal_separation(self):
        item = self.record()
        self.assertEqual(self.measurement.measurement_id, item.measurement_id)
        stored = self.repository.fetch_measurement(item.measurement_id)
        self.assertEqual(self.measurement.context_revision_id, stored.context_revision_id)
        self.assertEqual(self.measurement.aps_set_id, stored.aps_set_id)
        self.assertEqual(self.measurement.aps_version, stored.aps_version)
        self.assertEqual(self.measurement.measured_at, "2026-08-30T12:00:00.000000Z")
        self.assertNotEqual(stored.measured_at, item.evaluated_at)
        self.assertEqual("2026-08-30T12:01:00.000000Z", item.registered_at)

    def test_update_and_delete_are_rejected(self):
        item = self.record()
        with self.repository.transaction() as connection:
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute("UPDATE governed_evaluation SET status = 'CRITICO' WHERE evaluation_id = ?", (item.evaluation_id,))
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute("DELETE FROM governed_evaluation WHERE evaluation_id = ?", (item.evaluation_id,))

    def test_not_evaluable_with_valid_chain(self):
        item = self.record(status="NAO_AVALIAVEL", message="Sem limite observacional")
        self.assertEqual("NAO_AVALIAVEL", item.status)

    def test_missing_context_blocks_persistence(self):
        connection = self.repository._connect()
        connection.execute("UPDATE governed_monitoring_point SET current_context_revision_id = NULL WHERE point_id = ?", (self.measurement.point_id,))
        connection.commit()
        connection.close()
        with self.assertRaises(GovernedCoreError):
            self.record()
        self.assertEqual(0, len(self.repository.list_evaluations_by_measurement(self.measurement.measurement_id)))

    def test_ambiguous_aps_blocks_persistence(self):
        with self.repository.transaction() as connection:
            connection.execute("DELETE FROM aps_applicability WHERE context_revision_id = ?", (self.measurement.context_revision_id,))
        with self.assertRaises(GovernedReferenceError):
            self.record()
        self.assertEqual(0, len(self.repository.list_evaluations_by_measurement(self.measurement.measurement_id)))

    def test_engine_and_no_analytics_side_effects(self):
        item = self.record()
        self.assertEqual("OBSERVATIONAL_EVALUATOR_V1", item.evaluation_engine)
        self.assertEqual("1", item.evaluation_engine_version)
        self.assertIsNone(item.explanation_data)
        with self.repository._optional_connection(None) as connection:
            self.assertEqual(2, connection.execute("SELECT COUNT(*) FROM governance_event").fetchone()[0])

    def test_persistence_is_compatible_with_nullable_trailing_columns(self):
        item = self.record(explanation_data={"fixture": "nullable-extension"})
        rows = self.repository.list_evaluations_by_measurement(self.measurement.measurement_id)
        self.assertEqual((item,), rows)
        with self.repository._optional_connection(None) as connection:
            columns = {
                row[1] for row in connection.execute("PRAGMA table_info(governed_evaluation)")
            }
            self.assertTrue(
                {
                    "rule_id",
                    "rule_version",
                    "rule_payload_hash",
                    "authority_reference_ids",
                    "evidence_reference_ids",
                    "context_revision_id",
                    "aps_set_id",
                    "aps_version",
                }.issubset(columns)
            )
            self.assertEqual(
                (None,) * 8,
                connection.execute(
                    "SELECT rule_id, rule_version, rule_payload_hash, "
                    "authority_reference_ids, evidence_reference_ids, "
                    "context_revision_id, aps_set_id, aps_version "
                    "FROM governed_evaluation WHERE evaluation_id = ?",
                    (item.evaluation_id,),
                ).fetchone(),
            )


if __name__ == "__main__":
    unittest.main()
