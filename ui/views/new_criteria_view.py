from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPlainTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from ui.widgets import CustomButton, CustomEntry # Importe seu CustomEntry
from services.criteria_service import CriteriaService

class NewCriteriaView(QWidget):
    def __init__(self, on_criteria_created, on_back, criteria_id=None, parent=None):
        super().__init__(parent)
        self.on_criteria_created = on_criteria_created
        self.on_back = on_back
        
        self.criteria_id = criteria_id
        self.criteria_service = CriteriaService()
        
        self.build_ui()

    def build_ui(self):
        # O Layout vertical principal da página
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(80, 40, 80, 40)
        main_layout.setSpacing(20)

        # Cabeçalhos centralizados
        lbl_titulo = QLabel("CodeRate")
        lbl_titulo.setObjectName("titulo_app")
        lbl_titulo.setAlignment(Qt.AlignCenter)

        lbl_subtitulo = QLabel(self.get_subtitle())
        lbl_subtitulo.setObjectName("subtitulo_app")
        lbl_subtitulo.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(lbl_titulo)
        main_layout.addWidget(lbl_subtitulo)

        # --- A MÁGICA DA CENTRALIZAÇÃO (Pesos 1 : 2 : 1) ---
        center_layout = QHBoxLayout()
        center_layout.addStretch(1) # Equivalente à coluna 0 (Vazia)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # Campo Nome
        lbl_nome = QLabel("Nome")
        lbl_nome.setObjectName("label_entry_title")
        self.name_entry = CustomEntry() # Mantém o estilo do seu widget
        self.name_entry.setPlaceholderText("Digite o nome do critério")

        form_layout.addWidget(lbl_nome)
        form_layout.addWidget(self.name_entry)

        # Campo Descrição (Substitui o CTkTextbox)
        lbl_desc = QLabel("Descrição")
        lbl_desc.setObjectName("label_entry_title")
        self.description_entry = QPlainTextEdit()
        self.description_entry.setPlaceholderText("Digite a descrição do critério")
        self.description_entry.setObjectName("custom_textbox")

        form_layout.addWidget(lbl_desc)
        form_layout.addWidget(self.description_entry, stretch=1)

        # Botões
        btn_layout = QHBoxLayout()
        self.back_button = CustomButton("Voltar", command=self.back)
        self.create_button = CustomButton(self.get_button_text(), command=self.save_criteria)

        btn_layout.addWidget(self.back_button)
        btn_layout.addWidget(self.create_button)

        form_layout.addLayout(btn_layout)

        # Adiciona o formulário no centro com peso 2
        center_layout.addLayout(form_layout, 2) 
        center_layout.addStretch(1) # Equivalente à coluna 2 (Vazia)

        main_layout.addLayout(center_layout, stretch=1)

    def get_subtitle(self):
        return "Novo Critério"
    
    def get_button_text(self):
        return "Criar Critério"

    def back(self):
        self.on_back()

    def show_error(self, message):
        # A janela de erro nativa do Qt
        QMessageBox.critical(self, "Erro", message)

    def save_criteria(self):
        # No PySide6: QLineEdit usa .text() e QPlainTextEdit usa .toPlainText()
        name = self.name_entry.text().strip()
        description = self.description_entry.toPlainText().strip()

        if not name or not description:
            self.show_error("Erro: Preencha nome e descrição.")
            return

        criteria = self.criteria_service.create_criteria(name, description)
        if criteria:
            self.on_criteria_created()
        else:
            self.show_error("Erro: Não foi possível criar o critério.")