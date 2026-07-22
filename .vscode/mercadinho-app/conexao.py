import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class Conexao:
    @staticmethod
    def obter_conexao():
        try:
            conexao = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            return conexao
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None