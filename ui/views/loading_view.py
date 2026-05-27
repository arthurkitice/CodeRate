import customtkinter as ctk

class LoadingView(ctk.CTkFrame):
    def __init__(self, parent, total_files: int):
        super().__init__(parent) # Uma cor de fundo levemente transparente seria ideal
        self.total_files = total_files
        self.build_ui()

    def build_ui(self):
        # Um card centralizado para abrigar o conteúdo
        self.card = ctk.CTkFrame(self, width=400, height=200, corner_radius=15)
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        self.title_label = ctk.CTkLabel(self.card, text="Processando Avaliação", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(30, 10))

        self.progress_bar = ctk.CTkProgressBar(self.card, width=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0) # Começa zerada

        # Esse é o texto que vai tranquilizar o usuário
        self.status_label = ctk.CTkLabel(self.card, text="Iniciando...", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=(5, 20))

    def update_progress(self, current: int, filename: str):
        """Método chamado pela Thread da IA para atualizar a UI"""
        # Calcula a porcentagem (0.0 a 1.0)
        progress = current / self.total_files
        self.progress_bar.set(progress)
        
        # Atualiza o texto dinâmico
        self.status_label.configure(text=f"Avaliando: {filename} ({current}/{self.total_files})")

    def finish(self, success_message="Avaliação concluída!"):
        self.progress_bar.set(1)
        self.status_label.configure(text=success_message)