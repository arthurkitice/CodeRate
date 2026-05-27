from database import get_db
import customtkinter as ctk
from services import EvaluationService, SubmissionService
from ui.views.dashboard_form_view import DashboardFormView
from ui.widgets import SmallButton, EditButton, RemoveButton, CustomButton
from functools import partial

class FileView(DashboardFormView):
    def __init__(self, parent, submission, on_back = None):
        self.submission = submission
        self.on_back = on_back
        super().__init__(parent)

    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=80, sticky="nsew")

        self.add_title(frame=self.main_frame)

        self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="main")
        self.main_frame.grid_rowconfigure(2, weight=1, uniform="main")

        self.file_label = ctk.CTkLabel(self.main_frame, text=self.submission.file_name, font=ctk.CTkFont(size=20, weight="bold"))
        self.file_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        conteudo_bruto = self.submission.content if self.submission.content else "Conteúdo não disponível."
        conteudo_formatado = conteudo_bruto.replace('\t', '    ')
        fonte_codigo = ctk.CTkFont(family="Consolas", size=15)
        self.textbox = ctk.CTkTextbox(self.main_frame, border_width=2, font=fonte_codigo)
        self.textbox.grid(row=2, column=0, columnspan=3, padx=20, pady=(0, 10), sticky="nsew")
        self.textbox.insert("0.0", conteudo_formatado)
        self.textbox.configure(state="disabled")

        self.bottom_frame = ctk.CTkFrame(self.main_frame)
        self.bottom_frame.grid(row=99, column=0, pady=(0, 80), sticky="nsew")

        self.back_button = CustomButton(self.bottom_frame, text="Voltar", command=self.back)
        self.back_button.grid(row=0, column=0, padx=20, pady=10, sticky = "ws")

    def back(self):
        if self.on_back:
            self.on_back()
        else:
            self.destroy()