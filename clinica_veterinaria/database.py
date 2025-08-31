import sqlite3

def get_connection():
    conn = sqlite3.connect("clinica.db")
    return conn

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS donos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especie TEXT NOT NULL,
            raca TEXT NOT NULL,
            idade TEXT NOT NULL,
            vacinado TEXT NOT NULL,
            foto TEXT,
            dono_id INTEGER NOT NULL,
            deletado INTEGER DEFAULT 0,
            FOREIGN KEY (dono_id) REFERENCES donos (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            descricao TEXT,
            diagnostico TEXT,
            confirmado INTEGER DEFAULT 0,
            FOREIGN KEY (pet_id) REFERENCES pets (id)
        )
    ''')
    
    #verifica se a tabela atendimentos tem a coluna confirmado e se não tiver, adiciona a coluna com valor padrão = 0 (campo adicionado posteiormente)
    cursor.execute("PRAGMA table_info(atendimentos)")
    colunas = [info[1] for info in cursor.fetchall()]
    if "confirmado" not in colunas:
        cursor.execute("ALTER TABLE atendimentos ADD COLUMN confirmado INTEGER DEFAULT 0")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabelas()