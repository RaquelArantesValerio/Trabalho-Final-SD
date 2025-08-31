import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog, QGroupBox, QFormLayout
)
from crud import listar_pets, adicionar_pet, atualizar_pet, deletar_pet_logico, listar_donos
from api_integration import buscar_racas_cachorro, buscar_racas_gato
from PyQt6.QtGui import QPixmap

class TelaPets(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestão de Pets")
        self.id_pet_selecionado = None
        self.initUI()
        self.atualizar_tabela()

    def initUI(self):
        layout = QVBoxLayout()
        form_layout = QGridLayout()

        #inputs do formulário nome, espécie, raça, idade, vacinado, tutor e foto
        form_layout.addWidget(QLabel("Nome:"), 0, 0)
        self.nome_input = QLineEdit()
        form_layout.addWidget(self.nome_input, 0, 1)

        form_layout.addWidget(QLabel("Espécie:"), 1, 0)
        self.especie_combo = QComboBox()
        self.especie_combo.addItems(["Cachorro", "Gato"])
        self.especie_combo.currentTextChanged.connect(self.carregar_racas)
        form_layout.addWidget(self.especie_combo, 1, 1)

        form_layout.addWidget(QLabel("Raça:"), 2, 0)
        self.raca_combo = QComboBox()
        form_layout.addWidget(self.raca_combo, 2, 1)

        form_layout.addWidget(QLabel("Idade:"), 3, 0)
        self.idade_input = QLineEdit()
        form_layout.addWidget(self.idade_input, 3, 1)

        form_layout.addWidget(QLabel("Vacinado:"), 4, 0)
        self.vacinado_combo = QComboBox()
        self.vacinado_combo.addItems(["Sim", "Não"])
        form_layout.addWidget(self.vacinado_combo, 4, 1)

        form_layout.addWidget(QLabel("Tutor:"), 5, 0)
        self.dono_combo = QComboBox()
        form_layout.addWidget(self.dono_combo, 5, 1)

        form_layout.addWidget(QLabel("Foto:"), 6, 0)
        self.foto_label = QLabel("Nenhuma imagem selecionada")
        form_layout.addWidget(self.foto_label, 6, 1)
        self.btn_selecionar_foto = QPushButton("Selecionar Foto")
        self.btn_selecionar_foto.clicked.connect(self.selecionar_foto)
        form_layout.addWidget(self.btn_selecionar_foto, 6, 2)

        #botões de adicionar, atuualizar e excluir
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

        #tabela para listar os pets
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(7)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "Nome", "Espécie", "Raça", "Idade", "Vacinado", "Tutor"
        ])
        self.tabela.cellClicked.connect(self.carregar_pet)
        layout.addWidget(self.tabela)

        #mostra imagem e informações resumidas do pet e tutor selecionado
        self.visualizacao_group = QGroupBox("Visualização do Pet")
        self.visual_layout = QFormLayout()

        self.imagem_pet_label = QLabel()
        self.imagem_pet_label.setFixedSize(100, 100)

        self.nome_pet_label = QLabel("-")
        self.tutor_pet_label = QLabel("-")

        self.visual_layout.addRow("Imagem:", self.imagem_pet_label)
        self.visual_layout.addRow("Nome do Pet:", self.nome_pet_label)
        self.visual_layout.addRow("Tutor:", self.tutor_pet_label)

        self.visualizacao_group.setLayout(self.visual_layout)
        layout.addWidget(self.visualizacao_group)

        self.setLayout(layout)
        self.carregar_donos()
        self.carregar_racas(self.especie_combo.currentText())

    #preenche o combo com os nomes dos tutores do banco de dados
    def carregar_donos(self):
        self.dono_combo.clear()
        donos = listar_donos()
        for dono in donos:
            self.dono_combo.addItem(f"{dono[1]} (CPF: {dono[2]})", dono[0])

    #atualiza as raças dependendo da esspécie selecionada
    def carregar_racas(self, especie):
        self.raca_combo.clear()
        racas = buscar_racas_cachorro() if especie == "Cachorro" else buscar_racas_gato()
        self.raca_combo.addItems(racas)

    #abre seletor de arquivo, mostra imagem e atualiza rótulos de nome/tutor no grupo de visualização
    def selecionar_foto(self):
        caminho, _ = QFileDialog.getOpenFileName(self, "Selecione a foto do pet", "", "Imagens (*.png *.jpg *.jpeg)")
        if caminho:
            self.caminho_foto = caminho
            nome_arquivo = os.path.basename(caminho)
            self.foto_label.setText(nome_arquivo)
            pixmap = QPixmap(caminho).scaled(100, 100)
            self.imagem_pet_label.setPixmap(pixmap)
            self.nome_pet_label.setText(self.nome_input.text())
            self.tutor_pet_label.setText(self.dono_combo.currentText())

    #funções de crud até def excluir()
    def limpar_campos(self):
        self.nome_input.clear()
        self.idade_input.clear()
        self.vacinado_combo.setCurrentIndex(0)
        self.dono_combo.setCurrentIndex(0)
        self.carregar_racas(self.especie_combo.currentText())
        self.foto_label.setText("Nenhuma imagem selecionada")
        self.caminho_foto = None
        self.id_pet_selecionado = None
        self.imagem_pet_label.clear()
        self.nome_pet_label.setText("-")
        self.tutor_pet_label.setText("-")

    def adicionar(self):
        nome = self.nome_input.text().strip()
        especie = self.especie_combo.currentText()
        raca = self.raca_combo.currentText()
        idade = self.idade_input.text().strip()
        vacinado = self.vacinado_combo.currentText()
        dono_id = self.dono_combo.currentData()
        foto = getattr(self, "caminho_foto", None)

        if not nome or not raca or not idade or not dono_id:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            adicionar_pet(nome, especie, raca, idade, vacinado, foto, dono_id)
            QMessageBox.information(self, "Sucesso", "Pet adicionado com sucesso.")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao adicionar pet: {e}")

    #quando o usuário clica em uma linha da tabela, preenche os campos com os dados daquele pet
    def carregar_pet(self, row, _):
        self.id_pet_selecionado = int(self.tabela.item(row, 0).text())
        self.nome_input.setText(self.tabela.item(row, 1).text())
        especie = self.tabela.item(row, 2).text()
        self.especie_combo.setCurrentText(especie)
        self.carregar_racas(especie)
        self.raca_combo.setCurrentText(self.tabela.item(row, 3).text())
        self.idade_input.setText(self.tabela.item(row, 4).text())
        self.vacinado_combo.setCurrentText(self.tabela.item(row, 5).text())
        tutor_text = self.tabela.item(row, 6).text()

        donos = listar_donos()
        for i, dono in enumerate(donos):
            if dono[1] in tutor_text:
                self.dono_combo.setCurrentIndex(i)
                break
        '''
        foto = self.tabela.item(row, 7).text()
        if foto and foto != "Sem imagem":
            self.foto_label.setText(foto)
            self.caminho_foto = foto
            if os.path.exists(foto):
                pixmap = QPixmap(foto).scaled(100, 100)
                self.imagem_pet_label.setPixmap(pixmap)
        else:
            self.foto_label.setText("Nenhuma imagem selecionada")
            self.caminho_foto = None
            self.imagem_pet_label.clear()
        '''
        self.nome_pet_label.setText(self.nome_input.text())
        self.tutor_pet_label.setText(self.dono_combo.currentText())

    def atualizar(self):
        if self.id_pet_selecionado is None:
            QMessageBox.warning(self, "Erro", "Selecione um pet para atualizar.")
            return

        nome = self.nome_input.text().strip()
        especie = self.especie_combo.currentText()
        raca = self.raca_combo.currentText()
        idade = self.idade_input.text().strip()
        vacinado = self.vacinado_combo.currentText()
        dono_id = self.dono_combo.currentData()
        foto = getattr(self, "caminho_foto", None)

        if not nome or not raca or not idade or not dono_id:
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios.")
            return

        try:
            atualizar_pet(self.id_pet_selecionado, nome, especie, raca, idade, vacinado, foto, dono_id)
            QMessageBox.information(self, "Sucesso", "Pet atualizado com sucesso.")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao atualizar pet: {e}")

    #exclui logicamente (marca como deletado) o pet selecionado via deletar_pet_logico
    def excluir(self):
        if self.id_pet_selecionado is None:
            QMessageBox.warning(self, "Erro", "Selecione um pet para excluir.")
            return
        try:
            deletar_pet_logico(self.id_pet_selecionado)
            QMessageBox.information(self, "Sucesso", "Pet excluído logicamente com sucesso.")
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Não foi possível excluir o pet: {e}")

    #lê pets do banco e popula a tabela. Ignora pets com deletado = 1
    def atualizar_tabela(self):
        self.tabela.setRowCount(0)
        pets = listar_pets()
        for pet in pets:
            if pet[-2] == 1:  #deletado
                continue
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            for col, val in enumerate(pet[:-2]):  #ignora 'foto' e 'deletado'
                self.tabela.setItem(row, col, QTableWidgetItem(str(val)))

    #sempre que a janela for exibida, recarrega a lista de tutores para garantir que esteja atualizada
    def showEvent(self, event):
        super().showEvent(event)
        self.carregar_donos()