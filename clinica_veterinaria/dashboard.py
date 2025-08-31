import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard de Análise de Dados")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.combo = QComboBox()
        self.combo.addItems([
            "Pets por Espécie",
            "Pets por Raça",
            "Atendimentos por Mês",
            "Pets por Tutor",
            "Pets Vacinados vs Não Vacinados",
            "Atendimentos Concluídos vs Pendentes"
        ])
        self.combo.currentIndexChanged.connect(self.plotar_grafico)
        self.layout.addWidget(self.combo)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
        self.conexao = sqlite3.connect("clinica.db")

        self.plotar_grafico()

    def plotar_grafico(self):
        opcao = self.combo.currentText()
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        cursor = self.conexao.cursor()

        if opcao == "Pets por Espécie":
            cursor.execute("SELECT especie, COUNT(*) FROM pets GROUP BY especie")
            dados = cursor.fetchall()
            categorias = [d[0] for d in dados]
            valores = [d[1] for d in dados]
            ax.bar(categorias, valores)
            ax.set_title("Quantidade de Pets por Espécie")

        elif opcao == "Pets por Raça":
            cursor.execute("SELECT raca, COUNT(*) FROM pets GROUP BY raca ORDER BY COUNT(*) DESC LIMIT 10")
            dados = cursor.fetchall()
            categorias = [d[0] for d in dados]
            valores = [d[1] for d in dados]
            ax.barh(categorias[::-1], valores[::-1])
            ax.set_title("Top 10 Raças de Pets")

        elif opcao == "Atendimentos por Mês":
            cursor.execute("""
                SELECT strftime('%Y-%m', data), COUNT(*) FROM atendimentos
                GROUP BY strftime('%Y-%m', data)
                ORDER BY strftime('%Y-%m', data)
            """)
            dados = cursor.fetchall()
            categorias = [d[0] for d in dados]
            valores = [d[1] for d in dados]
            ax.plot(categorias, valores, marker='o')
            ax.set_title("Atendimentos por Mês")
            ax.tick_params(axis='x', rotation=45)

        elif opcao == "Pets por Tutor":
            cursor.execute("SELECT d.nome, COUNT(*) FROM pets p JOIN donos d ON p.dono_id = d.id GROUP BY d.nome")
            dados = cursor.fetchall()
            categorias = [d[0] for d in dados]
            valores = [d[1] for d in dados]
            ax.bar(categorias, valores)
            ax.set_title("Pets por Tutor")
            ax.tick_params(axis='x', rotation=45)

        elif opcao == "Pets Vacinados vs Não Vacinados":
            cursor.execute("SELECT vacinado, COUNT(*) FROM pets GROUP BY vacinado")
            dados = cursor.fetchall()
            categorias = [d[0] for d in dados]
            valores = [d[1] for d in dados]
            ax.pie(valores, labels=categorias, autopct='%1.1f%%')
            ax.set_title("Pets Vacinados vs Não Vacinados")

        elif opcao == "Atendimentos Concluídos vs Pendentes":
            cursor.execute("SELECT confirmado, COUNT(*) FROM atendimentos GROUP BY confirmado")
            dados = cursor.fetchall()

            if not dados:
                ax.text(0.5, 0.5, "Nenhum dado disponível", ha='center', va='center')
            else:
                categorias = ["Concluídos" if d[0] == 1 else "Pendentes" for d in dados]
                valores = [d[1] for d in dados]
                ax.pie(valores, labels=categorias, autopct='%1.1f%%')
                ax.set_title("Status dos Atendimentos")

        self.canvas.draw()