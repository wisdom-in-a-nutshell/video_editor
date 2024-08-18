from openai_client import OpenAIClient
from src.transcript_reader import TranscriptReader

class TranscriptEditor:
    def __init__(self, api_key, chunk_size=1000):
        self.openai_client = OpenAIClient(api_key)
        self.transcript_reader = TranscriptReader(chunk_size)

    def process_transcript(self, input_file, output_file):
        chunks = self.transcript_reader.read_and_chunk_transcript(input_file)
        edited_chunks = [self.openai_client.process_chunk(chunk) for chunk in chunks]
        edited_transcript = self._combine_chunks(edited_chunks)
        self._write_transcript(edited_transcript, output_file)

    def _write_transcript(self, transcript, file_path):
        with open(file_path, 'w') as file:
            file.write(transcript)

    def _combine_chunks(self, chunks):
        return ' '.join(chunks)