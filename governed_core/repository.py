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
from .authority_models import AuthorityEvent
from .models import APSReference, GovernedMonitoringPoint, PointContextRevision
from .rule_models import GovernedRule


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DATABASE_PATH = BASE_DIR / "data" / "governed_core_v1.sqlite3"
MIGRATIONS_DIR = BASE_DIR / "migrations"


class GovernedCoreError(RuntimeError):
    pass


class GovernedReferenceError(GovernedCoreError):
    pass


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
            raise GovernedReferenceError(
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
        connection.execute(
            "INSERT INTO governed_evaluation ("
            "evaluation_id, measurement_id, parameter_reference, status, message, "
            "rule_origin, evaluated_at, registered_at, evaluation_engine, "
            "evaluation_engine_version, explanation_data"
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            tuple(evaluation.__dict__.values()),
        )

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
            raise GovernedReferenceError(f"Temporal context resolution requires exactly one match: {point_id}")
        return PointContextRevision(*rows[0])

    def fetch_temporal_aps(self, context_revision_id, measured_at, connection=None):
        with self._optional_connection(connection) as active:
            rows = active.execute("SELECT aps_set_id, aps_version FROM aps_temporal_applicability WHERE context_revision_id = ? AND effective_from <= ? AND (effective_until IS NULL OR ? < effective_until)", (context_revision_id, measured_at, measured_at)).fetchall()
        if len(rows) != 1:
            raise GovernedReferenceError("Temporal APS resolution requires exactly one match")
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


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
