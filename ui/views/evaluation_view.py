from database import get_db
import customtkinter as ctk
from services import EvaluationService, SubmissionService
from ui.views.dashboard_form_view import DashboardFormView
from ui.views.file_view import FileView
from ui.widgets import SmallButton, EditButton, RemoveButton, CustomButton
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
        # Abre o seletor. Se o usuário escolher, ele já volta na pasta /tmp
        draft_dto = self.submission_service.select_file()
        
        if draft_dto:
            self.files.append(draft_dto)
            self.build_evaluation_files()

    def delete_evaluation(self, evaluation_id): #DELETAR AVALIAÇÃO AQUI
        self.evaluation_service.delete_evaluation(evaluation_id)
        self.build_evaluation_buttons()

    def build_evaluation_buttons(self, row=0, column=0):
        evaluation_list = self._list_all_evaluations()

        if getattr(self, "button_frame", None):
            self.button_frame.destroy()

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=row, column=column, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        for i, evaluation in enumerate(evaluation_list):
            self.evaluation_button = SmallButton(self.button_frame, text=evaluation.name, command=partial())
            self.evaluation_button.grid(row=i, column=0, padx=(20, 5), pady=10, sticky="ew")

            self.remove_button = RemoveButton(self.button_frame, command=partial(self.delete_evaluation, evaluation.id), no_bg_color=False)
            self.remove_button.grid(row=i, column=1, padx=5, pady=10, sticky="ew")

    def remove_file(self, submission):
        self.files.remove(submission)
        self.build_evaluation_files()

    def build_evaluation_files(self, row=2, column=0):
        if getattr(self.main_frame, "files_frame", None):
            self.files_frame.destroy()

        self.files_frame = ctk.CTkFrame(self.main_frame)
        self.files_frame.grid(row=row, column=column, sticky="nsew")
        self.files_frame.grid_columnconfigure(0, weight=1)

        for i, submission in enumerate(self.files):
            self.submission_button = SmallButton(self.files_frame, text=submission.file_name, command=partial(self.on_file_click, submission))
            self.submission_button.grid(row=i, column=0, padx=(20, 5), pady=10, sticky="ew")

            self.remove_file_button = RemoveButton(self.files_frame, command=partial(self.remove_file, submission), no_bg_color=False)
            self.remove_file_button.grid(row=i, column=2, padx=5, pady=10, sticky="ew")

    def build_new_evaluation(self):
        self.upper_frame = ctk.CTkFrame(self.main_frame)
        self.upper_frame.grid(row=1, column=0, pady=(20, 0), sticky="nsew")
        self.upper_frame.grid_columnconfigure(0, weight=1)

        self.text_frame = ctk.CTkFrame(self.upper_frame)
        self.text_frame.grid(row=0, column=0, sticky="nsew")

        self.evaluation_name = ctk.CTkLabel(self.text_frame, text="Nova avaliação", font=ctk.CTkFont(size=26))
        self.evaluation_name.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.evaluation_new_file = CustomButton(self.text_frame, text="Adicionar arquivo", command=self.add_new_file)
        self.evaluation_new_file.grid(row=0, column=1, padx=20, pady=10, sticky="nw")

        self.evaluation_name_entry = ctk.CTkEntry(self.upper_frame, placeholder_text="Nome da nova avaliação", font=ctk.CTkFont(size=16), height=45)
        self.evaluation_name_entry.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

    def on_file_click(self, submission):
        if hasattr(self, "file_view"):
            self.file_view = None

        self.file_view = FileView(self, submission)
        self.file_view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.file_view.tkraise()

    def start_evaluation_action(self):
        # if not self.files:
        #     print("Adicione pelo menos um arquivo!")
        #     return

        # 1. Cria e exibe a tela de carregamento por cima de tudo
        self.loading_overlay = LoadingView(self, total_files=len(self.files))
        self.loading_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.loading_overlay.tkraise()

        # 2. Desativa o botão de iniciar para evitar cliques duplos
        self.start_button.configure(state="disabled")

        # 3. Dispara a IA em uma Thread separada (para NÃO travar a tela)
        threading.Thread(target=self._run_ai_process, daemon=True).start()

    def _run_ai_process(self):
        """Este método roda escondido no fundo, liberando a interface gráfica."""
        
        for i, submission in enumerate(self.files, start=1):
            # AQUI ENTRA A INTEGRAÇÃO COM O AI_SERVICE futuramente
            # ex: ai_service.evaluate(submission.content)
            
            # Simulando o tempo de demora da IA (3 segundos por arquivo)
            time.sleep(3) 
            
            # ATENÇÃO: O Tkinter não gosta que métodos de fora atualizem a UI.
            # Usamos o .after(0, ...) para mandar a tela principal rodar a atualização com segurança.
            self.after(0, self.loading_overlay.update_progress, i, submission.file_name)

        # Quando o loop acabar, a avaliação terminou!
        self.after(0, self._on_evaluation_finished)

    def _on_evaluation_finished(self):
        """Volta para a thread principal para limpar a tela e ir para os resultados"""
        self.loading_overlay.finish()
        
        # Destrói o overlay após 1.5 segundos para o usuário ler "Concluído!"
        self.after(1500, self.loading_overlay.destroy)
        self.start_button.configure(state="normal")
        
        # Aqui você chamaria self.on_start() para mudar de fato para a tela final de Dashboard/Resultados
        self.on_start()

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

        self.back_button = CustomButton(self.bottom_frame, text="Voltar", command=self.back)
        self.back_button.grid(row=0, column=0, padx=20, pady=10, sticky = "ws")

        self.start_button = CustomButton(self.bottom_frame, text="Iniciar Avaliação", command=self.start_evaluation_action)
        self.start_button.grid(row=0, column=1, padx=20, pady=10, sticky = "ws")

    def back(self):
        self.on_back()