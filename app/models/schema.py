from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    video_filename = Column(String, nullable=False)
    audio_filename = Column(String, nullable=False)
    transcript_filename = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")
    segments = relationship("TranscriptionSegment", back_populates="transcription")

class TranscriptionSegment(Base):
    __tablename__ = "transcription_segments"

    id = Column(Integer, primary_key=True, index=True)
    transcription_id = Column(Integer, ForeignKey("transcriptions.id"))
    start_time = Column(Integer)  # em segundos
    end_time = Column(Integer)    # em segundos
    speaker = Column(String)
    text = Column(Text)
    transcription = relationship("Transcription", back_populates="segments")

# Modelos Pydantic para API
class TranscriptionCreate(BaseModel):
    video_filename: str

class TranscriptionResponse(BaseModel):
    id: int
    video_filename: str
    audio_filename: str
    transcript_filename: str
    created_at: datetime
    status: str

    class Config:
        from_attributes = True

class TranscriptionSegmentResponse(BaseModel):
    id: int
    transcription_id: int
    start_time: int
    end_time: int
    speaker: str
    text: str

    class Config:
        from_attributes = True 