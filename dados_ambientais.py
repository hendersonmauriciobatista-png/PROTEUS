import csv
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


DATA_FILE = Path(__file__).resolve().parent / "data" / "dados_ambientais_medicoes.csv"
CSV_FIELDS = [
    "timestamp",
    "temperatura_ambiente",
    "umidade_relativa",
    "chuva",
    "pressao_atmosferica",
    "observacao",
]


class DadosAmbientaisPage(QWidget):
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

        title = QLabel("Dados Ambientais")
        title.setObjectName("page_title")
        subtitle = QLabel("Cadastro manual e histórico de medições ambientais persistidas em CSV")
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

        self.inputs["temperatura_ambiente"] = self._make_spinbox(-20.0, 60.0, 25.0, 2, 0.1)
        self.inputs["umidade_relativa"] = self._make_spinbox(0.0, 100.0, 60.0, 2, 1.0)
        self.inputs["chuva"] = self._make_spinbox(0.0, 1000.0, 0.0, 2, 0.1)
        self.inputs["pressao_atmosferica"] = self._make_spinbox(800.0, 1100.0, 1013.25, 2, 0.5)
        self.inputs["observacao"] = QLineEdit()
        self.inputs["observacao"].setMaxLength(120)
        self.inputs["observacao"].setPlaceholderText("Observação curta")
        self.inputs["observacao"].setStyleSheet(
            "QLineEdit { background-color: #0d1b2a; color: #cfd8dc; "
            "border: 1px solid #1e3a5f; border-radius: 4px; padding: 4px; }"
        )

        form_layout.addRow("Temperatura ambiente (°C)", self.inputs["temperatura_ambiente"])
        form_layout.addRow("Umidade relativa (%)", self.inputs["umidade_relativa"])
        form_layout.addRow("Chuva (mm)", self.inputs["chuva"])
        form_layout.addRow("Pressão atmosférica (hPa)", self.inputs["pressao_atmosferica"])
        form_layout.addRow("Observação", self.inputs["observacao"])

        self.save_button = QPushButton("Salvar Medição")
        self.save_button.clicked.connect(self.save_measurement)
        form_layout.addRow("", self.save_button)
        layout.addWidget(form_frame)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Timestamp", "Temp. ambiente", "Umidade", "Chuva", "Pressão", "Observação"]
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
            "temperatura_ambiente": self.inputs["temperatura_ambiente"].value(),
            "umidade_relativa": self.inputs["umidade_relativa"].value(),
            "chuva": self.inputs["chuva"].value(),
            "pressao_atmosferica": self.inputs["pressao_atmosferica"].value(),
            "observacao": self.inputs["observacao"].text().strip(),
        }

        try:
            with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
                writer.writerow(measurement)

            self.inputs["observacao"].clear()
            self.load_history()
            QMessageBox.information(self, "Medição salva", "Medição ambiental salva com sucesso")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao salvar", f"Erro ao salvar medição ambiental: {error}")

    def load_history(self):
        self._ensure_storage()
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        rows.reverse()
        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            display_values = [
                row.get("timestamp", ""),
                f"{self._to_float(row.get('temperatura_ambiente')):.2f} °C",
                f"{self._to_float(row.get('umidade_relativa')):.2f} %",
                f"{self._to_float(row.get('chuva')):.2f} mm",
                f"{self._to_float(row.get('pressao_atmosferica')):.2f} hPa",
                row.get("observacao", ""),
            ]

            for column_index, value in enumerate(display_values):
                item = QTableWidgetItem(value)
                if column_index in (1, 2, 3, 4):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_index, column_index, item)

    def refresh(self):
        self.load_history()

    def _to_float(self, value):
        try:
            return float(value or 0)
        except ValueError:
            return 0.0
