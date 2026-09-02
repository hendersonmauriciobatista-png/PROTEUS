import json
import sqlite3
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.first_real_aps_bootstrap import FirstRealAPSBootstrap
from governed_core.repository import GovernedCoreRepository, GovernedReferenceError
from governed_core.rule_service import RuleResolutionService, RuleService, canonical_payload


class B3RuleCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = GovernedCoreRepository(Path(self.temp.name) / "rules.sqlite3").initialize()
        self.state = FirstRealAPSBootstrap(self.repo).execute()
        self.auth = self._ref("authority_reference", "authority")
        self.evidence = self._ref("evidence_reference", "evidence")
        self.service = RuleService(self.repo)

    def tearDown(self):
        self.temp.cleanup()

    def _ref(self, table, prefix):
        ident = f"{prefix}-b3"
        column = "authority_reference_id" if table == "authority_reference" else "evidence_reference_id"
        with self.repo.transaction() as cx:
            cx.execute(f"INSERT INTO {table} ({column}, locator) VALUES (?, ?)", (ident, ident))
        return ident

    def _create(self, payload, start="2026-01-01T00:00:00.000000Z", end=None, **kwargs):
        return self.service.create_version(
            self.state.context_revision_id, "test_parameter_ph", datetime.fromisoformat(start.replace("Z", "+00:00")),
            "test-origin", payload, "pH", (self.auth,), (self.evidence,), effective_until=(datetime.fromisoformat(end.replace("Z", "+00:00")) if end else None), **kwargs)

    def test_all_declarative_operators_and_stable_hash(self):
        for index, payload in enumerate((
            {"operator": "MIN_INCLUSIVE", "min": "1"},
            {"operator": "MAX_INCLUSIVE", "max": "9"},
            {"operator": "RANGE_INCLUSIVE", "min": "1", "max": "9"},
            {"operator": "EQUALS", "value": "7"},
        ), 1):
            canonical = canonical_payload(payload, "pH")
            self.assertEqual(canonical, canonical_payload(json.loads(canonical), "pH"))
            self._create(payload, rule_id=f"rule-{index}", start=f"2026-0{index}-01T00:00:00.000000Z", end=f"2026-0{index}-28T00:00:00.000000Z")

    def test_invalid_payloads_are_rejected(self):
        cases = (
            {"operator": "MIN_INCLUSIVE", "min": "1", "extra": 2},
            {"operator": "EXEC", "value": "1"},
            {"operator": "MIN_INCLUSIVE", "min": "NaN"},
            {"operator": "MIN_INCLUSIVE", "min": "Infinity"},
            {"operator": "RANGE_INCLUSIVE", "min": "9", "max": "1"},
        )
        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                canonical_payload(payload, "pH")

    def test_zero_one_and_multiple_resolution(self):
        resolver = RuleResolutionService(self.repo)
        instant = datetime(2026, 1, 1, tzinfo=timezone.utc)
        self.assertEqual("NAO_AVALIAVEL", resolver.resolve(self.state.context_revision_id, "test_parameter_ph", instant).state)
        self._create({"operator": "MIN_INCLUSIVE", "min": "1"})
        self.assertEqual("RESOLVED", resolver.resolve(self.state.context_revision_id, "test_parameter_ph", instant).state)
        with self.assertRaises(sqlite3.IntegrityError):
            self._create({"operator": "MAX_INCLUSIVE", "max": "9"}, rule_id="second")

    def test_temporal_boundaries_and_history(self):
        self._create({"operator": "MIN_INCLUSIVE", "min": "1"}, start="2026-01-01T00:00:00.000000Z", end="2026-02-01T00:00:00.000000Z")
        resolver = RuleResolutionService(self.repo)
        self.assertEqual("RESOLVED", resolver.resolve(self.state.context_revision_id, "test_parameter_ph", datetime(2026, 1, 1, tzinfo=timezone.utc)).state)
        self.assertEqual("NAO_AVALIAVEL", resolver.resolve(self.state.context_revision_id, "test_parameter_ph", datetime(2026, 2, 1, tzinfo=timezone.utc)).state)

    def test_missing_authority_or_evidence_blocks(self):
        class BrokenRepository:
            def fetch_rules(self, *_):
                from governed_core.rule_models import GovernedRule
                return (GovernedRule("broken", 1, "p", "c", "2026-01-01", None, "o", "{}", "h", (), ("e",)),)
        result = RuleResolutionService(BrokenRepository()).resolve("c", "p", datetime(2026, 1, 1, tzinfo=timezone.utc))
        self.assertEqual("BLOCKED", result.state)

    def test_rule_is_immutable(self):
        rule = self._create({"operator": "EQUALS", "value": "1"})
        with self.repo.transaction() as cx:
            with self.assertRaises(sqlite3.IntegrityError):
                cx.execute("UPDATE governed_rule SET origin = 'changed' WHERE rule_id = ?", (rule.rule_id,))
            with self.assertRaises(sqlite3.IntegrityError):
                cx.execute("DELETE FROM governed_rule WHERE rule_id = ?", (rule.rule_id,))


if __name__ == "__main__":
    unittest.main()
