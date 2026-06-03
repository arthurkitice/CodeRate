from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPlainTextEdit
from PySide6.QtGui import QFont
from ui.widgets import CustomButton # Seu botão já refatorado

class FileView(QWidget):
    def __init__(self, submission, on_back=None, parent=None):
        super().__init__(parent)
        self.submission = submission
        self.on_back = on_back

        # Opcional: Se esta tela for funcionar como um overlay (flutuante) 
        # bloqueando a tela de trás, esta flag escurece o fundo automaticamente
        # self.setAttribute(Qt.WA_StyledBackground, True)
        # self.setObjectName("file_view_overlay")

        self.build_ui()

    def build_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(80, 40, 80, 40)
        layout_principal.setSpacing(20)

        # --- Cabeçalho ---
        lbl_titulo = QLabel("CodeRate")
        lbl_titulo.setObjectName("titulo_app")
        
        # Aproveitando o estilo de subtítulo para o nome do arquivo
        self.file_label = QLabel(self.submission.file_name)
        self.file_label.setObjectName("subtitulo_app") 

        # --- Caixa de Código (QPlainTextEdit) ---
        self.textbox = QPlainTextEdit()
        self.textbox.setObjectName("code_viewer")
        
        # setReadOnly permite que o usuário selecione e copie o código, 
        # mas impede que ele digite ou apague. 
        # NÃO use setEnabled(False), pois isso bloqueia o scroll e deixa o texto cinza.
        self.textbox.setReadOnly(True)

        # Configurando a fonte Consolas (Monoespaçada)
        fonte_codigo = QFont("Consolas", 11)
        fonte_codigo.setStyleHint(QFont.Monospace)
        self.textbox.setFont(fonte_codigo)

        # Formatando e inserindo o conteúdo
        conteudo_bruto = self.submission.content if getattr(self.submission, 'content', None) else "Conteúdo não disponível."
        conteudo_formatado = conteudo_bruto.replace('\t', '    ')
        
        # Em vez de inserir em "0.0", o Qt usa setPlainText para repor tudo
        self.textbox.setPlainText(conteudo_formatado)

        # --- Rodapé ---
        layout_rodape = QHBoxLayout()
        self.back_button = CustomButton("Voltar", command=self.back)
        
        layout_rodape.addWidget(self.back_button)
        layout_rodape.addStretch() # Empurra o botão para a esquerda

        # --- Montagem Final ---
        layout_principal.addWidget(lbl_titulo)
        layout_principal.addWidget(self.file_label)
        layout_principal.addWidget(self.textbox, stretch=1) # stretch=1 faz a caixa ocupar todo o espaço vertical
        layout_principal.addLayout(layout_rodape)

    def back(self):
        if self.on_back:
            self.on_back()
        else:
            # deleteLater é o equivalente PySide6 ao destroy() do Tkinter
            self.deleteLater()