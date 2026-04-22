# ui/views/login_view.py
from services import UserService
from database import get_db
from ui.widgets import create_button
from ui.views.centered_form_view import CenteredFormView

class AuthSelectorView(CenteredFormView):
    def __init__(self, parent, on_login, on_register):
        self.on_login = on_login
        self.on_register = on_register
        self.user_service = UserService()
        super().__init__(parent)
    
    def build_ui(self):
        """Constrói a UI do login"""
        row = 1
        
        # Header
        row = self.add_title(row)
        row = self.add_heading(row, "Bem vindo(a)")
        row = self.add_description(row, "Crie ou conecte-se a uma conta para utilizar o aplicativo")

        # Botões
        self.login_button = create_button(self, "Fazer Login", self.on_login)
        self.login_button.grid(row=row, column=1, padx=20, pady=10)
        row += 1

        self.back_button = create_button(self, "Cadastrar", self.on_register)
        self.back_button.grid(row=row, column=1, padx=20, pady=10)
