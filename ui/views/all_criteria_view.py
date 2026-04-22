from database import get_db
import customtkinter as ctk
from services import UserService, CriteriaService
from ui.views.dashboard_form_view import DashboardFormView
from ui.widgets import create_small_criterion_button as criteria_button
from ui.widgets import create_edit_button, create_remove_button, NORMAL_COLOR

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

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.grid(row=2, column=0, sticky="nsew")
        self.button_frame.grid_columnconfigure(0, weight=1)

        for i, criterion in enumerate(criteria_list):
            self.criteria_button = criteria_button(self.button_frame, criterion=criterion, command= lambda c=criterion: self.build_criteria_info(c, 2, 1))
            self.criteria_button.grid(row=row+i, column=column, padx=(20, 5), pady=10, sticky="ew")

            self.edit_button = create_edit_button(self, self.button_frame, criterion=criterion, no_bg_color=False)
            self.remove_button = create_remove_button(self, self.button_frame, criterion, no_bg_color=False)

            self.edit_button.grid(row=row+i, column=column+1, padx=5, pady=10, sticky="ew")
            self.remove_button.grid(row=row+i, column=column+2, padx=5, pady=10, sticky="ew")
    
    def build_criteria_info(self, criteria, row=2, column=1):
        if getattr(self, "info_frame", None):
            self.info_frame.destroy()

        self.info_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color=NORMAL_COLOR)
        self.info_frame.grid(row=row, column=column, sticky="nsew", padx=20, pady=10)
        self.info_frame.grid_columnconfigure(0, weight=1)

        r = 0
        self.name_label = ctk.CTkLabel(self.info_frame, text="Nome:", font=ctk.CTkFont(size=15), justify="left", text_color="gray")
        self.name_label.grid(row=r, column=0, padx=10, pady=10, sticky="w")
        r+=1

        self.criteria_label = ctk.CTkLabel(self.info_frame, text=criteria.name, font=ctk.CTkFont(size=20), justify="left")
        self.criteria_label.grid(row=r, column=0, padx=10, pady=0, sticky="w")
        r+=1

        self.description_label = ctk.CTkLabel(self.info_frame, text="Descrição:", font=ctk.CTkFont(size=15), justify="left", text_color="gray")
        self.description_label.grid(row=r, column=0, padx=10, pady=(40, 10), sticky="w")
        r+=1

        self.criteria_desc_label = ctk.CTkLabel(self.info_frame, text=criteria.description, font=ctk.CTkFont(size=20), justify="left")
        self.criteria_desc_label.grid(row=r, column=0, padx=10, pady=0, sticky="w")
        r+=1


    def build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, padx=80, sticky="nsew")

        self.add_title(frame=self.main_frame)
        self.add_heading(frame=self.main_frame, text="Todos os critérios de avaliação", row=1)

        self.main_frame.grid_columnconfigure((0, 1), weight=1, uniform="main")
        self.main_frame.grid_rowconfigure(2, weight=1, uniform="main")

        self.build_criteria_buttons()

        self.info_frame = ctk.CTkFrame(self.main_frame, corner_radius=10, fg_color=NORMAL_COLOR)
        self.info_frame.grid(row=2, column=1, sticky="nsew", padx=20, pady=10)
        self.info_frame.grid_columnconfigure(0, weight=1)

        self.info_label = ctk.CTkLabel(self.info_frame, text="Selecione um critério\npara visualizar\nseu conteúdo", font=ctk.CTkFont(size=18), text_color="gray", justify="center")
        self.info_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.info_frame.grid_rowconfigure(0, weight=1)


        self.back_button = ctk.CTkButton(self, text="Voltar", command=lambda: self.on_back())
        self.back_button.grid(row=99, column=0, padx=80, pady=80, sticky = "ws")
