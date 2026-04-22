from services import UserService
from database import get_db
from ui.widgets import create_button, create_entry
from ui.views.centered_form_view import CenteredFormView

class RegisterView(CenteredFormView):
    def __init__(self, parent, on_registered, on_back):
        self.on_registered = on_registered
        self.on_back = on_back
        self.user_service = UserService()
        super().__init__(parent)
    
    def build_ui(self):
        """Constrói a UI do registro"""
        row = 1
        
        # Header
        row = self.add_title(row)
        row = self.add_heading(row, "Criar conta")
        row = self.add_description(row, "Crie sua conta e comece a avaliar seus códigos")
        
        # Campos
        self.name_entry = create_entry(self, "Nome de usuário")
        self.name_entry.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        self.email_entry = create_entry(self, "Email@dominio.com")
        self.email_entry.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        self.password_entry = create_entry(self, "Senha", show="*")
        self.password_entry.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        # Bindings
        self.name_entry.bind("<Return>", lambda e: self.email_entry.focus())
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.register())
        
        # Botões
        self.register_button = create_button(self, "Cadastrar", self.register, width=350, height=35)
        self.register_button.grid(row=row, column=1, padx=20, pady=10)
        row += 1
        
        self.back_button = create_button(self, "Voltar", self.back, width=350, height=35)
        self.back_button.grid(row=row, column=1, padx=20, pady=10)
    
    def back(self):
        """Limpa campos e volta"""
        self.clear_fields(self.name_entry, self.email_entry, self.password_entry)
        self.on_back()
    
    def register(self):
        """Realiza registro"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validação UX
        if not name or not email or not password:
            self.show_error("Preencha todos os campos.")
            return
        
        if "@" not in email:
            self.show_error("Email inválido.")
            return
        
        # Registra
        try:
            with get_db() as db:
                user = self.user_service.create_user(db, name, email, password)
                self.clear_fields(self.name_entry, self.email_entry, self.password_entry)
                self.focus()
                self.on_registered(user)
        except ValueError as e:
            self.show_error(str(e))
        except Exception as e:
            self.show_error(f"Erro inesperado: {str(e)}")