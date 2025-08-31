class Usuario:
    def __init__(self, id, username, senha, perfil):
        self.id = id
        self.username = username
        self.senha = senha
        self.perfil = perfil

class Dono:
    def __init__(self, id, nome, cpf, telefone, email):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.email = email

class Pet:
    def __init__(self, id, nome, especie, raca, idade, vacinado, foto, dono_id, deletado=0):
        self.id = id
        self.nome = nome
        self.especie = especie
        self.raca = raca
        self.idade = idade
        self.vacinado = vacinado
        self.foto = foto
        self.dono_id = dono_id
        self.deletado = deletado

class Atendimento:
    def __init__(self, id, pet_id, data, horario, descricao, diagnostico):
        self.id = id
        self.pet_id = pet_id
        self.data = data
        self.horario = horario
        self.descricao = descricao
        self.diagnostico = diagnostico