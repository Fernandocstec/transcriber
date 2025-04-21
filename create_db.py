import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import urllib.parse

from app.core.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

# Carrega variáveis de ambiente
load_dotenv()

def create_database():
    """
    Cria o banco de dados se não existir.
    """
    try:
        # Codifica a senha para URL
        encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
        
        # Conecta ao banco de dados postgres para criar o novo banco
        engine = create_engine(f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/postgres")
        
        # Verifica se o banco já existe
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}'"))
            if not result.scalar():
                conn.execute(text("COMMIT"))
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print(f"Banco de dados '{DB_NAME}' criado com sucesso!")
            else:
                print(f"Banco de dados '{DB_NAME}' já existe!")
    except Exception as e:
        print(f"Erro ao conectar ao PostgreSQL: {str(e)}")
        print("\nPor favor, verifique:")
        print("1. Se o PostgreSQL está instalado")
        print("2. Se a senha do usuário está correta")
        print("3. Se o serviço do PostgreSQL está rodando")
        print("\nVocê pode redefinir a senha do PostgreSQL usando o comando:")
        print(f"ALTER USER {DB_USER} WITH PASSWORD 'nova_senha';")
        raise

def create_tables():
    """
    Cria as tabelas no banco de dados.
    """
    try:
        from app.models.schema import Base
        from app.core.database import engine
        
        # Cria todas as tabelas definidas nos modelos
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        create_database()
        create_tables()
        print("Banco de dados e tabelas criados com sucesso!")
    except Exception as e:
        print(f"Erro ao criar banco de dados ou tabelas: {str(e)}") 