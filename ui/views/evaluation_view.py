from database import get_db
import customtkinter as ctk
from services import EvaluationService, SubmissionService
from dtos import SubmissionDTO
from ui.views.dashboard_form_view import DashboardFormView
from ui.widgets import create_small_button, create_button, create_edit_button, create_remove_button
from functools import partial

class EvaluationView(DashboardFormView):
    def __init__(self, parent, criteria_id, on_back):
        self.evaluation_service = EvaluationService()
        self.submission_service = SubmissionService()
        self.criteria_id = criteria_id
        self.on_back = on_back
        self.on_new_file = None
        self.on_start = None
        self.files:list[SubmissionDTO] = []
        super().__init__(parent)

    def _list_all_evaluations(self):
        try:
            with get_db() as db:
                evaluation = self.evaluation_service.list_evaluations_by_criteria(db, self.criteria_id)
                return list(reversed(evaluation))
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")

    def add_new_file(self):
        """Callback do botão 'Adicionar arquivo'"""
        # Aqui você precisa ter o evaluation_id
        # Se for uma nova avaliação, pode criar temporariamente ou esperar salvar
        
        file_name, file_path = self.submission_service.select_and_save_file(
            evaluation_id=999  # Temporário, ajustar depois
        )
        
        if file_name and file_path:
            # Cria DTO temporário (ainda não salvo no banco)
            submission = SubmissionDTO(
                id=0,
                evaluation_id=999,
                file_name=file_name,
                file_path=file_path,
                date="2026-04-29 00:28:31.560415",
                score=1,
                feedback=""
            )
            
            self.add_file(submission)

    def delete_evaluation(self, evaluation_id): #DELETAR AVALIAÇÃO AQUI
        try:
            with get_db() as db:
                self.evaluation_service.delete_evaluation(db, evaluation_id)
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")

        self.build_evaluation_buttons()

    def build_evaluation_buttons(self, row=0, column=0):
        evaluation_list = self._list_all_evaluations()

        if getattr(self, "button_frame", None):
            self.button_frame.destroy()

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=row, column=column, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        for i, evaluation in enumerate(evaluation_list):
            self.evaluation_button = create_small_button(self.button_frame, text=evaluation.name, command=partial())
            self.evaluation_button.grid(row=i, column=0, padx=(20, 5), pady=10, sticky="ew")

            self.remove_button = create_remove_button(self.button_frame, command=partial(self.delete_evaluation, evaluation.id), no_bg_color=False)
            self.remove_button.grid(row=i, column=1, padx=5, pady=10, sticky="ew")

    def add_file(self, submission):
        self.files.append(submission)
        self.build_evaluation_files(row=2)

    def remove_file(self, submission):
        self.files.remove(submission)
        self.build_evaluation_files(row=2)

    def build_evaluation_files(self, row=0, column=0):
        if getattr(self.main_frame, "files_frame", None):
            self.files_frame.destroy()

        self.files_frame = ctk.CTkFrame(self.main_frame)
        self.files_frame.grid(row=row, column=column, sticky="nsew")
        self.files_frame.grid_columnconfigure(0, weight=1)

        for i, submission in enumerate(self.files):
            self.submission_button = create_small_button(self.files_frame, text=submission.file_name, command=None, state="disabled")
            self.submission_button.grid(row=i, column=0, padx=(20, 5), pady=10, sticky="ew")

            self.remove_file_button = create_remove_button(self.files_frame, command=partial(self.remove_file, submission), no_bg_color=False)
            self.remove_file_button.grid(row=i, column=2, padx=5, pady=10, sticky="ew")

    def build_new_evaluation(self):
        self.upper_frame = ctk.CTkFrame(self.main_frame)
        self.upper_frame.grid(row=1, column=0, pady=(20, 0), sticky="nsew")
        self.upper_frame.grid_columnconfigure(0, weight=1)

        self.text_frame = ctk.CTkFrame(self.upper_frame)
        self.text_frame.grid(row=0, column=0, sticky="nsew")

        self.evaluation_name = ctk.CTkLabel(self.text_frame, text="Nova avaliação", font=ctk.CTkFont(size=26))
        self.evaluation_name.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.evaluation_new_file = create_button(self.text_frame, text="Adicionar arquivo", command=self.add_new_file)
        self.evaluation_new_file.grid(row=0, column=1, padx=20, pady=10, sticky="nw")

        self.evaluation_name_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Nome da nova avaliação", font=ctk.CTkFont(size=16), height=45)
        self.evaluation_name_entry.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=80, sticky="nsew")

        self.add_title(frame=self.main_frame)
        #self.add_heading(frame=self.main_frame, text="Todos os critérios de avaliação", row=1)

        self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="main")
        self.main_frame.grid_rowconfigure(2, weight=1, uniform="main")

        self.build_evaluation_buttons(row=2, column=1)

        self.build_new_evaluation()

        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.grid(row=99, column=0, pady=(0, 80), sticky="nsew")

        self.back_button = create_button(self.bottom_frame, text="Voltar", command=self.on_back)
        self.back_button.grid(row=0, column=0, padx=20, pady=10, sticky = "ws")

        self.start_button = create_button(self.bottom_frame, text="Iniciar Avaliação", command=self.on_start)
        self.start_button.grid(row=0, column=1, padx=20, pady=10, sticky = "ws")
