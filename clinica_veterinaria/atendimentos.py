from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QDateEdit, QTimeEdit,
    QTextEdit, QPushButton, QListWidget, QMessageBox, QFormLayout, QHBoxLayout
)
from PyQt6.QtCore import QDate, QTime
from crud import (
    listar_pets, adicionar_atendimento, listar_atendimentos_por_pet,
    listar_atendimentos_por_data, atualizar_atendimento, excluir_atendimento
)
import unicodedata  #modulo para remover e manipular acentuação de strings (usado na comparação dos perfis)

#função auxiliar para remoção de acentos 
def remover_acentos(texto):
        return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

class TelaAtendimentos(QWidget):

    def __init__(self, perfil):  #inicializa a tela com o perfil do usuário
        super().__init__()   #chama o constructor da classe pai QWidget
        self.perfil = remover_acentos(perfil.lower())
        #self.perfil = perfil
        self.setWindowTitle("Agendamento e Controle de Atendimentos") #titulo da janela
        #cria e define o layout principal da tela
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = QFormLayout() #cria layout de formulario

        #verifica se usuário tem permissão de agendar/editar/excluir
        if perfil in ["Recepcionista", "Administrador"]:
            #cria dropdown de pets e preenche com os pets cadastrados
            self.combo_pet = QComboBox()
            self.atualizar_pets()
            self.form_layout.addRow(QLabel("Selecionar Pet:"), self.combo_pet)

            #campo de data, com valor padrão para data atual
            self.data = QDateEdit()
            self.data.setDate(QDate.currentDate())
            self.form_layout.addRow(QLabel("Data:"), self.data)

            #campo de hora, com valor padrão para horario atual
            self.hora = QTimeEdit()
            self.hora.setTime(QTime.currentTime())
            self.form_layout.addRow(QLabel("Hora:"), self.hora)

            #botão chamando a função agendar
            self.btn_agendar = QPushButton("Agendar Atendimento")
            self.btn_agendar.clicked.connect(self.agendar)
            self.form_layout.addRow(self.btn_agendar)

            #botão chamando a função editar
            self.btn_editar = QPushButton("Editar Atendimento")
            self.btn_editar.clicked.connect(self.editar_atendimento)
            self.form_layout.addRow(self.btn_editar)

            #botão chamando a função excluir
            self.btn_excluir = QPushButton("Excluir Atendimento")
            self.btn_excluir.clicked.connect(self.excluir_atendimento)
            self.form_layout.addRow(self.btn_excluir)

        #adiciona o formulário ao layout principal
        self.layout.addLayout(self.form_layout)

        #cria e adiciona lista onde os atendimentos agendados são exibidos
        self.lista = QListWidget()
        self.layout.addWidget(QLabel("Histórico de Atendimentos:"))
        self.layout.addWidget(self.lista)

        #verifica se o usuário tem a permissão de colocar descrição do atendimento, etc
        if perfil in ["Veterinario", "Administrador"]:
            #área de texto para descrição feita pelo veterinário
            self.descricao = QTextEdit()
            self.descricao.setPlaceholderText("Descrição do atendimento")
            self.layout.addWidget(QLabel("Descrição:"))
            self.layout.addWidget(self.descricao)

            #área de texto para diagnóstico feito pelo veterinário
            self.diagnostico = QTextEdit()
            self.diagnostico.setPlaceholderText("Digite o diagnóstico aqui")
            self.layout.addWidget(QLabel("Diagnóstico:"))
            self.layout.addWidget(self.diagnostico)

            #botão que chama confirmar_atendimento()
            self.btn_confirmar = QPushButton("Confirmar Atendimento")
            self.btn_confirmar.clicked.connect(self.confirmar_atendimento)
            self.layout.addWidget(self.btn_confirmar)

        self.atendimento_selecionado_id = None #guarda o ID do atendimento clicado na lista

        self.atualizar_lista() #atualiza a lista com atendimentod

        #vincula a seleção de um item da lista a função carregar_atendimento_selecionado()
        self.lista.itemClicked.connect(self.carregar_atendimento_selecionado)

        #atualiza a lista ao trocar pet no combo
        if perfil in ["Recepcionista", "Administrador"]:
            self.combo_pet.currentIndexChanged.connect(self.atualizar_lista)

    #popula o combo_pet com os pets cadastrados, excluindo os marcados como deletados (== 1)
    def atualizar_pets(self):

        #verifica se o atributo combo_pet existe no objeto
        if not hasattr(self, "combo_pet"):
            return
        
        self.combo_pet.clear()
        pets = listar_pets() #busca todos os pets cadastrados no banco de dados
        #itera sobre cada pet e se campo deletado == 1, ignora este pet
        for pet in pets:
            if pet[-2] == 1:
                continue
            #adiciona o pet ao combo com nome, espécie e nome do tutor e associa o id como dado oculto
            self.combo_pet.addItem(f"{pet[1]} ({pet[2]}) - Tutor: {pet[8]}", pet[0])

    def agendar(self):
        #pegar o ID do pet selecionado, a data e a hora escolhidas no formulario
        pet_id = self.combo_pet.currentData()
        data = self.data.date().toString("yyyy-MM-dd")
        hora = self.hora.time().toString("HH:mm")

        #valida se um pet foi selecionado
        if not pet_id:
            QMessageBox.warning(self, "Erro", "Selecione um pet.")
            return

        try:
            adicionar_atendimento(pet_id, data, hora, descricao="", diagnostico="", confirmado=0)
            QMessageBox.information(self, "Sucesso", "Atendimento agendado com sucesso.")
            self.atualizar_lista()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao agendar atendimento: {e}")

    #atualizar os atendimentos com base no pet ou na data atual
    def atualizar_lista(self):
        self.lista.clear()
        #se o perfil for recepcionista, busca os atendimentos do pet selecionado
        if self.perfil == "Recepcionista":
            pet_id = self.combo_pet.currentData()
            if not pet_id:
                return
            atendimentos = listar_atendimentos_por_pet(pet_id)
        #senão busca os atendimentos do dia atual
        else:
            data_hoje = QDate.currentDate().toString("yyyy-MM-dd")
            atendimentos = listar_atendimentos_por_data(data_hoje)

        #itera os atendimentos e formata a string com data, hora, descrição e status
        for a in atendimentos:
            status = "[CONFIRMADO]" if a[6] == 1 else "[PENDENTE]"
            texto = f"{a[2]} {a[3]} - {a[4]} {status}"
            #adiciona à lista e armazena o atendimento completo no item (chave 1000 como "custom data")
            self.lista.addItem(texto)
            self.lista.item(self.lista.count()-1).setData(1000, a)

    def carregar_atendimento_selecionado(self, item):
        #recupera o dado armazenado e salva o ID do atendimento selecionado
        atendimento = item.data(1000)
        self.atendimento_selecionado_id = atendimento[0]
        #se for veterinário/admin, preenche os campos de descrição e diagnóstico
        if self.perfil in ["Veterinario", "Administrador"]:
            self.descricao.setText(atendimento[4] or "")
            self.diagnostico.setText(atendimento[5] or "")
        #se for recepcionista, preenche os campos de data e hora com os valores atuais do atendimento
        if self.perfil == "Recepcionista":
            data = QDate.fromString(atendimento[2], "yyyy-MM-dd")
            hora = QTime.fromString(atendimento[3], "HH:mm")
            self.data.setDate(data)
            self.hora.setTime(hora)

    def confirmar_atendimento(self):
        if self.atendimento_selecionado_id is None:
            QMessageBox.warning(self, "Erro", "Selecione um atendimento para confirmar.")
            return

        #coleta os textos, remove espaços, e exige que ambos estejam preenchidos
        descricao = self.descricao.toPlainText().strip()
        diag = self.diagnostico.toPlainText().strip()

        if not descricao or not diag:
            QMessageBox.warning(self, "Erro", "Preencha a descrição e o diagnóstico.")
            return
        #atualiza o atendimento com diagnóstico, descrição e marca como confirmado
        try:
            atualizar_atendimento(self.atendimento_selecionado_id, descricao=descricao, diagnostico=diag, confirmado=1)
            QMessageBox.information(self, "Sucesso", "Atendimento confirmado com sucesso.")
            self.descricao.clear()
            self.diagnostico.clear()
            self.atendimento_selecionado_id = None
            self.atualizar_lista()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao confirmar atendimento: {e}")

    def editar_atendimento(self):
        if self.atendimento_selecionado_id is None:
            QMessageBox.warning(self, "Erro", "Selecione um atendimento para editar.")
            return

        #pega os novos valores de data e hora
        nova_data = self.data.date().toString("yyyy-MM-dd")
        novo_horario = self.hora.time().toString("HH:mm")
        #tenta atualizar o banco com os novos valores. Limpa ID de atendimento selecionado, etc
        try:
            atualizar_atendimento(self.atendimento_selecionado_id, data=nova_data, horario=novo_horario)
            QMessageBox.information(self, "Sucesso", "Atendimento atualizado com sucesso.")
            self.atendimento_selecionado_id = None
            self.atualizar_lista()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao editar atendimento: {e}")

    def excluir_atendimento(self):
        if self.atendimento_selecionado_id is None:
            QMessageBox.warning(self, "Erro", "Selecione um atendimento para excluir.")
            return

        try:
            excluir_atendimento(self.atendimento_selecionado_id)
            QMessageBox.information(self, "Sucesso", "Atendimento excluído com sucesso.")
            self.atendimento_selecionado_id = None
            self.atualizar_lista()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao excluir atendimento: {e}")