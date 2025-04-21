export interface Transcription {
  id: number;
  video_filename: string;
  audio_filename: string;
  transcript_filename: string;
  created_at: string;
  status: string;
}

export interface TranscriptionSegment {
  id: number;
  transcription_id: number;
  start_time: number;
  end_time: number;
  speaker: string;
  text: string;
} 