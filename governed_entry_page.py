from datetime import datetime
from PyQt5.QtWidgets import QComboBox, QFormLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
from governed_core.entry_application import ExplicitGovernedEntryService
from governed_core.repository import GovernedCoreRepository


class GovernedEntryPage(QWidget):
    def __init__(self, repository=None, entry_service=None):
        super().__init__()
        self.entry_service = entry_service or ExplicitGovernedEntryService(repository or GovernedCoreRepository().initialize())
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Entrada Governada — Registro Explícito"))
        layout.addWidget(QLabel("Modo separado do histórico legado; um parâmetro por interação."))
        form = QFormLayout()
        self.point_input = QComboBox()
        self.point_input.addItem("Selecione explicitamente um ponto", None)
        self.point_input.currentIndexChanged.connect(self._load_parameters)
        self.parameter_input = QComboBox()
        self.parameter_input.addItem("Selecione um parâmetro APS", None)
        self.parameter_input.currentIndexChanged.connect(lambda _index: self._update_submit_state())
        self.value_input = QLineEdit()
        self.value_input.textChanged.connect(lambda _text: self._update_submit_state())
        self.measured_at_input = QLineEdit()
        self.measured_at_input.textChanged.connect(lambda _text: self._update_submit_state())
        self.measured_at_input.setPlaceholderText("AAAA-MM-DDTHH:MM:SS-03:00")
        self.provenance = QLabel("MANUAL_ENTRY (obrigatório e explícito)")
        self.save_button = QPushButton("Registrar medição governada")
        self.save_button.clicked.connect(self.submit)
        form.addRow("Ponto governado (ID)", self.point_input)
        form.addRow("Parâmetro APS (um)", self.parameter_input)
        form.addRow("Valor", self.value_input)
        form.addRow("Measured_at (com fuso)", self.measured_at_input)
        form.addRow("Provenance", self.provenance)
        form.addRow("", self.save_button)
        layout.addLayout(form)
        self.receipt = QLabel("Nenhum receipt governado nesta sessão.")
        self.receipt.setWordWrap(True)
        layout.addWidget(self.receipt)
        self.refresh()

    def refresh(self):
        self.point_input.clear()
        self.point_input.addItem("Selecione explicitamente um ponto", None)
        for point in self.entry_service.active_points():
            self.point_input.addItem("{} · {}".format(point.display_name, point.point_id), point.point_id)
        self.point_input.setCurrentIndex(0)
        self.parameter_input.clear()
        self.parameter_input.addItem("Selecione um parâmetro APS", None)
        self.save_button.setEnabled(False)

    def _update_submit_state(self):
        self.save_button.setEnabled(
            bool(self.point_input.currentData())
            and bool(self.parameter_input.currentData())
            and bool(self.value_input.text().strip())
            and bool(self.measured_at_input.text().strip())
        )

    def _load_parameters(self, index):
        self.parameter_input.clear()
        self.parameter_input.addItem("Selecione um parâmetro APS", None)
        point_id = self.point_input.itemData(index)
        if not point_id:
            return
        try:
            for parameter in self.entry_service.canonical_parameters(point_id):
                self.parameter_input.addItem(parameter, parameter)
            self._update_submit_state()
        except Exception as error:
            QMessageBox.critical(self, "Ponto não resolvível", str(error))

    def submit(self):
        point_id, parameter = self.point_input.currentData(), self.parameter_input.currentData()
        if not point_id or not parameter:
            QMessageBox.warning(self, "Entrada incompleta", "Selecione ponto e parâmetro.")
            return
        try:
            measured_at = datetime.fromisoformat(self.measured_at_input.text().strip())
            if measured_at.tzinfo is None or measured_at.utcoffset() is None:
                raise ValueError("Measured_at deve conter offset de fuso horário.")
            receipt = self.entry_service.submit(point_id, parameter, float(self.value_input.text().strip()), measured_at)
        except Exception as error:
            QMessageBox.critical(self, "Registro rejeitado", "Falha sem validação técnica: {}".format(error))
            return
        self.receipt.setText("Receipt governado: {} | Point={} | Parameter={} | Value={} | Measured_at={} | Registered_at={} | Provenance={}".format(receipt.measurement_id, receipt.point_id, receipt.parameter_reference, receipt.value, receipt.measured_at, receipt.registered_at, receipt.provenance))
