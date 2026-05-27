import customtkinter as ctk
from ui.views.dashboard_form_view import DashboardFormView
from ui.widgets import CustomButton, ResultButton, ScoreButton
from functools import partial

class ResultsView(DashboardFormView):
    def __init__(self, parent, evaluation_id, on_back):
        self.evaluation_id = evaluation_id
        self.on_back = on_back
        self.empty = False

        # Substituição definitiva dos dados fictícios pela busca real no banco
        from services.submission_service import SubmissionService
        self.submission_service = SubmissionService()
        
        # Recupera as submissões reais associadas à avaliação
        db_submissions = self.submission_service.list_submissions_by_evaluation(self.evaluation_id)
        
        # Converte os DTOs em dicionários usando o model_dump do Pydantic v2 para manter compatibilidade com sua view
        self.submissions = [sub.model_dump() for sub in db_submissions]
        
        super().__init__(parent)
        self.pack(padx=50, pady=50)

    def build_ui(self):
        # Configuração da Grid Principal da View (2 Colunas principais)
        self.grid_columnconfigure(0, weight=5, uniform="split") # Lado Esquerdo (Mestre)
        self.grid_columnconfigure(1, weight=4, uniform="split") # Lado Direito (Detalhes)
        self.grid_rowconfigure(2, weight=1)

        # Títulos da View
        self.add_title(self)
        self.add_heading(self, f"Resultados da Avaliação #{self.evaluation_id}")

        # --- PAINEL ESQUERDO: LISTA MESTRE ---
        self.master_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.master_frame.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=10)
        self.master_frame.grid_columnconfigure(0, weight=1)
        self.master_frame.grid_rowconfigure(1, weight=1)

        # Cabeçalhos da tabela interna
        self.headers_frame = ctk.CTkFrame(self.master_frame, fg_color="transparent", height=30)
        self.headers_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 5))
        self.headers_frame.grid_columnconfigure(0, weight=1) # Arquivos
        self.headers_frame.grid_columnconfigure(1, weight=0) # Notas
        
        lbl_arquivos = ctk.CTkLabel(self.headers_frame, text="Arquivos", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_arquivos.grid(row=0, column=0, sticky="w", padx=5)

        # 3. A SOLUÇÃO: O Label Notas recebe o width=120 (mesmo tamanho do ScoreButton), anchor="w" (para o texto ficar na esquerda) e padx=5
        lbl_notas = ctk.CTkLabel(self.headers_frame, text="Notas", font=ctk.CTkFont(size=20, weight="bold"), width=120, anchor="w")
        lbl_notas.grid(row=0, column=1, sticky="w", padx=5)

        self.scrollable_list = ctk.CTkScrollableFrame(self.master_frame, fg_color="transparent")
        self.scrollable_list.grid(row=1, column=0, sticky="nsew")
        
        # 2. Copiamos a exata mesma geometria do cabeçalho para dentro do scroll
        self.scrollable_list.grid_columnconfigure(0, weight=1)
        self.scrollable_list.grid_columnconfigure(1, weight=0)

        # 3. Colocamos as suas colunas de arquivos e notas DENTRO do scroll
        self.file_frame = ctk.CTkFrame(self.scrollable_list, fg_color="transparent")
        self.file_frame.grid(row=0, column=0, sticky="nsew", pady=5, padx=5)
        self.file_frame.grid_columnconfigure(0, weight=1)

        self.score_frame = ctk.CTkFrame(self.scrollable_list, fg_color="transparent")
        self.score_frame.grid(row=0, column=1, sticky="nsew", pady=5, padx=5)
        
        # ------------------------------------------------

        self.row_frames = {} 
        self.build_submissions_list()

        # --- PAINEL DIREITO: DETALHES ---
        self.detail_frame = ctk.CTkFrame(self)
        self.detail_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 20), pady=10)
        self.detail_frame.grid_columnconfigure(0, weight=1)
        self.detail_frame.grid_rowconfigure(1, weight=1)

        # Título dinâmico do painel de detalhes
        self.detail_title = ctk.CTkLabel(self.detail_frame, text="Justificativa", font=ctk.CTkFont(size=20, weight="bold"))
        self.detail_title.grid(row=0, column=0, sticky="w")

        # Caixa de texto para exibir o feedback ou similaridades (Inicia desativada)
        self.detail_text = ctk.CTkTextbox(self.detail_frame, font=ctk.CTkFont(size=14), border_width=1)
        self.detail_text.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.empty_frame = ctk.CTkFrame(self.detail_frame, fg_color="#212435")
        self.empty_frame.grid_columnconfigure(0, weight=1)
        self.empty_frame.grid_columnconfigure(99, weight=1)
        self.empty_frame.grid_rowconfigure(0, weight=1)
        self.empty_frame.grid_rowconfigure(99, weight=1)
        text = "Selecione o ícone de visualização (👁️)\nou de alerta (!) em um arquivo\npara exibir os detalhes aqui."
        self.empty_label = ctk.CTkLabel(self.empty_frame, text=text, font=ctk.CTkFont(size=16), text_color="grey")
        self.empty_label.grid(row=1, column=1, sticky="nsew")

        # Estado Inicial Vazio (Empty State)
        self.show_empty_state()

        # --- BOTÃO VOLTAR ---
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 20))
        
        self.back_button = CustomButton(self.bottom_frame, text="Voltar", command=self.on_back)
        self.back_button.pack(side="left", padx=20)

    def build_submissions_list(self):
        """Preenche a lista rolável com as submissões e seus botões"""
        for widget in self.file_frame.winfo_children():
            widget.destroy()
        for widget in self.score_frame.winfo_children():
            widget.destroy()

        for i, sub in enumerate(self.submissions):
            # ALTERAÇÃO: parent mudou de self.file_frame para self (para acessar as funções da view)
            # E adicionado submission=sub
            lbl_name = ResultButton(self, frame=self.file_frame, text=sub["file_name"], submission=sub, font=ctk.CTkFont(size=14))
            lbl_name.grid(row=i, column=0, sticky="we", padx=0, pady=(0, 10))

            # ALTERAÇÃO: adicionado submission=sub
            lbl_score = ScoreButton(self, self.score_frame, text=f"{sub['score']:.1f}", submission=sub)
            lbl_score.grid(row=i, column=0, sticky="we", padx=0, pady=(0, 10))

    def highlight_active_row(self, sub_id):
        """Aplica um destaque visual na linha selecionada e remove das outras"""
        for current_id, frame in self.row_frames.items():
            if current_id == sub_id:
                frame.configure(border_width=2, border_color=["#3a7ebf", "#1f538d"]) # Destaque ativo
            else:
                frame.configure(border_width=0)

    def show_empty_state(self):
        """Limpa o painel direito e coloca a mensagem instrucional padrão"""
        self.detail_title.configure(text="Justificativa")
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", "end")
        # self.detail_text.insert("50.0", "Selecione o ícone de visualização (👁️) ou de alerta (!) em um arquivo para exibir os detalhes aqui.")
        self.toggle_empty_frame()
        self.detail_text.configure(state="disabled")

    def toggle_empty_frame(self):
        if self.empty:
            self.empty_frame.grid_forget()
        else:
            self.empty_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.empty = not self.empty
        
    def display_feedback(self, submission):
        """Exibe o feedback da IA no painel lateral"""
        if self.empty:
            self.toggle_empty_frame()

        self.highlight_active_row(submission["id"])
        self.detail_title.configure(text=f"Justificativa: {submission['file_name']}")
        
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", "end")
        self.detail_text.insert("1.0", submission["feedback"])
        self.detail_text.configure(state="disabled")

    def display_similarity(self, submission):
        """Exibe o relatório de plágio/similaridade no painel lateral"""
        if self.empty:
            self.toggle_empty_frame()

        self.highlight_active_row(submission["id"])
        self.detail_title.configure(text=f"Similaridades: {submission['file_name']}")
        
        self.detail_text.configure(state="normal")
        self.detail_text.delete("1.0", "end")
        self.detail_text.insert("1.0", f"ALERTA DE ALTA TAXA DE SEMELHANÇA:\n\n{submission['similarity']}\n\nO sistema identificou uma correspondência estrutural atípica entre os arquivos acima. Cabe ao docente analisar se ocorreu plágio ou colaboração indevida.")
        self.detail_text.configure(state="disabled")

    def prompt_edit_score(self, submission):
        """Abre uma caixa de diálogo local para alterar a nota manualmente"""
        dialog = ctk.CTkInputDialog(
            text=f"Altere a nota de {submission['file_name']}:", 
            title="Editar Nota"
        )
        # O tkraise garante que o input apareça na frente do modal central
        dialog.tkraise()
        
        input_value = dialog.get_input()
        
        if input_value is not None:
            try:
                new_score = float(input_value)
                if 0.0 <= new_score <= 10.0:
                    # Atualiza o dado local na lista
                    submission["score"] = new_score
                    # Reconstrói a lista visual com o valor novo
                    self.build_submissions_list()
                    # Mantém o destaque na linha que acabou de ser editada
                    self.highlight_active_row(submission["id"])
                else:
                    print("A nota deve ser entre 0 e 10.")
            except ValueError:
                print("Insira um número decimal válido.")

    def display_code(self, submission):
        """Abre o código fonte da submissão na tela."""
        from ui.views.file_view import FileView # Importe no topo do arquivo se preferir
        
        if hasattr(self, "file_view") and self.file_view is not None:
            self.file_view.destroy()

        self.file_view = FileView(self, submission)
        self.file_view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.file_view.tkraise()