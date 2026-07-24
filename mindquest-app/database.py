import psycopg2
from psycopg2.extras import RealDictCursor

# Cole aqui a string ajustada com a sua senha
DATABASE_URL = "postgresql://postgres:ads2025.2p2mq@db.pvmpssupfckfmvvnnoan.supabase.co:5432/postgres?sslmode=require"
def get_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn

def criar_tabelas():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(150) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            perfil VARCHAR(50) NOT NULL,
            instituicao VARCHAR(150),
            matricula VARCHAR(50)
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

criar_tabelas()