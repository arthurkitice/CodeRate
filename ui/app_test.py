import customtkinter as ctk
from ui.views.test_views.users_test_view import UsersTestView
from ui.views.test_views.criteria_test_view import CriteriaTestView


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class TestApp(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="CodeRate",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.users_button = ctk.CTkButton(
            self.sidebar,
            text="Usuários",
            command=self.show_users_tests
        )
        self.users_button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.criteria_button = ctk.CTkButton(
            self.sidebar,
            text="Critérios",
            command=self.show_criteria_tests
        )
        self.criteria_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.exit_button = ctk.CTkButton(
            self.sidebar,
            text="Sair",
            command=self.destroy,
            fg_color="red"
        )
        self.exit_button.grid(row=99, column=0, padx=20, pady=20, sticky="ew")

        # Área principal
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self.show_home()

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_content()

        label = ctk.CTkLabel(
            self.content,
            text="Selecione uma área na sidebar para testar os métodos.",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        label.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

    def show_users_tests(self):
        self.clear_content()
        view = UsersTestView(self.content)
        view.grid(row=0, column=0, sticky="nsew")

    def show_criteria_tests(self):
        self.clear_content()
        view = CriteriaTestView(self.content)
        view.grid(row=0, column=0, sticky="nsew")