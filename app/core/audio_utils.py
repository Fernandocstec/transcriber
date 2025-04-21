import os
import uuid
from typing import Optional

from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def extract_audio_from_video(video_path: str, output_dir: str) -> str:
    """
    Extrai o áudio de um arquivo de vídeo e salva no formato WAV.
    
    Args:
        video_path: Caminho para o arquivo de vídeo
        output_dir: Diretório para salvar o arquivo de áudio
    
    Returns:
        Caminho para o arquivo de áudio extraído
    """
    try:
        # Gera um nome de arquivo único
        audio_filename = f"{uuid.uuid4()}.wav"
        audio_path = os.path.join(output_dir, audio_filename)
        
        # Carrega o vídeo e extrai o áudio
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path, codec='pcm_s16le')
        
        return audio_filename
    except Exception as e:
        raise Exception(f"Erro ao extrair o áudio: {str(e)}")
    finally:
        if 'video' in locals():
            video.close()

def convert_to_mono(audio_path: str) -> str:
    """
    Converte áudio estéreo para mono.
    
    Args:
        audio_path: Caminho para o arquivo de áudio
    
    Returns:
        Caminho para o arquivo de áudio mono
    """
    try:
        # Carrega o arquivo de áudio
        audio = AudioSegment.from_wav(audio_path)
        
        # Converte para mono
        mono_audio = audio.set_channels(1)
        
        # Salva o áudio mono
        mono_path = audio_path.replace('.wav', '_mono.wav')
        mono_audio.export(mono_path, format="wav")
        
        return mono_path
    except Exception as e:
        raise Exception(f"Erro ao converter para mono: {str(e)}")

def normalize_audio(audio_path: str) -> str:
    """
    Normaliza o volume do áudio.
    
    Args:
        audio_path: Caminho para o arquivo de áudio
    
    Returns:
        Caminho para o arquivo de áudio normalizado
    """
    try:
        # Carrega o arquivo de áudio
        audio = AudioSegment.from_wav(audio_path)
        
        # Normaliza o volume
        normalized_audio = audio.normalize()
        
        # Salva o áudio normalizado
        normalized_path = audio_path.replace('.wav', '_normalized.wav')
        normalized_audio.export(normalized_path, format="wav")
        
        return normalized_path
    except Exception as e:
        raise Exception(f"Erro ao normalizar o áudio: {str(e)}") 