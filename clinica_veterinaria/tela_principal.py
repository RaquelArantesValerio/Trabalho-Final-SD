from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QStackedWidget
from atendimentos import TelaAtendimentos
from dashboard import Dashboard
from calendario import TelaCalendario
from tela_donos import TelaDonos
from tela_pets import TelaPets

class TelaPrincipal(QMainWindow):
    def __init__(self, perfil):
        super().__init__()
        self.setWindowTitle(f"Sistema - {perfil}")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout_principal = QHBoxLayout(self.central_widget)
        self.menu_lateral = QVBoxLayout()
        layout_principal.addLayout(self.menu_lateral)

        self.stack = QStackedWidget()
        layout_principal.addWidget(self.stack)

        #botões de menu lateral
        self.botao_donos = QPushButton("Tutor")
        self.botao_pets = QPushButton("Pets")
        self.botao_calendario = QPushButton("Calendário")
        self.botao_sair = QPushButton("Sair")

        self.menu_lateral.addWidget(self.botao_donos)
        self.menu_lateral.addWidget(self.botao_pets)

        if perfil in ["Recepcionista", "Administrador", "Veterinario"]:
            self.botao_atendimentos = QPushButton("Atendimentos")
            self.menu_lateral.addWidget(self.botao_atendimentos)

        if perfil == "Administrador":
            self.botao_dashboard = QPushButton("Dashboard")
            self.menu_lateral.addWidget(self.botao_dashboard)

        self.menu_lateral.addWidget(self.botao_calendario)
        self.menu_lateral.addStretch()
        self.menu_lateral.addWidget(self.botao_sair)

        #telas
        self.tela_donos = TelaDonos()
        self.tela_pets = TelaPets()
        self.tela_calendario = TelaCalendario()

        self.stack.addWidget(self.tela_donos)
        self.stack.addWidget(self.tela_pets)
        self.stack.addWidget(self.tela_calendario)

        if perfil in ["Recepcionista", "Administrador", "Veterinario"]:
            self.tela_atendimentos = TelaAtendimentos(perfil)
            self.stack.addWidget(self.tela_atendimentos)

        if perfil == "Administrador":
            self.tela_dashboard = Dashboard()
            self.stack.addWidget(self.tela_dashboard)

        #conexões
        self.botao_donos.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_donos))
        self.botao_pets.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_pets))
        self.botao_calendario.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_calendario))

        if perfil in ["Recepcionista", "Administrador", "Veterinario"]:
            def abrir_atendimentos():
                self.tela_atendimentos.atualizar_pets()
                self.stack.setCurrentWidget(self.tela_atendimentos)

            self.botao_atendimentos.clicked.connect(abrir_atendimentos)

        if perfil == "Administrador":
            self.botao_dashboard.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela_dashboard))

        self.botao_sair.clicked.connect(self.fechar_sistema)

    def fechar_sistema(self):
        self.close()