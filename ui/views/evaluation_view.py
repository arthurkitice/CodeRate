import sys
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QThread, QSize
from PySide6.QtGui import QIcon
from ui.widgets import CustomButton, CustomEntry, SmallButton # Presumindo seus novos widgets
from services import EvaluationService, SubmissionService
from services import CriteriaService
from services import AIService

# ==========================================
# 2. A Tela Principal (EvaluationView)
# ==========================================
class EvaluationView(QWidget):
    def __init__(self, criteria_id, on_back, on_view_results, on_start_processing, on_view_file, parent=None):
        super().__init__(parent)
        self.evaluation_service = EvaluationService()
        self.submission_service = SubmissionService()
        self.criteria_id = criteria_id
        self.on_back = on_back
        self.on_view_file = on_view_file
        self.on_view_results = on_view_results
        self.on_start_processing = on_start_processing
        self.files = []
        
        # Variáveis de controle de overlays
        self.file_view = None
        self.loading_overlay = None
        self.ai_worker = None

        self.build_ui()
        self.build_evaluation_buttons()
        self.build_evaluation_files()

    def _list_all_evaluations(self):
        evaluations = self.evaluation_service.list_evaluations_by_criteria(self.criteria_id)
        return list(reversed(evaluations))

    # --- Utilitário de Limpeza ---
    def _clear_layout(self, layout):
        """Itera sobre um layout e destrói todos os widgets filhos."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif item.layout() is not None:
                    self._clear_layout(item.layout())

    # --- Construção Dinâmica de Listas ---
    def build_evaluation_buttons(self):
        self._clear_layout(self.layout_eval_list)
        evaluation_list = self._list_all_evaluations()

        for evaluation in evaluation_list:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)

            # Presumindo que o seu SmallButton novo aceite um ícone de exclusão
            # ou você pode criar um widget composto aqui rapidamente
            btn_open = CustomButton(evaluation.name, command=lambda _, e_id=evaluation.id: self.on_view_results(e_id))
            
            btn_del = CustomButton("")
            btn_del.setIcon(QIcon("ui/icons/trash_icon.png"))
            btn_del.setIconSize(QSize(40,40))
            btn_del.setFixedSize(40, 40)
            btn_del.clicked.connect(lambda e_id=evaluation.id: self.delete_evaluation(e_id))

            row_layout.addWidget(btn_open, stretch=1)
            row_layout.addWidget(btn_del)
            
            self.layout_eval_list.addWidget(row_widget)
            
        self.layout_eval_list.addStretch()

    def build_evaluation_files(self):
        self._clear_layout(self.layout_files_list)

        for submission in self.files:
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)

            btn_open = CustomButton(submission.file_name, command=lambda _, s=submission: self.on_file_click(s))
            
            btn_del = CustomButton("")
            btn_del.setIcon(QIcon("ui/icons/trash_icon.png"))
            btn_del.setIconSize(QSize(40,40))
            btn_del.setFixedSize(40, 40)
            btn_del.clicked.connect(lambda s=submission: self.remove_file(s))

            row_layout.addWidget(btn_open, stretch=1)
            row_layout.addWidget(btn_del)
            
            self.layout_files_list.addWidget(row_widget)

        self.layout_files_list.addStretch()

    # --- Ações ---
    def add_new_file(self):
        draft_dto = self.submission_service.select_file()
        if draft_dto:
            self.files.append(draft_dto)
            self.build_evaluation_files()

    def remove_file(self, submission):
        if submission in self.files:
            self.files.remove(submission)
            self.build_evaluation_files()

    def delete_evaluation(self, evaluation_id):
        self.evaluation_service.delete_evaluation(evaluation_id)
        self.build_evaluation_buttons()

    def on_file_click(self, submission):
        self.on_view_file(submission)

    # --- O Fluxo da IA (Multithreading) ---
    def start_evaluation_action(self):
        avaliacao_nome = self.evaluation_name_entry.text().strip()

        if not avaliacao_nome:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um nome para a avaliação.")
            return

        if not self.files:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos um arquivo de código para avaliar!")
            return

        # Simplesmente passa o bastão para o app.py mudar a tela!
        self.on_start_processing(self.criteria_id, avaliacao_nome, self.files)

    # --- Estrutura da Interface ---
    def build_ui(self):
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(80, 40, 80, 40)

        # Título Padrão
        lbl_titulo = QLabel("CodeRate")
        lbl_titulo.setObjectName("titulo_app")
        layout_principal.addWidget(lbl_titulo)

        # O Grid de Duas Colunas (Row 2 do seu código)
        grid_painel = QGridLayout()
        grid_painel.setSpacing(40)
        grid_painel.setColumnStretch(0, 1)
        grid_painel.setColumnStretch(1, 1)

        # --- Coluna Esquerda (Nova Avaliação) ---
        esq_widget = QWidget()
        esq_layout = QVBoxLayout(esq_widget)
        esq_layout.setContentsMargins(0, 0, 0, 0)

        header_esq = QHBoxLayout()
        lbl_nova = QLabel("Nova avaliação")
        lbl_nova.setObjectName("subtitulo_app")
        btn_add_file = CustomButton("Adicionar arquivo", command=self.add_new_file)
        header_esq.addWidget(lbl_nova)
        header_esq.addStretch()
        header_esq.addWidget(btn_add_file)

        self.evaluation_name_entry = CustomEntry(placeholder="Nome da nova avaliação")
        
        scroll_files = QScrollArea()
        scroll_files.setWidgetResizable(True)
        scroll_files.setObjectName("scroll_area")
        
        container_files = QWidget()
        container_files.setObjectName("fundo_transparente")
        self.layout_files_list = QVBoxLayout(container_files)
        scroll_files.setWidget(container_files)

        esq_layout.addLayout(header_esq)
        esq_layout.addWidget(self.evaluation_name_entry)
        esq_layout.addWidget(scroll_files)

        # --- Coluna Direita (Avaliações Anteriores) ---
        dir_widget = QWidget()
        dir_layout = QVBoxLayout(dir_widget)
        dir_layout.setContentsMargins(0, 0, 0, 0)

        lbl_antigas = QLabel("Avaliações Anteriores")
        lbl_antigas.setObjectName("subtitulo_app")

        scroll_evals = QScrollArea()
        scroll_evals.setWidgetResizable(True)
        scroll_evals.setObjectName("scroll_area")
        
        container_evals = QWidget()
        container_evals.setObjectName("fundo_transparente")
        self.layout_eval_list = QVBoxLayout(container_evals)
        scroll_evals.setWidget(container_evals)

        dir_layout.addWidget(lbl_antigas)
        dir_layout.addWidget(scroll_evals)

        # Adiciona as colunas ao Grid
        grid_painel.addWidget(esq_widget, 0, 0)
        grid_painel.addWidget(dir_widget, 0, 1)
        layout_principal.addLayout(grid_painel)

        # --- Rodapé ---
        layout_rodape = QHBoxLayout()
        self.back_button = CustomButton("Voltar", command=self.on_back)
        self.start_button = CustomButton("Iniciar Avaliação", command=self.start_evaluation_action)
        
        layout_rodape.addWidget(self.back_button)
        layout_rodape.addStretch()
        layout_rodape.addWidget(self.start_button)
        
        layout_principal.addLayout(layout_rodape)

    # Para Overlays (LoadingView e FileView) acompanharem a tela se for redimensionada
    def resizeEvent(self, event):
        if self.loading_overlay:
            self.loading_overlay.resize(self.size())
        if self.file_view:
            self.file_view.resize(self.size())
        super().resizeEvent(event)