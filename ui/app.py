import customtkinter as ctk
from tkinter import messagebox

from database import SessionLocal
from services.user_service import UserService

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CodeRate")
        self.geometry("900x600")
        self.minsize(800, 500)

        self.user_service = UserService()

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

        self.name_label = ctk.CTkLabel(self.main_frame, text="Nome")
        self.name_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.name_entry = ctk.CTkEntry(self.main_frame, width=300)
        self.name_entry.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.email_label = ctk.CTkLabel(self.main_frame, text="Email")
        self.email_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

        self.email_entry = ctk.CTkEntry(self.main_frame, width=300)
        self.email_entry.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.password_label = ctk.CTkLabel(self.main_frame, text="Senha")
        self.password_label.grid(row=6, column=0, padx=20, pady=10, sticky="w")

        self.password_entry = ctk.CTkEntry(self.main_frame, width=600, show="*")
        self.password_entry.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        self.save_button = ctk.CTkButton(
            self.main_frame,
            text="Cadastrar usuário",
            command=self.create_user
        )
        self.save_button.grid(row=8, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        self.list_button = ctk.CTkButton(
            self.main_frame,
            text="Listar usuários",
            command=self.list_users
        )
        self.list_button.grid(row=9, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        self.output_box = ctk.CTkTextbox(self.main_frame, height=250)
        self.output_box.grid(row=10, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

        self.main_frame.grid_rowconfigure(10, weight=1)

    def create_user(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showerror("Erro", "Preencha nome, email e senha.")
            return

        db = SessionLocal()
        try:
            user = self.user_service.create_user(db, name, email, password)

            messagebox.showinfo("Sucesso", f"Usuário {user.name} cadastrado com sucesso.")

            self.name_entry.delete(0, "end")
            self.email_entry.delete(0, "end")
            self.password_entry.delete(0, "end")

            self.list_users()

        except ValueError as e:
            messagebox.showerror("Erro", str(e))
        except Exception as e:
            messagebox.showerror("Erro inesperado", str(e))
        finally:
            db.close()

    def list_users(self):
        db = SessionLocal()
        try:
            users = self.user_service.list_users(db)

            self.output_box.delete("1.0", "end")

            if not users:
                self.output_box.insert("end", "Nenhum usuário cadastrado.\n")
                return

            for user in users:
                self.output_box.insert(
                    "end",
                    f"ID: {user.id} | Nome: {user.name} | Email: {user.email} | Senha: {user.password}\n"
                )

        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()