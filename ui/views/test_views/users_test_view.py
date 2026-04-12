import customtkinter as ctk
from tkinter import messagebox

from database import get_db
from services.user_service import UserService


class UsersTestView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.user_service = UserService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(8, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Testes de Usuário",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        # ID
        
        self.id_entry = ctk.CTkEntry(self, placeholder_text="ID")
        self.id_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Nome
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Nome")
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Email
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Senha
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Botões
        self.create_button = ctk.CTkButton(self, text="Criar", command=self.create_user)
        self.create_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.list_button = ctk.CTkButton(self, text="Listar", command=self.list_users)
        self.list_button.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        self.get_by_id_button = ctk.CTkButton(self, text="Buscar por ID", command=self.get_user_by_id)
        self.get_by_id_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.update_button = ctk.CTkButton(self, text="Atualizar", command=self.update_user)
        self.update_button.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        self.delete_button = ctk.CTkButton(self, text="Deletar", command=self.delete_user, fg_color="red", hover_color="#cc0a0a")
        self.delete_button.grid(row=7, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Saída
        self.output_box = ctk.CTkTextbox(self, height=220)
        self.output_box.grid(row=8, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    def write_output(self, text: str):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", text)

    def create_user(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showerror("Erro", "Preencha nome, email e senha.")
            return

        try:
            with get_db() as db:
                user = self.user_service.create_user(db, name, email, password)
                self.write_output(f"Usuário criado com sucesso:\nID: {user.id}\nNome: {user.name}\nEmail: {user.email}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def list_users(self):
        try:
            with get_db() as db:
                users = self.user_service.list_users(db)

                if not users:
                    self.write_output("Nenhum usuário cadastrado.")
                    return

                output = []
                for user in users:
                    output.append(f"ID: {user.id} | Nome: {user.name} | Email: {user.email} | Senha: {user.password}")

                self.write_output("\n".join(output))
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def get_user_by_id(self):
        user_id = self.id_entry.get().strip()

        if not user_id:
            messagebox.showerror("Erro", "Informe um ID.")
            return

        try:
            with get_db() as db:
                user = self.user_service.get_user_by_id(db, int(user_id))

                if user is None:
                    self.write_output("Usuário não encontrado.")
                    return

                self.write_output(f"Usuário encontrado:\nID: {user.id}\nNome: {user.name}\nEmail: {user.email}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def update_user(self):
        user_id = self.id_entry.get().strip()
        new_name = self.name_entry.get().strip()
        new_email = self.email_entry.get().strip()
        new_password = self.password_entry.get().strip()

        if not user_id:
            messagebox.showerror("Erro", "Informe o ID para atualizar.")
            return

        try:
            with get_db() as db:
                user = self.user_service.update_user(
                    db,
                    int(user_id),
                    new_name=new_name if new_name else None,
                    new_email=new_email if new_email else None,
                    new_password=new_password if new_password else None
                )

                if user is None:
                    self.write_output("Usuário não encontrado.")
                    return

                self.write_output(f"Usuário atualizado:\nID: {user.id}\nNome: {user.name}\nEmail: {user.email}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def delete_user(self):
        user_id = self.id_entry.get().strip()

        if not user_id:
            messagebox.showerror("Erro", "Informe o ID para deletar.")
            return

        try:
            with get_db() as db:
                deleted = self.user_service.delete_user(db, int(user_id))

                if not deleted:
                    self.write_output("Usuário não encontrado.")
                    return

                self.write_output("Usuário deletado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))