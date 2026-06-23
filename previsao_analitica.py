from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QColor

from analytics import AnalyticsService


class PrevisaoAnaliticaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.analytics_service = AnalyticsService()
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title = QLabel("Previsao Analitica")
        title.setObjectName("page_title")
        subtitle = QLabel("Tendencias deterministicas, alertas preventivos e Water Health Score")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.score_card = QFrame()
        self.score_card.setStyleSheet(
            "QFrame { background-color: #112240; border: 1px solid #4fc3f744; "
            "border-left: 4px solid #4fc3f7; border-radius: 8px; padding: 10px; }"
        )
        score_layout = QVBoxLayout(self.score_card)
        self.score_label = QLabel("Water Health Score: --")
        self.score_label.setStyleSheet("color: #4fc3f7; font-size: 20px; font-weight: bold;")
        self.score_explanation = QLabel("")
        self.score_explanation.setWordWrap(True)
        self.score_explanation.setStyleSheet("color: #cfd8dc;")
        score_layout.addWidget(self.score_label)
        score_layout.addWidget(self.score_explanation)
        layout.addWidget(self.score_card)

        self.trends_table = QTableWidget()
        self.trends_table.setColumnCount(5)
        self.trends_table.setHorizontalHeaderLabels(["Dominio", "Metrica", "Tendencia", "Media anterior", "Media recente"])
        self._style_table(self.trends_table)
        layout.addWidget(self.trends_table)

        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(5)
        self.alerts_table.setHorizontalHeaderLabels(["Severidade", "Dominio", "Metrica", "Mensagem", "Evidencia"])
        self._style_table(self.alerts_table)
        layout.addWidget(self.alerts_table)

        self.refresh_button = QPushButton("Atualizar Analise")
        self.refresh_button.clicked.connect(self.refresh)
        layout.addWidget(self.refresh_button, alignment=Qt.AlignRight)

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

    def refresh(self):
        snapshot = self.analytics_service.build_snapshot()
        score = snapshot.water_health_score
        self.score_label.setText(f"Water Health Score: {score.score}/100 - {score.status}")
        self.score_explanation.setText("\n".join(score.explanations[:4]))
        self._load_trends(snapshot.quality_trends + snapshot.consumption_trends)
        self._load_alerts(snapshot.alerts)

    def _load_trends(self, trends):
        self.trends_table.setRowCount(len(trends))
        for row_index, trend in enumerate(trends):
            values = [
                trend.domain,
                trend.metric,
                trend.direction,
                self._format_optional(trend.previous_average),
                self._format_optional(trend.recent_average),
            ]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index == 2:
                    self._apply_trend_style(item, trend.direction)
                if column_index in (3, 4):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.trends_table.setItem(row_index, column_index, item)

    def _load_alerts(self, alerts):
        self.alerts_table.setRowCount(len(alerts))
        for row_index, alert in enumerate(alerts):
            values = [alert.severity, alert.domain, alert.metric, alert.message, alert.evidence]
            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column_index == 0:
                    self._apply_alert_style(item, alert.severity)
                    item.setTextAlignment(Qt.AlignCenter)
                self.alerts_table.setItem(row_index, column_index, item)

    def _apply_trend_style(self, item, direction):
        colors = {
            "subindo": "#1e3f6e",
            "caindo": "#455a64",
            "estavel": "#1b5e20",
            "dados_insuficientes": "#5d4037",
        }
        item.setBackground(QColor(colors.get(direction, "#112240")))
        item.setForeground(QColor("#ffffff"))
        item.setTextAlignment(Qt.AlignCenter)

    def _apply_alert_style(self, item, severity):
        colors = {
            "baixo": "#1e3f6e",
            "medio": "#8a6d1d",
            "alto": "#8e2430",
        }
        item.setBackground(QColor(colors.get(severity, "#112240")))
        item.setForeground(QColor("#ffffff"))

    def _format_optional(self, value):
        if value is None:
            return "-"
        return f"{value:.4f}"
