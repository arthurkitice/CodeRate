import customtkinter as ctk
from tkinter import messagebox

from database import SessionLocal
from services.criteria_service import CriteriaService


class CriteriaTestView(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.criteria_service = CriteriaService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(8, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Testes de Critério",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")

        # ID
        
        self.id_entry = ctk.CTkEntry(self, placeholder_text="ID")
        self.id_entry.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Nome
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Nome")
        self.name_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Descrição
        self.description_entry = ctk.CTkEntry(self, placeholder_text="Descrição")
        self.description_entry.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # ID do usuário
        self.user_id_entry = ctk.CTkEntry(self, placeholder_text="ID do usuário")
        self.user_id_entry.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Botões
        self.create_button = ctk.CTkButton(self, text="Criar", command=self.create_user)
        self.create_button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

        self.list_button = ctk.CTkButton(self, text="Listar todos", command=self.list_all_criteria)
        self.list_button.grid(row=5, column=1, padx=20, pady=10, sticky="ew")

        self.get_by_id_button = ctk.CTkButton(self, text="Buscar por ID", command=self.list_criteria_by_id)
        self.get_by_id_button.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

        self.get_by_user_id_button = ctk.CTkButton(self, text="Buscar por ID do usuário", command=self.list_criteria_by_user_id)
        self.get_by_user_id_button.grid(row=6, column=1, padx=20, pady=10, sticky="ew")

        self.update_button = ctk.CTkButton(self, text="Atualizar", command=self.update_criteria)
        self.update_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

        self.delete_button = ctk.CTkButton(self, text="Deletar", command=self.delete_criteria, fg_color="red", hover_color="#cc0a0a")
        self.delete_button.grid(row=7, column=1, padx=20, pady=10, sticky="ew")

        # Saída
        self.output_box = ctk.CTkTextbox(self, height=220)
        self.output_box.grid(row=8, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    def write_output(self, text: str):
        self.output_box.delete("1.0", "end")
        self.output_box.insert("end", text)

    def create_user(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get().strip()
        user_id = self.user_id_entry.get().strip()

        if not name or not description or not user_id:
            messagebox.showerror("Erro", "Preencha nome, descrição e ID do usuário.")
            return

        db = SessionLocal()
        try:
            criteria = self.criteria_service.create_criteria(db, name, description, int(user_id))
            self.write_output(f"Critério criado com sucesso:\nID: {criteria.id}\nNome: {criteria.name}\nDescrição: {criteria.description}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()

    def list_all_criteria(self):
        db = SessionLocal()
        try:
            criteria_list = self.criteria_service.list_criteria(db)

            if not criteria_list:
                self.write_output("Nenhum critério cadastrado.")
                return

            output = []
            for criteria in criteria_list:
                output.append(f"ID: {criteria.id} | Nome: {criteria.name} | Descrição: {criteria.description} | ID do usuário: {criteria.user_id}")

            self.write_output("\n".join(output))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()

    def list_criteria_by_id(self):
        id = self.id_entry.get().strip()
    
        if not id:
            messagebox.showerror("Erro", "Informe um ID.")
            return

        db = SessionLocal()
        try:
            criteria = self.criteria_service.get_criteria_by_id(db, int(id))

            if not criteria:
                self.write_output("Nenhum critério encontrado para o usuário informado.")
                return

            self.write_output(f"ID: {criteria.id} | Nome: {criteria.name} | Descrição: {criteria.description} | ID do usuário: {criteria.user_id}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()

    def list_criteria_by_user_id(self):
        user_id = self.user_id_entry.get().strip()
    
        if not user_id:
            messagebox.showerror("Erro", "Informe um ID.")
            return

        db = SessionLocal()
        try:
            criteria_list = self.criteria_service.list_criteria_by_user_id(db, int(user_id))

            if not criteria_list:
                self.write_output("Nenhum critério encontrado para o usuário informado.")
                return

            output = []
            for criteria in criteria_list:
                output.append(f"ID: {criteria.id} | Nome: {criteria.name} | Descrição: {criteria.description} | ID do usuário: {criteria.user_id}")

            self.write_output("\n".join(output))
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()

    def update_criteria(self):
        criteria_id = self.id_entry.get().strip()
        new_name = self.name_entry.get().strip()
        new_description = self.description_entry.get().strip()


        if not criteria_id:
            messagebox.showerror("Erro", "Informe o ID para atualizar.")
            return

        db = SessionLocal()
        try:
            criteria = self.criteria_service.update_criteria(
                db,
                int(criteria_id),
                new_name=new_name if new_name else None,
                new_description=new_description if new_description else None
            )

            if criteria is None:
                self.write_output("Critério não encontrado.")
                return

            self.write_output(f"Critério atualizado:\nID: {criteria.id}\nNome: {criteria.name}\nDescrição: {criteria.description}")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()

    def delete_criteria(self):
        criteria_id = self.id_entry.get().strip()

        if not criteria_id:
            messagebox.showerror("Erro", "Informe o ID para deletar.")
            return

        db = SessionLocal()
        try:
            deleted = self.criteria_service.delete_criteria(db, int(criteria_id))

            if not deleted:
                self.write_output("Critério não encontrado.")
                return

            self.write_output("Critério deletado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
        finally:
            db.close()