import customtkinter as ctk
from .views.user_dashboard_view import DashboardView
from ui.views.new_criteria_view import NewCriteriaView
from ui.views.edit_criteria_view import EditCriteriaView
from ui.views.all_criteria_view import AllCriteriaView
from ui.views.evaluation_view import EvaluationView
from functools import partial

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("ui/color_theme.json")

class MainApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Container principal para as views
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.dashboard = partial(self.show_view, "dashboard")

        self.show_view("dashboard")

    def show_view(self, view_name, **kwargs):
        # Esconda/destrua a view atual se existir
        if hasattr(self, 'current_view') and self.current_view:
            self.current_view.pack_forget()

        if view_name not in self.views:
            if view_name == "dashboard":
                self.current_view = DashboardView(
                    self.container,
                    on_criteria_create=lambda: self.show_view("new_criteria"),
                    on_criteria_edit=lambda criteria_id: self.show_view("edit_criteria", criteria_id=criteria_id),
                    on_all_criteria=lambda: self.show_view("all_criteria"),
                    on_start_evaluation=lambda criteria_id: self.show_view("start_evaluation", criteria_id=criteria_id)
                )
            if view_name == "new_criteria":
                self.current_view = NewCriteriaView(
                    self.container,
                    on_criteria_created=self.dashboard,
                    on_back=self.dashboard
                )
            if view_name == "edit_criteria":
                criteria_id = kwargs.get("criteria_id")
                all_criteria = kwargs.get("all_criteria")

                command = self.dashboard if not all_criteria else partial(self.show_view, "all_criteria")
        
                self.current_view = EditCriteriaView(
                    self.container,
                    on_criteria_updated=command,
                    on_back=command,
                    criteria_id=criteria_id
                )
            if view_name == "all_criteria":
                self.current_view = AllCriteriaView(
                    self.container,
                    on_criteria_create=lambda: self.show_view("new_criteria"),
                    on_criteria_edit=lambda criteria_id: self.show_view("edit_criteria", criteria_id=criteria_id, all_criteria=True),
                    on_back=self.dashboard
                )
            if view_name == "start_evaluation":
                criteria_id = kwargs.get("criteria_id")
                self.current_view = EvaluationView(
                    self.container,
                    criteria_id=criteria_id,
                    on_back=self.dashboard
                )
        else:
            self.current_view = self.views[view_name]
        self.current_view.pack(fill="both", expand=True)
