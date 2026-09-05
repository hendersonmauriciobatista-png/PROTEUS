import hashlib
import sqlite3
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from governed_core.authority_service import AuthorityService
from governed_core.repository import GovernedCoreRepository


class SchemaAAuthorityArtifactVerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = GovernedCoreRepository(Path(self.tmp.name) / "db.sqlite3").initialize()
        self.service = AuthorityService(self.repo)
        self.when = datetime(2026, 1, 1, tzinfo=timezone.utc)

    def tearDown(self):
        self.tmp.cleanup()

    def _insert_verification_fixture(self, connection, suffix, verified_at):
        authority_id = f"fixture-{suffix}"
        artifact_id = f"artifact-{suffix}"
        raw = bytes([0, 10, 13, 255, int(suffix) if str(suffix).isdigit() else 1])
        digest = hashlib.sha256(raw).hexdigest()
        stamp = "2026-01-01T00:00:00.000001Z"
        connection.execute("INSERT INTO governed_authority VALUES (?,?,?,?,?)",
            (authority_id, 1, f"urn:{authority_id}", digest, stamp))
        connection.execute("INSERT INTO authority_scope VALUES (?,?,?,?)",
            (authority_id, 1, "ctx", "p"))
        connection.execute("INSERT INTO authority_temporal_boundary VALUES (?,?,?,?)",
            (authority_id, 1, stamp, None))
        connection.execute("INSERT INTO authority_artifact VALUES (?,?,?,?,?,?,?)",
            (artifact_id, 1, f"urn:{artifact_id}", raw, digest, "sha-256/v1", stamp))
        connection.execute("INSERT INTO authority_artifact_binding VALUES (?,?,?,?)",
            (authority_id, 1, artifact_id, 1))
        connection.commit()
        values = (f"verification-{suffix}", authority_id, 1, artifact_id, 1,
                  "sha-256/v1", "mcm-authority-artifact-hash/v1", digest, digest,
                  "VERIFIED", verified_at, "test:fixture")
        return values

    def test_verified_artifact_is_required_for_canonical_publication(self):
        raw = b"authority-document-v1"
        digest = hashlib.sha256(raw).hexdigest()
        authority = self.service.create_authority(
            "urn:authority", digest, "ctx", "p", self.when,
            effective_at=self.when,
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:publication",
            artifact_bytes=raw, artifact_locator_reference="urn:artifact:1",
            verification_provenance="test:verification",
        )
        verification = self.repo.fetch_authority_artifact_verification(
            authority.authority_id, authority.authority_version
        )
        self.assertEqual("VERIFIED", verification.verification_result)
        self.assertEqual(digest, verification.computed_digest)

    def test_canonical_publication_without_matching_artifact_rolls_back(self):
        raw = b"authority-document-v1"
        digest = hashlib.sha256(raw).hexdigest()
        with self.assertRaises(ValueError):
            self.service.create_authority(
                "urn:authority", digest, "ctx", "p", self.when,
                effective_at=self.when,
                effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
                effective_at_provenance="test:publication",
                artifact_bytes=b"different", artifact_locator_reference="urn:artifact:1",
                verification_provenance="test:verification",
            )
        connection = self.repo._connect()
        try:
            self.assertEqual(0, connection.execute("SELECT count(*) FROM governed_authority").fetchone()[0])
        finally:
            connection.close()

    def test_physical_names_and_database_digest_canonicality(self):
        connection = self.repo._connect()
        try:
            artifact_columns = {row[1] for row in connection.execute(
                "PRAGMA table_info(authority_artifact)"
            )}
            verification_columns = {row[1] for row in connection.execute(
                "PRAGMA table_info(authority_artifact_verification)"
            )}
            self.assertIn("artifact_locator_reference", artifact_columns)
            self.assertNotIn("artifact_locator", artifact_columns)
            self.assertIn("algorithm_id", verification_columns)
            self.assertNotIn("digest_algorithm", verification_columns)
            valid = "a" * 64
            invalid = ("A" * 64, "g" * 64, "a" * 63, "a" * 65,
                       " " + "a" * 63, "a" * 63 + " ")
            for index, digest in enumerate((valid, *invalid)):
                try:
                    connection.execute(
                        "INSERT INTO authority_artifact VALUES (?,?,?,?,?,?,?)",
                        (f"digest-{index}", 1, f"urn:digest:{index}", b"x", digest,
                         "sha-256/v1", "2026-01-01T00:00:00.000001Z"),
                    )
                    accepted = True
                except sqlite3.IntegrityError:
                    accepted = False
                self.assertEqual(index == 0, accepted, digest)
            connection.rollback()
        finally:
            connection.close()

    def test_verified_at_uses_strict_gregorian_utc_contract(self):
        invalid = (
            "2026-02-29T00:00:00.000000Z", "2026-02-30T00:00:00.000000Z",
            "2026-13-01T00:00:00.000000Z", "2026-01-01T24:00:00.000000Z",
            "2026-01-01T00:60:00.000000Z", "2026-01-01T00:00:60.000000Z",
            "2026-01-01T00:00:00Z", "2026-01-01T00:00:00.00000Z",
            "2026-01-01T00:00:00.000000+00:00",
        )
        for index, timestamp in enumerate(invalid):
            connection = self.repo._connect()
            try:
                values = self._insert_verification_fixture(connection, index, timestamp)
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute(
                        "INSERT INTO authority_artifact_verification VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                        values,
                    )
            finally:
                connection.close()
        for index, timestamp in enumerate((
            "2024-02-29T00:00:00.000000Z", "2026-01-01T00:00:00.000000Z"
        ), start=20):
            connection = self.repo._connect()
            try:
                values = self._insert_verification_fixture(connection, index, timestamp)
                connection.execute(
                    "INSERT INTO authority_artifact_verification VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    values,
                )
                connection.commit()
            finally:
                connection.close()

    def test_verified_at_is_independent_actual_verification_time(self):
        raw = b"time-role"
        digest = hashlib.sha256(raw).hexdigest()
        verification_time = datetime(2026, 1, 1, 0, 0, 2, 123456, tzinfo=timezone.utc)
        authority = self.service.create_authority(
            "urn:time", digest, "ctx", "p", self.when,
            effective_at=self.when,
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:effective",
            artifact_bytes=raw, artifact_locator_reference="urn:time:artifact",
            verification_provenance="test:actual-verification",
            verified_at=verification_time,
        )
        verification = self.repo.fetch_authority_artifact_verification(
            authority.authority_id, authority.authority_version
        )
        self.assertEqual("2026-01-01T00:00:02.123456Z", verification.verified_at)
        self.assertNotEqual(authority.created_at, verification.verified_at)

    def test_current_contract_is_unique_but_future_contract_can_be_recorded(self):
        raw = b"contract-version"
        digest = hashlib.sha256(raw).hexdigest()
        authority = self.service.create_authority(
            "urn:contract", digest, "ctx", "p", self.when,
            effective_at=self.when,
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:contract",
            artifact_bytes=raw, artifact_locator_reference="urn:contract:artifact",
            verification_provenance="test:contract-proof",
        )
        connection = self.repo._connect()
        try:
            verification = connection.execute(
                "SELECT verification_id,authority_id,authority_version,artifact_id,"
                "artifact_version,algorithm_id,verification_contract_version,"
                "expected_digest,computed_digest,verification_result,verified_at,"
                "verification_provenance FROM authority_artifact_verification "
                "WHERE authority_id=?", (authority.authority_id,)
            ).fetchone()
            future = list(verification)
            future[0] = "future-contract-verification"
            future[6] = "mcm-authority-artifact-hash/v2"
            future[10] = "2026-01-01T00:00:03.000000Z"
            connection.execute(
                "INSERT INTO authority_artifact_verification VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                future,
            )
            connection.commit()
            self.assertEqual(2, connection.execute(
                "SELECT count(*) FROM authority_artifact_verification WHERE authority_id=?",
                (authority.authority_id,),
            ).fetchone()[0])
        finally:
            connection.close()

    def test_immutable_artifact_can_be_explicitly_shared(self):
        raw = b"shared-artifact"
        digest = hashlib.sha256(raw).hexdigest()
        first = self.service.create_authority(
            "urn:first", digest, "ctx", "p", self.when,
            effective_at=self.when,
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:first",
            artifact_bytes=raw, artifact_locator_reference="urn:shared",
            artifact_id="shared-artifact", verification_provenance="test:proof",
        )
        connection = self.repo._connect()
        try:
            stamp = "2026-01-01T00:00:00.000001Z"
            connection.execute("INSERT INTO governed_authority VALUES (?,?,?,?,?)",
                ("second", 1, "urn:second", digest, stamp))
            connection.execute("INSERT INTO authority_scope VALUES (?,?,?,?)",
                ("second", 1, "ctx", "p"))
            connection.execute("INSERT INTO authority_temporal_boundary VALUES (?,?,?,?)",
                ("second", 1, stamp, None))
            connection.commit()
        finally:
            connection.close()
        AuthorityService(self.repo).verify_authority_artifact(
            "second", 1, raw, "urn:shared", "test:shared",
            artifact_id="shared-artifact",
            verified_at=datetime(2026, 1, 1, 0, 0, 2, tzinfo=timezone.utc),
        )
        connection = self.repo._connect()
        try:
            self.assertEqual(2, connection.execute(
                "SELECT count(*) FROM authority_artifact_binding WHERE artifact_id='shared-artifact'"
            ).fetchone()[0])
            self.assertEqual(1, connection.execute(
                "SELECT count(*) FROM authority_artifact WHERE artifact_id='shared-artifact'"
            ).fetchone()[0])
        finally:
            connection.close()

    def test_backup_restore_preserves_blob_and_verification(self):
        raw = bytes([0, 10, 13, 255, 42, 128])
        digest = hashlib.sha256(raw).hexdigest()
        authority = self.service.create_authority(
            "urn:backup", digest, "ctx", "p", self.when,
            effective_at=self.when,
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:backup",
            artifact_bytes=raw, artifact_locator_reference="urn:backup:artifact",
            verification_provenance="test:backup-proof",
        )
        destination = Path(self.tmp.name) / "backup.sqlite3"
        source = sqlite3.connect(self.repo.path)
        target = sqlite3.connect(destination)
        try:
            source.backup(target)
            target.commit()
            row = target.execute(
                "SELECT artifact_id,artifact_version,artifact_bytes,artifact_digest "
                "FROM authority_artifact"
            ).fetchone()
            evidence = target.execute(
                "SELECT verification_id FROM authority_artifact_verification "
                "WHERE authority_id=?", (authority.authority_id,)
            ).fetchone()
        finally:
            target.close()
            source.close()
        self.assertEqual(("" + authority.authority_id + ":artifact:1", 1, raw, digest), row)
        self.assertIsNotNone(evidence)

    def _create_direct_constraint_fixture(self, suffix):
        raw = f"direct-constraint-{suffix}".encode()
        digest = hashlib.sha256(raw).hexdigest()
        authority = self.service.create_authority(
            f"urn:direct-constraint:{suffix}", digest, "ctx", "p", self.when,
            effective_at=self.when,
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:direct-constraint",
            artifact_bytes=raw,
            artifact_locator_reference=f"urn:direct-constraint:{suffix}",
            verification_provenance="test:direct-constraint-proof",
        )
        return authority

    def _schema_a_rows(self, connection, authority_id):
        return {
            "artifact": connection.execute(
                "SELECT * FROM authority_artifact WHERE artifact_id=?",
                (f"{authority_id}:artifact:1",),
            ).fetchone(),
            "binding": connection.execute(
                "SELECT * FROM authority_artifact_binding WHERE authority_id=?",
                (authority_id,),
            ).fetchone(),
            "verification": connection.execute(
                "SELECT * FROM authority_artifact_verification WHERE authority_id=?",
                (authority_id,),
            ).fetchone(),
        }

    def test_direct_update_rejection_preserves_all_schema_a_rows(self):
        authority = self._create_direct_constraint_fixture("update")
        connection = self.repo._connect()
        try:
            before = self._schema_a_rows(connection, authority.authority_id)
            attempts = (
                (
                    "artifact",
                    "UPDATE authority_artifact SET artifact_bytes=? "
                    "WHERE artifact_id=? AND artifact_version=?",
                    (b"mutated", f"{authority.authority_id}:artifact:1", 1),
                ),
                (
                    "binding",
                    "UPDATE authority_artifact_binding SET artifact_version=? "
                    "WHERE authority_id=? AND authority_version=?",
                    (2, authority.authority_id, 1),
                ),
                (
                    "verification",
                    "UPDATE authority_artifact_verification SET verification_provenance=? "
                    "WHERE authority_id=? AND authority_version=?",
                    ("mutated", authority.authority_id, 1),
                ),
            )
            for object_name, statement, values in attempts:
                with self.subTest(object_name=object_name):
                    with self.assertRaises(sqlite3.Error):
                        connection.execute(statement, values)
                    connection.rollback()
                    self.assertEqual(before, self._schema_a_rows(connection, authority.authority_id))
        finally:
            connection.close()

    def test_direct_delete_rejection_preserves_all_schema_a_rows(self):
        authority = self._create_direct_constraint_fixture("delete")
        connection = self.repo._connect()
        try:
            before = self._schema_a_rows(connection, authority.authority_id)
            attempts = (
                (
                    "artifact",
                    "DELETE FROM authority_artifact WHERE artifact_id=? AND artifact_version=?",
                    (f"{authority.authority_id}:artifact:1", 1),
                ),
                (
                    "binding",
                    "DELETE FROM authority_artifact_binding "
                    "WHERE authority_id=? AND authority_version=?",
                    (authority.authority_id, 1),
                ),
                (
                    "verification",
                    "DELETE FROM authority_artifact_verification "
                    "WHERE authority_id=? AND authority_version=?",
                    (authority.authority_id, 1),
                ),
            )
            for object_name, statement, values in attempts:
                with self.subTest(object_name=object_name):
                    with self.assertRaises(sqlite3.Error):
                        connection.execute(statement, values)
                    connection.rollback()
                    self.assertEqual(before, self._schema_a_rows(connection, authority.authority_id))
        finally:
            connection.close()

    def test_direct_database_binding_cardinality_rejects_duplicate_binding(self):
        authority = self._create_direct_constraint_fixture("binding-cardinality")
        connection = self.repo._connect()
        try:
            artifact = connection.execute(
                "SELECT artifact_bytes,artifact_digest,registered_at "
                "FROM authority_artifact WHERE artifact_id=? AND artifact_version=1",
                (f"{authority.authority_id}:artifact:1",),
            ).fetchone()
            connection.execute(
                "INSERT INTO authority_artifact VALUES (?,?,?,?,?,?,?)",
                (
                    "alternate-binding-artifact", 1, "urn:alternate-binding-artifact",
                    artifact[0], artifact[1], "sha-256/v1", artifact[2],
                ),
            )
            connection.commit()
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "INSERT INTO authority_artifact_binding VALUES (?,?,?,?)",
                    (authority.authority_id, 1, "alternate-binding-artifact", 1),
                )
            connection.rollback()
            self.assertEqual(
                1,
                connection.execute(
                    "SELECT count(*) FROM authority_artifact_binding "
                    "WHERE authority_id=? AND authority_version=?",
                    (authority.authority_id, 1),
                ).fetchone()[0],
            )
        finally:
            connection.close()

    def test_direct_database_verification_cardinality_rejects_duplicate_contract(self):
        authority = self._create_direct_constraint_fixture("verification-cardinality")
        connection = self.repo._connect()
        try:
            original = connection.execute(
                "SELECT * FROM authority_artifact_verification WHERE authority_id=?",
                (authority.authority_id,),
            ).fetchone()
            duplicate = list(original)
            duplicate[0] = "direct-duplicate-verification"
            duplicate[10] = "2026-01-01T00:00:03.000000Z"
            duplicate[11] = "test:direct-duplicate-verification"
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    "INSERT INTO authority_artifact_verification VALUES "
                    "(?,?,?,?,?,?,?,?,?,?,?,?)",
                    duplicate,
                )
            connection.rollback()
            self.assertEqual(
                original,
                connection.execute(
                    "SELECT * FROM authority_artifact_verification WHERE authority_id=?",
                    (authority.authority_id,),
                ).fetchone(),
            )
            self.assertEqual(
                1,
                connection.execute(
                    "SELECT count(*) FROM authority_artifact_verification "
                    "WHERE authority_id=? AND authority_version=? "
                    "AND verification_contract_version=?",
                    (authority.authority_id, 1, "mcm-authority-artifact-hash/v1"),
                ).fetchone()[0],
            )
        finally:
            connection.close()

    def test_schema_a_failure_injection_rolls_back_all_publication_rows(self):
        stages = ("after_artifact", "after_authority_registration", "after_binding",
                  "after_verification", "before_publication")
        for index, stage in enumerate(stages):
            service = AuthorityService(self.repo)
            service._test_schema_a_failure_hook = lambda current, expected=stage: (
                (_ for _ in ()).throw(RuntimeError(expected)) if current == expected else None
            )
            raw = f"rollback-{index}".encode()
            with self.assertRaises(RuntimeError):
                service.create_authority(
                    f"urn:rollback:{index}", hashlib.sha256(raw).hexdigest(), "ctx", "p", self.when,
                    effective_at=self.when,
                    effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
                    effective_at_provenance="test:rollback",
                    artifact_bytes=raw, artifact_locator_reference=f"urn:rollback:{index}",
                    verification_provenance="test:rollback-proof",
                )
            connection = self.repo._connect()
            try:
                self.assertEqual(0, connection.execute(
                    "SELECT count(*) FROM governed_authority WHERE origin_locator=?",
                    (f"urn:rollback:{index}",)
                ).fetchone()[0])
            finally:
                connection.close()

    def test_failure_reason_codes_are_stable_and_not_nao_avaliavel(self):
        def attempt(**kwargs):
            with self.assertRaises(Exception) as caught:
                self.service.create_authority(
                    kwargs.pop("origin_locator", "urn:failure"), kwargs.pop("content_hash", "a" * 64),
                    "ctx", "p", self.when, effective_at=self.when,
                    effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
                    effective_at_provenance="test:failure", **kwargs,
                )
            self.assertIsInstance(caught.exception, Exception)
            self.assertNotEqual(getattr(caught.exception, "reason_code", ""), "NAO_AVALIAVEL")
            return getattr(caught.exception, "reason_code", None)
        self.assertEqual("MISSING_ARTIFACT_BYTES", attempt())
        self.assertEqual("MALFORMED_EXPECTED_DIGEST", attempt(content_hash="A" * 64, artifact_bytes=b"x", artifact_locator_reference="urn:x", verification_provenance="p"))
        self.assertEqual("DIGEST_MISMATCH", attempt(artifact_bytes=b"x", artifact_locator_reference="urn:x", verification_provenance="p"))
        self.assertEqual("UNSUPPORTED_ALGORITHM", attempt(artifact_bytes=b"x", artifact_locator_reference="urn:x", verification_provenance="p", algorithm_id="md5/v1"))
        self.assertEqual("UNSUPPORTED_VERIFICATION_CONTRACT", attempt(artifact_bytes=b"x", artifact_locator_reference="urn:x", verification_provenance="p", verification_contract_version="v2"))
        self.assertEqual("PUBLICATION_PROOF_INCOMPLETE", attempt(artifact_bytes=b"x", artifact_locator_reference="urn:x"))
        self.assertEqual("INVALID_VERIFIED_AT", attempt(content_hash=hashlib.sha256(b"x").hexdigest(), artifact_bytes=b"x", artifact_locator_reference="urn:x", verification_provenance="p", verified_at="2026-01-01T00:00:00Z"))

    def test_duplicate_verification_is_stable_failure(self):
        raw = b"duplicate"
        digest = hashlib.sha256(raw).hexdigest()
        authority = self.service.create_authority(
            "urn:duplicate", digest, "ctx", "p", self.when,
            effective_at=self.when,
            effective_at_source="CALLER_SUPPLIED_EXPLICIT_TIME",
            effective_at_provenance="test:duplicate",
            artifact_bytes=raw, artifact_locator_reference="urn:duplicate:artifact",
            verification_provenance="test:duplicate-proof",
        )
        with self.assertRaises(Exception) as caught:
            self.service.verify_authority_artifact(
                authority.authority_id, authority.authority_version, raw,
                "urn:duplicate:artifact", "test:duplicate-again",
            )
        self.assertEqual("DUPLICATE_VERIFICATION", caught.exception.reason_code)

    def test_legacy_authority_remains_readable_and_can_be_verified_later(self):
        raw = b"legacy-authority"
        legacy_digest = hashlib.sha256(raw).hexdigest()
        authority_id = "legacy"
        migration_dir = Path(self.tmp.name) / "migrations"
        migration_dir.mkdir()
        source_dir = Path(__file__).resolve().parents[1] / "migrations"
        for migration in source_dir.glob("*.sql"):
            if not migration.name.startswith(("017_", "018_", "019_", "020_")):
                shutil.copy2(migration, migration_dir / migration.name)
        legacy_repo = GovernedCoreRepository(Path(self.tmp.name) / "legacy.sqlite3", migration_dir).initialize()
        connection = legacy_repo._connect()
        try:
            connection.execute("INSERT INTO governed_authority VALUES (?,?,?,?,?)",
                (authority_id, 1, "urn:legacy", legacy_digest, "2026-01-01T00:00:00.000001Z"))
            connection.execute("INSERT INTO authority_scope VALUES (?,?,?,?)",
                (authority_id, 1, "ctx", "p"))
            connection.execute("INSERT INTO authority_temporal_boundary VALUES (?,?,?,?)",
                (authority_id, 1, "2026-01-01T00:00:00.000001Z", None))
            connection.execute("INSERT INTO authority_state VALUES (?,?,?,?,?)",
                (authority_id, 1, "PUBLISHED", "2026-01-01T00:00:00.000001Z", None))
            connection.execute("INSERT INTO authority_event VALUES (?,?,?,?,?,?,?,?,?)",
                ("legacy-event", authority_id, 1, "PUBLISHED", "actor", "legacy", None, None,
                 "2026-01-01T00:00:00.000001Z"))
            connection.commit()
        finally:
            connection.close()
        shutil.copy2(source_dir / "017_mcm_wq_historical_authority_temporal_extension.sql", migration_dir)
        GovernedCoreRepository(Path(self.tmp.name) / "legacy.sqlite3", migration_dir).initialize()
        shutil.copy2(source_dir / "018_mcm_wq_authority_artifact_verification.sql", migration_dir)
        migrated_repo = GovernedCoreRepository(Path(self.tmp.name) / "legacy.sqlite3", migration_dir).initialize()
        authority = AuthorityService(migrated_repo).verify_authority_artifact(
            authority_id, 1, raw, "urn:legacy:artifact", "test:legacy-verification",
            verified_at=datetime(2026, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
        )
        self.assertEqual("VERIFIED", authority.verification_result)
        connection = migrated_repo._connect()
        try:
            self.assertEqual("PUBLISHED", connection.execute(
                "SELECT status FROM authority_state WHERE authority_id='legacy' AND authority_version=1"
            ).fetchone()[0])
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
