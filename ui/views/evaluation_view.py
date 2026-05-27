from database import get_db
import customtkinter as ctk
from services import EvaluationService, SubmissionService
from ui.views.dashboard_form_view import DashboardFormView
from ui.views.file_view import FileView
from ui.widgets import SmallButton, RemoveButton, CustomButton
from functools import partial
import threading
import time
from ui.views.loading_view import LoadingView

class EvaluationView(DashboardFormView):
    def __init__(self, parent, criteria_id, on_back, on_start):
        self.evaluation_service = EvaluationService()
        self.submission_service = SubmissionService()
        self.criteria_id = criteria_id
        self.on_back = on_back
        self.on_new_file = None
        self.on_start = on_start
        self.files = []
        super().__init__(parent)

    def _list_all_evaluations(self):
        evaluation = self.evaluation_service.list_evaluations_by_criteria(self.criteria_id)
        return list(reversed(evaluation))

    def add_new_file(self):
        """Callback do botão 'Adicionar arquivo'"""
        draft_dto = self.submission_service.select_file()
        
        if draft_dto:
            self.files.append(draft_dto)
            self.build_evaluation_files()

    def delete_evaluation(self, evaluation_id):
        self.evaluation_service.delete_evaluation(evaluation_id)
        # Ao deletar, recria a lista garantindo que ela volte para a mesma posição
        self.build_evaluation_buttons()

    def build_evaluation_buttons(self, row, column):
        evaluation_list = self._list_all_evaluations()

        title = ctk.CTkLabel(self.main_frame, text="Avaliações Anteriores", font=ctk.CTkFont(size=26))
        title.grid(row=row - 1, column=column, sticky="w", padx=20, pady=10)

        self.scroll_evaluations = ctk.CTkScrollableFrame(self.main_frame)
        self.scroll_evaluations.grid(row=row, column=column, sticky="nsew", padx=20)
        self.scroll_evaluations.grid_columnconfigure(0, weight=1)

        for i, evaluation in enumerate(evaluation_list):
            btn = SmallButton(self.scroll_evaluations, text=evaluation.name, command=partial(self.on_start, evaluation.id))
            btn.grid(row=i, column=0, padx=(0, 5), pady=5, sticky="ew")

            rem = RemoveButton(self.scroll_evaluations, command=partial(self.delete_evaluation, evaluation.id), no_bg_color=False)
            rem.grid(row=i, column=1, padx=5, pady=5)

    def remove_file(self, submission):
        self.files.remove(submission)
        self.build_evaluation_files()

    def build_evaluation_files(self, row=2, column=0):
        if getattr(self, "files_frame", None):
            self.files_frame.destroy()

        # Agora vai dentro do left_content_frame, não no main_frame
        self.files_frame = ctk.CTkScrollableFrame(self.left_content_frame)
        self.files_frame.grid(row=1, column=0, sticky="nsew")
        self.files_frame.grid_columnconfigure(0, weight=1)

        for i, submission in enumerate(self.files):
            btn = SmallButton(self.files_frame, text=submission.file_name, command=partial(self.on_file_click, submission))
            btn.grid(row=i, column=0, padx=(0, 5), pady=5, sticky="ew")

            rem = RemoveButton(self.files_frame, command=partial(self.remove_file, submission), no_bg_color=False)
            rem.grid(row=i, column=1, padx=5, pady=5)

    def build_new_evaluation(self, row, column):
        # Só o cabeçalho (título + botão) no row anterior
        self.upper_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.upper_frame.grid(row=row - 1, column=column, sticky="nsew", padx=20)
        self.upper_frame.grid_columnconfigure(0, weight=1)

        self.evaluation_name = ctk.CTkLabel(self.upper_frame, text="Nova avaliação", font=ctk.CTkFont(size=26))
        self.evaluation_name.grid(row=0, column=0, pady=10, sticky="w")

        self.evaluation_new_file = CustomButton(self.upper_frame, text="Adicionar arquivo", command=self.add_new_file)
        self.evaluation_new_file.grid(row=0, column=0, pady=10, sticky="e")

        # Entry + files no row principal (mesmo row do scroll da direita)
        self.left_content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.left_content_frame.grid(row=row, column=column, sticky="nsew", padx=20)
        self.left_content_frame.grid_columnconfigure(0, weight=1)
        self.left_content_frame.grid_rowconfigure(1, weight=1)

        self.evaluation_name_entry = ctk.CTkEntry(self.left_content_frame, placeholder_text="Nome da nova avaliação", font=ctk.CTkFont(size=16), height=45)
        self.evaluation_name_entry.grid(row=0, column=0, pady=(0, 10), sticky="ew")

    def on_file_click(self, submission):
        if hasattr(self, "file_view") and self.file_view is not None:
            self.file_view.destroy()

        self.file_view = FileView(self, submission)
        self.file_view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.file_view.tkraise()

    def start_evaluation_action(self):
        avaliacao_nome = self.evaluation_name_entry.get().strip()

        if not avaliacao_nome:
            self.show_error("Por favor, insira um nome para a avaliação.")
            return

        if not self.files:
            self.show_error("Adicione pelo menos um arquivo de código para avaliar!")
            return

        self.loading_overlay = LoadingView(self, total_files=len(self.files))
        self.loading_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading_overlay.tkraise()
        self.start_button.configure(state="disabled")

        # Passa o nome capturado para a Thread
        threading.Thread(target=self._run_ai_process, args=(avaliacao_nome,), daemon=True).start()

    def _run_ai_process(self, avaliacao_nome):
        from services.criteria_service import CriteriaService
        from services.ai_service import AIService
        
        criteria_service = CriteriaService()
        try:
            ai_service = AIService()
        except ValueError as e:
            self.after(0, self.loading_overlay.destroy)
            self.after(0, self.start_button.configure, "normal")
            self.after(0, self.show_error, str(e))
            return

        criteria_dto = criteria_service.get_criteria_by_id(self.criteria_id)
        if not criteria_dto:
            self.after(0, self.loading_overlay.destroy)
            self.after(0, self.start_button.configure, "normal")
            self.after(0, self.show_error, "Erro: Critério de avaliação não encontrado.")
            return

        evaluation_dto = self.evaluation_service.create_evaluation(
            criteria_id=self.criteria_id,
            name=avaliacao_nome
        )

        for i, submission in enumerate(self.files, start=1):
            self.after(0, self.loading_overlay.update_progress, i, submission.file_name)
            
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

            time.sleep(5)

        self.after(0, self._on_evaluation_finished, evaluation_dto.id)

    def _on_evaluation_finished(self, evaluation_id):
        self.loading_overlay.finish()
        self.after(1500, self.loading_overlay.destroy)
        self.after(1500, self.start_button.configure, "normal")
        self.after(1500, lambda: self.on_start(evaluation_id))

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=80, sticky="nsew")

        self.add_title(frame=self.main_frame)

        # Configuração da grid interna: Coluna 0 (Nova avaliação/Arquivos) e Coluna 1 (Anteriores)
        self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="main")
        self.main_frame.grid_rowconfigure(2, weight=1) # A linha das listas expande

        self.build_new_evaluation(row=2, column=0)   # títulos em row=1, conteúdo em row=2
        self.build_evaluation_buttons(row=2, column=1)
        # build_evaluation_files agora é chamado dentro de build_new_evaluation implicitamente,
        # mas ainda precisa ser chamado para inicializar o files_frame:
        self.build_evaluation_files()

        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.grid(row=99, column=0, columnspan=2, pady=(0, 80), sticky="nsew")

        self.back_button = CustomButton(self.bottom_frame, text="Voltar", command=self.back)
        self.back_button.grid(row=0, column=0, padx=20, pady=10, sticky="ws")

        self.start_button = CustomButton(self.bottom_frame, text="Iniciar Avaliação", command=self.start_evaluation_action)
        self.start_button.grid(row=0, column=1, padx=20, pady=10, sticky="ws")

    def back(self):
        self.on_back()