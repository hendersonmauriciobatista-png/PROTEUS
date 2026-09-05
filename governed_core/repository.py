"""SQLite persistence boundary for governed Core V1."""

import hashlib
import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .measurement_models import (
    APSMemberAuthorizationResolution,
    AuthorizationBasisResolution,
    GovernedMeasurement,
    GovernedEvaluation,
)
from .authority_models import (
    AuthorityEvent, GovernedAuthorityArtifact, AuthorityArtifactBinding,
    AuthorityArtifactVerification,
)
from .models import APSReference, GovernedMonitoringPoint, PointContextRevision
from .rule_models import GovernedRule
from .geo_models import GeoReference, LocationProvenance


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_PATH = BASE_DIR / "data" / "governed_core_v1.sqlite3"
MIGRATIONS_DIR = BASE_DIR / "migrations"
EXPECTED_MIGRATION_019_SHA256 = "8db22fa64588a01aef54978066fbd459794dd8710317ec4b99882a52608ffd36"


class GovernedCoreError(RuntimeError):
    pass


class GovernedReferenceError(GovernedCoreError):
    pass


class MeasurementResolutionError(GovernedReferenceError):
    reason_code = "MEASUREMENT_UNRESOLVED"


class TemporalContextResolutionError(GovernedReferenceError):
    reason_code = "TEMPORAL_CONTEXT_UNRESOLVED"


class TemporalAPSResolutionError(GovernedReferenceError):
    reason_code = "APS_MEMBER_AUTHORIZATION_UNRESOLVED"


class GovernedConflictError(GovernedCoreError):
    pass


class GovernedCoreRepository:
    def __init__(self, path=DEFAULT_DATABASE_PATH, migrations_dir=MIGRATIONS_DIR):
        self.path = Path(path)
        self.migrations_dir = Path(migrations_dir)

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = self._connect()
        try:
            self._apply_migrations(connection)
        finally:
            connection.close()
        return self

    @contextmanager
    def transaction(self):
        connection = self._connect()
        try:
            self._apply_migrations(connection)
            self._assert_governed_connection(connection)
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            self._validate_active_points(connection)
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def fetch_point(self, point_id, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT point_id, project_reference, display_name, status, "
                "current_context_revision_id, external_station_reference "
                "FROM governed_monitoring_point WHERE point_id = ?",
                (point_id,),
            ).fetchone()
        if row is None:
            raise GovernedReferenceError(f"Ponto governado nao resolvivel: {point_id}")
        return GovernedMonitoringPoint(*row)

    def fetch_point_by_external_reference(
        self, project_reference, external_station_reference, connection=None
    ):
        if not external_station_reference or not external_station_reference.strip():
            raise ValueError("Referencia externa da estacao deve ser nao vazia.")
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT point_id, project_reference, display_name, status, "
                "current_context_revision_id, external_station_reference "
                "FROM governed_monitoring_point "
                "WHERE project_reference = ? AND external_station_reference = ?",
                (project_reference, external_station_reference),
            ).fetchall()
        if not rows:
            return None
        if len(rows) != 1:
            raise GovernedConflictError(
                "Referencia externa da estacao nao e univoca no projeto."
            )
        return GovernedMonitoringPoint(*rows[0])

    def list_active_points(self, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT point_id, project_reference, display_name, status, "
                "current_context_revision_id, external_station_reference "
                "FROM governed_monitoring_point WHERE status = 'ACTIVE' "
                "ORDER BY project_reference, point_id"
            ).fetchall()
        return tuple(GovernedMonitoringPoint(*row) for row in rows)

    def fetch_context_revision(self, context_revision_id, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT context_revision_id, revision, point_id, purpose, water_context, "
                "point_type, geo_reference, created_at, effective_from, effective_until FROM point_context_revision "
                "WHERE context_revision_id = ?",
                (context_revision_id,),
            ).fetchone()
        if row is None:
            raise GovernedReferenceError(
                f"Revisao contextual nao resolvivel: {context_revision_id}"
            )
        return PointContextRevision(*row)

    def fetch_geo_reference(self, context_revision_id, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT geo_reference_id, context_revision_id, availability_state, "
                "latitude, longitude, crs_identifier, location_provenance_id, "
                "state_reason, registered_at FROM geo_reference "
                "WHERE context_revision_id = ?",
                (context_revision_id,),
            ).fetchone()
        return None if row is None else GeoReference(*row)

    def fetch_location_provenance(self, provenance_id, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT provenance_id, source_reference, source_coordinate_1_raw, "
                "source_coordinate_2_raw, source_coordinate_1_numeric, "
                "source_coordinate_2_numeric, source_axis_order, source_crs_identifier, "
                "acquisition_method, captured_at, captured_at_status, "
                "transformation_method, transformation_parameters, "
                "transformation_provenance, accuracy_or_uncertainty_kind, "
                "accuracy_or_uncertainty_value, accuracy_or_uncertainty_unit, "
                "registered_at FROM location_provenance WHERE provenance_id = ?",
                (provenance_id,),
            ).fetchone()
        return None if row is None else LocationProvenance(*row)

    def insert_location_provenance(self, provenance, connection):
        self._assert_governed_connection(connection)
        connection.execute(
            "INSERT INTO location_provenance VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            tuple(provenance.__dict__.values()),
        )

    def insert_geo_reference(self, geo_reference, connection):
        self._assert_governed_connection(connection)
        connection.execute(
            "INSERT INTO geo_reference VALUES (?,?,?,?,?,?,?,?,?)",
            tuple(geo_reference.__dict__.values()),
        )

    def fetch_current_context(self, point_id, connection=None):
        point = self.fetch_point(point_id, connection)
        if not point.current_context_revision_id:
            raise GovernedReferenceError(f"Ponto sem revisao contextual atual: {point_id}")
        revision = self.fetch_context_revision(point.current_context_revision_id, connection)
        if revision.point_reference != point.point_id:
            raise GovernedReferenceError(
                f"Referencia contextual cruzada para o ponto: {point_id}"
            )
        return revision

    def fetch_aps_version(self, reference, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT context_revision_id FROM aps_version WHERE set_id = ? AND version = ?",
                (reference.set_id, reference.version),
            ).fetchone()
        if row is None:
            raise GovernedReferenceError(
                f"Versao APS nao resolvivel: {reference.set_id}/{reference.version}"
            )
        return row[0]

    def fetch_applicable_aps(self, context_revision_id, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT set_id, version FROM aps_applicability WHERE context_revision_id = ?",
                (context_revision_id,),
            ).fetchall()
        if len(rows) != 1:
            raise GovernedReferenceError(
                f"Contexto exige exatamente uma APS aplicavel; encontradas {len(rows)}"
            )
        return APSReference(rows[0][0], rows[0][1])

    def validate_authorization_chain(self, reference, connection=None):
        with self._optional_connection(connection) as active:
            members = active.execute(
                "SELECT parameter_reference FROM aps_member WHERE set_id = ? AND version = ?",
                (reference.set_id, reference.version),
            ).fetchall()
            if not members:
                raise GovernedReferenceError("Versao APS sem membros autorizados.")
            for member in members:
                bases = active.execute(
                    "SELECT basis_id FROM member_authorization_basis "
                    "WHERE set_id = ? AND version = ? AND parameter_reference = ?",
                    (reference.set_id, reference.version, member[0]),
                ).fetchall()
                if not bases:
                    raise GovernedReferenceError(
                        f"Membro sem authorization basis: {member[0]}"
                    )
                for basis in bases:
                    authority_count = active.execute(
                        "SELECT COUNT(*) FROM basis_authority WHERE basis_id = ?",
                        (basis[0],),
                    ).fetchone()[0]
                    evidence_count = active.execute(
                        "SELECT COUNT(*) FROM basis_evidence WHERE basis_id = ?",
                        (basis[0],),
                    ).fetchone()[0]
                    if authority_count < 1 or evidence_count < 1:
                        raise GovernedReferenceError(
                            f"Authorization basis com cadeia quebrada: {basis[0]}"
                        )
        return True

    def unresolved_disqualification_ids(self, reference, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT event_id FROM governance_event AS disqualification "
                "WHERE action = 'APS_VERSION_DISQUALIFIED' "
                "AND target_set_id = ? AND target_version = ? "
                "AND NOT EXISTS ("
                "SELECT 1 FROM governance_event_resolution AS resolution "
                "WHERE resolution.disqualification_event_id = disqualification.event_id"
                ")",
                (reference.set_id, reference.version),
            ).fetchall()
        return tuple(row[0] for row in rows)

    def resolve_member_authorization(
        self,
        reference,
        parameter_reference,
        connection=None,
    ):
        with self._optional_connection(connection) as active:
            member = active.execute(
                "SELECT 1 FROM aps_member WHERE set_id = ? AND version = ? "
                "AND parameter_reference = ?",
                (reference.set_id, reference.version, parameter_reference),
            ).fetchone()
            if member is None:
                raise GovernedReferenceError(
                    "Parametro nao pertence a versao APS exata: "
                    f"{reference.set_id}/{reference.version}/{parameter_reference}"
                )
            basis_rows = active.execute(
                "SELECT basis.basis_id FROM member_authorization_basis AS trace "
                "JOIN authorization_basis AS basis "
                "ON basis.basis_id = trace.basis_id "
                "AND basis.set_id = trace.set_id AND basis.version = trace.version "
                "WHERE trace.set_id = ? AND trace.version = ? "
                "AND trace.parameter_reference = ? ORDER BY basis.basis_id",
                (reference.set_id, reference.version, parameter_reference),
            ).fetchall()
            if not basis_rows:
                raise GovernedReferenceError(
                    f"Membro sem authorization basis exata: {parameter_reference}"
                )
            bases = []
            for basis_row in basis_rows:
                basis_id = basis_row[0]
                authorities = tuple(
                    row[0]
                    for row in active.execute(
                        "SELECT authority.authority_reference_id "
                        "FROM basis_authority AS trace "
                        "JOIN authority_reference AS authority "
                        "ON authority.authority_reference_id = trace.authority_reference_id "
                        "WHERE trace.basis_id = ? ORDER BY authority.authority_reference_id",
                        (basis_id,),
                    ).fetchall()
                )
                evidence = tuple(
                    row[0]
                    for row in active.execute(
                        "SELECT evidence.evidence_reference_id "
                        "FROM basis_evidence AS trace "
                        "JOIN evidence_reference AS evidence "
                        "ON evidence.evidence_reference_id = trace.evidence_reference_id "
                        "WHERE trace.basis_id = ? ORDER BY evidence.evidence_reference_id",
                        (basis_id,),
                    ).fetchall()
                )
                if not authorities or not evidence:
                    raise GovernedReferenceError(
                        f"Authorization basis com cadeia quebrada: {basis_id}"
                    )
                bases.append(
                    AuthorizationBasisResolution(basis_id, authorities, evidence)
                )
        return APSMemberAuthorizationResolution(
            reference,
            parameter_reference,
            tuple(bases),
        )

    def fetch_authority_applicability_candidates(
        self, context_revision_id, parameter_reference, measured_at, connection=None
    ):
        """Return all scoped applicability candidates, including their temporal end."""
        with self._optional_connection(connection) as active:
            return tuple(active.execute(
                "SELECT applicability_id, authority_id, authority_version, "
                "context_revision_id, parameter_reference, effective_from, "
                "terminal_effective_at "
                "FROM authority_applicability_temporal "
                "WHERE context_revision_id = ? AND parameter_reference = ? "
                "ORDER BY authority_id, authority_version, applicability_id",
                (context_revision_id, parameter_reference),
            ).fetchall())

    def fetch_authority_applicability_event_ids(
        self, applicability_id, measured_at, connection=None
    ):
        """Return every historical publication event available at measured_at."""
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT event_id FROM authority_applicability_event "
                "WHERE applicability_id = ? AND event_type = 'PUBLISHED' "
                "AND effective_at <= ? ORDER BY effective_at, event_id",
                (applicability_id, measured_at),
            ).fetchall()
        return tuple(row[0] for row in rows)

    def insert_measurement(self, measurement, connection):
        if connection is None:
            raise ValueError("Measurement insert requires an active transaction.")
        connection.execute(
            "INSERT INTO governed_measurement "
            "(measurement_id, point_id, context_revision_id, aps_set_id, aps_version, "
            "parameter_reference, value, measured_at, registered_at, provenance) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                measurement.measurement_id,
                measurement.point_id,
                measurement.context_revision_id,
                measurement.aps_set_id,
                measurement.aps_version,
                measurement.parameter_reference,
                measurement.value,
                measurement.measured_at,
                measurement.registered_at,
                measurement.provenance,
            ),
        )

    def fetch_measurement(self, measurement_id, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT measurement_id, point_id, context_revision_id, aps_set_id, "
                "aps_version, parameter_reference, value, measured_at, registered_at, "
                "provenance FROM governed_measurement WHERE measurement_id = ?",
                (measurement_id,),
            ).fetchone()
        if row is None:
            raise MeasurementResolutionError(
                f"Medicao governada nao resolvivel: {measurement_id}"
            )
        return GovernedMeasurement(*row)

    def list_measurements_by_point(self, point_id, connection=None):
        self.fetch_point(point_id, connection)
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT measurement_id, point_id, context_revision_id, aps_set_id, "
                "aps_version, parameter_reference, value, measured_at, registered_at, provenance "
                "FROM governed_measurement WHERE point_id = ? "
                "ORDER BY measured_at DESC, registered_at DESC, measurement_id DESC",
                (point_id,),
            ).fetchall()
        return tuple(GovernedMeasurement(*row) for row in rows)

    def insert_evaluation(self, evaluation, connection):
        self._assert_governed_connection(connection)
        connection.execute(
            "INSERT INTO governed_evaluation ("
            "evaluation_id, measurement_id, parameter_reference, status, message, "
            "rule_origin, evaluated_at, registered_at, evaluation_engine, "
            "evaluation_engine_version, explanation_data"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(evaluation.__dict__.values()),
        )

    def insert_authority_snapshot(self, snapshot, connection):
        self._assert_governed_connection(connection)
        connection.execute(
            "INSERT INTO governed_evaluation_authority_snapshot ("
            "evaluation_id, authority_id, authority_version, "
            "authority_applicability_id, authority_lifecycle_event_id, "
            "authority_applicability_event_id, verification_id, "
            "authority_gate_status, lifecycle_policy_result, "
            "rule_resolution_outcome, authority_gate_policy_contract_version"
            ") VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            tuple(snapshot),
        )

    def insert_authority_snapshot_basis(self, basis, connection):
        self._assert_governed_connection(connection)
        connection.execute(
            "INSERT INTO governed_evaluation_authority_snapshot_basis ("
            "evaluation_id, basis_id, aps_set_id, aps_version, "
            "parameter_reference"
            ") VALUES (?,?,?,?,?)",
            tuple(basis),
        )

    def fetch_authority_snapshot(self, evaluation_id, connection=None):
        with self._optional_connection(connection) as active:
            return active.execute(
                "SELECT evaluation_id, authority_id, authority_version, "
                "authority_applicability_id, authority_lifecycle_event_id, "
                "authority_applicability_event_id, verification_id, "
                "authority_gate_status, lifecycle_policy_result, "
                "rule_resolution_outcome, authority_gate_policy_contract_version "
                "FROM governed_evaluation_authority_snapshot "
                "WHERE evaluation_id = ?",
                (evaluation_id,),
            ).fetchone()

    def list_authority_snapshot_basis(self, evaluation_id, connection=None):
        with self._optional_connection(connection) as active:
            return tuple(active.execute(
                "SELECT evaluation_id, basis_id, aps_set_id, aps_version, "
                "parameter_reference "
                "FROM governed_evaluation_authority_snapshot_basis "
                "WHERE evaluation_id = ? ORDER BY basis_id",
                (evaluation_id,),
            ).fetchall())

    def insert_authority_artifact(self, artifact, connection):
        connection.execute(
            "INSERT INTO authority_artifact VALUES (?,?,?,?,?,?,?)",
            (artifact.artifact_id, artifact.artifact_version, artifact.artifact_locator_reference,
             artifact.artifact_bytes, artifact.artifact_digest, artifact.digest_algorithm,
             artifact.registered_at),
        )

    def fetch_authority_artifact(self, artifact_id, artifact_version, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT artifact_id,artifact_version,artifact_locator_reference,artifact_bytes,"
                "artifact_digest,digest_algorithm,registered_at FROM authority_artifact "
                "WHERE artifact_id=? AND artifact_version=?", (artifact_id, artifact_version)
            ).fetchone()
        return None if row is None else GovernedAuthorityArtifact(*row)

    def insert_authority_artifact_binding(self, binding, connection):
        connection.execute("INSERT INTO authority_artifact_binding VALUES (?,?,?,?)",
                           (binding.authority_id, binding.authority_version,
                            binding.artifact_id, binding.artifact_version))

    def insert_authority_artifact_verification(self, verification, connection):
        connection.execute("INSERT INTO authority_artifact_verification VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                           tuple(verification.__dict__.values()))

    def fetch_authority_artifact_verification(self, authority_id, authority_version,
                                              contract_version="mcm-authority-artifact-hash/v1",
                                              connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT verification_id,authority_id,authority_version,artifact_id,"
                "artifact_version,algorithm_id,verification_contract_version,"
                "expected_digest,computed_digest,verification_result,verified_at,"
                "verification_provenance FROM authority_artifact_verification "
                "WHERE authority_id=? AND authority_version=? AND verification_contract_version=?",
                (authority_id, authority_version, contract_version)).fetchone()
        return None if row is None else AuthorityArtifactVerification(*row)

    def fetch_authority_scope(self, authority_id, authority_version,
                              context_revision_id, parameter_reference,
                              connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT authority_id, authority_version, context_revision_id, "
                "parameter_reference FROM authority_scope "
                "WHERE authority_id = ? AND authority_version = ? "
                "AND context_revision_id = ? AND parameter_reference = ?",
                (authority_id, authority_version, context_revision_id,
                 parameter_reference),
            ).fetchall()
        return tuple(rows)

    def fetch_authority_boundary(self, authority_id, authority_version,
                                 connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT effective_from, effective_until "
                "FROM authority_temporal_boundary "
                "WHERE authority_id = ? AND authority_version = ?",
                (authority_id, authority_version),
            ).fetchone()
        return row

    def fetch_authority_events(self, authority_id, authority_version,
                               connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT event_id, authority_id, authority_version, event_type, "
                "actor_reference, reason, successor_authority_id, "
                "successor_authority_version, registered_at, effective_at, "
                "effective_at_source, effective_at_provenance "
                "FROM authority_event WHERE authority_id = ? "
                "AND authority_version = ? ORDER BY effective_at, event_id",
                (authority_id, authority_version),
            ).fetchall()
        return tuple(AuthorityEvent(*row) for row in rows)

    def list_evaluations_by_measurement(self, measurement_id, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute("SELECT evaluation_id, measurement_id, parameter_reference, status, message, rule_origin, evaluated_at, registered_at, evaluation_engine, evaluation_engine_version, explanation_data FROM governed_evaluation WHERE measurement_id = ? ORDER BY registered_at, evaluation_id", (measurement_id,)).fetchall()
        return tuple(GovernedEvaluation(*row) for row in rows)

    def fetch_temporal_context(self, point_id, measured_at, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute("SELECT context_revision_id, revision, point_id, purpose, water_context, point_type, geo_reference, created_at, effective_from, effective_until FROM point_context_revision WHERE point_id = ? AND effective_from IS NOT NULL AND effective_from <= ? AND (effective_until IS NULL OR ? < effective_until)", (point_id, measured_at, measured_at)).fetchall()
        if len(rows) != 1:
            raise TemporalContextResolutionError(f"Temporal context resolution requires exactly one match: {point_id}")
        return PointContextRevision(*rows[0])

    def fetch_temporal_aps(self, context_revision_id, measured_at, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute("SELECT aps_set_id, aps_version FROM aps_temporal_applicability WHERE context_revision_id = ? AND effective_from <= ? AND (effective_until IS NULL OR ? < effective_until)", (context_revision_id, measured_at, measured_at)).fetchall()
        if len(rows) != 1:
            raise TemporalAPSResolutionError("Temporal APS resolution requires exactly one match")
        return APSReference(*rows[0])

    def fetch_rules(self, context_revision_id, parameter_reference, measured_at, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute(
                "SELECT rule_id, rule_version, parameter_reference, context_revision_id, "
                "effective_from, effective_until, origin, rule_payload, payload_hash, "
                "authority_reference_ids, evidence_reference_ids FROM governed_rule "
                "WHERE context_revision_id = ? AND parameter_reference = ? "
                "AND effective_from <= ? AND (effective_until IS NULL OR ? < effective_until) "
                "ORDER BY rule_id, rule_version",
                (context_revision_id, parameter_reference, measured_at, measured_at),
            ).fetchall()
        return tuple(GovernedRule(*row[:9], tuple(json.loads(row[9])), tuple(json.loads(row[10]))) for row in rows)

    def insert_rule(self, rule, connection):
        connection.execute(
            "INSERT INTO governed_rule VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (rule.rule_id, rule.rule_version, rule.parameter_reference, rule.context_revision_id,
             rule.effective_from, rule.effective_until, rule.origin, rule.rule_payload,
             rule.payload_hash, json.dumps(rule.authority_reference_ids), json.dumps(rule.evidence_reference_ids)),
        )

    def _connect(self):
        connection = sqlite3.connect(self.path)
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        connection.execute("PRAGMA synchronous = FULL")
        return connection

    @staticmethod
    def _assert_governed_connection(connection):
        if connection is None:
            raise ValueError("Governed operation requires an active connection.")
        enabled = connection.execute("PRAGMA foreign_keys").fetchone()[0]
        if enabled != 1:
            raise GovernedConflictError(
                "Governed operation requires PRAGMA foreign_keys = 1."
            )

    @contextmanager
    def _optional_connection(self, connection):
        if connection is not None:
            yield connection
            return
        active = self._connect()
        try:
            self._apply_migrations(active)
            yield active
        finally:
            active.close()

    def _preflight_migration_020(self, connection):
        """Reject incompatible persisted state before executing migration 020."""
        tables = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        if "schema_migration" not in tables or "point_context_revision" not in tables:
            raise GovernedConflictError(
                "Migration 020 preflight failed: required table is missing."
            )
        required = {
            "context_revision_id", "point_id", "revision", "purpose",
            "water_context", "point_type", "geo_reference", "created_at",
            "effective_from", "effective_until",
        }
        present = {
            row[1] for row in connection.execute(
                "PRAGMA table_info(point_context_revision)"
            )
        }
        if not required.issubset(present):
            raise GovernedConflictError(
                "Migration 020 preflight failed: required column is missing."
            )
        if "geo_reference_id" in present:
            raise GovernedConflictError(
                "Migration 020 preflight failed: GEO link column already exists."
            )
        try:
            connection.execute(
                "SELECT context_revision_id, geo_reference FROM point_context_revision LIMIT 0"
            )
        except sqlite3.Error as error:
            raise GovernedConflictError(
                "Migration 020 preflight failed: legacy GEO field is unreadable."
            ) from error
        occupied = {
            "geo_reference", "location_provenance",
        }
        objects = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE name IN (?, ?) AND type IN ('table','view','index','trigger')",
                tuple(occupied),
            )
        }
        if objects:
            raise GovernedConflictError(
                "Migration 020 preflight failed: normalized GEO name is occupied."
            )
        reserved = {
            "geo_reference_context_unique", "geo_reference_state_lookup",
            "geo_reference_provenance_lookup", "location_provenance_source_lookup",
            "context_geo_link_required", "context_geo_link_immutable",
            "geo_context_link_guard", "location_provenance_immutable_update",
            "location_provenance_immutable_delete", "geo_reference_immutable_update",
            "geo_reference_immutable_delete",
        }
        placeholders = ",".join("?" for _ in reserved)
        if connection.execute(
            f"SELECT 1 FROM sqlite_master WHERE name IN ({placeholders}) LIMIT 1",
            tuple(reserved),
        ).fetchone():
            raise GovernedConflictError(
                "Migration 020 preflight failed: migration object name is occupied."
            )

    def _apply_migrations(self, connection):
        migrations = sorted(self.migrations_dir.glob("*.sql"))
        for migration in migrations:
            sql = migration.read_text(encoding="utf-8")
            checksum = hashlib.sha256(sql.encode("utf-8")).hexdigest()
            table_exists = connection.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'schema_migration'"
            ).fetchone()
            if table_exists:
                applied = connection.execute(
                    "SELECT checksum FROM schema_migration WHERE migration_id = ?",
                    (migration.name,),
                ).fetchone()
                if applied:
                    if applied[0] != checksum:
                        raise GovernedConflictError(
                            f"Checksum de migracao divergente: {migration.name}"
                        )
                    continue
            try:
                if migration.name.startswith("020_"):
                    self._preflight_migration_020(connection)
                    applied_019 = connection.execute(
                        "SELECT checksum FROM schema_migration WHERE migration_id = ?",
                        ("019_mcm_wq_evaluation_authority_snapshot.sql",),
                    ).fetchone()
                    if not applied_019 or applied_019[0] != EXPECTED_MIGRATION_019_SHA256:
                        raise GovernedConflictError(
                            "Migration 020 requires the published Migration 019 checksum."
                        )
                if migration.name.startswith("019_"):
                    required = {
                        "governed_authority",
                        "authority_applicability",
                        "authority_event",
                        "authority_artifact_verification",
                    }
                    present = {
                        row[0]
                        for row in connection.execute(
                            "SELECT name FROM sqlite_master WHERE type = 'table'"
                        )
                    }
                    if not required.issubset(present):
                        raise GovernedConflictError(
                            "Migration 019 requires the complete Schema A infrastructure."
                        )
                connection.executescript("BEGIN IMMEDIATE;\n" + sql)
                connection.execute(
                    "INSERT INTO schema_migration(migration_id, checksum, applied_at) "
                    "VALUES (?, ?, ?)",
                    (migration.name, checksum, _now()),
                )
                connection.execute(f"PRAGMA user_version = {int(migration.name[:3])}")
                connection.commit()
            except Exception:
                connection.rollback()
                raise

    def _validate_active_points(self, connection):
        invalid = connection.execute(
            "SELECT point_id FROM governed_monitoring_point "
            "WHERE status = 'ACTIVE' AND current_context_revision_id IS NULL"
        ).fetchone()
        if invalid:
            raise GovernedConflictError(
                f"Ponto ativo sem revisao contextual atual: {invalid[0]}"
            )
        cross_point = connection.execute(
            "SELECT point.point_id FROM governed_monitoring_point AS point "
            "JOIN point_context_revision AS revision "
            "ON revision.context_revision_id = point.current_context_revision_id "
            "WHERE revision.point_id != point.point_id"
        ).fetchone()
        if cross_point:
            raise GovernedConflictError(
                f"Ponto com referencia contextual cruzada: {cross_point[0]}"
            )
        geo_table = connection.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='geo_reference'"
        ).fetchone()
        if geo_table:
            missing_geo = connection.execute(
                "SELECT point.point_id FROM governed_monitoring_point AS point "
                "JOIN point_context_revision AS revision "
                "ON revision.context_revision_id = point.current_context_revision_id "
                "LEFT JOIN geo_reference AS geo "
                "ON geo.geo_reference_id = revision.geo_reference_id "
                "WHERE point.status = 'ACTIVE' "
                "AND (revision.geo_reference_id IS NULL OR geo.geo_reference_id IS NULL "
                "OR geo.context_revision_id <> revision.context_revision_id)"
            ).fetchone()
            if missing_geo:
                raise GovernedConflictError(
                    f"Ponto ativo sem classificacao GEO governada: {missing_geo[0]}"
                )


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
