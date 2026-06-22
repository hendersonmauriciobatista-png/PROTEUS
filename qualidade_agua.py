import csv
from datetime import datetime
from pathlib import Path

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


DATA_FILE = Path(__file__).resolve().parent / "data" / "qualidade_agua_medicoes.csv"
CSV_FIELDS = [
    "timestamp",
    "ph",
    "turbidez",
    "oxigenio_dissolvido",
    "temperatura",
    "agrotoxicos",
]

CONAMA = {
    "pH": {"min": 6.0, "max": 9.0, "unidade": ""},
    "Turbidez": {"min": 0.0, "max": 5.0, "unidade": "NTU"},
    "OD": {"min": 5.0, "max": 10.0, "unidade": "mg/L"},
    "Temperatura": {"min": 15.0, "max": 30.0, "unidade": "°C"},
    "Agrotóxicos": {"min": 0.0, "max": 0.1, "unidade": "mg/L"},
}


class QualidadeAguaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.inputs = {}
        self._ensure_storage()
        self._build_ui()
        self.load_history()

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

    def _ensure_storage(self):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
                writer.writeheader()

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
            with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
                writer.writerow(measurement)

            self.load_history()
            QMessageBox.information(self, "Medição salva", "Medição salva com sucesso")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao salvar", f"Erro ao salvar medição: {error}")

    def clear_fields(self):
        for field_name, default_value in self.default_values.items():
            self.inputs[field_name].setValue(default_value)

    def load_history(self):
        self._ensure_storage()
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        rows.reverse()
        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            values = self._parse_row(row)
            status = self.check_status(values)
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

    def _apply_status_style(self, item, status):
        if status == "Dentro do padrão":
            item.setBackground(QColor("#1b5e20"))
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

    def check_status(self, measurement):
        checks = [
            ("pH", measurement["ph"]),
            ("Turbidez", measurement["turbidez"]),
            ("OD", measurement["oxigenio_dissolvido"]),
            ("Temperatura", measurement["temperatura"]),
            ("Agrotóxicos", measurement["agrotoxicos"]),
        ]

        for parameter, value in checks:
            limits = CONAMA[parameter]
            if value < limits["min"] or value > limits["max"]:
                return "Fora do padrão"
        return "Dentro do padrão"
