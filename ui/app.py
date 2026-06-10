import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox
from .views import (
    DashboardView, EvaluationView,  FileView, 
    LoadingView, ResultsView, NewCriteriaView, 
    EditCriteriaView, SettingsView, AllCriteriaView
)

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeRate")
        self.resize(1100, 700)
        self.setObjectName("janela_principal")

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.dashboard_view = None
        self.settings_view = None
        self.current_dynamic_view = None
        self.show_dashboard()

    def dynamic_view(func):
        def wrapper(self, *args, **kwargs):
            self.clear_dynamic_view()
            function = func(self, *args, **kwargs)
            self.stacked_widget.addWidget(self.current_dynamic_view)
            self.stacked_widget.setCurrentWidget(self.current_dynamic_view)
            return function
        return wrapper

    def clear_dynamic_view(self):
       if self.current_dynamic_view is not None:
            self.stacked_widget.removeWidget(self.current_dynamic_view)
            self.current_dynamic_view.deleteLater()
            self.current_dynamic_view = None 

    def show_dashboard(self):
        # O Dashboard é a exceção: ele não é limpo, apenas criado uma vez
        if self.dashboard_view is None:
            self.dashboard_view = DashboardView(
                on_start_evaluation = self.show_start_evaluation,
                on_criteria_edit = self.show_edit_criteria,
                on_new_criteria = self.show_new_criteria,
                on_settings=self.show_settings,
                on_all_criteria=self.show_all_criteria_view
            )
            
            self.stacked_widget.addWidget(self.dashboard_view)

        # Se havia uma tela de arquivo ou resultado na frente, nós a destruímos
        self.clear_dynamic_view()
        self.stacked_widget.setCurrentWidget(self.dashboard_view)

    def show_settings(self):
        if self.settings_view is None:
            self.settings_view = SettingsView(
                on_back = self.show_dashboard
            )
            
            self.stacked_widget.addWidget(self.settings_view)
        self.stacked_widget.setCurrentWidget(self.settings_view)

    @dynamic_view
    def show_start_evaluation(self, criteria_id):
        self.current_dynamic_view = EvaluationView(
            criteria_id=criteria_id,
            on_back=self.show_dashboard,
            on_start_processing=self.show_loading_view, 
            on_view_results=lambda eval_id: self.show_results(eval_id, criteria_id), 
            on_view_file=lambda submission: self.show_file_view(submission)
        )

    def show_file_view(self, submission):
        file_view = FileView(
            submission=submission,
            on_back = lambda: self.close_and_return(file_view)
        )

        self.stacked_widget.addWidget(file_view)
        self.stacked_widget.setCurrentWidget(file_view)

    @dynamic_view
    def show_loading_view(self, criteria_id, avaliacao_nome, files):
        self.current_dynamic_view = LoadingView(
            criteria_id=criteria_id,
            avaliacao_nome=avaliacao_nome,
            files=files,
            on_finished=lambda eval_id: self.show_results(eval_id, criteria_id), 
            on_error=self.handle_evaluation_error 
        )

    @dynamic_view
    def show_results(self, eval_id, criteria_id):
        self.current_dynamic_view = ResultsView(
            evaluation_id=eval_id,
            on_back=lambda: self.show_start_evaluation(criteria_id),
            on_view_file=lambda submission: self.show_file_view(submission)
        )

    def handle_evaluation_error(self, error_msg, criteria_id):
        QMessageBox.critical(self, "Erro na Avaliação", error_msg)
        self.show_start_evaluation(criteria_id)

    def show_new_criteria(self):
        new_criteria_view = NewCriteriaView(
            on_criteria_created = lambda: self.update_dashboard_and_return(new_criteria_view),
            on_back = lambda: self.close_and_return(new_criteria_view)
        )

        self.stacked_widget.addWidget(new_criteria_view)
        self.stacked_widget.setCurrentWidget(new_criteria_view)

    def show_edit_criteria(self, criteria_id):
        edit_criteria_view = EditCriteriaView(
            on_criteria_updated = lambda: self.update_dashboard_and_return(edit_criteria_view),
            on_back = lambda: self.close_and_return(edit_criteria_view),
            criteria_id = criteria_id
        )

        self.stacked_widget.addWidget(edit_criteria_view)
        self.stacked_widget.setCurrentWidget(edit_criteria_view)

    @dynamic_view
    def show_all_criteria_view(self):
        self.current_dynamic_view = AllCriteriaView(
            on_criteria_create=self.show_new_criteria,
            on_criteria_edit=self.show_edit_criteria,
            on_back=self.show_dashboard,
            on_criteria_delete=self.dashboard_view.load_criteria,
            on_start_evaluation=self.show_start_evaluation
        )

    def update_dashboard_and_return(self, view):
        self.dashboard_view.load_criteria()
        if self.current_dynamic_view is not None:
            self.current_dynamic_view.build_criteria_buttons()
        self.close_and_return(view)

    def close_and_return(self, view):
        self.stacked_widget.removeWidget(view)
        view.deleteLater()
        self.stacked_widget.setCurrentWidget(self.current_dynamic_view if self.current_dynamic_view is not None else self.dashboard_view)