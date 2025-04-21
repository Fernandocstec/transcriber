import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do banco de dados
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Zx12cv34@infinito")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "transcriber_db")

# Codifica a senha para URL
encoded_password = quote_plus(DB_PASSWORD)

# URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    # Tenta conectar ao banco de dados
    engine = create_engine(DATABASE_URL)
    
    # Testa a conexão
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {str(e)}")
    raise

# Configuração da sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator:
    """
    Fornece uma sessão do banco de dados.
    
    Yields:
        Session: Sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 