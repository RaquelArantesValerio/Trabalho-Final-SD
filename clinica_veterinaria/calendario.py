from PyQt6.QtWidgets import QWidget, QCalendarWidget, QVBoxLayout, QLabel, QListWidget
from crud import listar_atendimentos_por_data

class TelaCalendario(QWidget):
    #inicializa o objeto e chama o construtor da classe pai (QWidget)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calendário de Atendimentos")
        self.setGeometry(200, 200, 400, 400)
        self.initUI() #chama o método para montar os componentes visuais da interface

    def initUI(self):
        layout = QVBoxLayout() #cria um layout vertical onde os componentes serão empilhados
        self.calendar = QCalendarWidget() #cria o componente de calendário (permite o usuário selecionar uma data)
        #conecta o evento "data selecionada" do calendário ao método data_selecionada
        self.calendar.selectionChanged.connect(self.data_selecionada)
        layout.addWidget(self.calendar) #adiciona o calendário ao layout da tela

        self.lista_atendimentos = QListWidget() #cria uma lista que vai mostrar os atendimentos do dia
        #adiciona o rótulo e a lista de atendimentos ao layout
        layout.addWidget(QLabel("Atendimentos do dia:"))
        layout.addWidget(self.lista_atendimentos)

        self.setLayout(layout) #aplica o layout à janela da TelaCalendario
        self.data_selecionada() #chama imediatamente o método para carregar os atendimentos da data atual (ou padrão), logo ao abrir a tela

    def data_selecionada(self):
        #pega a data selecionada no calendário e a formata no padrão
        data = self.calendar.selectedDate().toString("yyyy-MM-dd")
        self.lista_atendimentos.clear()
        #consulta o banco de dados para buscar os atendimentos registrados para a data selecionada
        atendimentos = listar_atendimentos_por_data(data)
        if atendimentos:
            for a in atendimentos:
                texto = f"{a[2]} - Pet: {a[5]} - Descrição: {a[3]} | Diagnóstico: {a[4]}"
                self.lista_atendimentos.addItem(texto)
        else:
            self.lista_atendimentos.addItem(f"Nenhum atendimento encontrado para {data}")