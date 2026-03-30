import customtkinter as ctk

ctk.set_appearance_mode("system")   # "light", "dark" ou "system"
ctk.set_default_color_theme("blue") # tema padrão

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CodeRate")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.main_frame.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="CodeRate",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Tela inicial para testes do sistema"
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.create_user_button = ctk.CTkButton(
            self.main_frame,
            text="Cadastrar usuário",
            command=self.on_create_user
        )
        self.create_user_button.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.list_users_button = ctk.CTkButton(
            self.main_frame,
            text="Listar usuários",
            command=self.on_list_users
        )
        self.list_users_button.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.output_box = ctk.CTkTextbox(self.main_frame, width=700, height=300)
        self.output_box.grid(row=4, column=0, padx=20, pady=20, sticky="nsew")

        self.main_frame.grid_rowconfigure(4, weight=1)

    def on_create_user(self):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "Aqui depois você vai abrir a tela de cadastro.\n")

    def on_list_users(self):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", "Aqui depois você vai buscar os usuários no banco.\n")