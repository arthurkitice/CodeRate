import customtkinter as ctk
from services.user_service import UserService

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.user_service = UserService()
        self.user = user
        self.on_logout = on_logout
        
        self.grid_columnconfigure(1, weight=1)

        # Título
        self.label = ctk.CTkLabel(
            self,
            text="CodeRate",
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="left"
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.label = ctk.CTkLabel(
            self,
            text=f"{self.user.name}",
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="left"
        )
        self.label.grid(row=0, column=2, padx=20, pady=20, sticky="w")

        # Subtítulo (opcional)
        self.subtitle = ctk.CTkLabel(
            self,
            text="\nCritérios de Avaliação",
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        self.subtitle.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")

        # Botão
        self.logout_button = ctk.CTkButton(self, text="Encerrar Sessão", command=self.logout)
        self.logout_button.grid(row=0, column=3, padx=20, pady=10, sticky="ew")

    def logout(self):
        self.on_logout()