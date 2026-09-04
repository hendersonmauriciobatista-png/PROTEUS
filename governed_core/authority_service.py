"""Governed authority lifecycle and historical temporal resolution."""

import hashlib
import re
import sqlite3
from datetime import datetime, timezone

from .authority_models import (
    AuthorityEvent,
    EFFECTIVE_TIME_SOURCES,
    GovernedAuthority,
    GovernedApplicability,
    HistoricalAuthorityResolution,
)
from .identifiers import IdentifierFactory


EVENT_TYPES = {"PUBLISHED", "ACTIVE", "REVOKED", "SUPERSEDED"}
TERMINAL_EVENT_TYPES = {"REVOKED", "SUPERSEDED"}
CANONICAL_INSTANT = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{6}Z$"
)
SCHEMA_A_ALGORITHM_ID = "sha-256/v1"
SCHEMA_A_VERIFICATION_CONTRACT_VERSION = "mcm-authority-artifact-hash/v1"
CANONICAL_DIGEST = re.compile(r"^[0-9a-f]{64}$")
SCHEMA_A_FAILURE_REASONS = frozenset({
    "MISSING_ARTIFACT_BYTES", "MALFORMED_EXPECTED_DIGEST", "DIGEST_MISMATCH",
    "UNSUPPORTED_ALGORITHM", "UNSUPPORTED_VERIFICATION_CONTRACT",
    "BINDING_MISMATCH", "DUPLICATE_VERIFICATION", "INVALID_VERIFIED_AT",
    "PUBLICATION_PROOF_INCOMPLETE", "ARTIFACT_STORAGE_FAILURE",
    "VERIFICATION_STORAGE_FAILURE", "UNEXPECTED_VERIFICATION_FAILURE",
})


class SchemaAArtifactVerificationError(ValueError):
    """Stable Schema A failure with a separate diagnostic cause."""

    def __init__(self, reason_code, message, *, diagnostic=None):
        if reason_code not in SCHEMA_A_FAILURE_REASONS:
            raise ValueError("Unknown Schema A failure reason")
        super().__init__(message)
        self.reason_code = reason_code
        self.diagnostic = diagnostic or message


def _instant(value):
    if not isinstance(value, datetime) or value.tzinfo is None:
        raise ValueError("Timezone-aware effective time required")
    return value.astimezone(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def _canonical_text(value):
    if not isinstance(value, str) or not CANONICAL_INSTANT.fullmatch(value):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        return False
    return True


def _canonical_digest(value):
    return isinstance(value, str) and CANONICAL_DIGEST.fullmatch(value) is not None


class AuthorityService:
    def __init__(self, repository, identifiers=None, clock=None):
        self.repository = repository
        self.identifiers = identifiers or IdentifierFactory()
        self.clock = clock or (lambda: datetime.now(timezone.utc))
        self._test_failure_hook = None
        self._test_supersession_failure_hook = None
        self._test_schema_a_failure_hook = None

    def _schema_a_checkpoint(self, stage):
        if self._test_schema_a_failure_hook is not None:
            self._test_schema_a_failure_hook(stage)

    def _effective_time(self, effective_at, source, provenance, immediate_effect):
        if source not in EFFECTIVE_TIME_SOURCES:
            raise ValueError("Valid effective-time source is required")
        if not isinstance(provenance, str) or not provenance.strip():
            raise ValueError("Effective-time provenance is required")
        if source == "CALLER_SUPPLIED_EXPLICIT_TIME":
            if immediate_effect or effective_at is None:
                raise ValueError("Caller-supplied effective time is required")
            return _instant(effective_at)
        if not immediate_effect or effective_at is not None:
            raise ValueError("Immediate-effect command is required")
        return _instant(self.clock())

    def _registration_time(self, effective_at):
        registered_at = _instant(self.clock())
        if registered_at == effective_at:
            raise ValueError("registered_at must remain distinct from effective_at")
        return registered_at

    def _insert_event(
        self, connection, event_id, authority_id, authority_version, event_type,
        actor_reference, reason, registered_at, effective_at, effective_at_source,
        effective_at_provenance, successor_authority_id=None,
        successor_authority_version=None,
    ):
        connection.execute(
            "INSERT INTO authority_event ("
            "event_id, authority_id, authority_version, event_type, actor_reference, "
            "reason, successor_authority_id, successor_authority_version, "
            "registered_at, effective_at, effective_at_source, effective_at_provenance"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event_id, authority_id, authority_version, event_type,
                actor_reference, reason, successor_authority_id,
                successor_authority_version, registered_at, effective_at,
                effective_at_source, effective_at_provenance,
            ),
        )

    def _validate_schema_a_inputs(
        self, content_hash, artifact_bytes, artifact_locator_reference,
        verification_provenance, algorithm_id, verification_contract_version,
    ):
        if artifact_bytes is None:
            raise SchemaAArtifactVerificationError(
                "MISSING_ARTIFACT_BYTES", "Exact artifact bytes are required"
            )
        if not isinstance(artifact_bytes, (bytes, bytearray, memoryview)):
            raise SchemaAArtifactVerificationError(
                "MISSING_ARTIFACT_BYTES", "Artifact bytes must be bytes-like"
            )
        if not _canonical_digest(content_hash):
            raise SchemaAArtifactVerificationError(
                "MALFORMED_EXPECTED_DIGEST", "Expected digest is not canonical lowercase hex"
            )
        if algorithm_id != SCHEMA_A_ALGORITHM_ID:
            raise SchemaAArtifactVerificationError(
                "UNSUPPORTED_ALGORITHM", "Unsupported Schema A digest algorithm"
            )
        if verification_contract_version != SCHEMA_A_VERIFICATION_CONTRACT_VERSION:
            raise SchemaAArtifactVerificationError(
                "UNSUPPORTED_VERIFICATION_CONTRACT",
                "Unsupported Schema A verification contract",
            )
        if not isinstance(artifact_locator_reference, str) or not artifact_locator_reference.strip():
            raise SchemaAArtifactVerificationError(
                "PUBLICATION_PROOF_INCOMPLETE", "Artifact locator reference is required"
            )
        if not isinstance(verification_provenance, str) or not verification_provenance.strip():
            raise SchemaAArtifactVerificationError(
                "PUBLICATION_PROOF_INCOMPLETE", "Verification provenance is required"
            )
        actual = hashlib.sha256(bytes(artifact_bytes)).hexdigest()
        if actual != content_hash:
            raise SchemaAArtifactVerificationError(
                "DIGEST_MISMATCH", "Artifact bytes do not match expected digest"
            )

    def _verification_time(self, verified_at):
        try:
            return _instant(verified_at if verified_at is not None else self.clock())
        except ValueError as exc:
            raise SchemaAArtifactVerificationError(
                "INVALID_VERIFIED_AT", "Verification time must be timezone-aware"
            ) from exc

    def _map_schema_a_storage_error(self, exc):
        message = str(exc)
        if "authority_artifact_verification" in message and "UNIQUE" in message.upper():
            reason = "DUPLICATE_VERIFICATION"
        elif "authority_artifact_binding" in message or "FOREIGN KEY" in message.upper():
            reason = "BINDING_MISMATCH"
        elif "authority_artifact_verification" in message:
            reason = "VERIFICATION_STORAGE_FAILURE"
        elif "authority_artifact" in message:
            reason = "ARTIFACT_STORAGE_FAILURE"
        else:
            reason = "UNEXPECTED_VERIFICATION_FAILURE"
        return SchemaAArtifactVerificationError(reason, "Schema A storage operation blocked", diagnostic=message)

    def _create_authority_in_transaction(
        self, connection, origin_locator, content_hash, context_revision_id,
        parameter_reference, effective_from, effective_until, authority_id,
        authority_version, actor_reference, reason, effective_at,
        effective_at_source, effective_at_provenance, registered_at,
        artifact_bytes, artifact_locator_reference, artifact_id,
        artifact_version, verification_provenance, artifact_registered_at,
        verified_at, algorithm_id, verification_contract_version,
        artifact_is_existing=False,
    ):
        start = _instant(effective_from)
        end = _instant(effective_until) if effective_until else None
        if end and end <= start:
            raise ValueError("Invalid authority interval")
        raw = bytes(artifact_bytes)
        digest = hashlib.sha256(raw).hexdigest()
        if artifact_is_existing:
            stored = connection.execute(
                "SELECT artifact_locator_reference,artifact_bytes,artifact_digest,"
                "digest_algorithm FROM authority_artifact WHERE artifact_id=? "
                "AND artifact_version=?", (artifact_id, artifact_version)
            ).fetchone()
            if stored is None or stored[0] != artifact_locator_reference or stored[1] != raw \
                    or stored[2] != digest or stored[3] != SCHEMA_A_ALGORITHM_ID:
                raise SchemaAArtifactVerificationError(
                    "BINDING_MISMATCH", "Existing artifact binding does not match"
                )
        else:
            connection.execute(
                "INSERT INTO authority_artifact VALUES (?,?,?,?,?,?,?)",
                (artifact_id, artifact_version, artifact_locator_reference, raw, digest,
                 SCHEMA_A_ALGORITHM_ID, artifact_registered_at),
            )
        self._schema_a_checkpoint("after_artifact")
        connection.execute(
            "INSERT INTO governed_authority "
            "(authority_id, authority_version, origin_locator, content_hash, created_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (authority_id, authority_version, origin_locator, content_hash, registered_at),
        )
        connection.execute(
            "INSERT INTO authority_scope "
            "(authority_id, authority_version, context_revision_id, parameter_reference) "
            "VALUES (?, ?, ?, ?)",
            (authority_id, authority_version, context_revision_id, parameter_reference),
        )
        self._schema_a_checkpoint("after_authority_registration")
        connection.execute(
            "INSERT INTO authority_temporal_boundary "
            "(authority_id, authority_version, effective_from, effective_until) "
            "VALUES (?, ?, ?, ?)",
            (authority_id, authority_version, start, end),
        )
        connection.execute("INSERT INTO authority_artifact_binding VALUES (?,?,?,?)",
            (authority_id, authority_version, artifact_id, artifact_version))
        self._schema_a_checkpoint("after_binding")
        connection.execute("INSERT INTO authority_artifact_verification VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (f"{authority_id}:verification:{artifact_version}", authority_id, authority_version,
             artifact_id, artifact_version, algorithm_id, verification_contract_version,
             content_hash, digest, "VERIFIED", verified_at, verification_provenance))
        self._schema_a_checkpoint("after_verification")
        connection.execute(
            "INSERT INTO authority_state "
            "(authority_id, authority_version, status, state_changed_at, last_event_id) "
            "VALUES (?, ?, 'PUBLISHED', ?, NULL)",
            (authority_id, authority_version, registered_at),
        )
        self._schema_a_checkpoint("before_publication")
        self._insert_event(
            connection, self.identifiers.new("event"), authority_id,
            authority_version, "PUBLISHED", actor_reference, reason,
            registered_at, effective_at, effective_at_source,
            effective_at_provenance,
        )
        return GovernedAuthority(
            authority_id, authority_version, origin_locator, content_hash,
            registered_at, context_revision_id, parameter_reference, start, end,
            "PUBLISHED",
        )

    def create_authority(
        self, origin_locator, content_hash, context_revision_id,
        parameter_reference, effective_from, effective_until=None, authority_id=None,
        authority_version=1, actor_reference="system", reason="published",
        *, effective_at=None, effective_at_source=None,
        effective_at_provenance=None, immediate_effect=False, artifact_bytes=None,
        artifact_locator_reference=None, artifact_id=None, artifact_version=1,
        verification_provenance=None, verified_at=None,
        algorithm_id=SCHEMA_A_ALGORITHM_ID,
        verification_contract_version=SCHEMA_A_VERIFICATION_CONTRACT_VERSION,
    ):
        if not all((origin_locator, content_hash, context_revision_id,
                    parameter_reference, actor_reference, reason)):
            raise ValueError("Authority fields are required")
        effective = self._effective_time(
            effective_at, effective_at_source, effective_at_provenance,
            immediate_effect,
        )
        self._validate_schema_a_inputs(
            content_hash, artifact_bytes, artifact_locator_reference,
            verification_provenance, algorithm_id, verification_contract_version,
        )
        raw = bytes(artifact_bytes)
        artifact_registered = _instant(self.clock())
        registered = self._registration_time(effective)
        verification_time = self._verification_time(verified_at)
        aid = authority_id or self.identifiers.new("authority")
        artifact_id = artifact_id or f"{aid}:artifact:{artifact_version}"
        try:
            with self.repository.transaction() as connection:
                return self._create_authority_in_transaction(
                    connection, origin_locator, content_hash, context_revision_id,
                    parameter_reference, effective_from, effective_until, aid,
                    authority_version, actor_reference, reason, effective,
                    effective_at_source, effective_at_provenance, registered,
                    raw, artifact_locator_reference, artifact_id, artifact_version,
                    verification_provenance, artifact_registered, verification_time,
                    algorithm_id, verification_contract_version,
                )
        except sqlite3.Error as exc:
            raise self._map_schema_a_storage_error(exc) from exc

    def activate(
        self, authority_id, authority_version, actor_reference="system",
        reason="activated", *, effective_at=None, effective_at_source=None,
        effective_at_provenance=None, immediate_effect=False,
    ):
        return self._transition(
            authority_id, authority_version, "ACTIVE", actor_reference, reason,
            effective_at=effective_at, effective_at_source=effective_at_source,
            effective_at_provenance=effective_at_provenance,
            immediate_effect=immediate_effect,
        )

    def verify_authority_artifact(
        self, authority_id, authority_version, artifact_bytes,
        artifact_locator_reference, verification_provenance, *,
        artifact_id=None, artifact_version=1, verified_at=None,
        algorithm_id=SCHEMA_A_ALGORITHM_ID,
        verification_contract_version=SCHEMA_A_VERIFICATION_CONTRACT_VERSION,
    ):
        """Record explicit Schema A proof for an existing authority."""
        try:
            with self.repository.transaction() as connection:
                authority = connection.execute(
                    "SELECT content_hash FROM governed_authority "
                    "WHERE authority_id=? AND authority_version=?",
                    (authority_id, authority_version),
                ).fetchone()
                if authority is None:
                    raise SchemaAArtifactVerificationError(
                        "BINDING_MISMATCH", "Authority identity is not resolvable"
                    )
                self._validate_schema_a_inputs(
                    authority[0], artifact_bytes, artifact_locator_reference,
                    verification_provenance, algorithm_id,
                    verification_contract_version,
                )
                if connection.execute(
                    "SELECT 1 FROM authority_artifact_verification "
                    "WHERE authority_id=? AND authority_version=? "
                    "AND verification_contract_version=?",
                    (authority_id, authority_version, verification_contract_version),
                ).fetchone():
                    raise SchemaAArtifactVerificationError(
                        "DUPLICATE_VERIFICATION", "Verification already exists"
                    )
                artifact_id = artifact_id or f"{authority_id}:artifact:{artifact_version}"
                raw = bytes(artifact_bytes)
                existing_artifact = connection.execute(
                    "SELECT artifact_locator_reference,artifact_bytes,artifact_digest,"
                    "digest_algorithm FROM authority_artifact WHERE artifact_id=? "
                    "AND artifact_version=?", (artifact_id, artifact_version)
                ).fetchone()
                if existing_artifact is None:
                    connection.execute(
                        "INSERT INTO authority_artifact VALUES (?,?,?,?,?,?,?)",
                        (artifact_id, artifact_version, artifact_locator_reference, raw,
                         hashlib.sha256(raw).hexdigest(), SCHEMA_A_ALGORITHM_ID,
                         _instant(self.clock())),
                    )
                elif existing_artifact != (
                    artifact_locator_reference, raw, hashlib.sha256(raw).hexdigest(),
                    SCHEMA_A_ALGORITHM_ID,
                ):
                    raise SchemaAArtifactVerificationError(
                        "BINDING_MISMATCH", "Existing artifact identity does not match bytes"
                    )
                connection.execute(
                    "INSERT INTO authority_artifact_binding VALUES (?,?,?,?)",
                    (authority_id, authority_version, artifact_id, artifact_version),
                )
                connection.execute(
                    "INSERT INTO authority_artifact_verification VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (f"{authority_id}:verification:{artifact_version}", authority_id,
                     authority_version, artifact_id, artifact_version, algorithm_id,
                     verification_contract_version, authority[0],
                     hashlib.sha256(raw).hexdigest(), "VERIFIED",
                     self._verification_time(verified_at), verification_provenance),
                )
        except SchemaAArtifactVerificationError:
            raise
        except sqlite3.Error as exc:
            raise self._map_schema_a_storage_error(exc) from exc
        return self.repository.fetch_authority_artifact_verification(
            authority_id, authority_version, verification_contract_version
        )

    def create_applicability(self, authority_id, authority_version, context_revision_id,
                             parameter_reference, effective_from, actor_reference, reason):
        if not all((authority_id, context_revision_id, parameter_reference,
                    actor_reference, reason)):
            raise ValueError("Applicability fields are required")
        start = _instant(effective_from)
        aid = self.identifiers.new("aps_applicability")
        now = _instant(self.clock())
        with self.repository.transaction() as c:
            if not c.execute(
                "SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?",
                (authority_id, authority_version),
            ).fetchone():
                raise ValueError("Unmapped authority")
            overlap = c.execute(
                "SELECT 1 FROM authority_applicability_temporal "
                "WHERE context_revision_id=? AND parameter_reference=? "
                "AND effective_from<=? "
                "AND (terminal_effective_at IS NULL OR ? < terminal_effective_at)",
                (context_revision_id, parameter_reference, start, start),
            ).fetchone()
            if overlap:
                raise ValueError("Applicability overlap blocked")
            c.execute(
                "INSERT INTO authority_applicability VALUES (?,?,?,?,?,?,?)",
                (aid, authority_id, authority_version, context_revision_id,
                 parameter_reference, start, now),
            )
            c.execute(
                "INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)",
                (self.identifiers.new("event"), aid, "PUBLISHED", start, now,
                 actor_reference, reason, None),
            )
        return GovernedApplicability(
            aid, authority_id, authority_version, context_revision_id,
            parameter_reference, start, now,
        )

    def resolve_applicability(self, context_revision_id, parameter_reference, measured_at):
        instant = _instant(measured_at)
        with self.repository._optional_connection(None) as c:
            rows = c.execute(
                "SELECT applicability_id,authority_id,authority_version,"
                "context_revision_id,parameter_reference,effective_from "
                "FROM authority_applicability_temporal "
                "WHERE context_revision_id=? AND parameter_reference=? "
                "AND effective_from<=? "
                "AND (terminal_effective_at IS NULL OR ?<terminal_effective_at)",
                (context_revision_id, parameter_reference, instant, instant),
            ).fetchall()
        if len(rows) != 1:
            raise ValueError("Applicability resolution blocked")
        return GovernedApplicability(*rows[0], "")

    def revoke_applicability(self, applicability_id, effective_at, actor_reference, reason):
        return self._terminal_applicability(
            applicability_id, "REVOKED", effective_at, actor_reference, reason, None,
        )

    def supersede_applicability(self, predecessor_id, authority_id, authority_version,
                                context_revision_id, parameter_reference, effective_from,
                                actor_reference, reason):
        if not all((authority_id, context_revision_id, parameter_reference,
                    actor_reference, reason)):
            raise ValueError("Applicability fields are required")
        start = _instant(effective_from)
        now = _instant(self.clock())
        with self.repository.transaction() as c:
            pred = c.execute(
                "SELECT authority_id,authority_version,context_revision_id,"
                "parameter_reference,effective_from FROM authority_applicability "
                "WHERE applicability_id=?", (predecessor_id,),
            ).fetchone()
            if not pred:
                raise ValueError("Invalid predecessor or backdating")
            state = c.execute(
                "SELECT state FROM authority_applicability_state WHERE applicability_id=?",
                (predecessor_id,),
            ).fetchone()
            if not state or state[0] != "ACTIVE":
                raise ValueError("Predecessor is not ACTIVE")
            if start < pred[4]:
                raise ValueError("Invalid predecessor or backdating")
            if not c.execute(
                "SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?",
                (authority_id, authority_version),
            ).fetchone():
                raise ValueError("Unmapped authority")
            successor = self.identifiers.new("aps_applicability")
            predecessor_event = self.identifiers.new("event")
            successor_event = self.identifiers.new("event")
            c.execute(
                "INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)",
                (predecessor_event, predecessor_id, "SUPERSEDED", start, now,
                 actor_reference, reason, successor),
            )
            if self._test_supersession_failure_hook is not None:
                self._test_supersession_failure_hook("after_predecessor_event")
            c.execute(
                "INSERT INTO authority_applicability VALUES (?,?,?,?,?,?,?)",
                (successor, authority_id, authority_version, context_revision_id,
                 parameter_reference, start, now),
            )
            if self._test_supersession_failure_hook is not None:
                self._test_supersession_failure_hook("after_successor_applicability")
            c.execute(
                "INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)",
                (successor_event, successor, "PUBLISHED", start, now,
                 actor_reference, reason, None),
            )
        return successor

    def _terminal_applicability(self, applicability_id, event_type, effective_at,
                                actor_reference, reason, successor):
        at = _instant(effective_at)
        now = _instant(self.clock())
        with self.repository.transaction() as c:
            row = c.execute(
                "SELECT effective_from,context_revision_id,parameter_reference,"
                "authority_id,authority_version FROM authority_applicability "
                "WHERE applicability_id=?", (applicability_id,),
            ).fetchone()
            if not row or at < row[0] or not row[1] or not row[2]:
                raise ValueError("Invalid terminal time or applicability linkage")
            authority = c.execute(
                "SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?",
                (row[3], row[4]),
            ).fetchone()
            if not authority:
                raise ValueError("Unmapped authority")
            affected = c.execute(
                "SELECT 1 FROM governed_evaluation e "
                "JOIN governed_measurement m ON m.measurement_id=e.measurement_id "
                "WHERE m.context_revision_id=? AND m.parameter_reference=? "
                "AND m.measured_at>=? AND m.measured_at<? LIMIT 1",
                (row[1], row[2], row[0], at),
            ).fetchone()
            if affected:
                raise ValueError("Retroactive terminal event affects persisted evaluation")
            try:
                c.execute(
                    "INSERT INTO authority_applicability_event VALUES (?,?,?,?,?,?,?,?)",
                    (self.identifiers.new("event"), applicability_id, event_type,
                     at, now, actor_reference, reason, successor),
                )
                if self._test_failure_hook is not None:
                    self._test_failure_hook()
            except Exception as error:
                raise ValueError("Applicability lifecycle transition blocked") from error
        return event_type

    def revoke(
        self, authority_id, authority_version, actor_reference, reason, *,
        effective_at=None, effective_at_source=None, effective_at_provenance=None,
        immediate_effect=False,
    ):
        return self._transition(
            authority_id, authority_version, "REVOKED", actor_reference, reason,
            effective_at=effective_at, effective_at_source=effective_at_source,
            effective_at_provenance=effective_at_provenance,
            immediate_effect=immediate_effect,
        )

    def _transition(
        self, aid, version, status, actor, reason, *, effective_at,
        effective_at_source, effective_at_provenance, immediate_effect,
    ):
        if status not in {"ACTIVE", "REVOKED"}:
            raise ValueError("Invalid authority transition")
        if not actor or not reason:
            raise ValueError("Lifecycle actor and reason are required")
        effective = self._effective_time(
            effective_at, effective_at_source, effective_at_provenance,
            immediate_effect,
        )
        registered = self._registration_time(effective)
        with self.repository.transaction() as c:
            if not c.execute(
                "SELECT 1 FROM authority_state WHERE authority_id=? AND authority_version=?",
                (aid, version),
            ).fetchone():
                raise ValueError("Unknown authority")
            self._insert_event(
                c, self.identifiers.new("event"), aid, version, status, actor,
                reason, registered, effective, effective_at_source,
                effective_at_provenance,
            )
        return status

    def supersede(self, predecessor_id, predecessor_version, **successor):
        successor.setdefault("authority_version", predecessor_version + 1)
        actor = successor.setdefault("actor_reference", "system")
        reason = successor.setdefault("reason", "superseded")
        effective_at = successor.pop("effective_at", None)
        effective_source = successor.pop("effective_at_source", None)
        effective_provenance = successor.pop("effective_at_provenance", None)
        immediate_effect = successor.pop("immediate_effect", False)
        if "effective_from" not in successor:
            raise ValueError("Successor effective_from is required")
        effective = self._effective_time(
            effective_at, effective_source, effective_provenance, immediate_effect,
        )
        predecessor_registered = self._registration_time(effective)
        successor_id = successor.get("authority_id") or self.identifiers.new("authority")
        successor["authority_id"] = successor_id
        successor_registered = self._registration_time(effective)
        successor_verification_time = self._verification_time(None)
        with self.repository.transaction() as c:
            row = c.execute(
                "SELECT origin_locator,content_hash,context_revision_id,"
                "parameter_reference,effective_until FROM governed_authority a "
                "JOIN authority_scope s USING(authority_id,authority_version) "
                "JOIN authority_temporal_boundary b USING(authority_id,authority_version) "
                "WHERE a.authority_id=? AND a.authority_version=?",
                (predecessor_id, predecessor_version),
            ).fetchone()
            if not row:
                raise ValueError("Unknown predecessor")
            state = c.execute(
                "SELECT status FROM authority_state WHERE authority_id=? AND authority_version=?",
                (predecessor_id, predecessor_version),
            ).fetchone()
            if not state or state[0] != "ACTIVE":
                raise ValueError("Predecessor is not ACTIVE")
            artifact = c.execute(
                "SELECT aa.artifact_id,aa.artifact_version,aa.artifact_locator_reference,"
                "aa.artifact_bytes,aa.registered_at FROM authority_artifact aa "
                "JOIN authority_artifact_binding ab ON ab.artifact_id=aa.artifact_id "
                "AND ab.artifact_version=aa.artifact_version "
                "WHERE ab.authority_id=? AND ab.authority_version=?",
                (predecessor_id, predecessor_version),
            ).fetchone()
            if artifact is None:
                raise SchemaAArtifactVerificationError(
                    "PUBLICATION_PROOF_INCOMPLETE", "Successor publication requires artifact proof"
                )
            if self._test_supersession_failure_hook is not None:
                self._test_supersession_failure_hook("before_successor_persistence")
            successor_authority = self._create_authority_in_transaction(
                c, row[0], row[1], row[2], row[3], successor["effective_from"],
                row[4], successor_id, successor["authority_version"], actor, reason,
                effective, effective_source, effective_provenance, successor_registered,
                artifact[3], artifact[2], artifact[0], artifact[1],
                "supersession:" + reason, artifact[4], successor_verification_time,
                SCHEMA_A_ALGORITHM_ID, SCHEMA_A_VERIFICATION_CONTRACT_VERSION, True,
            )
            if self._test_supersession_failure_hook is not None:
                self._test_supersession_failure_hook("after_successor_published")
                self._test_supersession_failure_hook("before_predecessor_terminal_event")
            self._insert_event(
                c, self.identifiers.new("event"), predecessor_id,
                predecessor_version, "SUPERSEDED", actor, reason,
                predecessor_registered, effective, effective_source,
                effective_provenance, successor_id, successor["authority_version"],
            )
        return successor_authority

    def resolve_historical_authority(self, authority_id, authority_version,
                                     measured_at, context_revision_id,
                                     parameter_reference, connection=None):
        measured = _instant(measured_at)
        with self.repository._optional_connection(connection) as c:
            authority = c.execute(
                "SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?",
                (authority_id, authority_version),
            ).fetchone()
            if authority is None:
                return HistoricalAuthorityResolution(
                    "UNDEFINED", "AUTHORITY_PROVENANCE_INCOMPLETE_OR_INVALID",
                )
            if len(self.repository.fetch_authority_scope(
                authority_id, authority_version, context_revision_id,
                parameter_reference, c,
            )) != 1:
                return HistoricalAuthorityResolution(
                    "UNDEFINED", "AUTHORITY_PROVENANCE_INCOMPLETE_OR_INVALID",
                )
            boundary = self.repository.fetch_authority_boundary(
                authority_id, authority_version, c,
            )
            if not boundary or not _canonical_text(boundary[0]) or (
                boundary[1] is not None and not _canonical_text(boundary[1])
            ):
                return HistoricalAuthorityResolution(
                    "UNDEFINED", "AUTHORITY_PROVENANCE_INCOMPLETE_OR_INVALID",
                )
            events = self.repository.fetch_authority_events(
                authority_id, authority_version, c,
            )
            if not events:
                return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_INCOMPLETE")
            if any(
                event.event_type not in EVENT_TYPES
                or not _canonical_text(event.effective_at)
                or event.effective_at_source not in EFFECTIVE_TIME_SOURCES
                or not event.effective_at_provenance
                for event in events
            ):
                return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_INCOMPLETE")
            if len({event.effective_at for event in events}) != len(events):
                return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_AMBIGUOUS")
            if events[0].event_type != "PUBLISHED":
                return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_MALFORMED")
            active_seen = False
            terminal_seen = False
            for index, event in enumerate(events):
                if event.event_type == "PUBLISHED" and index != 0:
                    return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_MALFORMED")
                if event.event_type == "ACTIVE":
                    if active_seen or terminal_seen:
                        return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_MALFORMED")
                    active_seen = True
                if event.event_type in TERMINAL_EVENT_TYPES:
                    if not active_seen or terminal_seen or index != len(events) - 1:
                        return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_MALFORMED")
                    if event.event_type == "SUPERSEDED":
                        if event.successor_authority_id is None or event.successor_authority_version is None:
                            return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_INCOMPLETE")
                        successor = c.execute(
                            "SELECT 1 FROM governed_authority WHERE authority_id=? AND authority_version=?",
                            (event.successor_authority_id, event.successor_authority_version),
                        ).fetchone()
                        if successor is None:
                            return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_INCOMPLETE")
                    terminal_seen = True
            if measured < boundary[0] or (
                boundary[1] is not None and measured >= boundary[1]
            ):
                return HistoricalAuthorityResolution(
                    "TECHNICALLY_INELIGIBLE", "AUTHORITY_OUT_OF_WINDOW",
                )
            selected = [event for event in events if event.effective_at <= measured]
            if not selected:
                return HistoricalAuthorityResolution("UNDEFINED", "AUTHORITY_HISTORY_INCOMPLETE")
            return HistoricalAuthorityResolution("RESOLVED", event=selected[-1])
