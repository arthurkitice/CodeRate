import customtkinter as ctk
from services import CriteriaService
from ui.views.dashboard_form_view import DashboardFormView
from ui.widgets import CriterionButton, CustomButton

class DashboardView(DashboardFormView):
    def __init__(
            self, 
            parent,
            on_criteria_create, 
            on_criteria_edit, 
            on_all_criteria, 
            on_start_evaluation
        ):

        self.criteria_service = CriteriaService()
        self.on_criteria_create = on_criteria_create
        self.on_criteria_edit = on_criteria_edit
        self.on_all_criteria = on_all_criteria
        self.on_start_evaluation = on_start_evaluation
        super().__init__(parent)

    def _gen_criteria_list(self):
        criteria = self.criteria_service.list_criteria()
        return list(reversed(criteria[-4:]))

    def create_criteria(self):
        self.on_criteria_create()

    def delete_criteria(self, criteria_id):
        self.criteria_service.delete_criteria(criteria_id)
        self._gen_criteria_buttons()

    def edit_criteria(self, criteria_id):
        self.on_criteria_edit(criteria_id=criteria_id)

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        # Título
        self.add_title(self)
        self.add_heading(self, "Critérios de Avaliação")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=1, column=0)

        self.create_criteria_button = CustomButton(self.button_frame, text="Criar Critério", command=self.create_criteria)
        self.create_criteria_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.list_criteria_button = CustomButton(self.button_frame, text="Todos os Critérios", command= self.on_all_criteria)
        self.list_criteria_button.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

        self._gen_criteria_buttons()

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
            criterion_button = CriterionButton(parent=self, frame=self.criteria_frame, text=criterion.name, criteria_id=criterion.id)
            criterion_button.grid(row=1, column=i, rowspan=3, padx=10, pady=5, sticky="we")
