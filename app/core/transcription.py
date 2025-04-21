import os
import json
from datetime import datetime
from typing import List, Dict, Any

import whisper

class WhisperTranscriber:
    def __init__(self, model_size: str = "base"):
        """
        Initialize Whisper transcriber with specified model size.
        
        Args:
            model_size: Size of the Whisper model to use (tiny, base, small, medium, large)
        """
        self.model = whisper.load_model(model_size)
    
    def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Dictionary containing transcription results
        """
        try:
            # Transcribe audio
            result = self.model.transcribe(
                audio_path,
                language="pt",  # Portuguese language
                task="transcribe",
                verbose=False
            )
            
            return result
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
    
    def save_transcription(self, transcription: Dict[str, Any], output_dir: str) -> str:
        """
        Save transcription results to a JSON file.
        
        Args:
            transcription: Transcription results from Whisper
            output_dir: Directory to save the transcription file
            
        Returns:
            Path to the saved transcription file
        """
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"transcription_{timestamp}.json"
            output_path = os.path.join(output_dir, filename)
            
            # Save transcription to file
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(transcription, f, ensure_ascii=False, indent=2)
            
            return filename
        except Exception as e:
            raise Exception(f"Error saving transcription: {str(e)}")
    
    def process_segments(self, transcription: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process transcription segments for database storage.
        
        Args:
            transcription: Transcription results from Whisper
            
        Returns:
            List of processed segments
        """
        processed_segments = []
        
        for segment in transcription.get('segments', []):
            processed_segment = {
                'start_time': int(segment['start']),
                'end_time': int(segment['end']),
                'text': segment['text'].strip(),
                'speaker': None  # Will be filled by diarization
            }
            processed_segments.append(processed_segment)
        
        return processed_segments 