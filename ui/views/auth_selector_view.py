import customtkinter as ctk
from tkinter import messagebox
from services.user_service import UserService
from database import get_db

class AuthSelectorView(ctk.CTkFrame):
    def __init__(self, parent, on_logon, on_login):
        super().__init__(parent)
        self.on_logon = on_logon
        self.on_login = on_login
        self.user_service = UserService()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(99, weight=1)

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
            text="Bem vindo(a)",
            font=ctk.CTkFont(size=28),
            justify="center"
        )
        label.grid(row=2, column=1, padx=20, pady=10, sticky="sew")

        label = ctk.CTkLabel(
            self,
            text="Conecte-se para utilizar o sistema",
            font=ctk.CTkFont(size=18),
            justify="center"
        )
        label.grid(row=3, column=1, padx=20, pady=10, sticky="new")
        
        # Botões
        self.logon_button = self._create_button("Conectar", self.on_logon)
        self.logon_button.grid(row=4, column=1, padx=20, pady=10)

        self.login_button = self._create_button("Cadastrar", self.on_login)
        self.login_button.grid(row=5, column=1, padx=20, pady=10)

    def _create_button(self, text, command):
        return ctk.CTkButton(
            self,
            font=ctk.CTkFont(size=15),
            width=350,
            height=35,
            text=text,
            cursor="hand2",
            command=command
        )
