# ui/views/base_view.py
import customtkinter as ctk
from abc import ABC, abstractmethod

class BaseView(ctk.CTkFrame, ABC):
    """
    View base para todas as telas do CodeRate.
    Define estrutura comum e métodos que podem ser sobrescritos.
    """
    def __init__(self, parent, **kwargs):
        super().__init__(parent)
        self.setup_grid()
        self.build_ui()
    
    def setup_grid(self):
        """Configura grid básico. Sobrescreva se precisar de config diferente."""
        pass
    
    @abstractmethod
    def build_ui(self):
        """Método abstrato - cada view implementa sua UI aqui"""
        pass
    
    def clear_fields(self, *fields):
        """Limpa campos de entrada"""
        for field in fields:
            if isinstance(field, ctk.CTkEntry):
                placeholder = field.cget("placeholder_text")
                field.delete(0, "end")
                field.configure(placeholder_text=placeholder)
            elif isinstance(field, ctk.CTkTextbox):
                field.delete("0.0", "end")
        self.focus()
    
    def show_error(self, message: str):
        """Exibe mensagem de erro"""
        from tkinter import messagebox
        messagebox.showerror("Erro", message)
    
    def show_info(self, message: str):
        """Exibe mensagem informativa"""
        from tkinter import messagebox
        messagebox.showinfo("Informação", message)