import sqlite3
from database import get_connection

def adicionar_usuario(username, senha_criptografada, perfil):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (username, senha, perfil) VALUES (?, ?, ?)",
                   (username, senha_criptografada, perfil))
    conn.commit()
    conn.close()

def buscar_usuario(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, senha, perfil FROM usuarios WHERE username=?", (username,))
    row = cursor.fetchone()
    conn.close()
    return row

def adicionar_dono(nome, cpf, telefone, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO donos (nome, cpf, telefone, email) VALUES (?, ?, ?, ?)",
                   (nome, cpf, telefone, email))
    conn.commit()
    conn.close()

def listar_donos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, cpf, telefone, email FROM donos")
    rows = cursor.fetchall()
    conn.close()
    return rows

#retorna o número de pets ativos (não deletados) associados a um tutor
def verificar_pets_por_dono(dono_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pets WHERE dono_id=? AND deletado=0", (dono_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

#verifica se o tutor não tem pets ativos — pré-condição para deletá-lo
def pode_deletar_dono(dono_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pets WHERE dono_id=? AND deletado=0", (dono_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0

def deletar_dono(dono_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM donos WHERE id=?", (dono_id,))
    conn.commit()
    conn.close()

#deleta o tutor apenas se não houver pets associados
def deletar_dono_com_validacao(dono_id):
    if pode_deletar_dono(dono_id):
        deletar_dono(dono_id)
        return True
    else:
        return False

def adicionar_pet(nome, especie, raca, idade, vacinado, foto, dono_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO pets (nome, especie, raca, idade, vacinado, foto, dono_id)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (nome, especie, raca, idade, vacinado, foto, dono_id))
    conn.commit()
    conn.close()

def listar_pets():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pets.id, pets.nome, pets.especie, pets.raca, pets.idade, pets.vacinado, pets.foto, pets.dono_id, donos.nome, pets.deletado
        FROM pets
        JOIN donos ON pets.dono_id = donos.id
        WHERE pets.deletado=0
    ''')
    rows = cursor.fetchall()
    conn.close()
    return rows

def atualizar_pet(id_pet, nome, especie, raca, idade, vacinado, foto, dono_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE pets SET nome=?, especie=?, raca=?, idade=?, vacinado=?, foto=?, dono_id=?
        WHERE id=?
    ''', (nome, especie, raca, idade, vacinado, foto, dono_id, id_pet))
    conn.commit()
    conn.close()

def atualizar_dono(dono_id, nome, cpf, telefone, email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE donos SET nome=?, cpf=?, telefone=?, email=? WHERE id=?
    ''', (nome, cpf, telefone, email, dono_id))
    conn.commit()
    conn.close()

#marca o pet como deletado (deletado=1) ao invés de removê-lo fisicamente
def deletar_pet_logico(id_pet):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE pets SET deletado=1 WHERE id=?", (id_pet,))
    conn.commit()
    conn.close()

def adicionar_atendimento(pet_id, data, horario, descricao, diagnostico="", confirmado=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO atendimentos (pet_id, data, horario, descricao, diagnostico, confirmado)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (pet_id, data, horario, descricao, diagnostico, confirmado))
    conn.commit()
    conn.close()

#lista os atendimentos de um pet específico, em ordem reversa (mais recente primeiro)
def listar_atendimentos_por_pet(pet_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM atendimentos
        WHERE pet_id=?
        ORDER BY data DESC, horario DESC
    ''', (pet_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def listar_atendimentos_por_data(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT *
        FROM atendimentos
        WHERE data = ?
        ORDER BY horario ASC
    ''', (data,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
'''
def atualizar_atendimento(id_atendimento, diagnostico, confirmado):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE atendimentos SET diagnostico=?, confirmado=? WHERE id=?", (diagnostico, confirmado, id_atendimento))
    conn.commit()
    conn.close()
'''
def excluir_atendimento(id_atendimento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM atendimentos WHERE id=?", (id_atendimento,))
    conn.commit()
    conn.close()

#atualização flexível: apenas campos não None são atualizados. Usa uma lista dinâmica para montar a query SQL
def atualizar_atendimento(id_atendimento, data=None, horario=None, descricao=None, diagnostico=None, confirmado=None):
    conn = get_connection()
    cursor = conn.cursor()

    campos = []
    valores = []

    if data is not None:
        campos.append("data=?")
        valores.append(data)
    if horario is not None:
        campos.append("horario=?")
        valores.append(horario)
    if descricao is not None:
        campos.append("descricao=?")
        valores.append(descricao)
    if diagnostico is not None:
        campos.append("diagnostico=?")
        valores.append(diagnostico)
    if confirmado is not None:
        campos.append("confirmado=?")
        valores.append(confirmado)

    if campos:
        query = f"UPDATE atendimentos SET {', '.join(campos)} WHERE id=?"
        valores.append(id_atendimento)
        cursor.execute(query, valores)

    conn.commit()
    conn.close()

def editar_data_hora_atendimento(id_atendimento, nova_data, novo_horario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE atendimentos
        SET data = ?, horario = ?
        WHERE id = ?
    ''', (nova_data, novo_horario, id_atendimento))
    conn.commit()
    conn.close()

def excluir_atendimento(id_atendimento):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM atendimentos WHERE id = ?', (id_atendimento,))
    conn.commit()
    conn.close()
