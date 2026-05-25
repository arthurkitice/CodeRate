from database import get_db
from ui.views.new_criteria_view import NewCriteriaView


class EditCriteriaView(NewCriteriaView):
    def __init__(self, parent, on_criteria_updated, on_back, criteria_id):
        self.on_criteria_updated = on_criteria_updated
        super().__init__(parent, on_criteria_updated, on_back, criteria_id)
        self.load_data()

    def get_subtitle(self):
        return "Editar Critério"
    
    def get_button_text(self):
        return "Atualizar Critério"

    def load_data(self):
        criteria = self.criteria_service.get_criteria_by_id(self.criteria_id)
        if criteria:
            self.name_entry.insert(0, criteria.name)
            self.description_entry.insert("0.0", criteria.description)


    def save_criteria(self):
        name = self.name_entry.get().strip()
        description = self.description_entry.get("0.0", "end").strip()

        if not name or not description:
            self.show_error("Erro: Preencha nome e descrição.")
            return

        criteria = self.criteria_service.update_criteria(self.criteria_id, name, description)
        if criteria:
            self.on_criteria_updated()
        else:
            self.show_error("Erro: Não foi possível atualizar o critério.")