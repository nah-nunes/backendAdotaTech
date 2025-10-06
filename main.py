import sqlite3
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

# Importa as funções do nosso arquivo database.py
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

class EventoBase(BaseModel):
    titulo: str
    descricao: str
    data: str
    horario: str
    local: str
    tipo: str
    imagem_url: str

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    data: Optional[str] = None
    horario: Optional[str] = None
    local: Optional[str] = None
    tipo: Optional[str] = None
    imagem_url: Optional[str] = None

class Evento(EventoBase):
    id: int

# --- Endpoints de Animais ---

@app.post("/animais/", response_model=Animal, status_code=status.HTTP_201_CREATED)
def create_animal(animal: AnimalCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    sql = "INSERT INTO animais (nome, raca, idade, sexo, tags, descricao, foto_url) VALUES (?, ?, ?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql, (animal.nome, animal.raca, animal.idade, animal.sexo, animal.tags, animal.descricao, animal.foto_url))
        conn.commit()
        new_id = cursor.lastrowid
        return Animal(id=new_id, **animal.dict())
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro no banco de dados: {e}")

@app.get("/animais/", response_model=List[Animal])
def read_animals(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM animais")
    rows = cursor.fetchall()
    return [Animal(**dict(row)) for row in rows]

# ... outros endpoints de animais aqui (GET por id, PUT, DELETE)...

# --- Endpoints de Eventos (COMPLETO) ---

@app.post("/eventos/", response_model=Evento, status_code=status.HTTP_201_CREATED)
def create_evento(evento: EventoCreate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    sql = "INSERT INTO eventos (titulo, descricao, data, horario, local, tipo, imagem_url) VALUES (?, ?, ?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql, (evento.titulo, evento.descricao, evento.data, evento.horario, evento.local, evento.tipo, evento.imagem_url))
        conn.commit()
        new_id = cursor.lastrowid
        return Evento(id=new_id, **evento.model_dump())
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Erro no banco de dados: {e}")

@app.get("/eventos/", response_model=List[Evento])
def read_eventos(conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos")
    rows = cursor.fetchall()
    return [Evento(**dict(row)) for row in rows]

@app.get("/eventos/{evento_id}", response_model=Evento)
def read_evento(evento_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM eventos WHERE id = ?", (evento_id,))
    row = cursor.fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    return Evento(**dict(row))

@app.put("/eventos/{evento_id}", response_model=Evento)
def update_evento(evento_id: int, evento: EventoUpdate, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    
  
    fields_to_update = {k: v for k, v in evento.model_dump().items() if v is not None}
    if not fields_to_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nenhum campo para atualizar")
        
    set_clause = ", ".join([f"{key} = ?" for key in fields_to_update.keys()])
    values = list(fields_to_update.values())
    values.append(evento_id)
    
    sql = f"UPDATE eventos SET {set_clause} WHERE id = ?"
    
    cursor.execute(sql, tuple(values))
    conn.commit()
    
    return read_evento(evento_id, conn)

@app.delete("/eventos/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evento(evento_id: int, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM eventos WHERE id = ?", (evento_id,))
    conn.commit()
    return None