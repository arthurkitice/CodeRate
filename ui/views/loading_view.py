from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QProgressBar
from PySide6.QtCore import Qt
import time
import random
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout,
    QLabel, QFrame
)
from PySide6.QtCore import Qt, Signal, QThread
from services import EvaluationService, SubmissionService
from services import CriteriaService
from services import AIService

class LoadingView(QWidget):
    def __init__(self, criteria_id, avaliacao_nome, files, on_finished, on_error, parent=None):
        super().__init__(parent)
        self.criteria_id = criteria_id
        self.avaliacao_nome = avaliacao_nome
        self.files = files
        self.total_files = len(files)
        
        # Rotas de navegação injetadas pelo app.py
        self.on_finished = on_finished
        self.on_error = on_error

        self.build_ui()
        self.start_processing()

    def build_ui(self):
        # Layout principal centraliza tudo no meio da tela
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter) 

        # O "Card" que você usava no CustomTkinter
        self.card = QFrame()
        self.card.setObjectName("loading_card")
        self.card.setFixedSize(450, 250)

        card_layout = QVBoxLayout(self.card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(25)

        self.title_label = QLabel("Processando Avaliação")
        self.title_label.setObjectName("loading_title")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Barra de progresso nativa
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("loading_progress")
        # A MÁGICA: O Qt calcula a porcentagem sozinho baseado no min/max
        self.progress_bar.setRange(0, self.total_files) 
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False) # Esconde aquele "0%" feio no meio da barra

        self.status_label = QLabel("Preparando arquivos...")
        self.status_label.setObjectName("loading_status")
        self.status_label.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(self.title_label)
        card_layout.addWidget(self.progress_bar)
        card_layout.addWidget(self.status_label)

        layout.addWidget(self.card)

    def start_processing(self):
        # A LoadingView instancia e roda a Thread
        self.ai_worker = AIEvaluationWorker(self.criteria_id, self.avaliacao_nome, self.files)
        
        self.ai_worker.progress_updated.connect(self.update_progress)
        self.ai_worker.error_occurred.connect(self.handle_error)
        self.ai_worker.finished_success.connect(self.finish)
        
        self.ai_worker.start()

    def update_progress(self, current: int, filename: str):
        self.progress_bar.setValue(current)
        self.status_label.setText(f"Avaliando: {filename} ({current}/{self.total_files})")

    def handle_error(self, error_msg):
        # Avisa o App para voltar e exibir o erro
        self.on_error(error_msg, self.criteria_id)

    def finish(self, evaluation_id):
        self.progress_bar.setValue(self.total_files)
        self.status_label.setText("Avaliação concluída!")
        
        # Um pequeno delay estético de 1.5s antes de pular para a tela de resultados
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1500, lambda: self.on_finished(evaluation_id))


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
                content=submission.content,
                score=score,
                feedback=feedback
            )
            
            if i < len(self.files):
                time.sleep(4.0 + random.uniform(0.1, 1.5)) # Simulação de delay

        self.submission_service.calculate_and_save_similarities(evaluation_dto.id)
        # Avisa a tela que terminou e passa o ID
        self.finished_success.emit(evaluation_dto.id)

