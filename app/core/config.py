import os
from dotenv import load_dotenv
import urllib.parse

# Carrega variáveis de ambiente
load_dotenv()

# Configurações do banco de dados
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "transcriber_db")

# Codifica a senha para URL
encoded_password = urllib.parse.quote_plus(DB_PASSWORD)

# URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}" 