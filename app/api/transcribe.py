import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.core.audio_utils import extract_audio_from_video, convert_to_mono, normalize_audio
from app.core.transcription import WhisperTranscriber
from app.core.diarization import SpeakerDiarizer
from app.models.schema import Transcription, TranscriptionSegment, TranscriptionCreate, TranscriptionResponse
from app.core.database import get_db

router = APIRouter()

# Configura os caminhos
VIDEOS_DIR = "videos"
TRANSCRIPTS_DIR = "transcripts"

# Inicializa os componentes
transcriber = WhisperTranscriber()
diarizer = SpeakerDiarizer()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def upload_and_transcribe(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = get_db()
):
    """
    Faz upload de um arquivo de vídeo e inicia o processo de transcrição.
    """
    try:
        # Cria diretórios se não existirem
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
        
        # Salva o vídeo enviado
        video_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        video_path = os.path.join(VIDEOS_DIR, video_filename)
        
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Cria registro de transcrição
        transcription = Transcription(
            video_filename=video_filename,
            audio_filename="",  # Será atualizado após o processamento
            transcript_filename="",  # Será atualizado após o processamento
            status="processing"
        )
        db.add(transcription)
        db.commit()
        db.refresh(transcription)
        
        # Inicia processamento em segundo plano
        background_tasks.add_task(
            process_transcription,
            video_path,
            transcription.id,
            db
        )
        
        return transcription
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()

async def process_transcription(video_path: str, transcription_id: int, db: Session):
    """
    Processa a transcrição do vídeo em segundo plano.
    """
    try:
        # Atualiza o status da transcrição
        transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
        if not transcription:
            return
        
        # Extrai o áudio
        audio_filename = extract_audio_from_video(video_path, VIDEOS_DIR)
        transcription.audio_filename = audio_filename
        db.commit()
        
        # Converte para mono e normaliza
        audio_path = os.path.join(VIDEOS_DIR, audio_filename)
        mono_path = convert_to_mono(audio_path)
        normalized_path = normalize_audio(mono_path)
        
        # Transcreve o áudio
        transcription_result = transcriber.transcribe_audio(normalized_path)
        transcript_filename = transcriber.save_transcription(transcription_result, TRANSCRIPTS_DIR)
        transcription.transcript_filename = transcript_filename
        db.commit()
        
        # Realiza a diarização
        diarization_segments = diarizer.diarize_audio(normalized_path)
        transcription_segments = transcriber.process_segments(transcription_result)
        final_segments = diarizer.assign_speakers_to_segments(transcription_segments, diarization_segments)
        
        # Salva os segmentos no banco de dados
        for segment in final_segments:
            db_segment = TranscriptionSegment(
                transcription_id=transcription_id,
                start_time=segment['start_time'],
                end_time=segment['end_time'],
                speaker=segment['speaker'],
                text=segment['text']
            )
            db.add(db_segment)
        
        # Atualiza o status da transcrição
        transcription.status = "completed"
        db.commit()
        
    except Exception as e:
        # Atualiza o status da transcrição para falha
        transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
        if transcription:
            transcription.status = "failed"
            db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transcripts", response_model=List[TranscriptionResponse])
async def list_transcriptions(db: Session = get_db()):
    """
    Lista todas as transcrições.
    """
    try:
        transcriptions = db.query(Transcription).all()
        return transcriptions
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transcripts/{transcription_id}", response_model=TranscriptionResponse)
async def get_transcription(transcription_id: int, db: Session = get_db()):
    """
    Obtém uma transcrição específica por ID.
    """
    try:
        transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
        if not transcription:
            raise HTTPException(status_code=404, detail="Transcrição não encontrada")
        return transcription
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 