import os
from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

from app.models.schema import Base
from app.api.transcribe import router as transcribe_router
from app.core.database import engine

# Carrega variáveis de ambiente
load_dotenv()

# Cria as tabelas do banco de dados
Base.metadata.create_all(bind=engine)

# Aplicação FastAPI
app = FastAPI(
    title="Transcriber API",
    description="API para transcrição de vídeo com diarização de falantes",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os roteadores
app.include_router(transcribe_router, prefix="/api", tags=["transcription"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API do Transcriber"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 