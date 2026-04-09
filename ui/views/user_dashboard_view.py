import customtkinter as ctk
from services.user_service import UserService
from services.criteria_service import CriteriaService
from ui.views.new_criteria_view import NewCriteriaView

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout):
        super().__init__(parent)
        self.user_service = UserService()
        self.criteria_service = CriteriaService()
        self.user = user
        self.on_logout = on_logout
        self.build_ui()

    def _gen_criteria_list(self):
        criteria = self.user.criteria
        return list(reversed(criteria[-4:]))

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
            font=ctk.CTkFont(size=38, weight="bold"),
            justify="left"
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        self.label = ctk.CTkLabel(
            self,
            text=f"{self.user.name}",
            font=ctk.CTkFont(size=26, weight="bold"),
            justify="left"
        )
        self.label.grid(row=0, column=2, padx=20, pady=20, sticky="w")

        # Subtítulo (opcional)
        self.subtitle = ctk.CTkLabel(
            self,
            text="\nCritérios de Avaliação",
            font=ctk.CTkFont(size=26),
            justify="left"
        )
        self.subtitle.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="n")

        # Botão
        self.logout_button = ctk.CTkButton(self, text="Encerrar Sessão", command=self.logout)
        self.logout_button.grid(row=0, column=3, padx=20, pady=10, sticky="ew")

        self.create_criteria_button = ctk.CTkButton(self, text="Criar Critério", command=self.create_criteria)
        self.create_criteria_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # Lista os últimos 4 critérios (ou menos, preenchidos com None)
        criteria_list = self._gen_criteria_list()

        # Container para a lista de critérios
        criteria_frame = ctk.CTkFrame(self, fg_color="transparent")  # Torna o fundo transparente
        criteria_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        # Configure weight para TODAS as 4 colunas (0 a 3), para dividir igualmente (1/4 cada)
        for col in range(4):
            criteria_frame.grid_columnconfigure(col, weight=1)

        for i, criterion in enumerate(criteria_list):
            if criterion is None:
                break  # Só adiciona botões para critérios válidos
            
            # Botão principal (parece label) para iniciar avaliação
            criterion_button = ctk.CTkButton(
                criteria_frame,
                text=f"{criterion.name}",
                command=lambda c=criterion: self.start_evaluation(c.id),
                border_width=0,
                corner_radius=30,
                font=ctk.CTkFont(size=12),
                anchor="center",  # Mantém fixo, mas agora a coluna o expande
                height=200
            )
            criterion_button.grid(row=1, column=i, rowspan=3, padx=10, pady=5, sticky="nsew")
            
            # Botão de editar - movido para row=0, sticky="ne" (canto superior direito, como overlay)
            button_frame = ctk.CTkFrame(criteria_frame, fg_color="transparent")
            button_frame.grid(row=0, column=i, sticky="nsew")

            edit_button = ctk.CTkButton(
                button_frame,
                text="Editar",
                border_width=0,
                hover_color=None,
                corner_radius=100,
                font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda c=criterion: self.edit_criterion(c.id),
                width=30,   # Um pouco menor para ficar discreto
                height=30   # Menor
            )
            remove_button = ctk.CTkButton(
                button_frame,
                text="Remover",
                border_width=0,
                hover_color=None,
                corner_radius=100,
                font=ctk.CTkFont(size=10, weight="bold"),
                command=lambda c=criterion: self.remove_criterion(c.id),
                width=30,   # Um pouco menor para ficar discreto
                height=30   # Menor
            )
            remove_button.grid(row=0, column=1, padx=10, pady=5, sticky="ne")  # Nordeste, sem sobrepor texto
            edit_button.grid(row=0, column=0, padx=10, pady=5, sticky="ne")  # Nordeste, sem sobrepor texto
