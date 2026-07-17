import ast
import unicodedata
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

PRESENTATION_FILES = (
    "main.py",
    "qualidade_agua.py",
    "relatorios.py",
    "painel_executivo.py",
    "previsao_analitica.py",
    "governanca_operacional.py",
    "dados_ambientais.py",
    "consumo_distribuicao.py",
    "projeto_monitoramento_page.py",
)

ANALYTICS_FILES = (
    "analytics/alerts.py",
    "analytics/dashboard_snapshot.py",
    "analytics/models.py",
    "analytics/repositories.py",
    "analytics/scoring.py",
    "analytics/service.py",
    "analytics/trends.py",
)

QUALITY_ADAPTER_FILES = (
    "monitoramento_hidrico/qualidade_agua_adapter.py",
    "monitoramento_hidrico/dashboard_adapter.py",
    "monitoramento_hidrico/operational_reports_adapter.py",
    "monitoramento_hidrico/analytics_adapter.py",
    "monitoramento_hidrico/governance_adapter.py",
)

EXECUTIVE_FILES = (
    "executive/service.py",
    "executive/rules.py",
    "executive/models.py",
    "executive_recommendation/service.py",
    "executive_recommendation/rules.py",
    "executive_recommendation/models.py",
)

COMMUNICATION_FILES = PRESENTATION_FILES + QUALITY_ADAPTER_FILES + ANALYTICS_FILES + EXECUTIVE_FILES

LOCAL_PARAMETER_AUTHORITIES = {
    "PARAMETROS_QUALIDADE_AGUA",
    "QUALITY_PARAMETER_FIELDS",
    "REPORT_QUALITY_PARAMETERS",
    "QUALITY_ANALYTICS_PARAMETERS",
    "GOVERNANCE_QUALITY_PARAMETERS",
}

QUALITY_PARAMETER_IDENTIFIERS = {
    "ph",
    "turbidez",
    "oxigenio_dissolvido",
    "temperatura",
    "agrotoxicos",
}

OFFICIAL_PARAMETER_FUNCTIONS = {
    "quality_parameter_triples",
    "quality_parameter_analytics_entries",
    "quality_parameter_governance_mapping",
}

FORBIDDEN_STATUS_LABELS = {
    "dentro do padrao",
    "fora do padrao",
    "status executivo",
    "status critico",
}


def _path(relative_path):
    return PROJECT_ROOT / relative_path


def _source(relative_path):
    return _path(relative_path).read_text(encoding="utf-8").lstrip("\ufeff")


def _tree(relative_path):
    return ast.parse(_source(relative_path), filename=relative_path)


def _imports(tree):
    references = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            references.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            references.add(node.module)
            references.update(f"{node.module}.{alias.name}" for alias in node.names)
    return references


def _called_names(tree):
    names = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name):
            names.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            names.add(node.func.attr)
    return names


def _assignment_names(node):
    names = set()
    targets = []
    if isinstance(node, (ast.Assign, ast.AnnAssign)):
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    for target in targets:
        for child in ast.walk(target):
            if isinstance(child, ast.Name):
                names.add(child.id)
    return names


def _string_literals(node):
    return {
        child.value
        for child in ast.walk(node)
        if isinstance(child, ast.Constant) and isinstance(child.value, str)
    }


def _normalized(value):
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(character for character in decomposed if not unicodedata.combining(character)).casefold()


def _format_violations(guardrail, violations):
    return f"[{guardrail}] fronteira arquitetural violada:\n- " + "\n- ".join(violations)


class PA01CommunicationGuardrailsTests(unittest.TestCase):
    def test_g_obr_01_ui_does_not_access_internal_analytics_dependencies(self):
        forbidden_modules = {"analytics.repositories", "analytics.scoring"}
        forbidden_symbols = {"AnalyticsRepository", "WaterHealthScoreCalculator"}
        violations = []

        for relative_path in PRESENTATION_FILES:
            tree = _tree(relative_path)
            imports = _imports(tree)
            calls = _called_names(tree)
            imported_forbidden_modules = sorted(forbidden_modules & imports)
            imported_forbidden_symbols = sorted(
                symbol
                for symbol in forbidden_symbols
                if any(reference.endswith(f".{symbol}") for reference in imports)
            )
            called_forbidden_symbols = sorted(forbidden_symbols & calls)

            if imported_forbidden_modules:
                violations.append(f"{relative_path}: imports proibidos {imported_forbidden_modules}")
            if imported_forbidden_symbols:
                violations.append(f"{relative_path}: símbolos importados diretamente {imported_forbidden_symbols}")
            if called_forbidden_symbols:
                violations.append(f"{relative_path}: dependências internas instanciadas {called_forbidden_symbols}")

        self.assertFalse(violations, _format_violations("G-OBR-01", violations))

    def test_g_obr_02_governance_service_retains_reevaluation_authority(self):
        service_path = "governance/service.py"
        source = _source(service_path)
        tree = ast.parse(source, filename=service_path)
        violations = []

        service_class = next(
            (
                node
                for node in tree.body
                if isinstance(node, ast.ClassDef) and node.name == "OperationalGovernanceService"
            ),
            None,
        )
        if service_class is None:
            violations.append(f"{service_path}: classe OperationalGovernanceService ausente")
        else:
            sync_method = next(
                (
                    node
                    for node in service_class.body
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and node.name == "sync_from_analytics"
                ),
                None,
            )
            if sync_method is None:
                violations.append(f"{service_path}: método sync_from_analytics ausente")
            else:
                decision_calls = [
                    node
                    for node in ast.walk(sync_method)
                    if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "_decidir_reavaliacao_controlada"
                ]
                adapter_calls = [
                    node
                    for node in ast.walk(sync_method)
                    if isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "enriquecer_alertas"
                ]

                if not decision_calls:
                    violations.append(
                        f"{service_path}: sync_from_analytics não chama _decidir_reavaliacao_controlada"
                    )
                if len(adapter_calls) != 1:
                    violations.append(
                        f"{service_path}: esperado um único envio governado a enriquecer_alertas; encontrado {len(adapter_calls)}"
                    )
                elif adapter_calls:
                    adapter_call = adapter_calls[0]
                    positional_decisions = len(adapter_call.args) >= 2 and isinstance(adapter_call.args[1], ast.Name)
                    positional_decisions = positional_decisions and adapter_call.args[1].id == "decisions"
                    keyword_decisions = any(
                        keyword.arg == "decisions"
                        and isinstance(keyword.value, ast.Name)
                        and keyword.value.id == "decisions"
                        for keyword in adapter_call.keywords
                    )
                    if not (positional_decisions or keyword_decisions):
                        violations.append(
                            f"{service_path}: enriquecer_alertas deve receber decisions calculadas pela Governança"
                        )
                    if decision_calls and min(call.lineno for call in decision_calls) >= adapter_call.lineno:
                        violations.append(
                            f"{service_path}: a decisão governada deve ocorrer antes da chamada ao adapter"
                        )

        external_consumers = PRESENTATION_FILES + ANALYTICS_FILES + EXECUTIVE_FILES
        forbidden_module = "monitoramento_hidrico.governance_adapter"
        forbidden_symbol = "OperationalGovernanceHydricMonitoringAdapter"
        for relative_path in external_consumers:
            consumer_tree = _tree(relative_path)
            imports = _imports(consumer_tree)
            calls = _called_names(consumer_tree)
            if forbidden_module in imports or any(
                reference.endswith(f".{forbidden_symbol}") for reference in imports
            ):
                violations.append(
                    f"{relative_path}: consumidor externo importa diretamente o adapter de Governança"
                )
            if forbidden_symbol in calls:
                violations.append(
                    f"{relative_path}: consumidor externo instancia diretamente o adapter de Governança"
                )

        self.assertFalse(violations, _format_violations("G-OBR-02", violations))

    def test_g_obr_03_quality_adapters_use_the_central_parameter_mapping(self):
        official_module = "quality_parameter_mapping"
        violations = []

        for relative_path in QUALITY_ADAPTER_FILES:
            tree = _tree(relative_path)
            imports = _imports(tree)
            imported_functions = {
                function
                for function in OFFICIAL_PARAMETER_FUNCTIONS
                if any(
                    official_module in reference and reference.endswith(f".{function}")
                    for reference in imports
                )
            }
            if not imported_functions:
                violations.append(
                    f"{relative_path}: não importa função da autoridade central quality_parameter_mapping.py"
                )

            for node in ast.walk(tree):
                if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                    continue
                assigned_authorities = LOCAL_PARAMETER_AUTHORITIES & _assignment_names(node)
                if assigned_authorities:
                    violations.append(
                        f"{relative_path}:{node.lineno}: recria autoridades locais {sorted(assigned_authorities)}"
                    )

                local_parameters = {
                    value.casefold()
                    for value in _string_literals(node)
                    if value.casefold() in QUALITY_PARAMETER_IDENTIFIERS
                }
                if len(local_parameters) >= 2:
                    violations.append(
                        f"{relative_path}:{node.lineno}: recria coleção local de parâmetros {sorted(local_parameters)}"
                    )

        self.assertFalse(violations, _format_violations("G-OBR-03", violations))

    def test_g_obr_04_runtime_avoids_non_official_sensitive_status_texts(self):
        violations = []

        for relative_path in COMMUNICATION_FILES:
            tree = _tree(relative_path)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                    continue
                normalized_literal = _normalized(node.value)
                matched_labels = sorted(
                    label for label in FORBIDDEN_STATUS_LABELS if label == normalized_literal.strip()
                )
                if matched_labels:
                    violations.append(
                        f"{relative_path}:{node.lineno}: texto funcional de status não oficial {matched_labels}"
                    )

        self.assertFalse(violations, _format_violations("G-OBR-04", violations))

    def test_g_obr_05_executive_uses_no_hydric_engine_adapter_or_csv(self):
        allowed_monitoring_module = "monitoramento_hidrico.status_semantics"
        forbidden_calls = {
            "PolicyEngine",
            "AvaliacaoObservacionalService",
            "AnalyticsHydricMonitoringAdapter",
            "DashboardMonitoringAdapter",
            "OperationalGovernanceHydricMonitoringAdapter",
            "OperationalReportsHydricMonitoringAdapter",
            "QualidadeAguaMonitoringAdapter",
        }
        violations = []

        for relative_path in EXECUTIVE_FILES:
            tree = _tree(relative_path)
            imports = _imports(tree)
            calls = _called_names(tree)

            forbidden_imports = sorted(
                reference
                for reference in imports
                if reference == "csv"
                or reference == "monitoramento_hidrico"
                or (
                    reference.startswith("monitoramento_hidrico.")
                    and reference != allowed_monitoring_module
                    and not reference.startswith(f"{allowed_monitoring_module}.")
                )
            )
            if forbidden_imports:
                violations.append(f"{relative_path}: imports diretos proibidos {forbidden_imports}")

            called_forbidden = sorted(forbidden_calls & calls)
            if called_forbidden:
                violations.append(f"{relative_path}: motores/adapters instanciados {called_forbidden}")

            csv_literals = sorted(
                literal
                for literal in _string_literals(tree)
                if literal.strip().casefold().endswith(".csv")
            )
            if csv_literals:
                violations.append(f"{relative_path}: referências diretas a CSV {csv_literals}")

        self.assertFalse(violations, _format_violations("G-OBR-05", violations))


if __name__ == "__main__":
    unittest.main()
