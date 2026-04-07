import customtkinter as ctk
from tkinter import messagebox
from services.criteria_service import CriteriaService
from database import SessionLocal

class NewCriteriaView(ctk.CTkFrame):
    def __init__(self, parent, on_criteria_created, on_back, user_id):
        super().__init__(parent)
        self.on_criteria_created = on_criteria_created
        self.on_back = on_back
        self.user_id = user_id

        self.criteria_service = CriteriaService()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(5, weight=1)

        # Título
        label = ctk.CTkLabel(
            self,
            text="CodeRate",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        label = ctk.CTkLabel(self, text="Novo Critério", font=ctk.CTkFont(size=14))
        label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        # Campos
        label = ctk.CTkLabel(self, text="Nome", font=ctk.CTkFont(size=12))
        label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Nome do critério")
        self.name_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        label = ctk.CTkLabel(self, text="Descrição", font=ctk.CTkFont(size=12))
        label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.description_entry = ctk.CTkTextbox(self)
        self.description_entry.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        
        # Botões
        self.create_button = ctk.CTkButton(self, text="Criar", command=self.create_criteria)
        self.create_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.back)
        self.back_button.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

    def back(self):
        self.on_back()

    def create_criteria(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get("0.0", "end").strip()

        if not name or not description:
            messagebox.showerror("Erro", "Preencha nome e descrição.")
            return

        db = SessionLocal()
        try:
            criteria = self.criteria_service.create_criteria(db, name, description, self.user_id)
            if criteria:
                self.on_criteria_created(criteria)
            else:
                messagebox.showerror("Erro", "Não foi possível criar o critério.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()