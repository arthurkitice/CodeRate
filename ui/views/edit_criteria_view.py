from tkinter import messagebox
from database import get_db
from ui.views.new_criteria_view import NewCriteriaView

class EditCriteriaView(NewCriteriaView):
    def __init__(self, parent, on_criteria_updated, on_back, user_id, criteria_id):
        self.on_criteria_updated = on_criteria_updated
        super().__init__(parent, on_criteria_updated, on_back, user_id, criteria_id)
        self.load_data()

    def get_subtitle(self):
        return "Editar Critério"
    
    def get_button_text(self):
        return "Atualizar Critério"

    def load_data(self):
        try:
            with get_db() as db:
                criteria = self.criteria_service.get_criteria_by_id(db, self.criteria_id)
                if criteria:
                    self.name_entry.insert(0, criteria.name)
                    self.description_entry.insert("0.0", criteria.description)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar critério: {str(e)}")

    def save_criteria(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get("0.0", "end").strip()

        if not name or not description:
            messagebox.showerror("Erro", "Preencha nome e descrição.")
            return

        try:
            with get_db() as db:
                criteria = self.criteria_service.update_criteria(db, self.criteria_id, name, description)
                if criteria:
                    self.on_criteria_updated()
                else:
                    messagebox.showerror("Erro", "Não foi possível atualizar o critério.")
        except Exception as e:
            messagebox.showerror("Erro", str(e))