import customtkinter as ctk
from ui.app import MainApp
from ui.app_test import TestApp

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("ui/color_theme.json")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CodeRate")
        self.geometry("1100x700")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.current_view = None
        self.show_menu()

    def clear_current_view(self):
        if self.current_view is not None:
            self.current_view.destroy()

    def show_menu(self):
        self.clear_current_view()

        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        label = ctk.CTkLabel(
            frame,
            text="CodeRate",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        subtitle = ctk.CTkLabel(
            frame,
            text="Escolha qual aplicação deseja acessar.",
            font=ctk.CTkFont(size=14)
        )
        subtitle.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        app_button = ctk.CTkButton(frame, text="Principal", command=self.show_main_app)
        app_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        test_button = ctk.CTkButton(frame, text="Testes", command=self.show_test_app)
        test_button.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

        self.current_view = frame

        self.show_main_app()

    def show_main_app(self):
        self.clear_current_view()
        self.current_view = MainApp(self)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def show_test_app(self):
        self.clear_current_view()
        self.current_view = TestApp(self)
        self.current_view.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()