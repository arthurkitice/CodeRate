from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from functools import partial # Mantido caso você ainda prefira usar
from dtos import SubmissionDTO
from services import SubmissionService

# ==========================================
# Entradas de Texto
# ==========================================
class CustomEntry(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setObjectName("custom_entry")
        self.setFixedHeight(40)

class LabelEntry(QWidget):
    def __init__(self, label_text="", placeholder_text="", parent=None):
        super().__init__(parent)
        
        # Um widget simples que empilha um texto e um input
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.label = QLabel(label_text)
        self.label.setObjectName("label_entry_title")
        
        self.entry = CustomEntry(placeholder=placeholder_text)

        layout.addWidget(self.label)
        layout.addWidget(self.entry)

    def get(self):
        return self.entry.text()
    
    def set(self, string):
        self.entry.setText(string)
    
    def clear(self):
        self.entry.clear()

# ==========================================
# Botões Básicos
# ==========================================
class CustomButton(QPushButton):
    def __init__(self, text, command=None, parent=None):
        super().__init__(text, parent)
        self.setObjectName("custom_btn")
        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        if command:
            self.clicked.connect(command)

class SmallButton(QPushButton):
    def __init__(self, text, command=None, parent=None):
        # Truncamento estático mantido, mas você pode usar o ElidedLabel aqui se quiser!
        max_len = 50
        display_text = text[:max_len] + '...' if len(text) > max_len else text
        
        super().__init__(display_text, parent)
        self.setObjectName("small_btn")
        self.setFixedHeight(40)
        if command:
            self.clicked.connect(command)

# ==========================================
# Cards Complexos (Substituem os antigos botões com `.place`)
# ==========================================
class ScoreCard(QFrame):
    edit_requested = Signal(SubmissionDTO) # Emite a submission inteira

    def __init__(self, text, submission, parent=None):
        super().__init__(parent)
        self.submission = submission
        self.setObjectName("score_card")
        self.setFixedHeight(40)
        self.setFixedWidth(120)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 5, 0)

        self.lbl_score = QLabel(text)
        self.lbl_score.setObjectName("score_text")

        self.btn_edit = QPushButton("")
        self.btn_edit.setIcon(QIcon("ui/icons/edit_icon.svg")) # Ajuste o caminho do seu ícone
        self.btn_edit.setIconSize(QSize(25, 25))
        self.btn_edit.setObjectName("btn_icon")
        self.btn_edit.setFixedSize(25, 25)
        self.btn_edit.setCursor(Qt.PointingHandCursor)

        layout.addWidget(self.lbl_score)
        layout.addWidget(self.btn_edit, 0, Qt.AlignRight)

        # O botão emite o sinal passando os dados da submissão
        self.btn_edit.clicked.connect(lambda: self.edit_requested.emit(self.submission))

class ResultCard(QFrame):
    view_code_requested = Signal(SubmissionDTO)
    view_feedback_requested = Signal(SubmissionDTO)
    view_similarity_requested = Signal(SubmissionDTO)

    def __init__(self, text, submission, parent=None):
        super().__init__(parent)
        self.submission = submission
        self.setObjectName("result_card")
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 10, 0)
        layout.setSpacing(10)

        self.lbl_text = QLabel(text)
        self.lbl_text.setObjectName("result_text")

        layout.addWidget(self.lbl_text)
        layout.addStretch()

        # Botão Alerta (Só entra se houver similaridade)
        if self.submission.similarity:
            self.btn_alert = QPushButton("")
            self.btn_alert.setObjectName("btn_alert")
            self.btn_alert.setIcon(QIcon("ui/icons/warning.svg"))
            self.btn_alert.setIconSize(QSize(25,25))
            self.btn_alert.setFixedSize(30, 30)
            layout.addWidget(self.btn_alert)
            self.btn_alert.clicked.connect(lambda: self.view_similarity_requested.emit(self.submission))

        # Botão Olho (Feedback)
        self.btn_eye = QPushButton("")
        self.btn_eye.setObjectName("btn_icon")
        self.btn_eye.setIcon(QIcon("ui/icons/message.svg"))
        self.btn_eye.setIconSize(QSize(25,25))
        self.btn_eye.setFixedSize(30, 30)
        layout.addWidget(self.btn_eye)
        
        self.btn_eye.clicked.connect(lambda: self.view_feedback_requested.emit(self.submission))

    # O card inteiro atua como botão para visualizar o código
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.view_code_requested.emit(self.submission)
        super().mouseReleaseEvent(event)

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import Qt, QRegularExpression

class CustomScoreDialog(QDialog):
    def __init__(self, submission: SubmissionDTO, parent=None):
        super().__init__(parent)
        
        self.submission_id = submission.id
        
        # Configurações de Janela Frameless
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(350, 250) # Aumentei 20px pra caber o texto de erro

        self.accepted_value = None 
        self.build_ui(submission.file_name, submission.score)

    def build_ui(self, filename, current_score):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        container = QFrame()
        container.setObjectName("modal_container")
        container.setStyleSheet("""
            QFrame#modal_container {
                background-color: #2b2b3b;
                border: 1px solid rgba(180, 155, 230, 0.3);
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        # --- Cabeçalho ---
        lbl_titulo = QLabel("Editar Nota")
        lbl_titulo.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        lbl_desc = QLabel(f"Altere a nota de:\n{filename}")
        lbl_desc.setStyleSheet("color: #b0b0b0; font-size: 14px;")

        # --- Input com Regex (Resolve o bug do zero sumindo) ---
        self.input_score = QLineEdit()
        self.input_score.setText(str(current_score))
        
        regex = QRegularExpression(r"^[0-9]{0,2}[.,]?[0-9]{0,2}$")
        validator = QRegularExpressionValidator(regex, self)
        self.input_score.setValidator(validator)
        
        # O estilo base da caixa de texto (guardamos na classe para poder restaurar depois)
        self.estilo_input_normal = """
            QLineEdit {
                background-color: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(180, 155, 230, 0.2);
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 16px;
            }
            QLineEdit:focus { border: 1px solid rgba(180, 155, 230, 0.8); }
        """
        self.input_score.setStyleSheet(self.estilo_input_normal)
        self.input_score.returnPressed.connect(self.accept_action)
        
        # Sempre que o usuário digitar algo, limpamos o erro (se houver)
        self.input_score.textChanged.connect(self.esconder_aviso_erro)

        # --- Mensagem de Erro Oculta ---
        self.lbl_erro = QLabel("A nota deve estar entre 0 e 10")
        self.lbl_erro.setStyleSheet("color: #ff4a4a; font-size: 12px; font-weight: bold;")
        self.lbl_erro.hide() # Fica invisível por padrão

        # --- Botões ---
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 10, 0, 0)
        btn_layout.setSpacing(10)
        
        btn_cancelar = CustomButton("Cancelar", command=self.reject_action)
        btn_salvar = CustomButton("Salvar", command=self.accept_action)

        btn_layout.addWidget(btn_cancelar)
        btn_layout.addWidget(btn_salvar)

        # --- Montagem Final ---
        layout.addWidget(lbl_titulo)
        layout.addWidget(lbl_desc)
        layout.addWidget(self.input_score)
        layout.addWidget(self.lbl_erro) # Adiciona o label oculto na estrutura
        layout.addLayout(btn_layout)

        main_layout.addWidget(container)

    # ==========================================
    # LÓGICA DE VALIDAÇÃO E ERROS
    # ==========================================
    def accept_action(self):
        texto = self.input_score.text().strip().replace(',', '.')
        
        # Barra campos vazios ou formatos pendentes como " . "
        if not texto or texto == '.':
            self.mostrar_aviso_nota_invalida()
            return
            
        nota_digitada = float(texto)
        
        # Tentamos salvar no banco direto usando a lógica que você criou
        sucesso = SubmissionService().update_score(self.submission_id, nota_digitada)
        
        if sucesso:
            self.accepted_value = nota_digitada
            self.accept() # Fecha o modal
        else:
            self.mostrar_aviso_nota_invalida() # Mantém o modal aberto e xinga o usuário
            
    def reject_action(self):
        self.accepted_value = None
        self.reject()

    def mostrar_aviso_nota_invalida(self):
        """Pinta a borda de vermelho e exibe o texto de alerta"""
        self.lbl_erro.show()
        self.input_score.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 0, 0, 0.05);
                border: 1px solid #ff4a4a;
                border-radius: 8px;
                padding: 10px;
                color: white;
                font-size: 16px;
            }
        """)

    def esconder_aviso_erro(self):
        """Devolve o modal ao estado normal assim que o usuário digita um novo número"""
        self.lbl_erro.hide()
        self.input_score.setStyleSheet(self.estilo_input_normal)

    # ==========================================
    # ARRASTE NATIVO DA JANELA (FRAMELESS)
    # ==========================================
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Protege o input de texto de ativar o arraste
            if self.input_score.geometry().contains(event.pos()):
                super().mousePressEvent(event)
                return
                
            # Chama a API nativa do X11/Wayland (Pop!_OS) ou Windows
            self.window().windowHandle().startSystemMove()
            event.accept()