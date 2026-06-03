import sys
import time
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QLabel, QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QThread
from ui.widgets import CustomButton, CustomEntry, SmallButton # Presumindo seus novos widgets
from services import EvaluationService, SubmissionService
from services import CriteriaService
from services import AIService

# Importações fictícias baseadas no seu código
# from ui.views.file_view import FileView
# from ui.views.loading_view import LoadingView

# ==========================================
# 1. A Classe da Thread (O Trabalhador em Background)
# ==========================================
class AIEvaluationWorker(QThread):
    # Sinais para comunicar com a interface principal de forma segura
    progress_updated = Signal(int, str)
    finished_success = Signal(int)
    error_occurred = Signal(str)

    def __init__(self, criteria_id, avaliacao_nome, files):
        super().__init__()
        self.criteria_id = criteria_id
        self.avaliacao_nome = avaliacao_nome
        self.files = files
        
        self.criteria_service = CriteriaService()
        self.evaluation_service = EvaluationService()
        self.submission_service = SubmissionService()

    def run(self):
        """Este método roda em um núcleo separado do processador."""
        try:
            ai_service = AIService()
        except ValueError as e:
            self.error_occurred.emit(str(e))
            return

        criteria_dto = self.criteria_service.get_criteria_by_id(self.criteria_id)
        if not criteria_dto:
            self.error_occurred.emit("Erro: Critério de avaliação não encontrado.")
            return

        evaluation_dto = self.evaluation_service.create_evaluation(
            criteria_id=self.criteria_id,
            name=self.avaliacao_nome
        )

        for i, submission in enumerate(self.files, start=1):
            # Emite sinal para atualizar a UI (substitui o self.after)
            self.progress_updated.emit(i, submission.file_name)
            
            resultado = ai_service.evaluate_code(
                criteria_name=criteria_dto.name,
                criteria_description=criteria_dto.description,
                file_name=submission.file_name,
                code_content=submission.content if submission.content else ""
            )
            
            score = resultado.get("score", 0.0)
            feedback = resultado.get("feedback", "Nenhum feedback foi gerado.")

            self.submission_service.create_submission(
                evaluation_id=evaluation_dto.id,
                file_name=submission.file_name,
                file_path=submission.file_path,
                score=score,
                feedback=feedback
            )
            time.sleep(5) # Simulação de delay

        # Avisa a tela que terminou e passa o ID
        self.finished_success.emit(evaluation_dto.id)


# ==========================================
# 2. A Tela Principal (EvaluationView)
# ==========================================
class EvaluationView(QWidget):
    def __init__(self, criteria_id, on_back, on_start, parent=None):
        super().__init__(parent)
        self.evaluation_service = EvaluationService()
        self.submission_service = SubmissionService()
        self.criteria_id = criteria_id
        self.on_back = on_back
        self.on_start = on_start
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
            btn_open = SmallButton(evaluation.name, command=lambda e_id=evaluation.id: self.on_start(e_id))
            
            btn_del = CustomButton("🗑️")
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

            btn_open = SmallButton(submission.file_name, command=lambda s=submission: self.on_file_click(s))
            
            btn_del = CustomButton("🗑️")
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
        if self.file_view is not None:
            self.file_view.deleteLater()

        # self.file_view = FileView(self, submission)
        # self.file_view.show()
        # self.file_view.raise_() # Equivalente ao tkraise()
        pass

    # --- O Fluxo da IA (Multithreading) ---
    def start_evaluation_action(self):
        avaliacao_nome = self.evaluation_name_entry.text().strip()

        if not avaliacao_nome:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um nome para a avaliação.")
            return

        if not self.files:
            QMessageBox.warning(self, "Aviso", "Adicione pelo menos um arquivo de código para avaliar!")
            return

        # self.loading_overlay = LoadingView(self, total_files=len(self.files))
        # self.loading_overlay.show()
        # self.loading_overlay.raise_()
        
        self.start_button.setEnabled(False)

        # Inicia a Thread da IA
        self.ai_worker = AIEvaluationWorker(self.criteria_id, avaliacao_nome, self.files)
        
        # Conecta os sinais da Thread às funções desta tela
        self.ai_worker.progress_updated.connect(self._update_loading_progress)
        self.ai_worker.error_occurred.connect(self._handle_ai_error)
        self.ai_worker.finished_success.connect(self._on_evaluation_finished)
        
        self.ai_worker.start()

    def _update_loading_progress(self, index, file_name):
        if self.loading_overlay:
            pass
            # self.loading_overlay.update_progress(index, file_name)

    def _handle_ai_error(self, error_msg):
        if self.loading_overlay:
            self.loading_overlay.deleteLater()
            self.loading_overlay = None
            
        self.start_button.setEnabled(True)
        QMessageBox.critical(self, "Erro na Avaliação", error_msg)

    def _on_evaluation_finished(self, evaluation_id):
        if self.loading_overlay:
            self.loading_overlay.deleteLater() # Você pode implementar a animação de "finish" antes
            self.loading_overlay = None
            
        self.start_button.setEnabled(True)
        self.on_start(evaluation_id)

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