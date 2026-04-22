# ui/views/login_view.py
from services import UserService
from database import get_db
from ui.widgets import create_button, create_entry
from ui.views.centered_form_view import CenteredFormView

class LoginView(CenteredFormView):
    def __init__(self, parent, on_authenticated, on_back):
        self.on_authenticated = on_authenticated
        self.on_back = on_back
        self.user_service = UserService()
        super().__init__(parent)
    
    def build_ui(self):
        """Constrói a UI do login"""
        row = 1
        
        # Header
        row = self.add_title(row)
        row = self.add_heading(row, "Fazer Login")
        row = self.add_description(row, "Digite suas credenciais para acessar a conta")
        
        # Campos
        self.email_entry = create_entry(self, "Email@dominio.com")
        self.email_entry.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        self.password_entry = create_entry(self, "Senha", show="*")
        self.password_entry.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        # Bindings
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Botões
        self.login_button = create_button(self, "Login", self.login, width=350, height=35)
        self.login_button.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        self.back_button = create_button(self, "Voltar", self.back, width=350, height=35)
        self.back_button.grid(row=row, column=1, padx=20, pady=10)
    
    def back(self):
        """Limpa campos e volta"""
        self.clear_fields(self.email_entry, self.password_entry)
        self.on_back()
    
    def login(self):
        """Realiza login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validação UX
        if not email or not password:
            self.show_error("Preencha email e senha.")
            return
        
        if "@" not in email:
            self.show_error("Email inválido.")
            return
        
        # Autentica
        try:
            with get_db() as db:
                user = self.user_service.authenticate_user(db, email, password)
                self.clear_fields(self.email_entry, self.password_entry)
                self.focus()
                self.on_authenticated(user)
        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")