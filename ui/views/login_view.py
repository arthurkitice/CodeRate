import customtkinter as ctk
from tkinter import messagebox
from services.user_service import UserService
from database import SessionLocal

class LoginView(ctk.CTkFrame):
    def __init__(self, parent, on_authenticated, on_back):
        super().__init__(parent)
        self.on_authenticated = on_authenticated
        self.on_back = on_back
        self.user_service = UserService()
        
        self.grid_columnconfigure(0, weight=1)

        # Título
        label = ctk.CTkLabel(
            self,
            text="Login",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Campos
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Botões
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.back_button = ctk.CTkButton(self, text="Voltar", command=self.back)
        self.back_button.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

    def back(self):
        self.on_back()

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Erro", "Preencha email e senha.")
            return

        db = SessionLocal()
        try:
            user = self.user_service.authenticate_user(db, email, password)
            if user:
                self.on_authenticated(user)
            else:
                messagebox.showerror("Erro", "Email ou senha inválidos.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()