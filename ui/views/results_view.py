from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QScrollArea, QFrame, QPlainTextEdit, 
    QStackedWidget, QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt
from ui.widgets import CustomButton, ResultCard, ScoreCard # Suas classes refatoradas
from services.submission_service import SubmissionService

class ResultsView(QWidget):
    def __init__(self, evaluation_id, on_back, on_view_file, parent=None):
        super().__init__(parent)
        self.evaluation_id = evaluation_id
        self.on_back = on_back
        self.on_view_file = on_view_file # Nova rota injetada (SPA)

        self.submission_service = SubmissionService()
        db_submissions = self.submission_service.list_submissions_by_evaluation(self.evaluation_id)
        self.submissions = [sub.model_dump() for sub in db_submissions]
        
        # Dicionário para guardar a referência das linhas e aplicar efeitos visuais
        self.row_frames = {}

        self.build_ui()
        self.build_submissions_list()

    def build_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(20)

        # --- Títulos ---
        lbl_titulo = QLabel("CodeRate")
        lbl_titulo.setObjectName("titulo_app")
        
        lbl_subtitulo = QLabel(f"Resultados da Avaliação #{self.evaluation_id}")
        lbl_subtitulo.setObjectName("subtitulo_app")

        layout_principal.addWidget(lbl_titulo)
        layout_principal.addWidget(lbl_subtitulo)

        # --- Grid Central (2 Colunas) ---
        grid_painel = QGridLayout()
        grid_painel.setSpacing(30)
        grid_painel.setColumnStretch(0, 5) # Coluna Esquerda (Arquivos) é maior
        grid_painel.setColumnStretch(1, 4) # Coluna Direita (Detalhes)

        # ==========================================
        # PAINEL ESQUERDO: LISTA MESTRE
        # ==========================================
        painel_esq = QWidget()
        layout_esq = QVBoxLayout(painel_esq)
        layout_esq.setContentsMargins(0, 0, 0, 0)

        # Cabeçalhos
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(10, 0, 10, 5)
        
        lbl_arquivos = QLabel("Arquivos")
        lbl_arquivos.setObjectName("tabela_header")
        
        lbl_notas = QLabel("Notas")
        lbl_notas.setObjectName("tabela_header")
        lbl_notas.setFixedWidth(120) # Mesmo tamanho do ScoreCard

        header_layout.addWidget(lbl_arquivos, stretch=1)
        header_layout.addWidget(lbl_notas)
        layout_esq.addLayout(header_layout)

        # Scroll da Lista
        scroll_list = QScrollArea()
        scroll_list.setWidgetResizable(True)
        scroll_list.setObjectName("scroll_area")
        
        self.container_list = QWidget()
        self.container_list.setObjectName("fundo_transparente")
        self.layout_list = QVBoxLayout(self.container_list)
        self.layout_list.setSpacing(10)
        self.layout_list.setAlignment(Qt.AlignTop)
        
        scroll_list.setWidget(self.container_list)
        layout_esq.addWidget(scroll_list)

        # ==========================================
        # PAINEL DIREITO: DETALHES (USANDO QSTACKEDWIDGET)
        # ==========================================
        self.painel_dir_stack = QStackedWidget()
        
        # Estado 1: Vazio / Instruções
        self.empty_frame = QFrame()
        self.empty_frame.setObjectName("empty_state_frame")
        empty_layout = QVBoxLayout(self.empty_frame)
        
        lbl_empty = QLabel("Selecione o ícone de visualização (👁️)\nou de alerta (!) em um arquivo\npara exibir os detalhes aqui.")
        lbl_empty.setObjectName("empty_state_text")
        lbl_empty.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(lbl_empty)
        
        # Estado 2: Conteúdo
        self.content_frame = QFrame()
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(10)
        
        self.detail_title = QLabel("Justificativa")
        self.detail_title.setObjectName("tabela_header")
        
        self.detail_text = QPlainTextEdit()
        self.detail_text.setObjectName("detail_textbox")
        self.detail_text.setReadOnly(True)
        
        content_layout.addWidget(self.detail_title)
        content_layout.addWidget(self.detail_text)

        # Adiciona os dois estados ao baralho interno
        self.painel_dir_stack.addWidget(self.empty_frame)
        self.painel_dir_stack.addWidget(self.content_frame)

        # ==========================================
        # MONTAGEM FINAL
        # ==========================================
        grid_painel.addWidget(painel_esq, 0, 0)
        grid_painel.addWidget(self.painel_dir_stack, 0, 1)
        layout_principal.addLayout(grid_painel, stretch=1)

        # Rodapé
        self.back_button = CustomButton("Voltar", command=self.on_back)
        layout_principal.addWidget(self.back_button, alignment=Qt.AlignLeft)

    # --- Lógica de Preenchimento ---
    def build_submissions_list(self):
        # Limpa o layout
        while self.layout_list.count():
            item = self.layout_list.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.row_frames.clear()

        for sub in self.submissions:
            # Container da linha
            row_widget = QWidget()
            row_widget.setObjectName("list_row")
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(10)

            # Instancia os seus Cards customizados
            result_card = ResultCard(sub["file_name"], sub)
            score_card = ScoreCard(f"{sub['score']:.1f}", sub)

            # Conectando os sinais do ResultCard
            result_card.view_code_requested.connect(self.display_code)
            result_card.view_feedback_requested.connect(self.display_feedback)
            if hasattr(result_card, 'view_similarity_requested'):
                result_card.view_similarity_requested.connect(self.display_similarity)

            # Conectando o sinal do ScoreCard
            score_card.edit_requested.connect(self.prompt_edit_score)

            row_layout.addWidget(result_card, stretch=1)
            row_layout.addWidget(score_card)

            self.layout_list.addWidget(row_widget)
            self.row_frames[sub["id"]] = row_widget # Salva a linha para o efeito de highlight

    # --- Ações ---
    def display_feedback(self, submission):
        self.painel_dir_stack.setCurrentWidget(self.content_frame)
        self.detail_title.setText(f"Justificativa: {submission['file_name']}")
        self.detail_text.setPlainText(submission["feedback"])

    def display_similarity(self, submission):
        self.painel_dir_stack.setCurrentWidget(self.content_frame)
        self.detail_title.setText(f"Similaridades: {submission['file_name']}")
        
        texto_alerta = (
            "ALERTA DE ALTA TAXA DE SEMELHANÇA:\n\n"
            f"{submission.get('similarity', '')}\n\n"
            "O sistema identificou uma correspondência estrutural atípica entre os arquivos acima. "
            "Cabe ao docente analisar se ocorreu plágio ou colaboração indevida."
        )
        self.detail_text.setPlainText(texto_alerta)

    def prompt_edit_score(self, submission):
        # A janela nativa do Qt para números decimais
        novo_valor, ok_pressionado = QInputDialog.getDouble(
            self, 
            "Editar Nota", 
            f"Altere a nota de {submission['file_name']}:", 
            submission["score"], # Valor atual
            0.0, # Mínimo
            10.0, # Máximo
            1 # Casas decimais
        )
        
        if ok_pressionado:
            # O PySide6 já faz a validação! O usuário não consegue digitar letras.
            submission["score"] = novo_valor
            self.build_submissions_list()
            
            # TODO: Atualizar no banco de dados via submission_service

    def display_code(self, submission):
        # Chama a rota centralizada em vez de tentar sobrepor a tela
        self.on_view_file(submission)