import customtkinter as ctk
from ui.app import MainApp
from ui.app_test import TestApp

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CodeRate")
        self.geometry("600x500")  # Tamanho melhor

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_columnconfigure(1, weight=1)  # << Adicione isso


        # Título
        self.label = ctk.CTkLabel(
            self.content,
            text=f"CodeRate",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        # Subtítulo (opcional)
        self.subtitle = ctk.CTkLabel(
            self.content,
            text="Escolha qual aplicação deseja acessar.",
            font=ctk.CTkFont(size=14)
        )
        self.subtitle.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="w")

        self.content.app_button = ctk.CTkButton(self.content, text="Principal", command=self.app_initialize)
        self.content.app_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        self.content.test_button = ctk.CTkButton(self.content, text="Testes", command=self.app_test)
        self.content.test_button.grid(row=2, column=1, padx=20, pady=10, sticky="ew")

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def app_initialize(self):
        self.destroy()
        app = MainApp()
        app.mainloop()

    def app_test(self):
        self.destroy()
        app = TestApp()
        app.mainloop()