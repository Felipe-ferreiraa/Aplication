import psycopg2

# Configurações de conexão
rds_host = 'bilheteria.cerczveferzk.us-east-1.rds.amazonaws.com'
rds_database = 'bilhetes'
rds_user = 'professor'
rds_password = 'professor'
rds_port = 5432  # Porta padrão do PostgreSQL

try:
    # conexao
    conn = psycopg2.connect(
        host=rds_host,
        database=rds_database,
        user=rds_user,
        password=rds_password,
        port=rds_port
    )
    print("Conexão bem-sucedida ao RDS PostgreSQL")
    
    # Criar um cursor
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM usuario;")
    
    #RESULTADOSS
    rows = cur.fetchall()
    
    # lista
    for row in rows:
        print(row)
    
    # fecha conexao
    cur.close()
    conn.close()

except Exception as e:
    print(f"Erro ao conectar ou consultar o banco de dados: {e}")
