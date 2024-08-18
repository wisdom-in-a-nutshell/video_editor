import assemblyai as aai
import json
import os
from typing import Optional, Dict, Any, List
import hashlib
from dotenv import load_dotenv

from src.transcriber.transcript_storage import TranscriptStorage

load_dotenv()  # Load environment variables from .env file

def generate_hash(file_path: str, config: Dict[str, Any]) -> str:
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        hasher.update(f.read())
    hasher.update(json.dumps(config, sort_keys=True).encode('utf-8'))
    return hasher.hexdigest()


class AssemblyAITranscriber:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided or set as ASSEMBLYAI_API_KEY environment variable")
        aai.settings.api_key = self.api_key
        self.transcriber = aai.Transcriber()
        self.transcript_storage = TranscriptStorage()

    def transcribe(self, file_path: str) -> aai.Transcript:
        transcription_config = aai.TranscriptionConfig(
            speech_model=aai.SpeechModel.nano, 
            language_code="en", 
            speaker_labels=True, 
            punctuate=True, 
            format_text=True, 
            disfluencies=True, 
            filter_profanity=False
        )
        
        # Check if the hash exists in the local storage
        file_hash = generate_hash(file_path, transcription_config._raw_transcription_config.__dict__)
        transcript_id = self.transcript_storage.get_transcript_id(file_hash)
        # If it exists, fetch the transcript from AssemblyAI
        if transcript_id:
            return aai.Transcript.get_by_id(transcript_id)
        # If it doesn't exist, transcribe and store the new transcript ID
        else:
            transcript = self.transcriber.transcribe(file_path, config=transcription_config)
            self.transcript_storage.save_transcript_id(file_hash, transcript.id)
            return transcript

    def get_sentences(self, file_path: str) -> List[aai.types.Sentence]:
        transcript = self.transcribe(file_path)
        return transcript.get_sentences()


if __name__ == "__main__":
    transcriber = AssemblyAITranscriber()
    # Transcribe an audio file
    transcript = transcriber.get_sentences("/Users/adi/Downloads/final_audio.mp3")

    print(transcript)