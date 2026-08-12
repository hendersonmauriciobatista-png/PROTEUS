from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QFormLayout,
    QFrame,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from monitoramento_hidrico.projeto_monitoramento import (
    CONTEXTOS_OPERACIONAIS,
    PONTOS_PRINCIPAIS_COLETA,
    PROJETO_ATIVO_ID,
    STATUS_ARQUIVADO,
    STATUS_ATIVO,
    STATUS_ENCERRADO,
    ProjetoMonitoramento,
    ProjetoMonitoramentoStore,
    arquivar_projeto,
    derivar_perfil_operacional,
    encerrar_projeto,
    reativar_monitoramento,
)


class ProjetoMonitoramentoPage(QWidget):
    def __init__(self, store=None):
        super().__init__()
        self.store = store or ProjetoMonitoramentoStore()
        self.inputs = {}
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(15)

        title = QLabel("Projeto de Monitoramento")
        title.setObjectName("page_title")
        subtitle = QLabel("Unidade principal para as medicoes futuras do sistema")
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

        self.inputs["nome"] = self._make_line_edit(120)
        self.inputs["cliente"] = self._make_line_edit(120)
        self.inputs["area_operacional"] = self._make_combo(CONTEXTOS_OPERACIONAIS)
        self.inputs["area_operacional"].currentIndexChanged.connect(self._update_perfil_operacional)
        self.inputs["perfil_operacional"] = self._make_line_edit(80)
        self.inputs["perfil_operacional"].setReadOnly(True)
        self.inputs["ponto_principal_coleta"] = self._make_combo(PONTOS_PRINCIPAIS_COLETA)
        self.inputs["coletor_responsavel"] = self._make_line_edit(120)
        self.inputs["data_criacao"] = self._make_line_edit(40)
        self.inputs["data_criacao"].setReadOnly(True)
        self.inputs["status"] = self._make_line_edit(40)
        self.inputs["status"].setReadOnly(True)

        form_layout.addRow("Nome do Projeto", self.inputs["nome"])
        form_layout.addRow("Cliente", self.inputs["cliente"])
        form_layout.addRow("Contexto Operacional", self.inputs["area_operacional"])
        form_layout.addRow("Perfil Operacional", self.inputs["perfil_operacional"])
        form_layout.addRow("Ponto Principal de Coleta", self.inputs["ponto_principal_coleta"])
        form_layout.addRow("Coletor Responsavel", self.inputs["coletor_responsavel"])
        form_layout.addRow("Data de criacao", self.inputs["data_criacao"])
        form_layout.addRow("Status", self.inputs["status"])

        self.save_button = QPushButton("Salvar Projeto")
        self.save_button.clicked.connect(self.save_project)
        form_layout.addRow("", self.save_button)
        self.close_button = QPushButton("Encerrar Projeto")
        self.close_button.clicked.connect(self.close_project)
        form_layout.addRow("", self.close_button)
        self.archive_button = QPushButton("Arquivar Projeto")
        self.archive_button.clicked.connect(self.archive_project)
        form_layout.addRow("", self.archive_button)
        self.reactivate_button = QPushButton("Reativar Monitoramento")
        self.reactivate_button.clicked.connect(self.reactivate_monitoring)
        form_layout.addRow("", self.reactivate_button)
        layout.addWidget(form_frame)
        layout.addStretch()

    def refresh(self):
        projeto = self.store.carregar()
        self.inputs["nome"].setText(projeto.nome)
        self.inputs["cliente"].setText(projeto.cliente)
        self._set_combo_value("area_operacional", projeto.area_operacional)
        self.inputs["perfil_operacional"].setText(projeto.perfil_operacional)
        self._set_combo_value("ponto_principal_coleta", projeto.ponto_principal_coleta)
        self.inputs["coletor_responsavel"].setText(projeto.coletor_responsavel)
        self.inputs["data_criacao"].setText(projeto.data_criacao)
        self.inputs["status"].setText(projeto.status)
        self._apply_status_state(projeto.status)

    def save_project(self):
        projeto_atual = self.store.carregar()
        projeto = ProjetoMonitoramento(
            identificador=PROJETO_ATIVO_ID,
            nome=self.inputs["nome"].text().strip(),
            cliente=self.inputs["cliente"].text().strip(),
            area_operacional=self.inputs["area_operacional"].currentData(),
            perfil_operacional=derivar_perfil_operacional(self.inputs["area_operacional"].currentData()),
            ponto_principal_coleta=self.inputs["ponto_principal_coleta"].currentData(),
            coletor_responsavel=self.inputs["coletor_responsavel"].text().strip(),
            data_criacao=projeto_atual.data_criacao,
            status=projeto_atual.status,
        )

        try:
            self.store.salvar(projeto)
            self.refresh()
            QMessageBox.information(self, "Projeto salvo", "Projeto de Monitoramento salvo com sucesso")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao salvar", f"Erro ao salvar projeto: {error}")

    def close_project(self):
        try:
            projeto = encerrar_projeto(self.store.carregar())
            self.store.salvar(projeto)
            self.refresh()
            QMessageBox.information(self, "Projeto encerrado", "Projeto de Monitoramento encerrado com sucesso")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao encerrar", f"Erro ao encerrar projeto: {error}")

    def archive_project(self):
        try:
            projeto = arquivar_projeto(self.store.carregar())
            self.store.salvar(projeto)
            self.refresh()
            QMessageBox.information(self, "Projeto arquivado", "Projeto de Monitoramento arquivado com sucesso")
        except Exception as error:
            QMessageBox.critical(self, "Erro ao arquivar", f"Erro ao arquivar projeto: {error}")

    def reactivate_monitoring(self):
        try:
            projeto = reativar_monitoramento(self.store.carregar())
            self.store.salvar(projeto)
            self.refresh()
            QMessageBox.information(
                self,
                "Monitoramento reativado",
                "Monitoramento do Projeto reativado com sucesso",
            )
        except Exception as error:
            QMessageBox.critical(self, "Erro ao reativar", f"Erro ao reativar monitoramento: {error}")

    def _make_line_edit(self, max_length):
        field = QLineEdit()
        field.setMaxLength(max_length)
        field.setStyleSheet(
            "QLineEdit { background-color: #0d1b2a; color: #cfd8dc; "
            "border: 1px solid #1e3a5f; border-radius: 4px; padding: 4px; }"
        )
        return field

    def _make_combo(self, values):
        field = QComboBox()
        for value in values:
            field.addItem(value, value)
        field.setStyleSheet(
            "QComboBox { background-color: #0d1b2a; color: #cfd8dc; "
            "border: 1px solid #1e3a5f; border-radius: 4px; padding: 4px; }"
        )
        return field

    def _set_combo_value(self, field_name, value):
        combo = self.inputs[field_name]
        index = combo.findData(value)
        if index >= 0:
            combo.setCurrentIndex(index)

    def _update_perfil_operacional(self):
        contexto = self.inputs["area_operacional"].currentData()
        self.inputs["perfil_operacional"].setText(derivar_perfil_operacional(contexto))

    def _apply_status_state(self, status):
        projeto_ativo = status == STATUS_ATIVO
        projeto_encerrado = status == STATUS_ENCERRADO
        projeto_arquivado = status == STATUS_ARQUIVADO

        self.save_button.setEnabled(projeto_ativo)
        self.close_button.setEnabled(projeto_ativo)
        self.archive_button.setEnabled(projeto_encerrado)
        self.reactivate_button.setEnabled(projeto_arquivado)

        for field_name in ["nome", "cliente", "coletor_responsavel"]:
            self.inputs[field_name].setReadOnly(not projeto_ativo)
        for field_name in ["area_operacional", "ponto_principal_coleta"]:
            self.inputs[field_name].setEnabled(projeto_ativo)

        if projeto_arquivado:
            self.inputs["status"].setToolTip("Projeto arquivado permanece disponivel para consulta.")
        elif projeto_encerrado:
            self.inputs["status"].setToolTip("Projeto encerrado pode ser arquivado.")
        else:
            self.inputs["status"].setToolTip("Projeto ativo pode ser editado ou encerrado.")
