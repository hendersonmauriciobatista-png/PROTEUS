import csv
import os
from dataclasses import dataclass
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from analytics import AnalyticsService
from analytics.repositories import AnalyticsRepository
from consumo_distribuicao import CSV_FIELDS as CONSUMO_FIELDS
from consumo_distribuicao import DATA_FILE as CONSUMO_FILE
from dados_ambientais import CSV_FIELDS as AMBIENTE_FIELDS
from dados_ambientais import DATA_FILE as AMBIENTE_FILE
from governance import OperationalGovernanceService
from governance.rules import ACTIVE_STATES
from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.operational_reports_adapter import (
    OperationalReportsHydricMonitoringAdapter,
)
from qualidade_agua import CSV_FIELDS as QUALIDADE_FIELDS
from qualidade_agua import DATA_FILE as QUALIDADE_FILE


MODULES = {
    "qualidade_agua": {
        "label": "Qualidade da Água",
        "path": QUALIDADE_FILE,
        "fields": QUALIDADE_FIELDS,
    },
    "consumo_distribuicao": {
        "label": "Consumo e Distribuição",
        "path": CONSUMO_FILE,
        "fields": CONSUMO_FIELDS,
    },
    "dados_ambientais": {
        "label": "Dados Ambientais",
        "path": AMBIENTE_FILE,
        "fields": AMBIENTE_FIELDS,
    },
}


@dataclass(frozen=True)
class DependencyStatus:
    analysis_nonconformities: int
    active_alerts: int
    active_events: int

    @property
    def blocked(self):
        return any(
            (
                self.analysis_nonconformities,
                self.active_alerts,
                self.active_events,
            )
        )

    @property
    def quality_reset_blocked(self):
        return self.active_events > 0

    @property
    def quality_reset_warnings(self):
        return self.analysis_nonconformities > 0 or self.active_alerts > 0


@dataclass(frozen=True)
class CleaningResult:
    cleared: bool
    removed_records: int
    dependencies: DependencyStatus
    confirmation_required: bool = False


class HistoryMaintenanceService:
    def __init__(
        self,
        modules=None,
        analytics_service=None,
        governance_service=None,
        monitoring_adapter=None,
    ):
        self.modules = modules or MODULES
        repository = AnalyticsRepository(
            quality_path=self.modules["qualidade_agua"]["path"],
            environment_path=self.modules["dados_ambientais"]["path"],
            consumption_path=self.modules["consumo_distribuicao"]["path"],
        )
        self.analytics_service = analytics_service or AnalyticsService(repository=repository)
        self.governance_service = governance_service or OperationalGovernanceService()
        self.monitoring_adapter = monitoring_adapter or OperationalReportsHydricMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )

    def record_count(self, module_id):
        return len(self._read_rows(module_id))

    def check_dependencies(self, module_id):
        self._module(module_id)
        nonconformities = 0
        if module_id == "qualidade_agua":
            nonconformities = self.monitoring_adapter.contar_observacional_atencao(
                self._read_rows(module_id)
            )

        snapshot = self.analytics_service.build_snapshot()
        active_alerts = sum(
            1 for alert in snapshot.alerts if alert.domain == module_id
        )
        active_events = sum(
            1
            for event in self.governance_service.list_events()
            if event.domain == module_id and event.state in ACTIVE_STATES
        )
        return DependencyStatus(nonconformities, active_alerts, active_events)

    def clear_history(self, module_id, confirmed=False):
        dependencies = self.check_dependencies(module_id)
        if module_id == "qualidade_agua":
            if dependencies.quality_reset_blocked:
                return CleaningResult(False, 0, dependencies)
            if dependencies.quality_reset_warnings and not confirmed:
                return CleaningResult(False, 0, dependencies, confirmation_required=True)
        elif dependencies.blocked:
            return CleaningResult(False, 0, dependencies)

        removed_records = self.record_count(module_id)
        module = self._module(module_id)
        path = Path(module["path"])
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(path.suffix + ".tmp")
        with temp_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=module["fields"])
            writer.writeheader()
        os.replace(temp_path, path)
        return CleaningResult(True, removed_records, dependencies)

    def _read_rows(self, module_id):
        path = Path(self._module(module_id)["path"])
        if not path.exists():
            return []
        with path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def _module(self, module_id):
        if module_id not in self.modules:
            raise ValueError(f"Módulo de histórico desconhecido: {module_id}")
        return self.modules[module_id]


class AdministracaoPage(QWidget):
    def __init__(self, maintenance_service=None):
        super().__init__()
        self.maintenance_service = maintenance_service or HistoryMaintenanceService()
        self.count_labels = {}
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(16)

        title = QLabel("Administração e Manutenção")
        title.setObjectName("page_title")
        subtitle = QLabel("Limpeza governada e individual dos históricos por módulo")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        for module_id, module in self.maintenance_service.modules.items():
            card = QFrame()
            card.setStyleSheet(
                "QFrame { background-color: #112240; border: 1px solid #1e3a5f; "
                "border-radius: 6px; }"
            )
            row = QHBoxLayout(card)
            name = QLabel(module["label"])
            name.setStyleSheet("font-size: 14px; font-weight: bold; color: #cfd8dc;")
            count = QLabel()
            count.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            button = QPushButton("Limpar histórico")
            button.setObjectName(f"clear_history_{module_id}")
            button.setStyleSheet(
                "QPushButton { background-color: #b71c1c; color: white; border: none; "
                "border-radius: 4px; padding: 9px 14px; } "
                "QPushButton:hover { background-color: #c62828; }"
            )
            button.clicked.connect(
                lambda _checked=False, selected=module_id: self._request_cleaning(selected)
            )
            row.addWidget(name, 1)
            row.addWidget(count)
            row.addWidget(button)
            self.count_labels[module_id] = count
            layout.addWidget(card)

        governance_card = QFrame()
        governance_card.setStyleSheet(
            "QFrame { background-color: #112240; border: 1px solid #1e3a5f; "
            "border-radius: 6px; }"
        )
        governance_row = QHBoxLayout(governance_card)
        governance_name = QLabel("Governança Operacional")
        governance_name.setStyleSheet("font-size: 14px; font-weight: bold; color: #cfd8dc;")
        self.governance_count_label = QLabel()
        self.governance_count_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        governance_button = QPushButton("Limpar histórico de Governança")
        governance_button.setObjectName("clear_governance_history")
        governance_button.clicked.connect(self._request_governance_cleaning)
        governance_row.addWidget(governance_name, 1)
        governance_row.addWidget(self.governance_count_label)
        governance_row.addWidget(governance_button)
        layout.addWidget(governance_card)

        layout.addStretch()

    def refresh(self):
        for module_id, label in self.count_labels.items():
            total = self.maintenance_service.record_count(module_id)
            label.setText(f"{total} registro(s)")
        status = self.maintenance_service.governance_service.governance_history_status()
        self.governance_count_label.setText(
            f"Resolvidos: {status.resolved_events} | Arquivados: {status.archived_events}"
        )

    def _request_governance_cleaning(self):
        service = self.maintenance_service.governance_service
        status = service.governance_history_status()
        if status.active_events:
            QMessageBox.warning(
                self,
                "Limpeza bloqueada",
                "A Governança possui eventos ativos.\n\n"
                f"Abertos: {status.open_events}\n"
                f"Em monitoramento: {status.monitoring_events}",
            )
            return

        answer = QMessageBox.question(
            self,
            "Confirmar limpeza da Governança",
            f"Eventos resolvidos que serão removidos: {status.resolved_events}\n"
            f"Eventos arquivados que serão removidos: {status.archived_events}\n\n"
            "Um backup será criado antes da limpeza. Esta operação é irreversível.\n"
            "Deseja continuar?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        result = service.reset_terminal_history(confirmed=True)
        if not result.cleared:
            QMessageBox.warning(
                self,
                "Limpeza bloqueada",
                result.error or "A limpeza da Governança não pôde ser concluída.",
            )
            return

        self.refresh()
        QMessageBox.information(
            self,
            "Limpeza concluída",
            f"{result.removed_events} evento(s) terminal(is) removido(s).\n"
            f"Backup: {result.backup_path}",
        )

    def _request_cleaning(self, module_id):
        module = self.maintenance_service.modules[module_id]
        dependencies = self.maintenance_service.check_dependencies(module_id)
        quality_reset = module_id == "qualidade_agua"
        reset_blocked = (
            dependencies.quality_reset_blocked
            if quality_reset
            else dependencies.blocked
        )
        if reset_blocked:
            QMessageBox.warning(
                self,
                "Limpeza bloqueada",
                "A operação não pode ser executada devido à existência de "
                "dependências operacionais.\n\n"
                f"Não conformidades de análise: {dependencies.analysis_nonconformities}\n"
                f"Alertas ativos: {dependencies.active_alerts}\n"
                f"Eventos operacionais ativos: {dependencies.active_events}",
            )
            return

        confirmation_message = f"Confirma a limpeza do histórico de {module['label']}?"
        if quality_reset:
            confirmation_message = (
                f"Medições que serão removidas: {self.maintenance_service.record_count(module_id)}\n"
                f"Não conformidades derivadas: {dependencies.analysis_nonconformities}\n"
                f"Alertas analíticos ativos: {dependencies.active_alerts}\n\n"
                "Esta operação é irreversível e remove somente as medições de Qualidade da Água.\n"
                "Deseja continuar?"
            )

        answer = QMessageBox.question(
            self,
            "Confirmar limpeza",
            confirmation_message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer != QMessageBox.Yes:
            return

        result = self.maintenance_service.clear_history(module_id, confirmed=True)
        if not result.cleared:
            QMessageBox.warning(
                self,
                "Limpeza bloqueada",
                "A operação não pode ser executada devido à existência de "
                "dependências operacionais.",
            )
            return

        self.refresh()
        QMessageBox.information(
            self,
            "Limpeza concluída",
            f"{result.removed_records} registro(s) removido(s) de {module['label']}.",
        )
