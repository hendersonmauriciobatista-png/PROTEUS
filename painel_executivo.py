from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from executive import ExecutiveIntelligenceService
from executive.models import EXECUTIVE_ATTENTION, EXECUTIVE_CRITICAL, EXECUTIVE_NORMAL


class PainelExecutivoPage(QWidget):
    def __init__(self):
        super().__init__()
        self.service = ExecutiveIntelligenceService()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title = QLabel("Painel Executivo")
        title.setObjectName("page_title")
        subtitle = QLabel("Visao observacional consolidada do estado geral do sistema")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        top_cards = QHBoxLayout()
        self.status_card, self.status_label = self._create_card("Status executivo observacional", "#4fc3f7")
        self.score_card, self.score_label = self._create_card("Water Health Score", "#66bb6a")
        self.open_card, self.open_label = self._create_card("ABERTO", "#4fc3f7")
        self.monitoring_card, self.monitoring_label = self._create_card("MONITORAMENTO", "#ffa726")
        self.resolved_card, self.resolved_label = self._create_card("RESOLVIDO", "#66bb6a")

        for card in [self.status_card, self.score_card, self.open_card, self.monitoring_card, self.resolved_card]:
            top_cards.addWidget(card)
        layout.addLayout(top_cards)

        self.message_label = QLabel("")
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet(
            "QLabel { background-color: #112240; color: #cfd8dc; "
            "border: 1px solid #1e3a5f; border-radius: 8px; padding: 10px; }"
        )
        layout.addWidget(self.message_label)

        self.recommendations_table = QTableWidget()
        self.recommendations_table.setColumnCount(5)
        self.recommendations_table.setHorizontalHeaderLabels(
            ["Prioridade", "Recomendacao", "Justificativa", "Confianca", "Evidencias"]
        )
        self._style_table(self.recommendations_table)
        self._style_explanatory_table(self.recommendations_table, (0, 3), (1, 2, 4))
        layout.addWidget(self.recommendations_table)

        self.priorities_table = QTableWidget()
        self.priorities_table.setColumnCount(5)
        self.priorities_table.setHorizontalHeaderLabels(["Nivel", "Prioridade observacional", "Fonte", "Evidencia", "Recomendacao"])
        self._style_table(self.priorities_table)
        self._style_explanatory_table(self.priorities_table, (0, 2), (1, 3, 4))
        layout.addWidget(self.priorities_table)

        self.signals_table = QTableWidget()
        self.signals_table.setColumnCount(4)
        self.signals_table.setHorizontalHeaderLabels(["Tipo", "Dominio", "Metrica", "Resumo"])
        self._style_table(self.signals_table)
        self._style_explanatory_table(self.signals_table, (0, 1, 2), (3,))
        layout.addWidget(self.signals_table)

        self.refresh_button = QPushButton("Atualizar Painel")
        self.refresh_button.clicked.connect(self.refresh)
        layout.addWidget(self.refresh_button, alignment=Qt.AlignRight)

    def _create_card(self, title, color):
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: #112240; border: 1px solid {color}44; "
            f"border-left: 4px solid {color}; border-radius: 8px; padding: 8px; }}"
        )
        card_layout = QVBoxLayout(card)
        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold; background: transparent; border: none;")
        value_label = QLabel("-")
        value_label.setWordWrap(True)
        value_label.setStyleSheet("color: #cfd8dc; font-size: 18px; font-weight: bold; background: transparent; border: none;")
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        return card, value_label

    def _style_table(self, table):
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setAlternatingRowColors(True)
        table.setStyleSheet(
            "QTableWidget { background-color: #112240; color: #cfd8dc; "
            "gridline-color: #1e3a5f; border: 1px solid #1e3a5f; }"
            "QHeaderView::section { background-color: #1e3f6e; color: #cfd8dc; "
            "font-weight: bold; border: 1px solid #1e3a5f; padding: 4px; }"
        )

    def _style_explanatory_table(self, table, compact_columns, long_columns):
        header = table.horizontalHeader()
        for column_index in compact_columns:
            header.setSectionResizeMode(column_index, QHeaderView.ResizeToContents)
        for column_index in long_columns:
            header.setSectionResizeMode(column_index, QHeaderView.Stretch)
        table.setWordWrap(True)

    def refresh(self):
        snapshot = self.service.build_snapshot()
        self.status_label.setText(snapshot.executive_status)
        self.score_label.setText(f"{snapshot.water_health_score}/100\n{snapshot.water_health_status}")
        self.open_label.setText(str(snapshot.open_events))
        self.monitoring_label.setText(str(snapshot.monitoring_events))
        self.resolved_label.setText(str(snapshot.resolved_events))
        self.message_label.setText(
            f"{snapshot.executive_message}\n" + "\n".join(snapshot.explanations[:3])
        )
        self._apply_status_style(snapshot.executive_status)
        self._load_recommendations(snapshot.recommendation_snapshot)
        self._load_priorities(snapshot.observational_priorities)
        self._load_signals(snapshot.relevant_alerts, snapshot.key_trends)

    def _load_recommendations(self, recommendation_snapshot):
        recommendations = []
        if recommendation_snapshot is not None:
            recommendations = recommendation_snapshot.recommendations

        self.recommendations_table.setRowCount(len(recommendations))
        for row_index, recommendation in enumerate(recommendations):
            priority = self._enum_value(recommendation.priority)
            values = [
                priority,
                recommendation.recommendation,
                recommendation.rationale,
                self._format_optional_value(getattr(recommendation, "confidence", None)),
                self._format_recommendation_evidence(recommendation.evidence),
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index in (1, 2, 4):
                    item.setToolTip(value)
                if column_index == 0:
                    self._apply_recommendation_priority_style(item, priority)
                self.recommendations_table.setItem(row_index, column_index, item)
        self.recommendations_table.resizeRowsToContents()

    def _load_priorities(self, priorities):
        self.priorities_table.setRowCount(len(priorities))
        for row_index, priority in enumerate(priorities):
            values = [priority.level, priority.title, priority.source, priority.evidence, priority.recommendation]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index in (1, 3, 4):
                    item.setToolTip(value)
                if column_index == 0:
                    self._apply_level_style(item, priority.level)
                self.priorities_table.setItem(row_index, column_index, item)
        self.priorities_table.resizeRowsToContents()

    def _format_recommendation_evidence(self, evidences):
        if not evidences:
            return "-"

        descriptions = []
        for evidence in evidences:
            value = ""
            if evidence.value is not None:
                value = f"={evidence.value}"
            descriptions.append(
                f"{evidence.source}:{evidence.metric}{value} - {evidence.description}"
            )
        return " | ".join(descriptions)

    def _format_optional_value(self, value):
        if value is None:
            return "-"
        return str(value)

    def _enum_value(self, value):
        return getattr(value, "value", str(value))

    def _load_signals(self, alerts, trends):
        rows = []
        for alert in alerts:
            rows.append(("Alerta", alert.domain, alert.metric, f"{alert.message} | {alert.evidence}"))
        for trend in trends:
            rows.append(("Tendencia", trend.domain, trend.metric, trend.explanation))

        self.signals_table.setRowCount(len(rows))
        for row_index, values in enumerate(rows):
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index == 3:
                    item.setToolTip(value)
                if column_index == 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.signals_table.setItem(row_index, column_index, item)
        self.signals_table.resizeRowsToContents()

    def _apply_status_style(self, status):
        colors = {
            EXECUTIVE_NORMAL: "#1b5e20",
            EXECUTIVE_ATTENTION: "#8a6d1d",
            EXECUTIVE_CRITICAL: "#8e2430",
        }
        color = colors.get(status, "#4fc3f7")
        self.status_card.setStyleSheet(
            f"QFrame {{ background-color: #112240; border: 1px solid {color}44; "
            f"border-left: 4px solid {color}; border-radius: 8px; padding: 8px; }}"
        )

    def _apply_level_style(self, item, level):
        colors = {
            "baixo": "#1e3f6e",
            "medio": "#8a6d1d",
            "alto": "#8e2430",
        }
        item.setBackground(QColor(colors.get(level, "#112240")))
        item.setForeground(QColor("#ffffff"))
        item.setTextAlignment(Qt.AlignCenter)

    def _apply_recommendation_priority_style(self, item, priority):
        colors = {
            "LOW": "#1e3f6e",
            "LOW_CONTROLLED": "#1e3f6e",
            "MEDIUM": "#8a6d1d",
            "HIGH": "#8e2430",
            "UNKNOWN": "#455a64",
        }
        item.setBackground(QColor(colors.get(priority, "#112240")))
        item.setForeground(QColor("#ffffff"))
        item.setTextAlignment(Qt.AlignCenter)
