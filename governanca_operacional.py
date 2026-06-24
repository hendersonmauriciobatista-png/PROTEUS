from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from governance import OperationalGovernanceService
from governance.models import EventState


class GovernancaOperacionalPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = OperationalGovernanceService()
        self.events = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title = QLabel("Governanca Operacional")
        title.setObjectName("page_title")
        subtitle = QLabel("Acompanhamento observacional de eventos derivados dos alertas analiticos")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        cards_layout = QHBoxLayout()
        self.summary_labels = {}
        for state, color in [
            (EventState.ABERTO.value, "#4fc3f7"),
            (EventState.MONITORAMENTO.value, "#ffa726"),
            (EventState.RESOLVIDO.value, "#66bb6a"),
            (EventState.ARQUIVADO.value, "#78909c"),
        ]:
            card, label = self._create_summary_card(state, color)
            self.summary_labels[state] = label
            cards_layout.addWidget(card)
        layout.addLayout(cards_layout)

        action_layout = QHBoxLayout()
        self.sync_button = QPushButton("Sincronizar Alertas")
        self.sync_button.clicked.connect(self.sync_alerts)
        self.monitor_button = QPushButton("Mover para Monitoramento")
        self.monitor_button.clicked.connect(self.move_selected_to_monitoring)
        self.resolve_button = QPushButton("Marcar como Resolvido")
        self.resolve_button.clicked.connect(self.resolve_selected)
        self.archive_button = QPushButton("Arquivar")
        self.archive_button.clicked.connect(self.archive_selected)

        action_layout.addWidget(self.sync_button)
        action_layout.addStretch()
        action_layout.addWidget(self.monitor_button)
        action_layout.addWidget(self.resolve_button)
        action_layout.addWidget(self.archive_button)
        layout.addLayout(action_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Estado", "Severidade", "Dominio", "Metrica", "Ocorrencias", "Atualizado", "Evidencia", "Recomendacao"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            "QTableWidget { background-color: #112240; color: #cfd8dc; "
            "gridline-color: #1e3a5f; border: 1px solid #1e3a5f; }"
            "QHeaderView::section { background-color: #1e3f6e; color: #cfd8dc; "
            "font-weight: bold; border: 1px solid #1e3a5f; padding: 4px; }"
        )
        layout.addWidget(self.table)

    def _create_summary_card(self, title, color):
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: #112240; border: 1px solid {color}44; "
            f"border-left: 4px solid {color}; border-radius: 8px; padding: 8px; }}"
        )
        card_layout = QVBoxLayout(card)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold; background: transparent; border: none;")
        value_label = QLabel("0")
        value_label.setStyleSheet("color: #cfd8dc; font-size: 20px; font-weight: bold; background: transparent; border: none;")
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        return card, value_label

    def refresh(self):
        self.events = self.service.list_events()
        self._load_summary()
        self._load_table()

    def sync_alerts(self):
        result = self.service.sync_from_analytics()
        self.refresh()
        QMessageBox.information(
            self,
            "Sincronizacao concluida",
            (
                "Alertas sincronizados para acompanhamento observacional.\n"
                f"Novos eventos: {result['created']}\n"
                f"Eventos atualizados: {result['updated']}\n"
                f"Alertas observados: {result['alerts']}"
            ),
        )

    def move_selected_to_monitoring(self):
        self._apply_selected_action(self.service.move_to_monitoring, "Evento movido para monitoramento observacional.")

    def resolve_selected(self):
        self._apply_selected_action(
            lambda event_id: self.service.resolve_event(event_id, "Resolucao observacional registrada pela interface."),
            "Evento marcado como resolvido para fins de acompanhamento.",
        )

    def archive_selected(self):
        self._apply_selected_action(
            lambda event_id: self.service.archive_event(event_id, "Arquivamento observacional registrado pela interface."),
            "Evento arquivado com historico preservado.",
        )

    def _apply_selected_action(self, action, success_message):
        event = self._selected_event()
        if not event:
            QMessageBox.warning(self, "Nenhum evento selecionado", "Selecione um evento para registrar o acompanhamento.")
            return

        if action(event.event_id):
            self.refresh()
            QMessageBox.information(self, "Registro atualizado", success_message)
            return

        QMessageBox.warning(
            self,
            "Transicao nao aplicada",
            "A transicao solicitada nao e permitida pelo estado atual do evento.",
        )

    def _selected_event(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.events):
            return None
        return self.events[row]

    def _load_summary(self):
        summary = {state.value: 0 for state in EventState}
        for event in self.events:
            summary[event.state] = summary.get(event.state, 0) + 1

        for state, label in self.summary_labels.items():
            label.setText(str(summary.get(state, 0)))

    def _load_table(self):
        self.table.setRowCount(len(self.events))
        for row_index, event in enumerate(self.events):
            values = [
                event.state,
                event.severity,
                event.domain,
                event.metric,
                str(event.occurrence_count),
                event.updated_at.isoformat(timespec="seconds"),
                event.evidence,
                event.recommendation,
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index == 0:
                    self._apply_state_style(item, event.state)
                if column_index in (1, 4):
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, column_index, item)

    def _apply_state_style(self, item, state):
        colors = {
            EventState.ABERTO.value: "#1e3f6e",
            EventState.MONITORAMENTO.value: "#8a6d1d",
            EventState.RESOLVIDO.value: "#1b5e20",
            EventState.ARQUIVADO.value: "#455a64",
        }
        item.setBackground(QColor(colors.get(state, "#112240")))
        item.setForeground(QColor("#ffffff"))
        item.setTextAlignment(Qt.AlignCenter)
