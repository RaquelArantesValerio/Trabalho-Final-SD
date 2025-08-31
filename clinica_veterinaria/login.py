from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox
import bcrypt #criptografar e verificar senhas com segurança
from crud import buscar_usuario, adicionar_usuario

class TelaLogin(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login - Clínica Veterinária")
        self.perfil = None  #usado para guardar o tipo de usuário após login
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        #campos para nome do usuário e senha, que oculta os caracteres com EchoMode.Password
        layout.addWidget(QLabel("Usuário:"))
        self.usuario_input = QLineEdit()
        layout.addWidget(self.usuario_input)

        layout.addWidget(QLabel("Senha:"))
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.senha_input)

        #botão que tenta autenticar o usuário ao ser clicado
        self.login_btn = QPushButton("Entrar")
        self.login_btn.clicked.connect(self.tentar_login)
        layout.addWidget(self.login_btn)

        #botão que abre a tela de cadastro
        self.btn_cadastrar = QPushButton("Cadastrar Novo Usuário")
        self.btn_cadastrar.clicked.connect(self.abrir_cadastro_usuario)
        layout.addWidget(self.btn_cadastrar)

        self.setLayout(layout)

    #coleta os dados digitados, valida se os campos estão preenchidos
    def tentar_login(self):
        usuario = self.usuario_input.text()
        senha = self.senha_input.text()

        if not usuario or not senha:
            QMessageBox.warning(self, "Erro", "Preencha usuário e senha.")
            return

        row = buscar_usuario(usuario)
        if not row:
            QMessageBox.warning(self, "Erro", "Usuário não encontrado.")
            return
        #extrai a senha criptografada e o perfil do banco
        _, _, senha_armazenada, perfil = row

        #compara a senha digitada com a do banco usando bcrypt
        if bcrypt.checkpw(senha.encode(), senha_armazenada):
            self.perfil = perfil
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Senha incorreta.")

    #cria uma nova instância da janela de cadastro e a abre como modal
    def abrir_cadastro_usuario(self):
        self.cadastro_dialog = TelaCadastroUsuario()
        self.cadastro_dialog.exec()

class TelaCadastroUsuario(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Usuário")
        self.setFixedSize(300, 200)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Usuário:"))
        self.usuario_input = QLineEdit()
        layout.addWidget(self.usuario_input)

        layout.addWidget(QLabel("Senha:"))
        self.senha_input = QLineEdit()
        self.senha_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.senha_input)

        layout.addWidget(QLabel("Perfil:"))
        self.perfil_combo = QComboBox()
        self.perfil_combo.addItems(["Recepcionista", "Veterinario"])
        layout.addWidget(self.perfil_combo)

        self.btn_cadastrar = QPushButton("Cadastrar")
        self.btn_cadastrar.clicked.connect(self.cadastrar_usuario)
        layout.addWidget(self.btn_cadastrar)

        self.setLayout(layout)

    def cadastrar_usuario(self):
        usuario = self.usuario_input.text().strip()
        senha = self.senha_input.text().strip()
        perfil = self.perfil_combo.currentText()

        if not usuario or not senha:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        #criptografa a senha usando bcrypt
        senha_criptografada = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

        try:
            adicionar_usuario(usuario, senha_criptografada, perfil)
            QMessageBox.information(self, "Sucesso", "Usuário cadastrado.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao cadastrar usuário: {e}")