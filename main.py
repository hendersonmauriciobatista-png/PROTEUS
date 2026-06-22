import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame, QStatusBar
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QPalette, QColor

# ─────────────────────────────────────────────
#  ESTILOS GLOBAIS
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
#  PÁGINAS DOS MÓDULOS
# ─────────────────────────────────────────────
class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)

        title = QLabel("🌊 Visão Geral do Sistema")
        title.setObjectName("page_title")
        subtitle = QLabel("Monitoramento em tempo real de todos os módulos")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        # Cards de resumo
        cards_layout = QHBoxLayout()
        cards = [
            ("💧", "Qualidade da Água", "pH: 7.2 | Turbidez: Normal", "#4fc3f7"),
            ("📊", "Consumo", "3.240 m³ hoje", "#66bb6a"),
            ("🌍", "Dados Ambientais", "12 sensores ativos", "#ffa726"),
            ("🤖", "Previsão ML", "Qualidade: BOA (94%)", "#ab47bc"),
        ]
        for icon, t, val, color in cards:
            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background-color: #112240; border: 1px solid {color}44; border-left: 4px solid {color}; border-radius: 10px; padding: 5px; }}")
            cl = QVBoxLayout(card)
            lbl1 = QLabel(f"{icon}  {t}")
            lbl1.setStyleSheet(f"color: {color}; font-weight: bold; background: transparent; border: none;")
            lbl2 = QLabel(val)
            lbl2.setStyleSheet("color: #cfd8dc; background: transparent; border: none;")
            cl.addWidget(lbl1); cl.addWidget(lbl2)
            cards_layout.addWidget(card)
        layout.addLayout(cards_layout)

        graph = QFrame()
        graph.setStyleSheet("QFrame { background-color: #112240; border: 1px solid #1e3a5f; border-radius: 10px; min-height: 250px; }")
        gl = QVBoxLayout(graph)
        gl_lbl = QLabel("📈  Gráfico de tendências (será integrado nos próximos módulos)")
        gl_lbl.setAlignment(Qt.AlignCenter)
        gl_lbl.setStyleSheet("color: #546e7a; font-size: 14px;")
        gl.addWidget(gl_lbl)
        layout.addWidget(graph)
        layout.addStretch()


def make_placeholder_page(icon, title, subtitle, desc):
    page = QWidget()
    layout = QVBoxLayout(page)
    layout.setContentsMargins(30, 20, 30, 20)
    t = QLabel(f"{icon} {title}"); t.setObjectName("page_title")
    s = QLabel(subtitle); s.setObjectName("page_subtitle")
    i = QLabel(desc); i.setAlignment(Qt.AlignCenter)
    i.setStyleSheet("color: #546e7a; font-size: 13px; padding: 60px;")
    layout.addWidget(t); layout.addWidget(s); layout.addWidget(i)
    layout.addStretch()
    return page


# ─────────────────────────────────────────────
#  JANELA PRINCIPAL
# ─────────────────────────────────────────────
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
        central = QWidget(); central.setObjectName("central")
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame(); sidebar.setObjectName("sidebar")
        sl = QVBoxLayout(sidebar); sl.setContentsMargins(0, 0, 0, 0); sl.setSpacing(0)
        logo = QLabel("💧 AquaAnalysis"); logo.setObjectName("logo")
        logo_sub = QLabel("SISTEMA DE ANÁLISE"); logo_sub.setObjectName("logo_sub")
        sl.addWidget(logo); sl.addWidget(logo_sub)

        sep = QFrame(); sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("background-color: #1e3a5f; max-height: 1px; margin: 5px 15px;")
        sl.addWidget(sep)

        self.nav_buttons = []
        nav_items = [
            ("🏠  Dashboard", 0), ("💧  Qualidade da Água", 1),
            ("📊  Consumo e Distribuição", 2), ("🌍  Dados Ambientais", 3),
            ("🤖  Previsão com ML", 4),
        ]
        for label, idx in nav_items:
            btn = QPushButton(label); btn.setObjectName("nav_btn"); btn.setCheckable(True)
            btn.clicked.connect(lambda _, i=idx: self._navigate(i))
            sl.addWidget(btn); self.nav_buttons.append(btn)

        sl.addStretch()
        ver = QLabel("v1.0 · Build 2026")
        ver.setStyleSheet("color: #37474f; font-size: 10px; padding: 10px 20px;")
        sl.addWidget(ver)
        main_layout.addWidget(sidebar)

        # Stack de páginas
        content = QFrame(); content.setObjectName("content_area")
        cl = QVBoxLayout(content); cl.setContentsMargins(0, 0, 0, 0)
        self.stack = QStackedWidget()
        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(make_placeholder_page("💧", "Qualidade da Água",
            "pH · Turbidez · Contaminantes · Alertas automáticos",
            "🔧 Módulo em desenvolvimento\nFormulários, leitura CSV, gráficos de pH/turbidez e alertas."))
        self.stack.addWidget(make_placeholder_page("📊", "Consumo e Distribuição",
            "Monitoramento de uso, perdas e distribuição regional",
            "🔧 Módulo em desenvolvimento\nConsumo por região, perdas na rede, relatórios."))
        self.stack.addWidget(make_placeholder_page("🌍", "Dados Ambientais",
            "Sensores IoT · APIs externas · Clima",
            "🔧 Módulo em desenvolvimento\nLeitura IoT, APIs de clima, mapa de sensores."))
        self.stack.addWidget(make_placeholder_page("🤖", "Previsão com ML",
            "Random Forest · LSTM · Previsão de qualidade e demanda",
            "🔧 Módulo em desenvolvimento\nTreinamento, previsões futuras, métricas de acurácia."))
        cl.addWidget(self.stack)
        main_layout.addWidget(content)

        # Status bar
        self.status_bar = QStatusBar(); self.setStatusBar(self.status_bar)
        self.clock_label = QLabel()
        self.status_bar.addPermanentWidget(self.clock_label)
        self.status_bar.showMessage("  ✅ Sistema iniciado · Todos os módulos carregados")
        self._navigate(0)

    def _navigate(self, index):
        self.stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def _start_clock(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_clock)
        self.timer.start(1000)
        self._update_clock()

    def _update_clock(self):
        now = QDateTime.currentDateTime().toString("dd/MM/yyyy  hh:mm:ss")
        self.clock_label.setText(f"🕐 {now}  ")


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