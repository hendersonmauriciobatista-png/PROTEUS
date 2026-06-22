import random
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QTableWidget,
    QTableWidgetItem, QHeaderView, QPushButton, QDoubleSpinBox,
    QFormLayout, QGroupBox, QScrollArea, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt

# ─────────────────────────────────────────────
#  LIMITES CONAMA 357/2005 — Classe 2 (uso geral)
# ─────────────────────────────────────────────
CONAMA = {
    "pH": {"min": 6.0, "max": 9.0, "unidade": "", "critico_min": 5.0, "critico_max": 10.0},
    "Turbidez": {"min": 0.0, "max": 5.0, "unidade": "NTU", "critico_min": 10.0, "critico_max": 50.0},
    "OD": {"min": 5.0, "max": 10.0, "unidade": "mg/L", "critico_min": 3.0, "critico_max": 15.0},
    "Temperatura": {"min": 15, "max": 30, "unidade": "°C", "critico_min": 10, "critico_max": 35},
    "Agrotóxicos": {"min": 0.0, "max": 0.1, "unidade": "mg/L", "critico_min": 0.2, "critico_max": 1.0},
}

class QualidadeAguaPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Qualidade da Água")
        layout = QVBoxLayout(self)

        title = QLabel("💧 Qualidade da Água")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #4fc3f7;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setRowCount(len(CONAMA))
        self.table.setHorizontalHeaderLabels(["Parâmetro", "Valor", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Populando a tabela com dados
        for i, (param, limits) in enumerate(CONAMA.items()):
            value = random.uniform(limits["min"], limits["max"])  # Simulando valores
            status = self.check_status(param, value)
            self.table.setItem(i, 0, QTableWidgetItem(param))
            self.table.setItem(i, 1, QTableWidgetItem(f"{value:.2f} {limits['unidade']}"))
            self.table.setItem(i, 2, QTableWidgetItem(status))

        layout.addWidget(self.table)

        # Botão de atualizar
        update_btn = QPushButton("Atualizar Dados")
        update_btn.clicked.connect(self.update_data)
        layout.addWidget(update_btn)

        self.setLayout(layout)

    def check_status(self, param, value):
        limits = CONAMA[param]
        if value < limits["min"] or value > limits["max"]:
            return "Fora do padrão"
        return "Dentro do padrão"

    def update_data(self):
        for i, (param, limits) in enumerate(CONAMA.items()):
            value = random.uniform(limits["min"], limits["max"])  # Simulando novos valores
            status = self.check_status(param, value)
            self.table.setItem(i, 1, QTableWidgetItem(f"{value:.2f} {limits['unidade']}"))
            self.table.setItem(i, 2, QTableWidgetItem(status))
