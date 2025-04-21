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

# Configure paths
VIDEOS_DIR = "videos"
TRANSCRIPTS_DIR = "transcripts"

# Initialize components
transcriber = WhisperTranscriber()
diarizer = SpeakerDiarizer()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def upload_and_transcribe(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = get_db()
):
    """
    Upload a video file and start the transcription process.
    """
    try:
        # Create directories if they don't exist
        os.makedirs(VIDEOS_DIR, exist_ok=True)
        os.makedirs(TRANSCRIPTS_DIR, exist_ok=True)
        
        # Save uploaded video
        video_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        video_path = os.path.join(VIDEOS_DIR, video_filename)
        
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create transcription record
        transcription = Transcription(
            video_filename=video_filename,
            audio_filename="",  # Will be updated after processing
            transcript_filename="",  # Will be updated after processing
            status="processing"
        )
        db.add(transcription)
        db.commit()
        db.refresh(transcription)
        
        # Start background processing
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
    Process video transcription in the background.
    """
    try:
        # Update transcription status
        transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
        if not transcription:
            return
        
        # Extract audio
        audio_filename = extract_audio_from_video(video_path, VIDEOS_DIR)
        transcription.audio_filename = audio_filename
        db.commit()
        
        # Convert to mono and normalize
        audio_path = os.path.join(VIDEOS_DIR, audio_filename)
        mono_path = convert_to_mono(audio_path)
        normalized_path = normalize_audio(mono_path)
        
        # Transcribe audio
        transcription_result = transcriber.transcribe_audio(normalized_path)
        transcript_filename = transcriber.save_transcription(transcription_result, TRANSCRIPTS_DIR)
        transcription.transcript_filename = transcript_filename
        db.commit()
        
        # Perform diarization
        diarization_segments = diarizer.diarize_audio(normalized_path)
        transcription_segments = transcriber.process_segments(transcription_result)
        final_segments = diarizer.assign_speakers_to_segments(transcription_segments, diarization_segments)
        
        # Save segments to database
        for segment in final_segments:
            db_segment = TranscriptionSegment(
                transcription_id=transcription_id,
                start_time=segment['start_time'],
                end_time=segment['end_time'],
                speaker=segment['speaker'],
                text=segment['text']
            )
            db.add(db_segment)
        
        # Update transcription status
        transcription.status = "completed"
        db.commit()
        
    except Exception as e:
        # Update transcription status to failed
        transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
        if transcription:
            transcription.status = "failed"
            db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transcripts", response_model=List[TranscriptionResponse])
async def list_transcriptions(db: Session = get_db()):
    """
    List all transcriptions.
    """
    try:
        transcriptions = db.query(Transcription).all()
        return transcriptions
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transcripts/{transcription_id}", response_model=TranscriptionResponse)
async def get_transcription(transcription_id: int, db: Session = get_db()):
    """
    Get a specific transcription by ID.
    """
    try:
        transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
        if not transcription:
            raise HTTPException(status_code=404, detail="Transcription not found")
        return transcription
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e)) 