import customtkinter as ctk
from services.user_service import UserService

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.user_service = UserService()
        self.user = user
        self.on_logout = on_logout
        
        self.grid_columnconfigure(0, weight=1)

        # Título
        self.label = ctk.CTkLabel(
            self,
            text=f"Bem-vindo, {self.user.name}!",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Subtítulo (opcional)
        self.subtitle = ctk.CTkLabel(
            self,
            text="Você está autenticado no sistema.",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Botão
        self.logout_button = ctk.CTkButton(self, text="Encerrar Sessão", command=self.logout)
        self.logout_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

    def logout(self):
        self.on_logout()