import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QDateTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPen, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from analytics.dashboard_snapshot import DashboardAnalyticsSnapshotService
from administracao import AdministracaoPage
from consumo_distribuicao import ConsumoDistribuicaoPage
from data_access import CSVMeasurementRepository, build_quality_water_repository
from dados_ambientais import DadosAmbientaisPage
from governanca_operacional import GovernancaOperacionalPage
from monitoramento_hidrico import carregar_projeto_ativo
from monitoramento_hidrico.application_context import HydricApplicationContext
from monitoramento_hidrico.dashboard_adapter import DashboardMonitoringAdapter
from painel_executivo import PainelExecutivoPage
from previsao_analitica import PrevisaoAnaliticaPage
from projeto_monitoramento_page import ProjetoMonitoramentoPage
from qualidade_agua import QualidadeAguaPage
from relatorios import RelatoriosPage


DATA_DIR = Path(__file__).resolve().parent / "data"
AMBIENTE_CSV = DATA_DIR / "dados_ambientais_medicoes.csv"
CONSUMO_CSV = DATA_DIR / "consumo_distribuicao_medicoes.csv"
AMBIENTE_FIELDS = (
    "timestamp",
    "temperatura_ambiente",
    "umidade_relativa",
    "chuva",
    "pressao_atmosferica",
    "observacao",
)
CONSUMO_FIELDS = (
    "timestamp",
    "consumo_diario",
    "consumo_mensal",
    "volume_distribuido",
    "perdas_estimadas",
    "observacao",
)


STYLE_MAIN = """
QMainWindow { background-color: #0d1b2a; }
QWidget#central { background-color: #0d1b2a; }

QFrame#sidebar {
    background-color: #112240;
    border-right: 2px solid #1e3a5f;
    min-width: 220px; max-width: 220px;
}
QLabel#logo { color: #4fc3f7; font-size: 18px; font-weight: bold; padding: 20px 10px 5px 10px; }
QLabel#logo_sub { color: #78909c; font-size: 10px; padding: 0px 10px 20px 10px; }

QPushButton#nav_btn {
    background-color: transparent; color: #b0bec5;
    border: none; text-align: left; padding: 12px 20px;
    font-size: 13px; border-left: 3px solid transparent;
}
QPushButton#nav_btn:hover { background-color: #1a3558; color: #4fc3f7; border-left: 3px solid #4fc3f7; }
QPushButton#nav_btn:checked { background-color: #1e3f6e; color: #4fc3f7; border-left: 3px solid #4fc3f7; font-weight: bold; }

QFrame#content_area { background-color: #0d1b2a; }
QStatusBar { background-color: #112240; color: #78909c; font-size: 11px; border-top: 1px solid #1e3a5f; }
QLabel { color: #cfd8dc; }
QLabel#page_title { color: #4fc3f7; font-size: 22px; font-weight: bold; padding: 10px 0; }
QLabel#page_subtitle { color: #78909c; font-size: 12px; padding-bottom: 15px; }
"""


class WaterHealthScoreChart(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.setMinimumHeight(230)

    def set_points(self, points):
        self.points = list(points)
        self.update()

    def paintEvent(self, _event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor("#112240"))

        if len(self.points) < 2:
            painter.setPen(QColor("#78909c"))
            painter.drawText(
                self.rect(),
                Qt.AlignCenter,
                "Historico insuficiente para exibir a evolucao do Water Health Score.\n"
                "Registre ao menos duas medicoes de qualidade da agua.",
            )
            return

        left = 48
        top = 18
        right = 18
        bottom = 38
        width = max(1, self.width() - left - right)
        height = max(1, self.height() - top - bottom)
        x0 = left
        y0 = top + height

        grid_pen = QPen(QColor("#1e3a5f"))
        axis_pen = QPen(QColor("#78909c"))
        text_color = QColor("#90a4ae")
        line_pen = QPen(QColor("#4fc3f7"), 2)

        painter.setPen(grid_pen)
        for value in (0, 25, 50, 75, 100):
            y = y0 - int((value / 100) * height)
            painter.drawLine(x0, y, x0 + width, y)
            painter.setPen(text_color)
            painter.drawText(8, y + 4, f"{value}")
            painter.setPen(grid_pen)

        painter.setPen(axis_pen)
        painter.drawLine(x0, top, x0, y0)
        painter.drawLine(x0, y0, x0 + width, y0)

        coordinates = []
        denominator = max(1, len(self.points) - 1)
        for index, point in enumerate(self.points):
            score = max(0, min(100, int(point["score"])))
            x = x0 + int((index / denominator) * width)
            y = y0 - int((score / 100) * height)
            coordinates.append((x, y, score, point["label"]))

        painter.setPen(line_pen)
        for index in range(1, len(coordinates)):
            previous = coordinates[index - 1]
            current = coordinates[index]
            painter.drawLine(previous[0], previous[1], current[0], current[1])

        for x, y, score, _label in coordinates:
            painter.setBrush(QColor(self._score_color(score)))
            painter.setPen(QColor("#0d1b2a"))
            painter.drawEllipse(x - 4, y - 4, 8, 8)

        painter.setPen(text_color)
        label_indexes = sorted({0, len(coordinates) // 2, len(coordinates) - 1})
        for index in label_indexes:
            x, _y, _score, label = coordinates[index]
            painter.drawText(x - 26, y0 + 18, 52, 18, Qt.AlignCenter, label)

        last_x, last_y, last_score, _last_label = coordinates[-1]
        painter.setPen(QColor("#cfd8dc"))
        painter.drawText(last_x - 42, last_y - 24, 84, 18, Qt.AlignCenter, f"{last_score}/100")

    def _score_color(self, score):
        if score >= 85:
            return "#66bb6a"
        if score >= 70:
            return "#9ccc65"
        if score >= 50:
            return "#ffa726"
        return "#ef5350"


class DashboardPage(QWidget):
    def __init__(
        self,
        quality_repository,
        environment_repository,
        consumption_repository,
        application_context,
    ):
        super().__init__()
        self.quality_repository = quality_repository
        self.environment_repository = environment_repository
        self.consumption_repository = consumption_repository
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        title = QLabel("Visão Geral do Sistema")
        title.setObjectName("page_title")
        subtitle = QLabel("Painel consolidado dos módulos funcionais")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        cards_layout = QHBoxLayout()
        self.cards = [
            self._create_card("Qualidade da Água", "#4fc3f7"),
            self._create_card("Dados Ambientais", "#ffa726"),
            self._create_card("Consumo", "#66bb6a"),
            self._create_card("Total de Registros", "#ab47bc"),
        ]
        for card, _value_label in self.cards:
            cards_layout.addWidget(card)
        layout.addLayout(cards_layout)

        info = QFrame()
        info.setStyleSheet(
            "QFrame { background-color: #112240; border: 1px solid #1e3a5f; "
            "border-radius: 10px; min-height: 250px; }"
        )
        info_layout = QVBoxLayout(info)
        chart_title = QLabel("Evolucao do Water Health Score")
        chart_title.setStyleSheet("color: #4fc3f7; font-weight: bold; background: transparent; border: none;")
        self.score_chart = WaterHealthScoreChart()
        info_layout.addWidget(chart_title)
        info_layout.addWidget(self.score_chart)
        layout.addWidget(info)
        layout.addStretch()
        self.monitoring_adapter = application_context.build_policy_adapter(
            DashboardMonitoringAdapter
        )
        self.dashboard_analytics = DashboardAnalyticsSnapshotService()
        self.refresh()

    def _create_card(self, title, color):
        card = QFrame()
        card.setStyleSheet(
            f"QFrame {{ background-color: #112240; border: 1px solid {color}44; "
            f"border-left: 4px solid {color}; border-radius: 10px; padding: 5px; }}"
        )
        card_layout = QVBoxLayout(card)
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-weight: bold; background: transparent; border: none;")
        value_label = QLabel("Sem registros")
        value_label.setWordWrap(True)
        value_label.setStyleSheet("color: #cfd8dc; background: transparent; border: none;")
        card_layout.addWidget(title_label)
        card_layout.addWidget(value_label)
        return card, value_label

    def refresh(self):
        qualidade_rows = self.quality_repository.read_all()
        ambiente_rows = self.environment_repository.read_all()
        consumo_rows = self.consumption_repository.read_all()

        self.cards[0][1].setText(self._format_qualidade(qualidade_rows))
        self.cards[1][1].setText(self._format_ambiente(ambiente_rows))
        self.cards[2][1].setText(self._format_consumo(consumo_rows))
        self.cards[3][1].setText(
            f"Água: {len(qualidade_rows)}\n"
            f"Ambiente: {len(ambiente_rows)}\n"
            f"Consumo: {len(consumo_rows)}"
        )
        self.score_chart.set_points(self.dashboard_analytics.water_health_score_series())

    def _format_qualidade(self, rows):
        if not rows:
            return "Sem registros"

        latest = rows[-1]
        ph = self._to_float(latest.get("ph"))
        return f"pH: {ph:.2f}\nStatus: {self._quality_status(latest)}"

    def _format_ambiente(self, rows):
        if not rows:
            return "Sem registros"

        latest = rows[-1]
        temperatura = self._to_float(latest.get("temperatura_ambiente"))
        umidade = self._to_float(latest.get("umidade_relativa"))
        return f"Temperatura: {temperatura:.2f} °C\nUmidade: {umidade:.2f} %"

    def _format_consumo(self, rows):
        if not rows:
            return "Sem registros"

        latest = rows[-1]
        consumo_diario = self._to_float(latest.get("consumo_diario"))
        perdas = self._to_float(latest.get("perdas_estimadas"))
        return f"Consumo diário: {consumo_diario:.2f} m³\nPerdas: {perdas:.2f} %"

    def _quality_status(self, row):
        return self.monitoring_adapter.quality_status(row)

    def _to_float(self, value):
        try:
            return float(value or 0)
        except ValueError:
            return 0.0


def make_placeholder_page(icon, title, subtitle, desc):
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(30, 20, 30, 20)
    title_label = QLabel(f"{icon} {title}")
    title_label.setObjectName("page_title")
    subtitle_label = QLabel(subtitle)
    subtitle_label.setObjectName("page_subtitle")
    info_label = QLabel(desc)
    info_label.setAlignment(Qt.AlignCenter)
    info_label.setStyleSheet("color: #546e7a; font-size: 13px; padding: 60px;")
    layout.addWidget(title_label)
    layout.addWidget(subtitle_label)
    layout.addWidget(info_label)
    layout.addStretch()
    return page


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        projeto_ativo = carregar_projeto_ativo()
        self.hydric_application_context = HydricApplicationContext.from_active_profile(
            projeto_ativo.perfil_operacional
        )
        self.quality_water_repository = build_quality_water_repository()
        self.environment_repository = CSVMeasurementRepository(AMBIENTE_CSV, AMBIENTE_FIELDS)
        self.consumption_repository = CSVMeasurementRepository(CONSUMO_CSV, CONSUMO_FIELDS)
        self.setWindowTitle("PROTEUS")
        self.setMinimumSize(1100, 700)
        self.resize(1280, 780)
        self.setStyleSheet(STYLE_MAIN)
        self._build_ui()
        self._start_clock()

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        logo = QLabel("PROTEUS")
        logo.setObjectName("logo")
        logo_sub = QLabel("MONITORAMENTO INTELIGENTE DA ÁGUA")
        logo_sub.setObjectName("logo_sub")
        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(logo_sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #1e3a5f; max-height: 1px; margin: 5px 15px;")
        sidebar_layout.addWidget(sep)

        self.nav_buttons = []
        nav_items = [
            ("Projeto de Monitoramento", 0),
            ("Dashboard", 1),
            ("Painel Executivo", 2),
            ("Qualidade da Água", 2),
            ("Consumo e Distribuição", 3),
            ("Dados Ambientais", 4),
            ("Relatórios", 5),
            ("Previsao Analitica", 7),
            ("Governanca Operacional", 8),
            ("Administração", 9),
        ]
        for index, item in enumerate(nav_items):
            label = item[0]
            button = QPushButton(label)
            button.setObjectName("nav_btn")
            button.setCheckable(True)
            button.clicked.connect(lambda _, i=index: self._navigate(i))
            sidebar_layout.addWidget(button)
            self.nav_buttons.append(button)

        sidebar_layout.addStretch()
        version = QLabel("v1.0 · Build 2026")
        version.setStyleSheet("color: #37474f; font-size: 10px; padding: 10px 20px;")
        sidebar_layout.addWidget(version)
        main_layout.addWidget(sidebar)

        content = QFrame()
        content.setObjectName("content_area")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        self.stack.addWidget(ProjetoMonitoramentoPage())
        self.stack.addWidget(
            DashboardPage(
                quality_repository=self.quality_water_repository,
                environment_repository=self.environment_repository,
                consumption_repository=self.consumption_repository,
                application_context=self.hydric_application_context,
            )
        )
        self.stack.addWidget(PainelExecutivoPage())
        self.stack.addWidget(
            QualidadeAguaPage(
                repository=self.quality_water_repository,
                application_context=self.hydric_application_context,
            )
        )
        self.stack.addWidget(ConsumoDistribuicaoPage())
        self.stack.addWidget(DadosAmbientaisPage())
        self.stack.addWidget(RelatoriosPage())
        self.stack.addWidget(PrevisaoAnaliticaPage())
        self.stack.addWidget(GovernancaOperacionalPage())
        self.stack.addWidget(AdministracaoPage())
        content_layout.addWidget(self.stack)
        main_layout.addWidget(content)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.clock_label = QLabel()
        self.status_bar.addPermanentWidget(self.clock_label)
        self.status_bar.showMessage("Sistema iniciado · Todos os módulos carregados")
        self._navigate(0)

    def _navigate(self, index):
        self.stack.setCurrentIndex(index)
        current_page = self.stack.currentWidget()
        if hasattr(current_page, "refresh"):
            current_page.refresh()
        for i, button in enumerate(self.nav_buttons):
            button.setChecked(i == index)

    def _start_clock(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        now = QDateTime.currentDateTime().toString("dd/MM/yyyy  hh:mm:ss")
        self.clock_label.setText(f"{now}  ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0d1b2a"))
    palette.setColor(QPalette.WindowText, QColor("#cfd8dc"))
    palette.setColor(QPalette.Base, QColor("#112240"))
    palette.setColor(QPalette.Text, QColor("#cfd8dc"))
    palette.setColor(QPalette.Button, QColor("#112240"))
    palette.setColor(QPalette.ButtonText, QColor("#cfd8dc"))
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
