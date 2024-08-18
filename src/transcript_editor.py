from openai_client import OpenAIClient
from src.transcript_reader import TranscriptReader
from src.transcriber.chunked_transcriber import ChunkedTranscriber

class TranscriptEditor:
    def __init__(self, api_key, chunk_size=1000):
        self.openai_client = OpenAIClient(api_key)
        self.transcript_reader = TranscriptReader(chunk_size)

    def process_transcript(self, input_file, output_file):
        chunks = self.transcript_reader.read_and_chunk_transcript(input_file)
        with open(output_file, 'w') as file:
            for chunk in chunks:
                edited_chunk = self.openai_client.process_chunk(chunk)
                file.write(edited_chunk)
                file.write('\n\n\n')  # Add separator between chunks

    def _write_transcript(self, transcript, file_path):
        with open(file_path, 'a') as file:
            file.write(transcript)
