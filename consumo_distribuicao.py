import csv
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
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


DATA_FILE = Path(__file__).resolve().parent / "data" / "consumo_distribuicao_medicoes.csv"
CSV_FIELDS = [
    "timestamp",
    "consumo_diario",
    "consumo_mensal",
    "volume_distribuido",
    "perdas_estimadas",
    "observacao",
]


class ConsumoDistribuicaoPage(QWidget):
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

        title = QLabel("Consumo e Distribuição")
        title.setObjectName("page_title")
        subtitle = QLabel("Cadastro manual e histórico operacional persistido em CSV")
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

        self.inputs["consumo_diario"] = self._make_spinbox(0.0, 1000000.0, 0.0, 2, 1.0)
        self.inputs["consumo_mensal"] = self._make_spinbox(0.0, 10000000.0, 0.0, 2, 10.0)
        self.inputs["volume_distribuido"] = self._make_spinbox(0.0, 10000000.0, 0.0, 2, 10.0)
        self.inputs["perdas_estimadas"] = self._make_spinbox(0.0, 100.0, 0.0, 2, 0.5)
        self.inputs["observacao"] = QLineEdit()
        self.inputs["observacao"].setMaxLength(120)
        self.inputs["observacao"].setPlaceholderText("Observação curta")
        self.inputs["observacao"].setStyleSheet(
            "QLineEdit { background-color: #0d1b2a; color: #cfd8dc; "
            "border: 1px solid #1e3a5f; border-radius: 4px; padding: 4px; }"
        )

        form_layout.addRow("Consumo diário (m³)", self.inputs["consumo_diario"])
        form_layout.addRow("Consumo mensal (m³)", self.inputs["consumo_mensal"])
        form_layout.addRow("Volume distribuído (m³)", self.inputs["volume_distribuido"])
        form_layout.addRow("Perdas estimadas (%)", self.inputs["perdas_estimadas"])
        form_layout.addRow("Observação", self.inputs["observacao"])

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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Timestamp", "Consumo diário", "Consumo mensal", "Volume distribuído", "Perdas", "Observação"]
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
            "consumo_diario": self.inputs["consumo_diario"].value(),
            "consumo_mensal": self.inputs["consumo_mensal"].value(),
            "volume_distribuido": self.inputs["volume_distribuido"].value(),
            "perdas_estimadas": self.inputs["perdas_estimadas"].value(),
            "observacao": self.inputs["observacao"].text().strip(),
        }

        try:
            with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=CSV_FIELDS)
                writer.writerow(measurement)

            self.load_history()
            QMessageBox.information(self, "Medição salva", "Medição de consumo salva com sucesso")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao salvar", f"Erro ao salvar medição de consumo: {error}")

    def clear_fields(self):
        self.inputs["consumo_diario"].setValue(0.0)
        self.inputs["consumo_mensal"].setValue(0.0)
        self.inputs["volume_distribuido"].setValue(0.0)
        self.inputs["perdas_estimadas"].setValue(0.0)
        self.inputs["observacao"].clear()

    def load_history(self):
        self._ensure_storage()
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))

        rows.reverse()
        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            display_values = [
                row.get("timestamp", ""),
                f"{self._to_float(row.get('consumo_diario')):.2f} m³",
                f"{self._to_float(row.get('consumo_mensal')):.2f} m³",
                f"{self._to_float(row.get('volume_distribuido')):.2f} m³",
                f"{self._to_float(row.get('perdas_estimadas')):.2f} %",
                row.get("observacao", ""),
            ]

            for column_index, value in enumerate(display_values):
                item = QTableWidgetItem(value)
                if column_index in (1, 2, 3, 4):
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.table.setItem(row_index, column_index, item)

    def _to_float(self, value):
        try:
            return float(value or 0)
        except ValueError:
            return 0.0
