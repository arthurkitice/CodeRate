import customtkinter as ctk
from tkinter import messagebox
from services.criteria_service import CriteriaService
from database import get_db
from ui.views.dashboard_form_view import DashboardFormView

class NewCriteriaView(DashboardFormView):
    def __init__(self, parent, on_criteria_created, on_back, user_id, criteria_id=None):
        self.on_criteria_created = on_criteria_created
        self.on_back = on_back
        self.user_id = user_id
        self.criteria_id = criteria_id
        self.criteria_service = CriteriaService()
        super().__init__(parent)

    def build_ui(self):
        self.add_title()
        self.add_heading(self.get_subtitle(), row=1, column=1)

        self.grid_columnconfigure(0, weight=1, uniform="main")
        self.grid_columnconfigure(1, weight=3, uniform="main")
        self.grid_columnconfigure(2, weight=1, uniform="main")
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(99, weight=1)

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=3, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure((0, 1), weight=1)
        self.content_frame.grid_rowconfigure(3, weight=1)

        # Campos
        row = 0
        self.label = ctk.CTkLabel(self.content_frame, text="Nome", font=ctk.CTkFont(size=18))
        self.label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        row+=1

        self.name_entry = ctk.CTkEntry(self.content_frame, height=40)
        self.name_entry.grid(row=row, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
        row+=1

        self.label = ctk.CTkLabel(self.content_frame, text="Descrição", font=ctk.CTkFont(size=18))
        self.label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        row+=1

        self.description_entry = ctk.CTkTextbox(self.content_frame, border_width=2)
        self.description_entry.grid(row=row, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="nsew")
        row+=1

        # Botões
        self.create_button = ctk.CTkButton(
            self.content_frame, 
            text=self.get_button_text(), 
            command=self.save_criteria, 
            font=ctk.CTkFont(size=15),
            height=35
        )
        self.create_button.grid(row=row, column=0, padx=20, pady=30, sticky="ew")

        self.back_button = ctk.CTkButton(
            self.content_frame, 
            text="Voltar", 
            command=self.back, 
            font=ctk.CTkFont(size=15), 
            height=35
        )
        self.back_button.grid(row=row, column=1, padx=20, pady=30, sticky="ew")

    def get_subtitle(self):
        return "Novo Critério"
    
    def get_button_text(self):
        return "Criar Critério"

    def back(self):
        self.on_back()

    def save_criteria(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get("0.0", "end").strip()

        if not name or not description:
            self.show_error("Erro: Preencha nome e descrição.")
            return

        try:
            with get_db() as db:
                criteria = self.criteria_service.create_criteria(db, name, description, self.user_id)
                if criteria:
                    self.on_criteria_created()
                else:
                    messagebox.showerror("Erro", "Não foi possível criar o critério.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))