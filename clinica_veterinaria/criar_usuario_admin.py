import sqlite3
import bcrypt

def get_connection():
    return sqlite3.connect("clinica.db")

def criar_usuario_admin():
    conn = get_connection()
    cursor = conn.cursor()

    username = "admin"
    senha = "admin123"  
   
    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, senha, perfil) VALUES (?, ?, ?)",
            (username, senha_hash, "Administrador")
        )
        conn.commit()
        print("Usuário admin criado com sucesso!")
    except sqlite3.IntegrityError:
        print("Usuário admin já existe no banco.")
    finally:
        conn.close()

if __name__ == "__main__":
    criar_usuario_admin()