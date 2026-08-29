"""SQLite persistence boundary for governed Core V1."""

import hashlib
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from .models import APSReference, GovernedMonitoringPoint, PointContextRevision


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
                "current_context_revision_id FROM governed_monitoring_point WHERE point_id = ?",
                (point_id,),
            ).fetchone()
        if row is None:
            raise GovernedReferenceError(f"Ponto governado nao resolvivel: {point_id}")
        return GovernedMonitoringPoint(*row)

    def fetch_context_revision(self, context_revision_id, connection=None):
        with self._optional_connection(connection) as active:
            row = active.execute(
                "SELECT context_revision_id, revision, point_id, purpose, water_context, "
                "point_type, geo_reference, created_at FROM point_context_revision "
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
            connection.executescript(sql)
            connection.execute(
                "INSERT INTO schema_migration(migration_id, checksum, applied_at) VALUES (?, ?, ?)",
                (migration.name, checksum, _now()),
            )
            connection.execute(f"PRAGMA user_version = {int(migration.name[:3])}")
            connection.commit()

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
