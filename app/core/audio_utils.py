import os
import uuid
from typing import Optional

from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def extract_audio_from_video(video_path: str, output_dir: str) -> str:
    """
    Extract audio from video file and save it as WAV format.
    
    Args:
        video_path: Path to the video file
        output_dir: Directory to save the audio file
    
    Returns:
        Path to the extracted audio file
    """
    try:
        # Generate unique filename
        audio_filename = f"{uuid.uuid4()}.wav"
        audio_path = os.path.join(output_dir, audio_filename)
        
        # Load video and extract audio
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        
        return audio_filename
    except Exception as e:
        raise Exception(f"Error extracting audio: {str(e)}")
    finally:
        if 'video' in locals():
            video.close()

def convert_to_mono(audio_path: str) -> str:
    """
    Convert stereo audio to mono.
    
    Args:
        audio_path: Path to the audio file
    
    Returns:
        Path to the mono audio file
    """
    try:
        # Load audio file
        audio = AudioSegment.from_wav(audio_path)
        
        # Convert to mono
        mono_audio = audio.set_channels(1)
        
        # Save mono audio
        mono_path = audio_path.replace('.wav', '_mono.wav')
        mono_audio.export(mono_path, format="wav")
        
        return mono_path
    except Exception as e:
        raise Exception(f"Error converting to mono: {str(e)}")

def normalize_audio(audio_path: str) -> str:
    """
    Normalize audio volume.
    
    Args:
        audio_path: Path to the audio file
    
    Returns:
        Path to the normalized audio file
    """
    try:
        # Load audio file
        audio = AudioSegment.from_wav(audio_path)
        
        # Normalize volume
        normalized_audio = audio.normalize()
        
        # Save normalized audio
        normalized_path = audio_path.replace('.wav', '_normalized.wav')
        normalized_audio.export(normalized_path, format="wav")
        
        return normalized_path
    except Exception as e:
        raise Exception(f"Error normalizing audio: {str(e)}") 