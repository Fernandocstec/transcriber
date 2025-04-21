# Video Transcription API

A FastAPI-based service for transcribing videos with speaker diarization capabilities. This project uses OpenAI's Whisper for transcription and pyannote.audio for speaker diarization.

## Features

- Video to audio extraction
- Audio transcription using Whisper
- Speaker diarization using pyannote.audio
- RESTful API endpoints for video upload and transcription
- Background processing for long-running tasks
- PostgreSQL database for storing transcriptions

## Prerequisites

- Python 3.8+
- PostgreSQL
- FFmpeg (for audio processing)
- Hugging Face account and API token (for pyannote.audio)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd transcriber
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/transcriber_db
HUGGINGFACE_TOKEN=your_huggingface_token
```

5. Initialize the database:
```bash
# Create the database in PostgreSQL
createdb transcriber_db

# Run database migrations (if any)
alembic upgrade head
```

## Project Structure

```
transcriber/
├── app/
│   ├── api/
│   │   └── transcribe.py       # API endpoints
│   ├── core/
│   │   ├── audio.py           # Audio processing
│   │   ├── audio_utils.py     # Audio utility functions
│   │   ├── diarization.py     # Speaker diarization
│   │   └── transcription.py   # Transcription logic
│   ├── models/
│   │   └── schema.py          # Database models
│   └── main.py                # FastAPI application
├── frontend/                  # Frontend application
├── setup.py                   # Package configuration
└── README.md                  # This file
```

## Usage

1. Start the API server:
```bash
uvicorn app.main:app --reload
```

2. The API will be available at `http://localhost:8000`

### API Endpoints

- `POST /api/transcribe`: Upload a video file for transcription
- `GET /api/transcripts`: List all transcriptions
- `GET /api/transcripts/{transcription_id}`: Get a specific transcription

### Example Usage

```python
import requests

# Upload a video file
with open('video.mp4', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/api/transcribe', files=files)
    transcription_id = response.json()['id']

# Get transcription status
response = requests.get(f'http://localhost:8000/api/transcripts/{transcription_id}')
print(response.json())
```

## Development

### Running Tests

```bash
pytest
```

### Code Style

This project uses:
- Black for code formatting
- isort for import sorting
- flake8 for linting

Run code style checks:
```bash
black .
isort .
flake8
```

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 