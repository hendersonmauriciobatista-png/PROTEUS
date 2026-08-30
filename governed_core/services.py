"""Transactional application services for DFA-02 governed Core V1."""

from contextlib import contextmanager
from datetime import datetime, timezone

from .identifiers import IdentifierFactory
from .models import (
    APSReference,
    APSVersionDraft,
    AuthorizationBasisDraft,
    GovernanceAction,
    POINT_TYPES,
    PURPOSES,
    PointStatus,
    WATER_CONTEXTS,
)
from .reference_resolver import GovernedReferenceResolver
from .repository import GovernedConflictError, GovernedReferenceError


class PointContextService:
    def __init__(self, repository, identifiers=None):
        self.repository = repository
        self.identifiers = identifiers or IdentifierFactory()

    def create_point_with_initial_context(
        self,
        project_reference,
        display_name,
        purpose,
        water_context,
        point_type,
        actor_reference,
        geo_reference=None,
        status=PointStatus.ACTIVE.value,
        external_station_reference=None,
        connection=None,
    ):
        self._validate_context_values(purpose, water_context, point_type)
        self._validate_point_input(project_reference, display_name, status, actor_reference)
        if external_station_reference is not None and not external_station_reference.strip():
            raise ValueError("Referencia externa da estacao deve ser nao vazia.")
        point_id = self.identifiers.new("point")
        revision_id = self.identifiers.new("context_revision")
        now = _now()
        with _operation(self.repository, connection) as active:
            active.execute(
                "INSERT INTO governed_monitoring_point "
                "(point_id, project_reference, display_name, status, "
                "current_context_revision_id, external_station_reference) "
                "VALUES (?, ?, ?, 'INACTIVE', NULL, ?)",
                (point_id, project_reference, display_name, external_station_reference),
            )
            active.execute(
                "INSERT INTO point_context_revision "
                "(context_revision_id, point_id, revision, purpose, water_context, "
                "point_type, geo_reference, created_at) VALUES (?, ?, 1, ?, ?, ?, ?, ?)",
                (
                    revision_id,
                    point_id,
                    purpose,
                    water_context,
                    point_type,
                    geo_reference,
                    now,
                ),
            )
            active.execute(
                "UPDATE governed_monitoring_point SET status = ?, "
                "current_context_revision_id = ? WHERE point_id = ?",
                (status, revision_id, point_id),
            )
            self._insert_context_event(
                active,
                actor_reference,
                previous_context_revision_id=None,
                new_context_revision_id=revision_id,
            )
        return self.repository.fetch_point(point_id, connection)

    def create_context_revision(
        self,
        point_id,
        purpose,
        water_context,
        point_type,
        actor_reference,
        geo_reference=None,
    ):
        self._validate_context_values(purpose, water_context, point_type)
        if not actor_reference or not actor_reference.strip():
            raise ValueError("Referencia do ator e obrigatoria.")
        new_revision_id = self.identifiers.new("context_revision")
        with self.repository.transaction() as connection:
            current = self.repository.fetch_current_context(point_id, connection)
            next_revision = current.revision + 1
            connection.execute(
                "INSERT INTO point_context_revision "
                "(context_revision_id, point_id, revision, purpose, water_context, "
                "point_type, geo_reference, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    new_revision_id,
                    point_id,
                    next_revision,
                    purpose,
                    water_context,
                    point_type,
                    geo_reference,
                    _now(),
                ),
            )
            connection.execute(
                "UPDATE governed_monitoring_point SET current_context_revision_id = ? "
                "WHERE point_id = ?",
                (new_revision_id, point_id),
            )
            self._insert_context_event(
                connection,
                actor_reference,
                previous_context_revision_id=current.context_revision_id,
                new_context_revision_id=new_revision_id,
            )
        return self.repository.fetch_context_revision(new_revision_id)

    def update_display_name(self, point_id, display_name):
        if not display_name or not display_name.strip():
            raise ValueError("Nome de exibicao e obrigatorio.")
        with self.repository.transaction() as connection:
            self.repository.fetch_point(point_id, connection)
            connection.execute(
                "UPDATE governed_monitoring_point SET display_name = ? WHERE point_id = ?",
                (display_name, point_id),
            )
        return self.repository.fetch_point(point_id)

    def update_status(self, point_id, status):
        if status not in {item.value for item in PointStatus}:
            raise ValueError(f"Status de ponto invalido: {status}")
        with self.repository.transaction() as connection:
            self.repository.fetch_point(point_id, connection)
            connection.execute(
                "UPDATE governed_monitoring_point SET status = ? WHERE point_id = ?",
                (status, point_id),
            )
        return self.repository.fetch_point(point_id)

    def _insert_context_event(
        self,
        connection,
        actor_reference,
        previous_context_revision_id,
        new_context_revision_id,
    ):
        connection.execute(
            "INSERT INTO governance_event "
            "(event_id, action, actor_reference, registered_at, "
            "previous_context_revision_id, new_context_revision_id) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                self.identifiers.new("event"),
                GovernanceAction.CURRENT_CONTEXT_REFERENCE_CHANGED.value,
                actor_reference,
                _now(),
                previous_context_revision_id,
                new_context_revision_id,
            ),
        )

    def _validate_point_input(self, project_reference, display_name, status, actor_reference):
        for label, value in (
            ("Projeto", project_reference),
            ("Nome de exibicao", display_name),
            ("Ator", actor_reference),
        ):
            if not value or not value.strip():
                raise ValueError(f"{label} e obrigatorio.")
        if status not in {item.value for item in PointStatus}:
            raise ValueError(f"Status de ponto invalido: {status}")

    def _validate_context_values(self, purpose, water_context, point_type):
        if purpose not in PURPOSES:
            raise ValueError(f"Purpose invalido: {purpose}")
        if water_context not in WATER_CONTEXTS:
            raise ValueError(f"Water context invalido: {water_context}")
        if point_type not in POINT_TYPES:
            raise ValueError(f"Point type invalido: {point_type}")


class APSService:
    def __init__(self, repository, identifiers=None):
        self.repository = repository
        self.identifiers = identifiers or IdentifierFactory()

    def register_authority_reference(self, locator, content_hash=None, connection=None):
        return self._register_reference("authority", locator, content_hash, connection)

    def register_evidence_reference(self, locator, content_hash=None, connection=None):
        return self._register_reference("evidence", locator, content_hash, connection)

    def make_basis(self, authority_references, evidence_references, member_references):
        return AuthorizationBasisDraft(
            basis_id=self.identifiers.new("basis"),
            authority_references=tuple(authority_references),
            evidence_references=tuple(evidence_references),
            member_references=tuple(member_references),
        )

    def create_version(
        self,
        context_revision_id,
        parameter_references,
        bases,
        set_id=None,
        connection=None,
    ):
        parameters = tuple(dict.fromkeys(parameter_references))
        bases = tuple(bases)
        if not parameters:
            raise GovernedConflictError("Versao APS exige ao menos um membro.")
        if not bases:
            raise GovernedConflictError("Versao APS exige authorization basis.")
        set_id = set_id or self.identifiers.new("aps")
        with _operation(self.repository, connection) as active:
            self.repository.fetch_context_revision(context_revision_id, active)
            current = active.execute(
                "SELECT MAX(version) FROM aps_version WHERE set_id = ?",
                (set_id,),
            ).fetchone()[0]
            version = 1 if current is None else current + 1
            if current is None:
                active.execute(
                    "INSERT INTO authorized_parameter_set(set_id) VALUES (?)",
                    (set_id,),
                )
            self._validate_basis_inputs(active, parameters, bases)
            active.execute(
                "INSERT INTO aps_version(set_id, version, context_revision_id) VALUES (?, ?, ?)",
                (set_id, version, context_revision_id),
            )
            for parameter in parameters:
                active.execute(
                    "INSERT INTO aps_member(set_id, version, parameter_reference) "
                    "VALUES (?, ?, ?)",
                    (set_id, version, parameter),
                )
            for basis in bases:
                active.execute(
                    "INSERT INTO authorization_basis(basis_id, set_id, version) VALUES (?, ?, ?)",
                    (basis.basis_id, set_id, version),
                )
                for authority_id in basis.authority_references:
                    active.execute(
                        "INSERT INTO basis_authority(basis_id, authority_reference_id) VALUES (?, ?)",
                        (basis.basis_id, authority_id),
                    )
                for evidence_id in basis.evidence_references:
                    active.execute(
                        "INSERT INTO basis_evidence(basis_id, evidence_reference_id) VALUES (?, ?)",
                        (basis.basis_id, evidence_id),
                    )
                for parameter in basis.member_references:
                    active.execute(
                        "INSERT INTO member_authorization_basis "
                        "(set_id, version, parameter_reference, basis_id) VALUES (?, ?, ?, ?)",
                        (set_id, version, parameter, basis.basis_id),
                    )
            reference = APSReference(set_id, version)
            self.repository.validate_authorization_chain(reference, active)
        return reference

    def _register_reference(self, kind, locator, content_hash, connection=None):
        if not locator or not locator.strip():
            raise ValueError("Locator de referencia e obrigatorio.")
        reference_id = self.identifiers.new(kind)
        table = f"{kind}_reference"
        id_column = f"{kind}_reference_id"
        with _operation(self.repository, connection) as active:
            active.execute(
                f"INSERT INTO {table}({id_column}, locator, content_hash) VALUES (?, ?, ?)",
                (reference_id, locator, content_hash),
            )
        return reference_id

    def _validate_basis_inputs(self, connection, parameters, bases):
        covered = set()
        parameter_set = set(parameters)
        for basis in bases:
            if not basis.member_references:
                raise GovernedConflictError(f"Authorization basis orfa: {basis.basis_id}")
            if not basis.authority_references or not basis.evidence_references:
                raise GovernedConflictError(
                    f"Authorization basis sem autoridade ou evidencia: {basis.basis_id}"
                )
            unknown = set(basis.member_references) - parameter_set
            if unknown:
                raise GovernedConflictError(
                    "Authorization basis referencia membros externos: " + ", ".join(sorted(unknown))
                )
            for authority_id in basis.authority_references:
                self._require_reference(connection, "authority", authority_id)
            for evidence_id in basis.evidence_references:
                self._require_reference(connection, "evidence", evidence_id)
            covered.update(basis.member_references)
        uncovered = parameter_set - covered
        if uncovered:
            raise GovernedConflictError(
                "Membros sem authorization basis: " + ", ".join(sorted(uncovered))
            )

    def _require_reference(self, connection, kind, reference_id):
        row = connection.execute(
            f"SELECT 1 FROM {kind}_reference WHERE {kind}_reference_id = ?",
            (reference_id,),
        ).fetchone()
        if row is None:
            raise GovernedReferenceError(
                f"Referencia de {kind} nao resolvivel: {reference_id}"
            )


class ApplicabilityService:
    def __init__(self, repository, identifiers=None):
        self.repository = repository
        self.identifiers = identifiers or IdentifierFactory()
        self.resolver = GovernedReferenceResolver(repository)

    def assign(self, context_revision_id, reference, actor_reference, connection=None):
        self._require_actor(actor_reference)
        with _operation(self.repository, connection) as active:
            self.repository.fetch_context_revision(context_revision_id, active)
            target_context = self.repository.fetch_aps_version(reference, active)
            if target_context != context_revision_id:
                raise GovernedReferenceError("APS e contexto da applicability nao coincidem.")
            previous_row = active.execute(
                "SELECT set_id, version FROM aps_applicability WHERE context_revision_id = ?",
                (context_revision_id,),
            ).fetchone()
            previous = APSReference(*previous_row) if previous_row else None
            if previous == reference:
                return previous
            if previous is None:
                action = GovernanceAction.APPLICABILITY_ASSIGNED.value
                active.execute(
                    "INSERT INTO aps_applicability(context_revision_id, set_id, version) "
                    "VALUES (?, ?, ?)",
                    (context_revision_id, reference.set_id, reference.version),
                )
            else:
                action = GovernanceAction.APPLICABILITY_CHANGED.value
                active.execute(
                    "UPDATE aps_applicability SET set_id = ?, version = ? "
                    "WHERE context_revision_id = ?",
                    (reference.set_id, reference.version, context_revision_id),
                )
            self._insert_event(
                active,
                action,
                actor_reference,
                context_revision_id=context_revision_id,
                previous=previous,
                new=reference,
            )
        return reference

    def remove(self, context_revision_id, actor_reference):
        self._require_actor(actor_reference)
        with self.repository.transaction() as connection:
            previous = self.repository.fetch_applicable_aps(context_revision_id, connection)
            connection.execute(
                "DELETE FROM aps_applicability WHERE context_revision_id = ?",
                (context_revision_id,),
            )
            self._insert_event(
                connection,
                GovernanceAction.APPLICABILITY_REMOVED.value,
                actor_reference,
                context_revision_id=context_revision_id,
                previous=previous,
            )
        return previous

    def disqualify(self, reference, actor_reference):
        self._require_actor(actor_reference)
        with self.repository.transaction() as connection:
            self.repository.fetch_aps_version(reference, connection)
            return self._insert_event(
                connection,
                GovernanceAction.APS_VERSION_DISQUALIFIED.value,
                actor_reference,
                target=reference,
            )

    def requalify(self, reference, disqualification_event_ids, actor_reference):
        self._require_actor(actor_reference)
        event_ids = tuple(dict.fromkeys(disqualification_event_ids))
        if not event_ids:
            raise GovernedConflictError(
                "Requalification exige ao menos uma disqualification exata."
            )
        with self.repository.transaction() as connection:
            self.repository.fetch_aps_version(reference, connection)
            for event_id in event_ids:
                row = connection.execute(
                    "SELECT action, target_set_id, target_version FROM governance_event "
                    "WHERE event_id = ?",
                    (event_id,),
                ).fetchone()
                if row is None:
                    raise GovernedReferenceError(f"Evento nao resolvivel: {event_id}")
                if row != (
                    GovernanceAction.APS_VERSION_DISQUALIFIED.value,
                    reference.set_id,
                    reference.version,
                ):
                    raise GovernedConflictError(
                        f"Disqualification nao pertence a versao APS alvo: {event_id}"
                    )
                resolved = connection.execute(
                    "SELECT 1 FROM governance_event_resolution "
                    "WHERE disqualification_event_id = ?",
                    (event_id,),
                ).fetchone()
                if resolved:
                    raise GovernedConflictError(
                        f"Disqualification ja resolvida: {event_id}"
                    )
            requalification_id = self._insert_event(
                connection,
                GovernanceAction.APS_VERSION_REQUALIFIED.value,
                actor_reference,
                target=reference,
            )
            for event_id in event_ids:
                connection.execute(
                    "INSERT INTO governance_event_resolution "
                    "(requalification_event_id, disqualification_event_id) VALUES (?, ?)",
                    (requalification_id, event_id),
                )
        return requalification_id

    def assert_future_use_allowed(self, point_id):
        return self.resolver.resolve_operational_aps(point_id)

    def _insert_event(
        self,
        connection,
        action,
        actor_reference,
        context_revision_id=None,
        previous=None,
        new=None,
        target=None,
    ):
        event_id = self.identifiers.new("event")
        connection.execute(
            "INSERT INTO governance_event "
            "(event_id, action, actor_reference, registered_at, context_revision_id, "
            "previous_set_id, previous_version, new_set_id, new_version, "
            "target_set_id, target_version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                event_id,
                action,
                actor_reference,
                _now(),
                context_revision_id,
                previous.set_id if previous else None,
                previous.version if previous else None,
                new.set_id if new else None,
                new.version if new else None,
                target.set_id if target else None,
                target.version if target else None,
            ),
        )
        return event_id

    def _require_actor(self, actor_reference):
        if not actor_reference or not actor_reference.strip():
            raise ValueError("Referencia do ator e obrigatoria.")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def _operation(repository, connection):
    if connection is not None:
        yield connection
        return
    with repository.transaction() as active:
        yield active
