from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
)
import re #importa modulo de expressões regulares, para validar cpf e email
from crud import listar_donos, adicionar_dono, atualizar_dono, deletar_dono_com_validacao

def validar_cpf(cpf: str) -> bool:
    return bool(re.fullmatch(r'\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2}', cpf))

def validar_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

class TelaDonos(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestão de Tutores")
        self.id_dono_selecionado = None
        self.initUI()
        self.atualizar_tabela()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QGridLayout()

        #adicona os campos, nome, cpf, telefone, email
        form_layout.addWidget(QLabel("Nome:"), 0, 0)
        self.nome_input = QLineEdit()
        form_layout.addWidget(self.nome_input, 0, 1)

        form_layout.addWidget(QLabel("CPF:"), 1, 0)
        self.cpf_input = QLineEdit()
        form_layout.addWidget(self.cpf_input, 1, 1)

        form_layout.addWidget(QLabel("Telefone:"), 2, 0)
        self.telefone_input = QLineEdit()
        form_layout.addWidget(self.telefone_input, 2, 1)

        form_layout.addWidget(QLabel("Email:"), 3, 0)
        self.email_input = QLineEdit()
        form_layout.addWidget(self.email_input, 3, 1)

        #botões de adicionar, atualizar e excluir
        btn_layout = QHBoxLayout()
        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_adicionar.clicked.connect(self.adicionar)
        btn_layout.addWidget(self.btn_adicionar)

        self.btn_atualizar = QPushButton("Atualizar")
        self.btn_atualizar.clicked.connect(self.atualizar)
        btn_layout.addWidget(self.btn_atualizar)

        self.btn_excluir = QPushButton("Excluir")
        self.btn_excluir.clicked.connect(self.excluir)
        btn_layout.addWidget(self.btn_excluir)

        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)

        #cria a tabela com 5 colunas e define os títulos
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(5)
        self.tabela.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Telefone", "Email"])
        self.tabela.cellClicked.connect(self.carregar_dono)
        layout.addWidget(self.tabela)

        self.setLayout(layout)

    #limpa os campos de entrada e reseta o id_dono_selecionado
    def limpar_campos(self):
        self.nome_input.clear()
        self.cpf_input.clear()
        self.telefone_input.clear()
        self.email_input.clear()
        self.id_dono_selecionado = None

    def adicionar(self):
        nome = self.nome_input.text().strip()
        cpf = self.cpf_input.text().strip()
        telefone = self.telefone_input.text().strip()
        email = self.email_input.text().strip()

        if not nome or not cpf or not telefone or not email:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        if not validar_cpf(cpf):
            QMessageBox.warning(self, "Erro", "CPF inválido.")
            return

        if not validar_email(email):
            QMessageBox.warning(self, "Erro", "Email inválido.")
            return

        try:
            adicionar_dono(nome, cpf, telefone, email)
            QMessageBox.information(self, "Sucesso", "Tutor adicionado com sucesso.")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao adicionar tutor: {e}")

    #preenche os campos de entrada com os dados da linha selecionada da tabela e guarda o ID para uso em atualização ou exclusão
    def carregar_dono(self, row, _):
        self.id_dono_selecionado = int(self.tabela.item(row, 0).text())
        self.nome_input.setText(self.tabela.item(row, 1).text())
        self.cpf_input.setText(self.tabela.item(row, 2).text())
        self.telefone_input.setText(self.tabela.item(row, 3).text())
        self.email_input.setText(self.tabela.item(row, 4).text())

    def atualizar(self):
        if self.id_dono_selecionado is None:
            QMessageBox.warning(self, "Erro", "Selecione um tutor para atualizar.")
            return

        nome = self.nome_input.text().strip()
        cpf = self.cpf_input.text().strip()
        telefone = self.telefone_input.text().strip()
        email = self.email_input.text().strip()

        if not nome or not cpf or not telefone or not email:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos.")
            return

        if not validar_cpf(cpf):
            QMessageBox.warning(self, "Erro", "CPF inválido.")
            return

        if not validar_email(email):
            QMessageBox.warning(self, "Erro", "Email inválido.")
            return

        try:
            atualizar_dono(self.id_dono_selecionado, nome, cpf, telefone, email)
            QMessageBox.information(self, "Sucesso", "Tutor atualizado com sucesso.")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao atualizar tutor: {e}")

    def excluir(self):
        if self.id_dono_selecionado is None:
            QMessageBox.warning(self, "Erro", "Selecione um tutor para excluir.")
            return
        try:
            deletar_dono_com_validacao(self.id_dono_selecionado)
            QMessageBox.information(self, "Sucesso", "Tutor excluído com sucesso.")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Não foi possível excluir: {e}")

    def atualizar_tabela(self):
        self.tabela.setRowCount(0) #zera a tabela
        donos = listar_donos()  #chama listar donos para obter os tutores
        #preenche a tabela com os dados retornados
        for dono in donos:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            for col, val in enumerate(dono):
                self.tabela.setItem(row, col, QTableWidgetItem(str(val)))