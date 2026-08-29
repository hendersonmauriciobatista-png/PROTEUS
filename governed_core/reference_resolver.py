"""Fail-safe resolution of approved governed reference chains."""

from .repository import GovernedReferenceError
from .models import PointStatus


class GovernedReferenceResolver:
    def __init__(self, repository):
        self.repository = repository

    def resolve_point_context(self, point_id, connection=None):
        return self.repository.fetch_current_context(point_id, connection)

    def resolve_operational_aps(self, point_id, connection=None):
        _context, reference = self.resolve_operational_references(point_id, connection)
        return reference

    def resolve_operational_references(self, point_id, connection=None):
        point = self.repository.fetch_point(point_id, connection)
        if point.status != PointStatus.ACTIVE.value:
            raise GovernedReferenceError(f"Ponto inativo para uso operacional: {point_id}")
        context = self.resolve_point_context(point_id, connection)
        reference = self.repository.fetch_applicable_aps(
            context.context_revision_id,
            connection,
        )
        aps_context_id = self.repository.fetch_aps_version(reference, connection)
        if aps_context_id != context.context_revision_id:
            raise GovernedReferenceError("APS aplicavel pertence a outro contexto.")
        self.repository.validate_authorization_chain(reference, connection)
        unresolved = self.repository.unresolved_disqualification_ids(reference, connection)
        if unresolved:
            raise GovernedReferenceError(
                "Versao APS bloqueada por disqualification nao resolvida: "
                + ", ".join(unresolved)
            )
        return context, reference
