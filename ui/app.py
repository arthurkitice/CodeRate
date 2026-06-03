import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from .views.dashboard_view import DashboardView
from .views.evaluation_view import EvaluationView
from .views.file_view import FileView # Importe a tela de arquivos
from .views.loading_view import LoadingView
from .views.results_view import ResultsView

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeRate")
        self.resize(1100, 700)
        self.setObjectName("janela_principal")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.views_cache = {}

        self.show_dashboard()

    def show_dashboard(self):
        if "dashboard" not in self.views_cache:
            view = DashboardView()
            view.on_criteria_create = self.show_new_criteria
            view.on_criteria_edit = self.show_edit_criteria
            view.on_start_evaluation = self.show_start_evaluation
            
            self.stacked_widget.addWidget(view)
            self.views_cache["dashboard"] = view

        self.stacked_widget.setCurrentWidget(self.views_cache["dashboard"])

    def show_start_evaluation(self, criteria_id):
        if "evaluation" in self.views_cache:
            old_view = self.views_cache.pop("evaluation")
            self.stacked_widget.removeWidget(old_view)
            old_view.deleteLater() 

        view = EvaluationView(
            criteria_id=criteria_id,
            on_back=self.show_dashboard,
            
            # Rota para INICIAR uma NOVA avaliação (vai pro Loading)
            on_start_processing=self.show_loading_view, 
            
            # Rota para VER uma avaliação ANTIGA do histórico (pula direto pros Resultados)
            on_view_results=lambda eval_id: self.show_results(eval_id, criteria_id), 
            
            # Rota para VER um arquivo de código
            on_view_file=lambda submission: self.show_file_view(submission, criteria_id)
        )

        self.stacked_widget.addWidget(view)
        self.views_cache["evaluation"] = view
        self.stacked_widget.setCurrentWidget(view)

    # --- A Nova Rota de Arquivos ---
    def show_file_view(self, submission, criteria_id):
        if "file_view" in self.views_cache:
            old_view = self.views_cache.pop("file_view")
            self.stacked_widget.removeWidget(old_view)
            old_view.deleteLater()

        view = FileView(
            submission=submission,
            # AQUI ESTÁ A CORREÇÃO: 
            # Em vez de chamar show_start_evaluation e recriar tudo, 
            # chamamos a nova rota de retorno.
            on_back=self.return_to_evaluation 
        )

        self.stacked_widget.addWidget(view)
        self.views_cache["file_view"] = view
        self.stacked_widget.setCurrentWidget(view)

    def show_loading_view(self, criteria_id, avaliacao_nome, files):
        if "loading" in self.views_cache:
            old_view = self.views_cache.pop("loading")
            self.stacked_widget.removeWidget(old_view)
            old_view.deleteLater()

        view = LoadingView(
            criteria_id=criteria_id,
            avaliacao_nome=avaliacao_nome,
            files=files,
            
            # Se a IA terminar com sucesso, avança para os Resultados repassando o criteria_id
            on_finished=lambda eval_id: self.show_results(eval_id, criteria_id), 
            
            # Se der erro, volta para a tela anterior
            on_error=self.handle_evaluation_error 
        )

        self.stacked_widget.addWidget(view)
        self.views_cache["loading"] = view
        self.stacked_widget.setCurrentWidget(view)

    def show_results(self, eval_id, criteria_id):
        if "results" in self.views_cache:
            old_view = self.views_cache.pop("results")
            self.stacked_widget.removeWidget(old_view)
            old_view.deleteLater()

        view = ResultsView(
            evaluation_id=eval_id,
            
            # Repassando o criteria_id para o botão Voltar conseguir reconstruir a tela anterior
            on_back=lambda: self.show_start_evaluation(criteria_id),
            
            # Repassando o criteria_id para a visualização de código saber para onde voltar
            on_view_file=lambda submission: self.show_file_view(submission, criteria_id)
        )

        self.stacked_widget.addWidget(view)
        self.views_cache["results"] = view
        self.stacked_widget.setCurrentWidget(view)

    def handle_evaluation_error(self, error_msg, criteria_id):
        QMessageBox.critical(self, "Erro na Avaliação", error_msg)
        self.show_start_evaluation(criteria_id)

    def return_to_evaluation(self):
        """
        Apenas tira a FileView da frente e devolve o foco para a 
        EvaluationView que já estava preenchida na memória.
        """
        # 1. Limpa a tela de leitura de código pesada da RAM
        if "file_view" in self.views_cache:
            old_view = self.views_cache.pop("file_view")
            self.stacked_widget.removeWidget(old_view)
            old_view.deleteLater()
            
        # 2. Puxa a tela de avaliação intacta (com textos e arquivos) de volta pro topo
        if "evaluation" in self.views_cache:
            self.stacked_widget.setCurrentWidget(self.views_cache["evaluation"])

    # --- Placeholders ---
    def show_new_criteria(self):
        print("Navegando para: New Criteria")

    def show_edit_criteria(self, criteria_id, all_criteria=False):
        print(f"Navegando para: Edit Criteria (ID: {criteria_id})")
