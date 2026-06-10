from ui.views.new_criteria_view import NewCriteriaView

class EditCriteriaView(NewCriteriaView):
    def __init__(self, criteria_id, on_criteria_updated, on_back, parent=None):
        # Passamos a função 'on_criteria_updated' para assumir o lugar do 'on_criteria_created' na classe Pai
        super().__init__(
            on_criteria_created=on_criteria_updated, 
            on_back=on_back, 
            criteria_id=criteria_id, 
            parent=parent
        )
        self.load_data()

    def get_subtitle(self):
        return "Editar Critério"
    
    def get_button_text(self):
        return "Atualizar Critério"

    def load_data(self):
        criteria = self.criteria_service.get_criteria_by_id(self.criteria_id)
        if criteria:
            # Em vez de self.name_entry.insert(0, ...), reescrevemos o texto direto
            self.name_entry.setText(criteria.name)
            self.description_entry.setPlainText(criteria.description)

    def save_criteria(self):
        name = self.name_entry.text().strip()
        description = self.description_entry.toPlainText().strip()

        if not name or not description:
            self.show_error("Erro: Preencha nome e descrição.")
            return

        criteria = self.criteria_service.update_criteria(self.criteria_id, name, description)
        if criteria:
            # Executa a função injetada pelo roteador para voltar de tela
            self.on_criteria_created() 
        else:
            self.show_error("Erro: Não foi possível atualizar o critério.")