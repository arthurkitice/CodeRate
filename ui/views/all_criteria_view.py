from database import get_db
import customtkinter as ctk
from services.user_service import UserService
from services.criteria_service import CriteriaService
from ui.views.dashboard_form_view import DashboardFormView
from ui.widgets import create_small_criterion_button as criteria_button
from ui.widgets import create_edit_button, create_remove_button

class AllCriteriaView(DashboardFormView):
    def __init__(self, parent, user_id, on_criteria_create, on_criteria_edit, on_back):
        self.user_service = UserService()
        self.criteria_service = CriteriaService()
        self.user_id = user_id
        self.on_criteria_create = on_criteria_create
        self.on_criteria_edit = on_criteria_edit
        self.on_back = on_back
        super().__init__(parent)

    def _list_all_criteria(self):
        try:
            with get_db() as db:
                criteria = self.criteria_service.list_criteria_by_user_id(db, self.user_id)
                return list(reversed(criteria))
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")

    def edit_criteria(self, criteria_id):
        self.on_criteria_edit(criteria_id=criteria_id, user_id=self.user_id)

    def delete_criteria(self, criteria_id):
        try:
            with get_db() as db:
                self.criteria_service.delete_criteria(db, criteria_id)
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")

        self.build_criteria_buttons()

    def build_criteria_buttons(self, row=0, column=0):
        criteria_list = self._list_all_criteria()

        if getattr(self, "button_frame", None):
            self.button_frame.destroy()

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        for i, criterion in enumerate(criteria_list):
            self.criteria_button = criteria_button(self.button_frame, criterion=criterion, command=lambda: self.show_info("Função à ser implementada."))
            self.criteria_button.grid(row=row+i, column=column, padx=(20, 5), pady=10, sticky="ew")

            self.edit_button = create_edit_button(self, self.button_frame, criterion=criterion, no_bg_color=False)
            self.remove_button = create_remove_button(self, self.button_frame, criterion, no_bg_color=False)

            self.edit_button.grid(row=row+i, column=column+1, padx=5, pady=10, sticky="ew")
            self.remove_button.grid(row=row+i, column=column+2, padx=5, pady=10, sticky="ew")
        
    def build_ui(self):
        self.add_title()
        self.add_heading("Todos os critérios de avaliação", row=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.build_criteria_buttons()

        self.back_button = ctk.CTkButton(self, text="Voltar", command=lambda: self.on_back())
        self.back_button.grid(row=99, column=0, padx=20, pady=20, sticky = "w")
