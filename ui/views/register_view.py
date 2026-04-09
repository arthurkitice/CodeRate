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
        self.grid_rowconfigure(9, weight=1)


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
            text="Criar conta",
            font=ctk.CTkFont(size=28),
            justify="center"
        )
        label.grid(row=2, column=1, padx=20, pady=10, sticky="sew")

        label = ctk.CTkLabel(
            self,
            text="Cadastre seus dados para criar a conta",
            font=ctk.CTkFont(size=18),
            justify="center"
        )
        label.grid(row=3, column=1, padx=20, pady=10, sticky="new")

        # Campos
        self.name_entry = self._create_entry("Nome de usuário")
        self.name_entry.grid(row=4, column=1, padx=20, pady=10)

        self.email_entry = self._create_entry("Email@dominio.com")
        self.email_entry.grid(row=5, column=1, padx=20, pady=10)

        self.password_entry = self._create_entry("Senha", show="*")
        self.password_entry.grid(row=6, column=1, padx=20, pady=10)

        # Botões
        self.register_button = self._create_button("Cadastrar", self.register)
        self.register_button.grid(row=7, column=1, padx=20, pady=10)

        self.back_button = self._create_button("Voltar", self.back)
        self.back_button.grid(row=8, column=1, padx=20, pady=10)

    def _create_entry(parent, placeholder, **kwargs):
        return ctk.CTkEntry(
            parent,
            font=ctk.CTkFont(size=15),
            width=400,
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
            width=400,
            height=35,
            text=text,
            cursor="hand2",
            command=command
        )
    
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