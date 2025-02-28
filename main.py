from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

#conexao
conn = psycopg2.connect(
    host="bilheteria.cerczveferzk.us-east-1.rds.amazonaws.com",
    database="bilhetes",
    user="professor",
    password="professor",
    port=5432
)

#framework
app = FastAPI()

#dados
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

class Enderecos(BaseModel):
    cidade: str
    cep: int
    estado: str
    logradouro: str
    numero: int
    pais: str
    complemento: str

class Clientes(BaseModel):
    nome_completo: str
    documento: str
    telefone: int
    email_cliente: str
    usuario_login: str
    id_endereco: int

class Cliente(BaseModel):
    id_cliente: int
    nome_completo: str
    documento: str
    telefone: int
    email_cliente: str
    usuario_login: str
    id_endereco: int

#tabela usuario
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
    

# tabela endereco
@app.post("/endereco/")
def create_endereco(endereco: Endereco):
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO endereco (id_endereco, cidade, cep, estado, logradouro, numero, pais, complemento)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """,
            (endereco.id, endereco.cidade, endereco.cep, endereco.estado, endereco.logradouro, endereco.numero, endereco.pais, endereco.complemento)
        )
        conn.commit()
        cur.close()
        return {"message": "Endereço inserido com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao inserir endereço: {str(e)}")

@app.get("/endereco/")
def read_endereco():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM endereco")
        enderecos = cur.fetchall()
        cur.close()
        return [{"id": endereco[0], "cidade": endereco[1], "cep": endereco[2], "estado": endereco[3], "logradouro": endereco[4],
                 "numero": endereco[5], "pais": endereco[6], "complemento": endereco[7]} for endereco in enderecos]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/enderecos/{id}")
def update_enderecos(id: int, enderecos: Enderecos):
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE endereco
            SET cidade = %s,
                cep = %s,
                estado = %s,
                logradouro = %s,
                numero = %s,
                pais = %s,
                complemento = %s
            WHERE Id_endereco = %s;
            """,
            (enderecos.cidade, enderecos.cep, enderecos.estado, enderecos.logradouro, enderecos.numero, enderecos.pais, enderecos.complemento, id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")
        
        conn.commit()
        cur.close()
        return {"message": "Endereço atualizado com sucesso."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar endereço: {str(e)}")

@app.delete("/endereco/{id}")
def delete_endereco(id: str):
    try:
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM endereco
            WHERE Id_endereco = %s;
            """,
            (id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Endereço não encontrado")
        
        conn.commit()
        cur.close()
        return {"message": "Excluido."}

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar endereço: {str(e)}")


#tabela cliente
@app.post("/cliente/")
def criar_cliente(cliente: Cliente):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO cliente (id_cliente, nome_completo, documento, telefone, email_cliente, usuario_login, Id_endereco) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (cliente.id_cliente, cliente.nome_completo, cliente.documento, cliente.telefone, cliente.email_cliente, cliente.usuario_login, cliente.id_endereco))
        conn.commit()
        cur.close()
        return {"message": "cliente inserido com sucesso."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/cliente/")
def listar_clientes():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM cliente")
        clientes = cur.fetchall()
        cur.close()
        return [{"id": cliente[0], "nome": cliente[1], "documento": cliente[2], "telefone": cliente[3], "email": cliente[4], "usuario": cliente[5], "id_endereco": cliente[6] } for cliente in clientes]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/cliente/{id}")
def update_cliente(id: str, cliente: Clientes):
       try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE cliente
            SET nome_completo = %s,
                documento = %s,
                telefone = %s,
                email_cliente = %s,
                usuario_login = %s,
                id_endereco = %s
            WHERE id_cliente = %s;
            """,
            (cliente.nome_completo, cliente.documento, cliente.telefone, cliente.email_cliente, cliente.usuario_login, cliente.id_endereco, id)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Cliente não encontrado")
        
        conn.commit()
        cur.close()
        return {"message": "Cliennte atualizado com sucesso."}

       except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cliente: {str(e)}")

@app.delete("/cliente/{id}")
def delete_cliente(id: str):
    try:
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM cliente
            WHERE id_cliente = %s;
            """,
            (id)
        )        
        conn.commit()
        cur.close()
        return {"message": "Excluido."}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar Cliente: {str(e)}")
    
#por ultimo transacao
class Loca(BaseModel):
    id: int
    nome: str
    quantidade: int
    id_endereco: int

@app.post("/loca/")
def create_loca(loca: Loca):
    try:
        # Inicia uma transação
        cur = conn.cursor()
        
        # Insere um registro na tabela `loca`
        cur.execute(
            """
            INSERT INTO loca (id_local, nome, quantidade, id_endereco)
            VALUES (%s, %s, %s, %s)
            """,
            (loca.id, loca.nome, loca.quantidade, loca.id_endereco)
        )
        
        # Confirma a transação
        conn.commit()
        
        # Fecha o cursor
        cur.close()
        
        return {"message": "Registro inserido com sucesso na tabela 'loca'."}

    except Exception as e:
        # Reverte a transação em caso de erro
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao inserir registro na tabela 'loca': {str(e)}")

@app.get("/loca/")
def listar_local():
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM loca")
        locals = cur.fetchall()
        cur.close()
        return [{"id": loca[0], "nome": loca[1], "quantidade": loca[2], "id_endereco": loca[3]} for loca in locals]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))