import axios from 'axios';
import { Transcription } from '../types';

const API_URL = 'http://localhost:8000/api';

export const api = {
  async uploadVideo(file: File): Promise<Transcription> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_URL}/transcribe`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async getTranscriptions(): Promise<Transcription[]> {
    const response = await axios.get(`${API_URL}/transcripts`);
    return response.data;
  },

  async getTranscription(id: number): Promise<Transcription> {
    const response = await axios.get(`${API_URL}/transcripts/${id}`);
    return response.data;
  },
}; 