from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QFrame, QScrollArea, QPushButton, QStackedWidget
)
from PySide6.QtCore import Qt, QSize
from ui.widgets import CustomButton
from PySide6.QtGui import QIcon

class AllCriteriaView(QWidget):
    def __init__(self, on_criteria_create, on_criteria_edit, on_back, on_criteria_delete, on_start_evaluation, parent=None):
        super().__init__(parent)
        self.on_criteria_create = on_criteria_create
        self.on_criteria_edit = on_criteria_edit
        self.on_back = on_back
        self.on_criteria_delete = on_criteria_delete
        self.on_start_evaluation = on_start_evaluation
        self.selected_criteria_id = None

        from services import CriteriaService
        self.criteria_service = CriteriaService()

        self.build_ui()

    # ------------------------------------------------------------------
    # Helpers internos
    # ------------------------------------------------------------------
    def _list_all_criteria(self):
        criteria = self.criteria_service.list_criteria()
        return list(reversed(criteria))

    def _clear_info_panel(self):
        self.info_stack.setCurrentIndex(0)
        self.selected_criteria_id = None
        self.btn_avaliar.setVisible(False)

    # ------------------------------------------------------------------
    # Ações dos botões da lista
    # ------------------------------------------------------------------
    def edit_criteria(self, criteria_id):
        self.on_criteria_edit(criteria_id=criteria_id)

    def delete_criteria(self, criteria_id):
        self.criteria_service.delete_criteria(criteria_id)
        self.build_criteria_buttons()
        self.on_criteria_delete()
        self._clear_info_panel()

    def _start_evaluation(self):
        if self.selected_criteria_id is not None:
            self.on_start_evaluation(self.selected_criteria_id)

    # ------------------------------------------------------------------
    # Monta / reconstrói a lista de critérios
    # ------------------------------------------------------------------
    def build_criteria_buttons(self):
        # Limpa o conteúdo anterior dentro do container
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        criteria_list = self._list_all_criteria()

        for criterion in criteria_list:
            row_widget = QWidget()
            row_widget.setObjectName("fundo_transparente")
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(6)

            # Botão principal com o nome do critério
            btn_name = QPushButton(criterion.name)
            btn_name.setObjectName("custom_btn")
            btn_name.setCursor(Qt.PointingHandCursor)
            btn_name.clicked.connect(
                lambda checked=False, c=criterion: self.build_criteria_info(c)
            )

            # Botão editar
            btn_edit = QPushButton("")
            btn_edit.setObjectName("btn_icon")
            btn_edit.setIcon(QIcon("ui/icons/edit_icon.png"))
            btn_edit.setIconSize(QSize(30, 30))
            btn_edit.setFixedSize(32, 32)
            btn_edit.setCursor(Qt.PointingHandCursor)
            btn_edit.setToolTip("Editar")
            btn_edit.clicked.connect(
                lambda checked=False, c_id=criterion.id: self.edit_criteria(c_id)
            )

            # Botão remover
            btn_remove = QPushButton("")
            btn_remove.setObjectName("btn_icon")
            btn_remove.setIcon(QIcon("ui/icons/trash_icon.png"))
            btn_remove.setIconSize(QSize(30, 30))
            btn_remove.setFixedSize(32, 32)
            btn_remove.setCursor(Qt.PointingHandCursor)
            btn_remove.setToolTip("Remover")
            btn_remove.clicked.connect(
                lambda checked=False, c_id=criterion.id: self.delete_criteria(c_id)
            )

            row_layout.addWidget(btn_name, stretch=1)
            row_layout.addWidget(btn_edit)
            row_layout.addWidget(btn_remove)

            self.list_layout.addWidget(row_widget)

        # Empurra tudo para cima quando a lista for curta
        self.list_layout.addStretch()

    # ------------------------------------------------------------------
    # Exibe detalhes do critério selecionado no painel direito
    # ------------------------------------------------------------------
    def build_criteria_info(self, criteria):
        self.selected_criteria_id = criteria.id
        self.btn_avaliar.setVisible(True)
        # Limpa o painel direito
        while self.info_layout.count():
            item = self.info_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        # Label "Nome:"
        lbl_nome_header = QLabel("Nome:")
        lbl_nome_header.setObjectName("loading_status")   # tom acinzentado

        lbl_nome = QLabel(criteria.name)
        lbl_nome.setObjectName("result_text")
        lbl_nome.setWordWrap(True)

        # Label "Descrição:"
        lbl_desc_header = QLabel("Descrição:")
        lbl_desc_header.setObjectName("loading_status")
        lbl_desc_header.setContentsMargins(0, 24, 0, 0)

        lbl_desc = QLabel(criteria.description)
        lbl_desc.setObjectName("result_text")
        lbl_desc.setWordWrap(True)

        self.info_layout.addWidget(lbl_nome_header)
        self.info_layout.addWidget(lbl_nome)
        self.info_layout.addWidget(lbl_desc_header)
        self.info_layout.addWidget(lbl_desc)
        self.info_layout.addStretch()

        self.info_stack.setCurrentWidget(self.content_frame)

    # ------------------------------------------------------------------
    # Monta a UI principal
    # ------------------------------------------------------------------
    def build_ui(self):
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(50, 50, 50, 50)
        root_layout.setSpacing(30)

        lbl_titulo = QLabel("CodeRate")
        lbl_titulo.setObjectName("titulo_app")
        root_layout.addWidget(lbl_titulo)

        lbl_heading = QLabel("Todos os critérios de avaliação")
        lbl_heading.setObjectName("subtitulo_app")
        root_layout.addWidget(lbl_heading)

        # --- Área de conteúdo ---
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Painel esquerdo
        scroll_area = QScrollArea()
        scroll_area.setObjectName("scroll_area")
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        list_container = QWidget()
        list_container.setObjectName("fundo_transparente")
        self.list_layout = QVBoxLayout(list_container)
        self.list_layout.setContentsMargins(0, 0, 8, 0)
        self.list_layout.setSpacing(8)

        scroll_area.setWidget(list_container)
        content_layout.addWidget(scroll_area, stretch=1)

        # Painel direito
        self.info_stack = QStackedWidget()

        empty_frame = QFrame()
        empty_frame.setObjectName("empty_state_frame")
        empty_layout = QVBoxLayout(empty_frame)
        lbl_empty = QLabel("Selecione um critério\npara visualizar\nseu conteúdo")
        lbl_empty.setObjectName("empty_state_text")
        lbl_empty.setAlignment(Qt.AlignCenter)
        empty_layout.addWidget(lbl_empty)
        empty_layout.setAlignment(lbl_empty, Qt.AlignCenter)

        self.content_frame = QFrame()
        self.content_frame.setObjectName("criteria_detail_card")
        self.info_layout = QVBoxLayout(self.content_frame)
        self.info_layout.setContentsMargins(20, 20, 20, 20)
        self.info_layout.setSpacing(4)

        self.info_stack.addWidget(empty_frame)
        self.info_stack.addWidget(self.content_frame)

        content_layout.addWidget(self.info_stack, stretch=1)

        # Adiciona o content_layout ao root
        root_layout.addLayout(content_layout, stretch=1)

        # Botão voltar no rodapé
        footer_layout = QHBoxLayout()

        btn_voltar = CustomButton("Voltar", command=self.on_back)
        footer_layout.addWidget(btn_voltar)
        footer_layout.addStretch()

        self.btn_avaliar = CustomButton("Iniciar Avaliação", command=self._start_evaluation)
        self.btn_avaliar.setVisible(False)
        footer_layout.addWidget(self.btn_avaliar)

        root_layout.addLayout(footer_layout)

        self.build_criteria_buttons()
        self._clear_info_panel()