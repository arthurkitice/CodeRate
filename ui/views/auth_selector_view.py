import customtkinter as ctk

class AuthSelectorView(ctk.CTkFrame):
    def __init__(self, parent, on_login, on_register):
        super().__init__(parent)
        self.on_login = on_login
        self.on_register = on_register
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)

        # Título
        self.label = ctk.CTkLabel(
            self,  # << Direto em self, não em self.content
            text="CodeRate",
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="left"
        )
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Subtítulo
        self.subtitle = ctk.CTkLabel(
            self,
            text="\nCritérios de Avaliação",
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        self.subtitle.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="n")

        # Botões
        self.register_button = ctk.CTkButton(self, text="Registrar", command=self.register)
        self.register_button.grid(row=0, column=2, padx=20, pady=10, sticky="ew")

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.grid(row=0, column=3, padx=20, pady=10, sticky="ew")

    def register(self):
        self.on_register()

    def login(self):
        self.on_login()