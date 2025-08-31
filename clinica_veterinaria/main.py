import sys
from PyQt6.QtWidgets import QApplication
from login import TelaLogin
from tela_principal import TelaPrincipal

def main():
    app = QApplication(sys.argv)

    login = TelaLogin()
    if login.exec():
        janela_principal = TelaPrincipal(login.perfil)
        janela_principal.show()
        app.exec()
    else:
        sys.exit()

if __name__ == "__main__":
    main()