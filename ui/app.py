import customtkinter as ctk
from services.user_service import UserService
from ui.views.login_view import LoginView
from ui.views.register_view import RegisterView
from ui.views.auth_selector_view import AuthSelectorView
from ui.views.user_dashboard_view import DashboardView
from ui.views.new_criteria_view import NewCriteriaView
from ui.views.edit_criteria_view import EditCriteriaView
from ui.views.all_criteria_view import AllCriteriaView

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("ui/color_theme.json")

class MainApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Container principal para as views
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.current_user = None

        # Dicionário para armazenar views (lazy loading)
        self.views = {
            "auth_selector":
            AuthSelectorView(
                self.container,
                on_login=lambda: self.show_view("login"),
                on_register=lambda: self.show_view("register")
            ),
            "login":
            LoginView(
                self.container,
                on_authenticated=self.on_authenticated,
                on_back=lambda: self.show_view("auth_selector")
            ),
            "register":
            RegisterView(
                self.container,
                on_registered=self.on_authenticated,
                on_back=lambda: self.show_view("auth_selector")
            ),
        }

        # Comece com a view inicial (ex.: auth selector)
        self.show_view("auth_selector")

    def show_view(self, view_name, **kwargs):
        # Esconda/destrua a view atual se existir
        if hasattr(self, 'current_view') and self.current_view:
            self.current_view.pack_forget()  # Destrua completamente para liberar memória

        # Crie a nova view se não existir
        if view_name not in self.views:
            if view_name == "dashboard":
                user = kwargs.get("user")
                self.current_view = DashboardView(
                    self.container,
                    user=user,
                    on_criteria_create=lambda user_id: self.show_view("new_criteria", user_id=user_id),
                    on_criteria_edit=lambda user_id, criteria_id: self.show_view("edit_criteria", user_id=user_id, criteria_id=criteria_id),
                    on_all_criteria=lambda user_id: self.show_view("all_criteria", user_id=user_id),
                    on_logout=lambda: self.show_view("auth_selector")
                )
            if view_name == "new_criteria":
                user_id = kwargs.get("user_id")
                self.current_view = NewCriteriaView(
                    self.container,
                    on_criteria_created=self.go_to_dashboard,
                    on_back=self.go_to_dashboard,
                    user_id=user_id
                )
            if view_name == "edit_criteria":
                user_id = kwargs.get("user_id")
                criteria_id = kwargs.get("criteria_id")
                all_criteria = kwargs.get("all_criteria")

                command = self.go_to_dashboard if not all_criteria else self.go_to_all_criteria
        
                self.current_view = EditCriteriaView(
                    self.container,
                    on_criteria_updated=command,
                    on_back=command,
                    criteria_id=criteria_id,
                    user_id=user_id
                )
            if view_name == "all_criteria":
                user_id = kwargs.get("user_id")
                self.current_view = AllCriteriaView(
                    self.container,
                    user_id=user_id,
                    on_criteria_create=lambda user_id: self.show_view("new_criteria", user_id=user_id),
                    on_criteria_edit=lambda user_id, criteria_id: self.show_view("edit_criteria", user_id=user_id, criteria_id=criteria_id, all_criteria=True),
                    on_back=self.go_to_dashboard
                )
            # ... adicione outras views aqui
        else:
            # Mostre a nova view
            if view_name == "auth_selector": self.current_user = None
            self.current_view = self.views[view_name]
        self.current_view.pack(fill="both", expand=True)
    
    def refresh_current_user(self):
        """Recarrega o usuário atual do banco de dados"""
        if self.current_user:
            from database import get_db
            
            try:
                with get_db() as db:
                    user_service = UserService()
                    self.current_user = user_service.get_user_with_criteria(db, self.current_user.id)
            except Exception as e:
                print(f"Erro: {e}")

    def go_to_dashboard(self):
        self.refresh_current_user()
        self.show_view("dashboard", user=self.current_user)

    def go_to_all_criteria(self):
        self.refresh_current_user()
        self.show_view("all_criteria", user_id=self.current_user.id)

    def on_authenticated(self, user):
        self.show_view("dashboard", user=user)
        self.current_user = user