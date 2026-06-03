import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from .views.dashboard_view import DashboardView
from .views.evaluation_view import EvaluationView

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeRate")
        self.resize(1100, 700)
        
        # ID para aplicarmos o degradê/estilo de fundo no QSS global
        self.setObjectName("janela_principal")

        # O QStackedWidget substitui o seu "self.container"
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Dicionário para armazenar em cache as telas estáticas
        self.views_cache = {}

        # Inicia a aplicação na rota padrão
        self.show_dashboard()

    def show_dashboard(self):
        """
        Telas como o Dashboard são ESTÁTICAS. 
        Não precisamos recriá-las toda vez que voltamos a elas.
        """
        if "dashboard" not in self.views_cache:
            # Assumindo que o seu DashboardView novo aceita essas injeções de dependência
            view = DashboardView()
            
            # Conectando os eventos simulando o seu comportamento original
            # No Qt puro, usaríamos Signals, mas injetar métodos (callables) também funciona perfeitamente
            view.on_criteria_create = self.show_new_criteria
            view.on_criteria_edit = self.show_edit_criteria
            view.on_start_evaluation = self.show_start_evaluation
            
            self.stacked_widget.addWidget(view)
            self.views_cache["dashboard"] = view

        # Apenas muda a "carta" no topo do baralho
        self.stacked_widget.setCurrentWidget(self.views_cache["dashboard"])

    def show_start_evaluation(self, criteria_id):
        """
        Telas como Evaluation são DINÂMICAS. 
        Dependem de um 'criteria_id' específico para buscar no banco.
        """
        # 1. Limpeza de Memória: Removemos a avaliação antiga caso o usuário
        # tenha aberto uma, voltado pro dashboard, e agora clicou em outra.
        if "evaluation" in self.views_cache:
            old_view = self.views_cache.pop("evaluation")
            self.stacked_widget.removeWidget(old_view)
            old_view.deleteLater() # Destrói a tela velha do processador/RAM

        # 2. Instanciamos a nova tela com os dados frescos
        view = EvaluationView(
            criteria_id=criteria_id,
            on_back=self.show_dashboard,
            on_start=self.show_results
        )

        # 3. Adicionamos ao baralho e mostramos
        self.stacked_widget.addWidget(view)
        self.views_cache["evaluation"] = view
        self.stacked_widget.setCurrentWidget(view)

    # --- Placeholders para as outras telas do seu roteador ---
    
    def show_new_criteria(self):
        print("Navegando para: New Criteria")

    def show_edit_criteria(self, criteria_id, all_criteria=False):
        print(f"Navegando para: Edit Criteria (ID: {criteria_id})")

    def show_results(self, eval_id):
        print(f"Navegando para: Results (Avaliação ID: {eval_id})")

