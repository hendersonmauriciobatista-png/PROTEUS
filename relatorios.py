import csv
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from monitoramento_hidrico import AvaliacaoObservacionalService, PolicyEngine
from monitoramento_hidrico.operational_reports_adapter import OperationalReportsHydricMonitoringAdapter


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORTS_DIR / "relatorio_operacional.txt"

QUALIDADE_CSV = DATA_DIR / "qualidade_agua_medicoes.csv"
AMBIENTE_CSV = DATA_DIR / "dados_ambientais_medicoes.csv"
CONSUMO_CSV = DATA_DIR / "consumo_distribuicao_medicoes.csv"


class RelatoriosPage(QWidget):
    def __init__(self):
        super().__init__()
        self.current_report = ""
        self.monitoring_adapter = OperationalReportsHydricMonitoringAdapter(
            policy_engine=PolicyEngine(),
            evaluation_service=AvaliacaoObservacionalService(),
        )
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title = QLabel("RelatÃ³rios")
        title.setObjectName("page_title")
        subtitle = QLabel("Resumo operacional consolidado em modo somente leitura")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        report_frame = QFrame()
        report_frame.setStyleSheet(
            "QFrame { background-color: #112240; border: 1px solid #1e3a5f; "
            "border-radius: 8px; padding: 8px; }"
        )
        report_layout = QVBoxLayout(report_frame)

        self.report_view = QTextEdit()
        self.report_view.setReadOnly(True)
        self.report_view.setStyleSheet(
            "QTextEdit { background-color: #0d1b2a; color: #cfd8dc; "
            "border: 1px solid #1e3a5f; border-radius: 4px; padding: 8px; "
            "font-family: Consolas, monospace; font-size: 12px; }"
        )
        report_layout.addWidget(self.report_view)
        layout.addWidget(report_frame)

        self.export_button = QPushButton("Exportar RelatÃ³rio TXT")
        self.export_button.clicked.connect(self.export_report)
        layout.addWidget(self.export_button, alignment=Qt.AlignRight)

    def refresh(self):
        self.current_report = self._build_report()
        self.report_view.setPlainText(self.current_report)

    def export_report(self):
        try:
            REPORTS_DIR.mkdir(parents=True, exist_ok=True)
            REPORT_FILE.write_text(self.current_report, encoding="utf-8")
            QMessageBox.information(self, "RelatÃ³rio exportado", f"RelatÃ³rio salvo em:\n{REPORT_FILE}")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao exportar", f"Erro ao exportar relatÃ³rio: {error}")

    def _build_report(self):
        qualidade_rows = self._read_csv(QUALIDADE_CSV)
        ambiente_rows = self._read_csv(AMBIENTE_CSV)
        consumo_rows = self._read_csv(CONSUMO_CSV)
        registros_observacionais_atencao = self.monitoring_adapter.contar_observacional_atencao(qualidade_rows)

        lines = [
            "RELATÃ“RIO OPERACIONAL",
            f"Gerado em: {datetime.now().isoformat(timespec='seconds')}",
            "",
            "TOTAL DE REGISTROS",
            f"- Ãgua: {len(qualidade_rows)}",
            f"- Ambiente: {len(ambiente_rows)}",
            f"- Consumo: {len(consumo_rows)}",
            "",
            "ÃšLTIMAS MEDIÃ‡Ã•ES",
            f"- Ãgua: {self._format_latest_quality(qualidade_rows)}",
            f"- Ambiente: {self._format_latest_environment(ambiente_rows)}",
            f"- Consumo: {self._format_latest_consumption(consumo_rows)}",
            "",
            "QUALIDADE DA ÃGUA",
            f"- Registros com avaliacao observacional em atencao: {registros_observacionais_atencao}",
            f"- MÃ©dia de pH: {self._format_average(qualidade_rows, 'ph')}",
            f"- MÃ©dia de turbidez: {self._format_average(qualidade_rows, 'turbidez')}",
            f"- MÃ©dia de temperatura da Ã¡gua: {self._format_average(qualidade_rows, 'temperatura')}",
        ]
        return "\n".join(lines)

    def _read_csv(self, path):
        if not path.exists():
            return []

        with path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def _format_latest_quality(self, rows):
        if not rows:
            return "Sem registros"

        latest = rows[-1]
        return (
            f"{latest.get('timestamp', '')} | "
            f"pH {self._to_float(latest.get('ph')):.2f} | "
            f"Turbidez {self._to_float(latest.get('turbidez')):.2f} | "
            f"Status {self.monitoring_adapter.status_linha(latest)}"
        )

    def _format_latest_environment(self, rows):
        if not rows:
            return "Sem registros"

        latest = rows[-1]
        return (
            f"{latest.get('timestamp', '')} | "
            f"Temperatura {self._to_float(latest.get('temperatura_ambiente')):.2f} Â°C | "
            f"Umidade {self._to_float(latest.get('umidade_relativa')):.2f} %"
        )

    def _format_latest_consumption(self, rows):
        if not rows:
            return "Sem registros"

        latest = rows[-1]
        return (
            f"{latest.get('timestamp', '')} | "
            f"Consumo diÃ¡rio {self._to_float(latest.get('consumo_diario')):.2f} mÂ³ | "
            f"Perdas {self._to_float(latest.get('perdas_estimadas')):.2f} %"
        )

    def _format_average(self, rows, field):
        values = [self._to_float(row.get(field)) for row in rows if row.get(field) not in (None, "")]
        if not values:
            return "Sem dados"
        return f"{sum(values) / len(values):.2f}"

    def _to_float(self, value):
        try:
            return float(value or 0)
        except ValueError:
            return 0.0

