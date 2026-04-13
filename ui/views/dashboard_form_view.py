# ui/views/centered_form_view.py
import customtkinter as ctk
from ui.views.base_view import BaseView

class DashboardFormView(BaseView):
    def setup_grid(self):
        self.grid_columnconfigure(1, weight=1)
    
    def add_title(self, row: int = 0, column: int = 0):
        """Adiciona título 'CodeRate' padrão"""
        label = ctk.CTkLabel(
            self,
            text="CodeRate",
            font=ctk.CTkFont(size=38, weight="bold"),
            justify="left"
        )
        label.grid(row=row, column=column, padx=20, pady=(40, 20), sticky="w")
    
    def add_heading(self, text: str, row: int = 2, column: int = 0):
        """Adiciona subtítulo (ex: 'Fazer Login')"""
        label = ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=26),
            justify="left"
        )
        label.grid(row=row, column=column, padx=20, pady=20, sticky="wn")
    
    def add_username(self, name: str, row: int = 0, column: int = 2):
        """Adiciona descrição (ex: 'Digite suas credenciais...')"""
        label = ctk.CTkLabel(
            self,
            text=name,
            font=ctk.CTkFont(size=26, weight="bold"),
            justify="left"
        )
        label.grid(row=row, column=column, padx=20, pady=20, sticky="w")