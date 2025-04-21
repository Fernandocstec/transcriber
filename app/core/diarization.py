from typing import List, Dict, Any
import numpy as np
from pyannote.audio import Pipeline
import os

class SpeakerDiarizer:
    def __init__(self, auth_token: str = None):
        """
        Inicializar pipeline de diarização de interlocutores.
        
        Args:
            auth_token: Token de autenticação Hugging Face para pyannote.audio
        """
        self.auth_token = auth_token or os.getenv("HUGGINGFACE_TOKEN")
        if not self.auth_token:
            raise ValueError("O token de autenticação Hugging Face é necessário")
        
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization",
            use_auth_token=self.auth_token
        )
    
    def diarize_audio(self, audio_path: str) -> List[Dict[str, Any]]:
        """
        Executar a diarização do locutor em um arquivo de áudio.
        
        Args:
            audio_path: Caminho para o arquivo de áudio
            
        Returns:
            Lista de segmentos de diarização com rótulos de interlocutores
        """
        try:
            # Executar separação de locutores
            diarization = self.pipeline(audio_path)
            
            # Converter para lista de segmentos
            segments = []
            for segment, _, speaker in diarization.itertracks(yield_label=True):
                segments.append({
                    'start_time': int(segment.start),
                    'end_time': int(segment.end),
                    'speaker': speaker
                })
            
            return segments
        except Exception as e:
            raise Exception(f"Error performing diarization: {str(e)}")
    
    def assign_speakers_to_segments(self, 
                                  transcription_segments: List[Dict[str, Any]], 
                                  diarization_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Assign speaker labels to transcription segments based on diarization results.
        
        Args:
            transcription_segments: List of transcription segments
            diarization_segments: List of diarization segments with speaker labels
            
        Returns:
            List of transcription segments with assigned speaker labels
        """
        try:
            # Classificar segmentos por hora de início
            transcription_segments.sort(key=lambda x: x['start_time'])
            diarization_segments.sort(key=lambda x: x['start_time'])
            
            # Atribuir interlocutores a segmentos de transcrição
            for trans_segment in transcription_segments:
                # Encontre segmentos de diarização sobrepostos
                overlapping_speakers = []
                for diar_segment in diarization_segments:
                    if (diar_segment['start_time'] <= trans_segment['end_time'] and 
                        diar_segment['end_time'] >= trans_segment['start_time']):
                        # Calcular a duração da sobreposição
                        overlap_start = max(trans_segment['start_time'], diar_segment['start_time'])
                        overlap_end = min(trans_segment['end_time'], diar_segment['end_time'])
                        overlap_duration = overlap_end - overlap_start
                        
                        overlapping_speakers.append({
                            'speaker': diar_segment['speaker'],
                            'duration': overlap_duration
                        })
                
                # Atribuir interlocutor com sobreposição máxima
                if overlapping_speakers:
                    max_overlap = max(overlapping_speakers, key=lambda x: x['duration'])
                    trans_segment['speaker'] = max_overlap['speaker']
                else:
                    trans_segment['speaker'] = "unknown"
            
            return transcription_segments
        except Exception as e:
            raise Exception(f"Error assigning speakers: {str(e)}") 