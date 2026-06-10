from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem
from ui.widgets import CustomButton, CustomEntry
from services import SettingsService

class SettingsView(QWidget):
    def __init__(self, on_back):
        super().__init__()

        self.on_back = on_back
        
        self.settings_service = SettingsService()
        
        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(50, 50, 50, 50)
        main_layout.setSpacing(30)

        lbl_titulo = QLabel("CodeRate")
        lbl_titulo.setObjectName("titulo_app")

        lbl_subtitulo = QLabel("Configurações")
        lbl_subtitulo.setObjectName("subtitulo_app")

        main_layout.addWidget(lbl_titulo)
        main_layout.addWidget(lbl_subtitulo)

        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)

        # Campo Nome
        lbl_nome = QLabel("Chave API")
        lbl_nome.setObjectName("label_entry_title")
        self.api_entry = CustomEntry()
        self.api_entry.setPlaceholderText("Adicione a chave API do Google Gemini")

        chave_salva = self.settings_service.get_api_key()
        if chave_salva:
            self.api_entry.setText(chave_salva)

        form_layout.addWidget(lbl_nome)
        form_layout.addWidget(self.api_entry)

        # --- A MÁGICA DO LINK AQUI ---
        # Usamos uma tag <a> do HTML. Você pode mudar a cor no atributo style para combinar com seu app
        lbl_link = QLabel("<a href='https://aistudio.google.com/app/apikey' style='color: #a78bfa; text-decoration: underline;'>Não possui uma chave API? Crie uma gratuitamente aqui.</a>")
        
        # Essa é a função crucial: diz ao Qt para abrir o link no navegador do sistema, 
        # em vez de tentar abrir dentro do seu próprio aplicativo
        lbl_link.setOpenExternalLinks(True) 
        
        lbl_link.setObjectName("link_api") # Caso queira aplicar margens via QSS depois
        
        form_layout.addWidget(lbl_link)

        btn_layout = QHBoxLayout()
        self.back_button = CustomButton("Voltar", command=self.back)

        btn_layout.addWidget(self.back_button)
        btn_layout.addStretch()

        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        main_layout.addLayout(btn_layout)

    def back(self):
        self.settings_service.save_api_key(self.api_entry.text().strip())
        self.on_back()