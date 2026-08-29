"""Fail-safe resolution of approved governed reference chains."""

from .repository import GovernedReferenceError


class GovernedReferenceResolver:
    def __init__(self, repository):
        self.repository = repository

    def resolve_point_context(self, point_id, connection=None):
        return self.repository.fetch_current_context(point_id, connection)

    def resolve_operational_aps(self, point_id, connection=None):
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
        return reference
