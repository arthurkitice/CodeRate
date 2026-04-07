import customtkinter as ctk
from services.user_service import UserService
from ui.views.new_criteria_view import NewCriteriaView

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.user_service = UserService()
        self.user = user
        self.on_logout = on_logout
        
        self.build_ui()
        

    def logout(self):
        self.on_logout()

    def clear_content(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_criteria(self):
        self.clear_content()
        self.grid_rowconfigure(1, weight=1)
        view = NewCriteriaView(
            self,
            on_criteria_created=self.show_dashboard,
            on_back=self.show_dashboard,
            user_id=self.user.id
        )
        view.grid(row=1, column=1, rowspan=3, sticky="nsew")

    def show_dashboard(self, *args):
        self.clear_content()
        self.build_ui()

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)

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

        self.create_criteria_button = ctk.CTkButton(self, text="Criar Critério", command=self.create_criteria)
        self.create_criteria_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
