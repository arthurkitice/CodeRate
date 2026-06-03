ESTILO_GLOBAL = """
    /* O SEGREDO DO DEGRADÊ: Aplicado apenas à janela principal */
    QWidget#janela_principal {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #3b265d, stop: 1 #1c0f34);
    }

    QWidget {
        color: #ffffff;
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    QLabel#titulo_app {
        font-size: 42px;
        font-weight: bold;
        background: transparent;
    }

    QLabel#subtitulo_app {
        font-size: 20px;
        font-weight: 600;
        background: transparent;
    }

    /* ATIVANDO A MÃOZINHA VIA CSS */
    QPushButton {
        /* R (Red), G (Green), B (Blue), A (Alpha/Transparência) */
        /* Fundo roxo claro com apenas 8% de opacidade */
        background-color: rgba(180, 155, 230, 0.08);
        
        /* Borda fina, mas um pouco mais visível (40% de opacidade) */
        border: 1px solid rgba(180, 155, 230, 0.4);
        border-radius: 8px;
        padding: 10px 24px;
        
        font-size: 13px;
        /* Reduzimos o peso da fonte de 'bold' para '500' para maior elegância */
        font-weight: 500; 
        color: #d1c1eb; /* Texto acompanhando o tom da borda */
        qproperty-cursor: 13;
    }
    
    QPushButton:hover {
        /* No hover, o fundo e a borda "acendem" */
        background-color: rgba(180, 155, 230, 0.15);
        border: 1px solid rgba(180, 155, 230, 0.8);
        color: #ffffff; /* O texto brilha em branco puro */
    }

    QPushButton:pressed {
        /* Feedback tátil rápido ao clicar */
        background-color: rgba(180, 155, 230, 0.25);
        border: 1px solid rgba(180, 155, 230, 1.0);
    }

    QScrollArea#scroll_area, QWidget#container_cards {
        border: none;
        background-color: transparent;
    }
    
    /* CARDS */
   QFrame#criterion_card {
        /* Fundo super sutil (apenas 4% de opacidade para diferenciar do fundo da janela) */
        background-color: rgba(180, 155, 230, 0.04); 
        
        /* Borda levemente visível (20% de opacidade) */
        border: 1px solid rgba(180, 155, 230, 0.2);
        border-radius: 14px;
    }
    
    QFrame#criterion_card:hover {
        /* No hover, acendemos o fundo e destacamos a borda */
        background-color: rgba(180, 155, 230, 0.1); 
        border: 1px solid rgba(180, 155, 230, 0.5);
    }

    QLabel#criterion_name {
        font-size: 16px;
        font-weight: bold;
        color: #e6ddf5; /* Título num tom de roxo/branco mais vibrante */
        background-color: transparent; 
    }

    QLabel#criterion_desc {
        font-size: 13px;
        color: #9e91b5; /* Descrição num tom mais apagado para dar contraste */
        background-color: transparent; 
    }

    QPushButton#btn_icon {
        background-color: transparent;
        border: none;
        font-size: 16px;
        padding: 4px;
    }
    QPushButton#btn_icon:hover {
        background-color: rgba(180, 155, 230, 0.2);
        border-radius: 6px;
    }

    QPushButton#custom_btn {
        font-size: 14px;
        color: #e6ddf5;
    }
    /* ======================================= */
    /* ENTRADAS DE TEXTO (CustomEntry e Label)   */
    /* ======================================= */
    QLineEdit#custom_entry {
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(180, 155, 230, 0.2);
        border-radius: 8px;
        padding: 0px 15px;
        color: #ffffff;
        font-size: 14px;
    }
    
    QLineEdit#custom_entry:focus {
        border: 1px solid rgba(180, 155, 230, 0.8);
        background-color: rgba(180, 155, 230, 0.05);
    }

    QLabel#label_entry_title {
        color: #cfc5dd;
        font-size: 14px;
        font-weight: bold;
    }

    /* ======================================= */
    /* BOTÃO DE ALERTA DE SIMILARIDADE         */
    /* ======================================= */
    QPushButton#btn_alert {
        background-color: #a30000;
        border: none;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        font-size: 14px;
    }
    QPushButton#btn_alert:hover {
        background-color: #ff3333;
    }

    /* ======================================= */
    /* RESULT CARD E SCORE CARD                */
    /* ======================================= */
    QFrame#result_card, QFrame#score_card {
        background-color: rgba(180, 155, 230, 0.04);
        border: 1px solid rgba(180, 155, 230, 0.2);
        border-radius: 10px;
    }
    
    QFrame#result_card:hover {
        background-color: rgba(180, 155, 230, 0.1);
        border: 1px solid rgba(180, 155, 230, 0.5);
    }

    QLabel#result_text, QLabel#score_text {
        font-size: 14px;
        font-weight: bold;
        color: #e6ddf5;
        background-color: transparent;
    }
    QScrollArea#scroll_area {
        border: none;
        background-color: transparent;
    }
    
    /* Isso garante que a "tela" de fundo dentro do scroll não fique branca */
    QWidget#fundo_transparente {
        background-color: transparent;
    }
    
    /* Como os botões antigos não são cards escuros, vamos dar uma cor 
       de fundo para os itens da lista para eles não sumirem no fundo roxo */
    QWidget#fundo_transparente QWidget {
        background-color: transparent;
    }
    QPlainTextEdit#code_viewer {
        /* Um fundo um pouco mais escuro para contrastar com o degradê da janela */
        background-color: rgba(0, 0, 0, 0.25);
        border: 1px solid rgba(180, 155, 230, 0.15);
        border-radius: 10px;
        padding: 15px;
        
        /* Cor da fonte do código */
        color: #e2e8f0; 
        
        /* O tamanho e a família (Consolas) já foram definidos no Python 
           usando QFont para garantir o espaçamento correto das letras, 
           mas definimos a altura da linha aqui se necessário */
    }

    /* Opcional: Se for usar a tela como Overlay flutuante */
    QWidget#file_view_overlay {
        background-color: rgba(15, 7, 30, 0.95); /* Roxo super escuro e translúcido */
    }
    /* ======================================= */
    /* TELA DE CARREGAMENTO (LoadingView)      */
    /* ======================================= */

    QLabel#loading_title {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
    }

    QLabel#loading_status {
        font-size: 14px;
        color: #9e91b5;
    }

    /* A Borda da Barra de Progresso */
    QProgressBar#loading_progress {
        background-color: rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(180, 155, 230, 0.1);
        border-radius: 6px;
        min-height: 12px;
        max-height: 12px;
    }

    /* O Preenchimento (A parte que anda) */
    QProgressBar#loading_progress::chunk {
        background-color: #6366f1; /* Um roxo vibrante ou azul */
        border-radius: 5px;
    }
    QLabel#tabela_header {
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
    }

    /* O Painel de "Estado Vazio" */
    QFrame#empty_state_frame {
        background-color: rgba(180, 155, 230, 0.03);
        border: 2px dashed rgba(180, 155, 230, 0.2);
        border-radius: 15px;
    }

    QLabel#empty_state_text {
        color: #7a6e96;
        font-size: 15px;
        line-height: 1.5;
    }

    /* A Caixa de Texto do Feedback */
    QPlainTextEdit#detail_textbox {
        background-color: rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(180, 155, 230, 0.15);
        border-radius: 10px;
        padding: 15px;
        color: #e2e8f0;
        font-size: 14px;
        line-height: 1.4;
    }
"""