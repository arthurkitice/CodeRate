from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon
from functools import partial # Mantido caso você ainda prefira usar

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
    edit_requested = Signal(dict) # Emite a submission inteira

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
        self.btn_edit.setIcon(QIcon("ui/icons/edit_icon.png")) # Ajuste o caminho do seu ícone
        self.btn_edit.setIconSize(QSize(18, 18))
        self.btn_edit.setObjectName("btn_icon")
        self.btn_edit.setFixedSize(25, 25)

        layout.addWidget(self.lbl_score)
        layout.addWidget(self.btn_edit, 0, Qt.AlignRight)

        # O botão emite o sinal passando os dados da submissão
        self.btn_edit.clicked.connect(lambda: self.edit_requested.emit(self.submission))

class ResultCard(QFrame):
    # Sinais limpos, removendo a necessidade de passar o 'parent'
    view_code_requested = Signal(dict)
    view_feedback_requested = Signal(dict)
    view_similarity_requested = Signal(dict)

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
        if self.submission.get("similarity"):
            self.btn_alert = QPushButton("!")
            self.btn_alert.setObjectName("btn_alert")
            self.btn_alert.setFixedSize(25, 25)
            layout.addWidget(self.btn_alert)
            self.btn_alert.clicked.connect(lambda: self.view_similarity_requested.emit(self.submission))

        # Botão Olho (Feedback)
        self.btn_eye = QPushButton("👁️") # Substitua por QIcon se tiver um SVG de olho
        self.btn_eye.setObjectName("btn_icon")
        self.btn_eye.setFixedSize(30, 30)
        layout.addWidget(self.btn_eye)
        
        self.btn_eye.clicked.connect(lambda: self.view_feedback_requested.emit(self.submission))

    # O card inteiro atua como botão para visualizar o código
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.view_code_requested.emit(self.submission)
        super().mouseReleaseEvent(event)