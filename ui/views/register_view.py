import customtkinter as ctk
from tkinter import messagebox
from services.user_service import UserService
from database import SessionLocal

class RegisterView(ctk.CTkFrame):
    def __init__(self, parent, on_registered, on_back):
        super().__init__(parent)
        self.on_registered = on_registered
        self.on_back = on_back
        self.user_service = UserService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)


        # Título
        label = ctk.CTkLabel(
            self,
            text="CodeRate",
            font=ctk.CTkFont(size=24, weight="bold"),
            justify="center"
        )
        label.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        label = ctk.CTkLabel(
            self,
            text="Conectar",
            font=ctk.CTkFont(size=14),
            justify="center"
        )
        label.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        # Campos
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Nome")
        self.name_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.grid(row=4, column=1, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.password_entry.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        # Botões
        self.register_button = ctk.CTkButton(self, text="Registrar", command=self.register)
        self.register_button.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.back)
        self.back_button.grid(row=7, column=1, padx=20, pady=10, sticky="ew")

    def back(self):
        self.on_back()

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showerror("Erro", "Preencha nome, email e senha.")
            return

        db = SessionLocal()
        try:
            user = self.user_service.create_user(db, name, email, password)
            self.on_registered(user)
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()