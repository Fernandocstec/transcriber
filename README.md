# API de Transcrição de Vídeo

Um serviço baseado em FastAPI para transcrição de vídeos. Este projeto utiliza o Whisper da OpenAI para transcrição e pyannote.audio para diarização de interlocutores.

## Funcionalidades

- Extração de áudio de vídeo
- Transcrição de áudio usando Whisper
- Diarização de interlocutores usando pyannote.audio
- Endpoints RESTful para upload de vídeo e transcrição
- Processamento em segundo plano para tarefas longas
- Banco de dados PostgreSQL para armazenar transcrições

## Pré-requisitos

- Python 3.8+
- PostgreSQL
- FFmpeg (para processamento de áudio)
- Conta no Hugging Face e token de API (para pyannote.audio)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Fernandocstec/transcriber.git
cd transcriber
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -e .
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` no diretório raiz com as seguintes variáveis:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/transcriber_db
HUGGINGFACE_TOKEN=seu_token_do_huggingface
```

5. Inicialize o banco de dados:
```bash
# Crie o banco de dados no PostgreSQL
createdb transcriber_db

# Execute as migrações do banco de dados (se houver)
alembic upgrade head
```

## Estrutura do Projeto

```
transcriber/
├── app/
│   ├── api/
│   │   └── transcribe.py       # Endpoints da API
│   ├── core/
│   │   ├── audio.py           # Processamento de áudio
│   │   ├── audio_utils.py     # Funções utilitárias de áudio
│   │   ├── diarization.py     # Diarização de interlocutores
│   │   └── transcription.py   # Lógica de transcrição
│   ├── models/
│   │   └── schema.py          # Modelos do banco de dados
│   └── main.py                # Aplicação FastAPI
├── frontend/                  # Aplicação frontend
├── setup.py                   # Configuração do pacote
└── README.md                  # Este arquivo
```

## Uso

1. Inicie o servidor da API:
```bash
uvicorn app.main:app --reload
```

2. A API estará disponível em `http://localhost:8000`

### Endpoints da API

- `POST /api/transcribe`: Envie um arquivo de vídeo para transcrição
- `GET /api/transcripts`: Liste todas as transcrições
- `GET /api/transcripts/{transcription_id}`: Obtenha uma transcrição específica

### Exemplo de Uso

```python
import requests

# Envie um arquivo de vídeo
with open('video.mp4', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/transcribe', files=files)
    transcription_id = response.json()['id']

# Obtenha o status da transcrição
response = requests.get(f'http://localhost:8000/api/transcripts/{transcription_id}')
print(response.json())
```

## Desenvolvimento

### Executando Testes

```bash
pytest
```

### Estilo de Código

Este projeto utiliza:
- Black para formatação de código
- isort para ordenação de imports
- flake8 para linting

Execute as verificações de estilo:
```bash
black .
isort .
flake8
```

## Licença

[Licença MIT](LICENSE)

## Contribuindo

1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das suas alterações
4. Envie para a branch
5. Abra um Pull Request 