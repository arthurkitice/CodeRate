import customtkinter as ctk
from ui.views.login_view import LoginView
from ui.views.register_view import RegisterView
from ui.views.auth_selector_view import AuthSelectorView
from ui.views.user_dashboard_view import DashboardView

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CodeRate")
        self.geometry("600x500")  # Tamanho melhor

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.show_auth_selector()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_auth_selector(self):
        self.clear_content()
        view = AuthSelectorView(self.content,
            on_login=self.show_login,
            on_register=self.show_register)
        view.grid(row=0, column=0, sticky="nsew")

    def show_login(self):
        self.clear_content()
        view = LoginView(self.content,
            on_authenticated=self.show_dashboard,
            on_back=self.show_auth_selector)
        view.grid(row=0, column=0, sticky="nsew")

    def show_register(self):
        self.clear_content()
        view = RegisterView(self.content, on_registered=self.show_dashboard, on_back=self.show_auth_selector)
        view.grid(row=0, column=0, sticky="nsew")

    def show_dashboard(self, user):
        self.clear_content()
        view = DashboardView(self.content, user=user, on_logout=self.show_auth_selector)
        view.grid(row=0, column=0, sticky="nsew")