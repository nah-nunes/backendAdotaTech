import sqlite3
import os

# Define o nome do arquivo do banco de dados
DB_FILE = "adotatech.db"

def init_db():
    """
    Cria as tabelas do banco de dados se elas não existirem.
    Esta função é o equivalente manual do 'Base.metadata.create_all()'.
    """
  
    if os.path.exists(DB_FILE):
        print("Banco de dados existente encontrado. Não será recriado.")
        return

    print("Criando novo banco de dados com tabelas...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # --- Criando tabela de animais ---
    cursor.execute("""
    CREATE TABLE animais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        raca TEXT NOT NULL,
        idade INTEGER NOT NULL,
        sexo TEXT,
        tags TEXT,
        descricao TEXT,
        foto_url TEXT
    );
    """)

    # Criando tabela de eventos ---
    cursor.execute("""
    CREATE TABLE eventos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descricao TEXT,
        data TEXT,
        horario TEXT,
        local TEXT,
        tipo TEXT,
        imagem_url TEXT
    );
    """)

    conn.commit()
    conn.close()
    print("Banco de dados e tabelas criados com sucesso.")

def get_db():
    """
    Dependência do FastAPI para obter uma conexão com o banco de dados.
    """
    conn = sqlite3.connect(DB_FILE)
    
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()