import sys
from PySide6.QtWidgets import QApplication
from ui.app import App
from constants import ESTILO_GLOBAL


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Você injetaria sua string de ESTILO_GLOBAL aqui
    app.setStyleSheet(ESTILO_GLOBAL)
    
    janela = App()
    janela.show()
    sys.exit(app.exec())