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
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        # Título
        label = ctk.CTkLabel(
            self,
            text="CodeRate",
            font=ctk.CTkFont(size=50),
            justify="center"
        )
        label.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        label = ctk.CTkLabel(
            self,
            text="Fazer Login",
            font=ctk.CTkFont(size=28),
            justify="center"
        )
        label.grid(row=2, column=1, padx=20, pady=10, sticky="sew")

        label = ctk.CTkLabel(
            self,
            text="Digite suas credenciais para acessar a conta",
            font=ctk.CTkFont(size=18),
            justify="center"
        )
        label.grid(row=3, column=1, padx=20, pady=10, sticky="new")

        # Campos
        self.email_entry = self._create_entry("Email@dominio.com")
        self.email_entry.grid(row=4, column=1, padx=20, pady=10)

        self.password_entry = self._create_entry("Senha", show="*")
        self.password_entry.grid(row=5, column=1, padx=20, pady=10)

        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Botões
        self.login_button = self._create_button("Login", self.login)
        self.login_button.grid(row=6, column=1, padx=20, pady=10)

        self.back_button = self._create_button("Voltar", self.back)
        self.back_button.grid(row=7, column=1, padx=20, pady=10)

    def back(self):
        self.on_back()

    def _create_entry(parent, placeholder, **kwargs):
        return ctk.CTkEntry(
            parent,
            font=ctk.CTkFont(size=15),
            width=350,
            height=35,
            placeholder_text=placeholder,
            border_width=0,
            fg_color="white",
            text_color="black",
            **kwargs
        )

    def _create_button(parent, text, command):
        return ctk.CTkButton(
            parent,
            font=ctk.CTkFont(size=15),
            width=350,
            height=35,
            text=text,
            cursor="hand2",
            command=command
        )
   

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