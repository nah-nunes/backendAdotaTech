import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List

# Importa as funções de database.py
from database import init_db, get_db

# Inicializa o banco de dados e cria as tabelas ao iniciar a aplicação
init_db()

app = FastAPI(
    title="AdotaTech API (com SQL Puro)",
    description="Esta é uma versão da API que usa SQL puro para manipulação de dados."
)

# --- Modelos de Dados (Pydantic) ---

class AnimalBase(BaseModel):
    nome: str
    raca: str
    idade: int
    sexo: str
    tags: str
    descricao: str
    foto_url: str

class AnimalCreate(AnimalBase):
    pass

class Animal(AnimalBase):
    id: int

# --- Endpoints da API ---

@app.post("/animais/", response_model=Animal, status_code=status.HTTP_201_CREATED)
def create_animal(animal: AnimalCreate, conn: sqlite3.Connection = Depends(get_db)):
    """
    Cria um novo animal no banco de dados usando INSERT.
    """
    cursor = conn.cursor()


    sql = """
    INSERT INTO animais (nome, raca, idade, sexo, tags, descricao, foto_url)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    try:
        cursor.execute(sql, (
            animal.nome, animal.raca, animal.idade, animal.sexo,
            animal.tags, animal.descricao, animal.foto_url
        ))
        conn.commit()

        # Pega o ID do animal recém-criado
        new_id = cursor.lastrowid
        return Animal(id=new_id, **animal.dict())

    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro no banco de dados: {e}")

@app.get("/animais/", response_model=List[Animal])
def read_animals(conn: sqlite3.Connection = Depends(get_db)):
    """
    Lista todos os animais do banco de dados usando SELECT.
    """
    cursor = conn.cursor()


    sql = "SELECT * FROM animais"

    cursor.execute(sql)
    rows = cursor.fetchall() 


    return [Animal(**dict(row)) for row in rows]

@app.get("/animais/{animal_id}", response_model=Animal)
def read_animal(animal_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """
    Busca um animal específico pelo ID usando SELECT ... WHERE.
    """
    cursor = conn.cursor()

 
    sql = "SELECT * FROM animais WHERE id = ?"

    cursor.execute(sql, (animal_id,))
    row = cursor.fetchone() 

    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal não encontrado")

    return Animal(**dict(row))

# --- endpoint de Eventos ---

class Evento(BaseModel):
    id: int
    titulo: str
    local: str

@app.get("/eventos/", response_model=List[Evento])
def read_eventos(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    sql = "SELECT id, titulo, local FROM eventos"
    cursor.execute(sql)
    rows = cursor.fetchall()
    return [Evento(**dict(row)) for row in rows]