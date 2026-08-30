"""Explicit, atomic bootstrap for the first real governed APS state."""

from dataclasses import dataclass

from .models import APSReference
from .repository import GovernedConflictError
from .services import APSService, ApplicabilityService, PointContextService


PROJECT_REFERENCE = "SISTEMA_MONITORAMENTO_AGUAS"
EXTERNAL_STATION_REFERENCE = "64447000"
DISPLAY_NAME = "Engenheiro Rosaldo Leitão"
ACTOR_REFERENCE = "ACTOR_PO_001"
PURPOSE = "ENVIRONMENTAL_CONDITION_MONITORING"
WATER_CONTEXT = "FLOWING_SURFACE_WATER"
POINT_TYPE = "GENERAL"
APS_MEMBERS = ("PH", "TURBIDITY", "DISSOLVED_OXYGEN")

AUTHORITY_LOCATORS = (
    "https://conama.mma.gov.br/images/conteudo/LivroConama.pdf",
    "https://www.gov.br/ana/pt-br/legislacao/resolucoes/resolucoes-regulatorias/2013/903",
)
EVIDENCE_LOCATOR = (
    "https://www.iat.pr.gov.br/sites/agua-terra/arquivos_restritos/files/"
    "documento/2023-12/bacia_tibagi_-_2023.pdf"
)


@dataclass(frozen=True)
class FirstRealAPSBootstrapResult:
    point_id: str
    context_revision_id: str
    aps_reference: APSReference


class FirstRealAPSBootstrap:
    """Creates or resolves the canonical state only when execute is called."""

    def __init__(self, repository, identifiers=None):
        self.repository = repository
        self.points = PointContextService(repository, identifiers)
        self.aps = APSService(repository, identifiers)
        self.applicability = ApplicabilityService(repository, identifiers)

    def execute(self, failure_hook=None):
        hook = failure_hook or (lambda _stage: None)
        with self.repository.transaction() as connection:
            initial_measurement_count = connection.execute(
                "SELECT COUNT(*) FROM governed_measurement"
            ).fetchone()[0]
            point = self.repository.fetch_point_by_external_reference(
                PROJECT_REFERENCE, EXTERNAL_STATION_REFERENCE, connection
            )
            if point is None:
                point = self.points.create_point_with_initial_context(
                    project_reference=PROJECT_REFERENCE,
                    display_name=DISPLAY_NAME,
                    purpose=PURPOSE,
                    water_context=WATER_CONTEXT,
                    point_type=POINT_TYPE,
                    actor_reference=ACTOR_REFERENCE,
                    external_station_reference=EXTERNAL_STATION_REFERENCE,
                    connection=connection,
                )
            self._validate_point(point, connection)
            hook("after_point")

            authority_ids = tuple(
                self._resolve_or_register_reference(connection, "authority", locator)
                for locator in AUTHORITY_LOCATORS
            )
            hook("after_authority")
            evidence_id = self._resolve_or_register_reference(
                connection, "evidence", EVIDENCE_LOCATOR
            )

            reference = self._resolve_aps(connection, point.current_context_revision_id)
            if reference is None:
                basis = self.aps.make_basis(
                    authority_references=authority_ids,
                    evidence_references=(evidence_id,),
                    member_references=APS_MEMBERS,
                )
                reference = self.aps.create_version(
                    context_revision_id=point.current_context_revision_id,
                    parameter_references=APS_MEMBERS,
                    bases=(basis,),
                    connection=connection,
                )
            self._validate_aps(connection, reference)
            hook("during_aps")

            applicable = connection.execute(
                "SELECT set_id, version FROM aps_applicability "
                "WHERE context_revision_id = ?",
                (point.current_context_revision_id,),
            ).fetchone()
            if applicable is not None and APSReference(*applicable) != reference:
                raise GovernedConflictError(
                    "Contexto inicial ja possui outra APS aplicavel."
                )
            self.applicability.assign(
                point.current_context_revision_id,
                reference,
                ACTOR_REFERENCE,
                connection=connection,
            )
            hook("during_applicability")

            final_measurement_count = connection.execute(
                "SELECT COUNT(*) FROM governed_measurement"
            ).fetchone()[0]
            if final_measurement_count != initial_measurement_count:
                raise GovernedConflictError(
                    "Bootstrap alterou indevidamente o estado de medicoes."
                )

        return FirstRealAPSBootstrapResult(
            point.point_id, point.current_context_revision_id, reference
        )

    def _resolve_or_register_reference(self, connection, kind, locator):
        table = f"{kind}_reference"
        id_column = f"{kind}_reference_id"
        rows = connection.execute(
            f"SELECT {id_column}, content_hash FROM {table} WHERE locator = ?",
            (locator,),
        ).fetchall()
        if len(rows) > 1:
            raise GovernedConflictError(
                f"Locator de {kind} possui referencias duplicadas."
            )
        if rows:
            if rows[0][1] is not None:
                raise GovernedConflictError(
                    f"Referencia canonica de {kind} possui content_hash nao autorizado."
                )
            return rows[0][0]
        register = getattr(self.aps, f"register_{kind}_reference")
        return register(locator, content_hash=None, connection=connection)

    def _resolve_aps(self, connection, context_revision_id):
        rows = connection.execute(
            "SELECT set_id, version FROM aps_version WHERE context_revision_id = ?",
            (context_revision_id,),
        ).fetchall()
        matches = []
        expected = set(APS_MEMBERS)
        for row in rows:
            members = {
                item[0]
                for item in connection.execute(
                    "SELECT parameter_reference FROM aps_member "
                    "WHERE set_id = ? AND version = ?",
                    row,
                ).fetchall()
            }
            if members == expected:
                matches.append(APSReference(*row))
        if len(matches) > 1:
            raise GovernedConflictError(
                "Mais de uma versao APS possui o estado semantico canonico."
            )
        return matches[0] if matches else None

    def _validate_point(self, point, connection):
        context = self.repository.fetch_current_context(point.point_id, connection)
        actual = (
            point.project_reference,
            point.external_station_reference,
            point.display_name,
            point.status,
            context.revision,
            context.purpose,
            context.water_context,
            context.point_type,
        )
        expected = (
            PROJECT_REFERENCE,
            EXTERNAL_STATION_REFERENCE,
            DISPLAY_NAME,
            "ACTIVE",
            1,
            PURPOSE,
            WATER_CONTEXT,
            POINT_TYPE,
        )
        if actual != expected:
            raise GovernedConflictError(
                "Ponto externo existente diverge do contexto inicial canonico."
            )

    def _validate_aps(self, connection, reference):
        members = {
            row[0]
            for row in connection.execute(
                "SELECT parameter_reference FROM aps_member "
                "WHERE set_id = ? AND version = ?",
                (reference.set_id, reference.version),
            ).fetchall()
        }
        if members != set(APS_MEMBERS) or "BOD_5D_20C" in members:
            raise GovernedConflictError("Membros da APS canonica divergem.")
        expected_authorities = set(AUTHORITY_LOCATORS)
        for member in APS_MEMBERS:
            authorities = {
                row[0]
                for row in connection.execute(
                    "SELECT DISTINCT authority.locator "
                    "FROM member_authorization_basis AS member_basis "
                    "JOIN basis_authority AS basis_authority "
                    "ON basis_authority.basis_id = member_basis.basis_id "
                    "JOIN authority_reference AS authority "
                    "ON authority.authority_reference_id = basis_authority.authority_reference_id "
                    "WHERE member_basis.set_id = ? AND member_basis.version = ? "
                    "AND member_basis.parameter_reference = ?",
                    (reference.set_id, reference.version, member),
                ).fetchall()
            }
            evidence = {
                row[0]
                for row in connection.execute(
                    "SELECT DISTINCT evidence.locator "
                    "FROM member_authorization_basis AS member_basis "
                    "JOIN basis_evidence AS basis_evidence "
                    "ON basis_evidence.basis_id = member_basis.basis_id "
                    "JOIN evidence_reference AS evidence "
                    "ON evidence.evidence_reference_id = basis_evidence.evidence_reference_id "
                    "WHERE member_basis.set_id = ? AND member_basis.version = ? "
                    "AND member_basis.parameter_reference = ?",
                    (reference.set_id, reference.version, member),
                ).fetchall()
            }
            if authorities != expected_authorities or evidence != {EVIDENCE_LOCATOR}:
                raise GovernedConflictError(
                    f"Cadeia de autorizacao canonica divergente para {member}."
                )
        self.repository.validate_authorization_chain(reference, connection)
