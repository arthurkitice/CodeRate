import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QPushButton, QScrollArea, QFrame, QMessageBox, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QFontMetrics
from services import CriteriaService
from ui.widgets import CustomButton

class ElidedLabel(QLabel):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        # 1. Guardamos o texto original intacto na memória
        self._texto_original = text
        
        # 2. Impedimos que a label force a expansão do layout
        self.setMinimumWidth(1)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    # 3. Sobrescrevemos o método padrão de definir texto
    def setText(self, text):
        self._texto_original = text
        self._atualizar_elipses()

    # 4. O SEGREDO: O motor do Qt chama essa função sempre que a janela muda de tamanho
    def resizeEvent(self, event):
        self._atualizar_elipses()
        super().resizeEvent(event)

    def _atualizar_elipses(self):
        # Mede a fonte atual da Label
        metricas = QFontMetrics(self.font())
        
        # Calcula o corte: (Texto Base, Onde colocar os pontinhos, Largura máxima em pixels)
        texto_cortado = metricas.elidedText(
            self._texto_original, 
            Qt.ElideRight, 
            self.width()
        )
        
        # Define visualmente o texto cortado, sem perder a variável original
        super().setText(texto_cortado)

class CriterionCard(QFrame):
    evaluation_requested = Signal(int)
    edit_requested = Signal(int)
    delete_requested = Signal(int)

    def __init__(self, criteria_id, name, description, parent=None):
        super().__init__(parent)
        self.criteria_id = criteria_id
        self.setObjectName("criterion_card")
        self.setFixedHeight(200) 
        self.setCursor(Qt.PointingHandCursor)

        layout = QGridLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        # Define um espaçamento vertical e horizontal entre os elementos do grid
        layout.setSpacing(10) 

        # --- 1. TÍTULO ---
        self.lbl_name = ElidedLabel(name) 
        self.lbl_name.setObjectName("criterion_name")
        self.lbl_name.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)

        # --- 2. DESCRIÇÃO ---
        self.lbl_desc = QLabel(description)
        self.lbl_desc.setObjectName("criterion_desc")
        self.lbl_desc.setWordWrap(True) 
        
        # AQUI ESTÁ A CORREÇÃO: Alinhamos o TEXTO dentro do espaço da label
        self.lbl_desc.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Mantemos o truque contra o estiramento horizontal do card
        self.lbl_desc.setMinimumWidth(1)
        # Horizontal = Ignored (não estica o card) | Vertical = Preferred (ocupa a altura disponível)
        self.lbl_desc.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Preferred)

        # --- 3. BOTÕES ---
        botoes_layout = QHBoxLayout()
        botoes_layout.setSpacing(8)
        self.btn_edit = QPushButton("")
        self.btn_delete = QPushButton("")
        self.btn_edit.setIcon(QIcon("ui/icons/edit_icon.png"))
        self.btn_edit.setIconSize(QSize(30, 30))
        self.btn_edit.setObjectName("btn_icon")
        self.btn_delete.setIcon(QIcon("ui/icons/trash_icon.png"))
        self.btn_delete.setIconSize(QSize(30, 30))
        self.btn_delete.setObjectName("btn_icon")
        self.btn_edit.setFixedSize(30, 30)
        self.btn_delete.setFixedSize(30, 30)

        botoes_layout.addWidget(self.btn_edit)
        botoes_layout.addWidget(self.btn_delete)

        # --- 4. MONTANDO O QUEBRA-CABEÇA NO GRID ---
        layout.addWidget(self.lbl_name, 0, 0, Qt.AlignTop)
        layout.addLayout(botoes_layout, 0, 1, Qt.AlignTop | Qt.AlignRight)
        
        # AQUI ESTÁ A SEGUNDA PARTE DA CORREÇÃO: 
        # Removido o argumento de alinhamento daqui. 
        # Agora o Grid vai esticar essa caixa por todas as 2 colunas.
        layout.addWidget(self.lbl_desc, 1, 0, 1, 2)
        
        # Opcional: Para evitar que o título e os botões fiquem muito largos 
        # em relação ao texto, forçamos a coluna 0 a ser expansível
        layout.setColumnStretch(0, 1)
        layout.setRowStretch(1, 1)

        # --- 5. SINAIS ---
        self.btn_edit.clicked.connect(lambda: self.edit_requested.emit(self.criteria_id))
        self.btn_delete.clicked.connect(lambda: self.delete_requested.emit(self.criteria_id))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.evaluation_requested.emit(self.criteria_id)
        super().mouseReleaseEvent(event)


# ==========================================
# 2. A Tela Principal
# ==========================================
class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        # ID crucial para aplicarmos o degradê apenas no fundo, sem vazar para os cards
        self.setObjectName("janela_principal")
        
        self.mock_criteria_db = [
            {"id": 6, "name": "Critério 6", "desc": "Descrição do critério 6"},
            {"id": 5, "name": "Critério 5", "desc": "Descrição do critério 5"},
            {"id": 4, "name": "Critério 4", "desc": "Descrição do critério 4"},
            {"id": 3, "name": "Critério 3", "desc": "Descrição do critério 3"}
        ]

        self.build_ui()
        self.load_criteria()

    def build_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(50, 50, 50, 50)
        layout_principal.setSpacing(35) 

        # --- Cabeçalho ---
        lbl_titulo = QLabel("CodeRate")
        lbl_titulo.setObjectName("titulo_app")

        # --- Botões ---
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(20)
        
        # Nomes adaptados à sua nova imagem
        btn_criar = CustomButton("Criar Critério")
        btn_historico = CustomButton("Histórico de Avaliações")
        btn_todos = CustomButton("Todos os Critérios")

        layout_botoes.addWidget(btn_criar)
        layout_botoes.addWidget(btn_historico)
        layout_botoes.addWidget(btn_todos)
        layout_botoes.addStretch()

        # --- Subtítulo ---
        lbl_subtitulo = QLabel("Últimos Critérios de Avaliação Criados")
        lbl_subtitulo.setObjectName("subtitulo_app")

        # --- Área de Rolagem ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        
        self.container_cards = QWidget()
        self.container_cards.setObjectName("container_cards")
        
        self.grid_cards = QGridLayout(self.container_cards)
        self.grid_cards.setSpacing(20)
        self.grid_cards.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area.setWidget(self.container_cards)

        layout_principal.addWidget(lbl_titulo)
        layout_principal.addLayout(layout_botoes)
        layout_principal.addWidget(lbl_subtitulo)
        layout_principal.addWidget(self.scroll_area)

    def load_criteria(self):
        for i in reversed(range(self.grid_cards.count())): 
            item = self.grid_cards.itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()
            elif item.spacerItem() is not None:
                self.grid_cards.removeItem(item)

        coluna = 0
        linha = 0
        max_colunas = 4

        criteria_list = CriteriaService().list_criteria()[::-1][:max_colunas]

        for criterion in criteria_list:
            card = CriterionCard(criterion.id, criterion.name, criterion.description)
            card.evaluation_requested.connect(self.on_start_evaluation)
            self.grid_cards.addWidget(card, linha, coluna)
            
            coluna += 1
            if coluna >= max_colunas:
                coluna = 0
                linha += 1

        for col in range(max_colunas):
            self.grid_cards.setColumnStretch(col, 1)

        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.grid_cards.addItem(spacer, linha + 1, 0, 1, max_colunas)

    def on_start_evaluation(self, criteria_id):
        QMessageBox.information(self, "Avaliação", f"Iniciando: {criteria_id}")
