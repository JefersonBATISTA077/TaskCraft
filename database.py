import sqlite3

def conectar():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela no banco de dados
def criar_tabela():

    conn = conectar()
    
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  senha TEXT NOT NULL)''')
    conn.commit()
    conn.close()