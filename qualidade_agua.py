from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QColor

from data_access import (
    MeasurementRepository,
    QUALITY_WATER_CSV_PATH,
    QUALITY_WATER_FIELDS,
    build_quality_water_repository,
)
from monitoramento_hidrico import carregar_projeto_ativo
from monitoramento_hidrico.application_context import HydricApplicationContext
from monitoramento_hidrico.qualidade_agua_adapter import (
    STATUS_QUALIDADE_OBSERVACIONAL_ATENCAO,
    STATUS_QUALIDADE_OBSERVACIONAL_NAO_AVALIAVEL,
    STATUS_QUALIDADE_OBSERVACIONAL_NORMAL,
    QualidadeAguaApplicationService,
    QualidadeAguaMonitoringAdapter,
)


DATA_FILE = QUALITY_WATER_CSV_PATH
CSV_FIELDS = list(QUALITY_WATER_FIELDS)

class QualidadeAguaPage(QWidget):
    def __init__(self, repository: MeasurementRepository = None, application_context=None):
        super().__init__()
        self.inputs = {}
        self.repository = repository or build_quality_water_repository()
        self.application_context = application_context or self._load_application_context()
        self.monitoring_adapter = self.application_context.build_policy_adapter(
            QualidadeAguaMonitoringAdapter
        )
        self.quality_service = QualidadeAguaApplicationService(
            repository=self.repository,
            monitoring_adapter=self.monitoring_adapter,
        )
        self._build_ui()
        self.load_history()

    def _load_application_context(self):
        projeto_ativo = carregar_projeto_ativo()
        return HydricApplicationContext.from_active_profile(projeto_ativo.perfil_operacional)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title = QLabel("Qualidade da Água")
        title.setObjectName("page_title")
        subtitle = QLabel("Cadastro manual e histórico de medições persistidas em CSV")
        subtitle.setObjectName("page_subtitle")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        form_frame = QFrame()
        form_frame.setStyleSheet(
            "QFrame { background-color: #112240; border: 1px solid #1e3a5f; "
            "border-radius: 8px; padding: 10px; }"
        )
        form_layout = QFormLayout(form_frame)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setHorizontalSpacing(16)
        form_layout.setVerticalSpacing(10)

        self.inputs["ph"] = self._make_spinbox(0.0, 14.0, 7.0, 2, 0.1)
        self.inputs["turbidez"] = self._make_spinbox(0.0, 1000.0, 0.0, 2, 0.1)
        self.inputs["oxigenio_dissolvido"] = self._make_spinbox(0.0, 30.0, 5.0, 2, 0.1)
        self.inputs["temperatura"] = self._make_spinbox(-10.0, 60.0, 25.0, 2, 0.1)
        self.inputs["agrotoxicos"] = self._make_spinbox(0.0, 100.0, 0.0, 4, 0.01)
        self.default_values = {
            "ph": 7.0,
            "turbidez": 0.0,
            "oxigenio_dissolvido": 5.0,
            "temperatura": 25.0,
            "agrotoxicos": 0.0,
        }

        form_layout.addRow("pH", self.inputs["ph"])
        form_layout.addRow("Turbidez (NTU)", self.inputs["turbidez"])
        form_layout.addRow("Oxigênio Dissolvido - OD (mg/L)", self.inputs["oxigenio_dissolvido"])
        form_layout.addRow("Temperatura (°C)", self.inputs["temperatura"])
        form_layout.addRow("Agrotóxicos (mg/L)", self.inputs["agrotoxicos"])

        self.save_button = QPushButton("Salvar Medição")
        self.save_button.clicked.connect(self.save_measurement)
        self.clear_button = QPushButton("Limpar Campos")
        self.clear_button.clicked.connect(self.clear_fields)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)
        form_layout.addRow("", button_layout)
        layout.addWidget(form_frame)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Timestamp", "pH", "Turbidez", "OD", "Temperatura", "Agrotóxicos", "Status"]
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

    def _make_spinbox(self, minimum, maximum, value, decimals, step):
        field = QDoubleSpinBox()
        field.setRange(minimum, maximum)
        field.setValue(value)
        field.setDecimals(decimals)
        field.setSingleStep(step)
        field.setStyleSheet(
            "QDoubleSpinBox { background-color: #0d1b2a; color: #cfd8dc; "
            "border: 1px solid #1e3a5f; border-radius: 4px; padding: 4px; }"
        )
        return field

    def save_measurement(self):
        measurement = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "ph": self.inputs["ph"].value(),
            "turbidez": self.inputs["turbidez"].value(),
            "oxigenio_dissolvido": self.inputs["oxigenio_dissolvido"].value(),
            "temperatura": self.inputs["temperatura"].value(),
            "agrotoxicos": self.inputs["agrotoxicos"].value(),
        }

        try:
            self.quality_service.salvar_medicao(measurement)
            self.load_history()
            QMessageBox.information(self, "Medição salva", "Medição salva com sucesso")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao salvar", f"Erro ao salvar medição: {error}")

    def clear_fields(self):
        for field_name, default_value in self.default_values.items():
            self.inputs[field_name].setValue(default_value)

    def load_history(self):
        rows = self.quality_service.listar_medicoes()
        rows.reverse()
        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            values = self._parse_row(row)
            status = self.quality_service.status_medicao(values)
            display_values = [
                row.get("timestamp", ""),
                f"{values['ph']:.2f}",
                f"{values['turbidez']:.2f} NTU",
                f"{values['oxigenio_dissolvido']:.2f} mg/L",
                f"{values['temperatura']:.2f} °C",
                f"{values['agrotoxicos']:.4f} mg/L",
                status,
            ]

            for column_index, value in enumerate(display_values):
                item = QTableWidgetItem(value)
                if column_index == 6:
                    item.setTextAlignment(Qt.AlignCenter)
                    self._apply_status_style(item, status)
                self.table.setItem(row_index, column_index, item)

    def refresh(self):
        self.load_history()

    def _apply_status_style(self, item, status):
        if status == STATUS_QUALIDADE_OBSERVACIONAL_NORMAL:
            item.setBackground(QColor("#1b5e20"))
            item.setForeground(QColor("#ffffff"))
            return

        if status == STATUS_QUALIDADE_OBSERVACIONAL_NAO_AVALIAVEL:
            item.setBackground(QColor("#455a64"))
            item.setForeground(QColor("#ffffff"))
            return

        if status == STATUS_QUALIDADE_OBSERVACIONAL_ATENCAO:
            item.setBackground(QColor("#e65100"))
            item.setForeground(QColor("#ffffff"))
            return

        item.setBackground(QColor("#8e2430"))
        item.setForeground(QColor("#ffffff"))

    def _parse_row(self, row):
        return {
            "ph": float(row.get("ph") or 0),
            "turbidez": float(row.get("turbidez") or 0),
            "oxigenio_dissolvido": float(row.get("oxigenio_dissolvido") or 0),
            "temperatura": float(row.get("temperatura") or 0),
            "agrotoxicos": float(row.get("agrotoxicos") or 0),
        }

