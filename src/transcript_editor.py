from openai_client import OpenAIClient

class TranscriptEditor:
    def __init__(self, api_key, chunk_size=1000):
        self.openai_client = OpenAIClient(api_key)
        self.chunk_size = chunk_size

    def process_transcript(self, input_file, output_file):
        transcript = self._read_transcript(input_file)
        chunks = self._split_into_chunks(transcript)
        edited_chunks = [self.openai_client.process_chunk(chunk) for chunk in chunks]
        edited_transcript = self._combine_chunks(edited_chunks)
        self._write_transcript(edited_transcript, output_file)

    def _read_transcript(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def _write_transcript(self, transcript, file_path):
        with open(file_path, 'w') as file:
            file.write(transcript)

    def _split_into_chunks(self, text):
        words = text.split()
        return [' '.join(words[i:i+self.chunk_size]) for i in range(0, len(words), self.chunk_size)]

    def _combine_chunks(self, chunks):
        return ' '.join(chunks)