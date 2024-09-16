from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

conn = psycopg2.connect(
    host="bilheteria.cerczveferzk.us-east-1.rds.amazonaws.com",
    database="bilhetes",
    user="professor",
    password="professor",
    port=5432
)

app = FastAPI()

class Usuario(BaseModel):
    login: str
    senha: int
    tipo: str

class Endereco(BaseModel):
    id: int
    cidade: str
    cep: int
    estado: str
    logradouro: str
    numero: int
    pais: str
    complemento: str

class Cliente(BaseModel):
    id_cliente: int
    nome_completo: str
    documento: str
    telefone: int
    email_cliente: str
    usuario_login: str
    id_endereco: int

@app.post("/usuario/")
def create_usuario(usuario: Usuario):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO usuario (login, senha, tipo) VALUES (%s, %i, %s)", (usuario.login, usuario.senha, usuario.tipo))
        user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/usuario/")
def read_usuario():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario")
        users = cur.fetchall()
        cur.close()
        return [{"login": user[0], "senha": user[1], "tipo": user[2]} for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/usuario/{user_id}")
def update_usuario(user_id: str, usuario: Usuario):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE usuario SET senha = %s, tipo = %s WHERE login = %s", (usuario.senha, usuario.tipo, user_id))
        conn.commit()
        cur.close()
        return {"login": user_id, "senha": usuario.senha, "tipo": usuario.tipo}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/usuario/{user_id}")
def delete_usuario(user_id: str):
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM usuario WHERE login = %s", (user_id,))
        conn.commit()
        cur.close()
        return {"message": "Usuario deletado com sucesso"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

