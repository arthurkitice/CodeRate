import customtkinter as ctk
from services import SettingsService
from ui.views.dashboard_form_view import DashboardFormView
from ui.widgets import LabelEntry, CustomButton

class SettingsView(DashboardFormView):
    def __init__(
            self, 
            parent,
            on_back
        ):

        self.settings_service = SettingsService()
        self.on_back = on_back
        super().__init__(parent)
        
        self.pack(padx=50, pady=50)

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        # Título
        self.add_title(self)
        self.add_heading(self, "Configurações")

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=3, column=0, padx=20, sticky="nsew")

        self.api_frame = LabelEntry(self.content_frame, "Chave API:")
        self.api_frame.grid(row=0, column=0, sticky="nsew")
        self.api_frame.set(self.settings_service.get_api_key())

        self.back_button = CustomButton(self, text="Voltar", command=self.back)
        self.back_button.grid(row=10, column=0, padx=20, pady=30, sticky="ew")

    def back(self):
        self.settings_service.save_api_key(self.api_frame.get())
        self.on_back()
