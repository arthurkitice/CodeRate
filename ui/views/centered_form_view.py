# ui/views/centered_form_view.py
import customtkinter as ctk
from ui.views.base_view import BaseView

class CenteredFormView(BaseView):
    """
    View base para formulários centralizados (Login, Register, etc).
    Define grid 3x3 com conteúdo na coluna central.
    """
    
    def setup_grid(self):
        """Grid 3 colunas, conteúdo centralizado"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(99, weight=1)  # Última row expande
    
    def add_title(self, row: int):
        """Adiciona título 'CodeRate' padrão"""
        label = ctk.CTkLabel(
            self,
            text="CodeRate",
            font=ctk.CTkFont(size=50),
            justify="center"
        )
        label.grid(row=row, column=1, padx=20, pady=10, sticky="ew")
        return row + 1
    
    def add_heading(self, row: int, text: str):
        """Adiciona subtítulo (ex: 'Fazer Login')"""
        label = ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=28),
            justify="center"
        )
        label.grid(row=row, column=1, padx=20, pady=10, sticky="sew")
        return row + 1
    
    def add_description(self, row: int, text: str):
        """Adiciona descrição (ex: 'Digite suas credenciais...')"""
        label = ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=18),
            justify="center"
        )
        label.grid(row=row, column=1, padx=20, pady=10, sticky="new")
        return row + 1