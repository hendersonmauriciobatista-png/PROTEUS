import csv
import sys
from pathlib import Path

from PyQt5.QtCore import Qt, QDateTime, QTimer
from PyQt5.QtGui import QColor, QPalette
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

from consumo_distribuicao import ConsumoDistribuicaoPage
from dados_ambientais import DadosAmbientaisPage
from governanca_operacional import GovernancaOperacionalPage
from previsao_analitica import PrevisaoAnaliticaPage
from qualidade_agua import QualidadeAguaPage
from relatorios import RelatoriosPage


DATA_DIR = Path(__file__).resolve().parent / "data"
QUALIDADE_CSV = DATA_DIR / "qualidade_agua_medicoes.csv"
AMBIENTE_CSV = DATA_DIR / "dados_ambientais_medicoes.csv"
CONSUMO_CSV = DATA_DIR / "consumo_distribuicao_medicoes.csv"


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


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
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
        info_label = QLabel("Dados consolidados a partir dos CSVs locais. Gráficos serão adicionados em etapa futura.")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("color: #546e7a; font-size: 14px;")
        info_layout.addWidget(info_label)
        layout.addWidget(info)
        layout.addStretch()
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
        qualidade_rows = self._read_csv(QUALIDADE_CSV)
        ambiente_rows = self._read_csv(AMBIENTE_CSV)
        consumo_rows = self._read_csv(CONSUMO_CSV)

        self.cards[0][1].setText(self._format_qualidade(qualidade_rows))
        self.cards[1][1].setText(self._format_ambiente(ambiente_rows))
        self.cards[2][1].setText(self._format_consumo(consumo_rows))
        self.cards[3][1].setText(
            f"Água: {len(qualidade_rows)}\n"
            f"Ambiente: {len(ambiente_rows)}\n"
            f"Consumo: {len(consumo_rows)}"
        )

    def _read_csv(self, path):
        if not path.exists():
            return []

        with path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

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
        checks = [
            (self._to_float(row.get("ph")), 6.0, 9.0),
            (self._to_float(row.get("turbidez")), 0.0, 5.0),
            (self._to_float(row.get("oxigenio_dissolvido")), 5.0, 10.0),
            (self._to_float(row.get("temperatura")), 15.0, 30.0),
            (self._to_float(row.get("agrotoxicos")), 0.0, 0.1),
        ]

        for value, minimum, maximum in checks:
            if value < minimum or value > maximum:
                return "Fora do padrão"
        return "Dentro do padrão"

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
        self.setWindowTitle("Sistema de Análise de Água v1.0")
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
        logo = QLabel("AquaAnalysis")
        logo.setObjectName("logo")
        logo_sub = QLabel("SISTEMA DE ANÁLISE")
        logo_sub.setObjectName("logo_sub")
        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(logo_sub)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #1e3a5f; max-height: 1px; margin: 5px 15px;")
        sidebar_layout.addWidget(sep)

        self.nav_buttons = []
        nav_items = [
            ("Dashboard", 0),
            ("Qualidade da Água", 1),
            ("Consumo e Distribuição", 2),
            ("Dados Ambientais", 3),
            ("Relatórios", 4),
            ("Previsao Analitica", 5),
            ("Governanca Operacional", 6),
        ]
        for label, index in nav_items:
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
        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(QualidadeAguaPage())
        self.stack.addWidget(ConsumoDistribuicaoPage())
        self.stack.addWidget(DadosAmbientaisPage())
        self.stack.addWidget(RelatoriosPage())
        self.stack.addWidget(PrevisaoAnaliticaPage())
        self.stack.addWidget(GovernancaOperacionalPage())
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
