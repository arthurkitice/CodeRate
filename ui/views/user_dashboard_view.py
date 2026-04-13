import customtkinter as ctk
from services.user_service import UserService
from services.criteria_service import CriteriaService
from ui.views.new_criteria_view import NewCriteriaView
from ui.views.dashboard_form_view import DashboardFormView
from database import get_db
from ui.widgets import create_criterion_button, create_edit_button, create_remove_button

class DashboardView(DashboardFormView):
    def __init__(self, parent, user, on_criteria_create, on_criteria_edit, on_logout):
        self.user_service = UserService()
        self.criteria_service = CriteriaService()
        self.user = user
        self.on_criteria_create = on_criteria_create
        self.on_criteria_edit = on_criteria_edit
        self.on_logout = on_logout
        super().__init__(parent)

    def _gen_criteria_list(self):
        try:
            with get_db() as db:
                criteria = self.criteria_service.list_criteria_by_user_id(db, self.user.id)
                return list(reversed(criteria[-4:]))
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")

    def logout(self):
        self.on_logout()

    def create_criteria(self):
        user_id = self.user.id
        self.on_criteria_create(user_id)

    def delete_criteria(self, criteria_id):
        try:
            with get_db() as db:
                self.criteria_service.delete_criteria(db, criteria_id)
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")

        self._gen_criteria_buttons()

    def build_ui(self):
        # Título
        self.add_title()
        self.add_heading("Critérios de Avaliação")
        self.add_username(self.user.name)

        # Botão
        self.logout_button = ctk.CTkButton(self, text="Encerrar Sessão", command=self.logout)
        self.logout_button.grid(row=0, column=3, padx=20, pady=10, sticky="ew")

        self.create_criteria_button = ctk.CTkButton(self, text="Criar Critério", command=self.create_criteria)
        self.create_criteria_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self._gen_criteria_buttons()

    def _on_criterion_hover_enter(self, edit_btn, remove_btn):
        """Quando mouse entra no critério"""
        hover_color = "#171926"
        edit_btn.configure(fg_color=hover_color, bg_color=hover_color)
        remove_btn.configure(fg_color=hover_color, bg_color=hover_color)

    def _on_criterion_hover_leave(self, edit_btn, remove_btn):
        """Quando mouse sai do critério"""
        normal_color = "#212435"
        edit_btn.configure(fg_color=normal_color, bg_color=normal_color)
        remove_btn.configure(fg_color=normal_color, bg_color=normal_color)

    def _gen_criteria_buttons(self): 
        # Lista os últimos 4 critérios (ou menos, preenchidos com None)
        criteria_list = self._gen_criteria_list()

        if getattr(self, "criteria_frame", None):
            self.criteria_frame.destroy()

        # Container para a lista de critérios
        self.criteria_frame = ctk.CTkFrame(self, fg_color="transparent")  # Torna o fundo transparente
        self.criteria_frame.grid(row=4, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

        # Configure weight para TODAS as 4 colunas (0 a 3), para dividir igualmente (1/4 cada)
        for col in range(4):
            self.criteria_frame.grid_columnconfigure(col, weight=1, minsize=400, pad=5)

        for i, criterion in enumerate(criteria_list):
            # Botão principal
            criterion_button = create_criterion_button(self, frame=self.criteria_frame, criterion=criterion)
            criterion_button.grid(row=1, column=i, rowspan=3, padx=10, pady=5, sticky="we")
            
            # Botões pequenos
            edit_button = create_edit_button(self, frame=self.criteria_frame, criterion=criterion)
            edit_button.place(in_=criterion_button, relx=0.85, rely=0.1, anchor="ne")
            
            remove_button = create_remove_button(self, frame=self.criteria_frame, criterion=criterion)
            remove_button.place(in_=criterion_button, relx=0.97, rely=0.1, anchor="ne")

            # Sincroniza o hover: quando o mouse entra/sai do criterion_button, muda os pequenos
            criterion_button.bind("<Enter>", lambda e, eb= edit_button, rb=remove_button: self._on_criterion_hover_enter(eb, rb))
            criterion_button.bind("<Leave>", lambda e, eb= edit_button, rb=remove_button: self._on_criterion_hover_leave(eb, rb))
