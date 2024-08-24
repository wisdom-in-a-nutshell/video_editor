from src.openai_client import OpenAIClient
from src.transcriber.chunked_transcriber import ChunkedTranscriber
import concurrent.futures

class AudioTranscriptProcessor:
    def __init__(self, chunk_size=1000):
        self.openai_client = OpenAIClient()
        self.chunked_transcriber = ChunkedTranscriber(chunk_size)
        self.chunk_size = chunk_size

    def process_chunk(self, chunk):
        try:
            return self.openai_client.process_chunk(chunk.strip())
        except Exception:
            return "OpenAI Call Failure"

    def process_audio_file(self, audio_file_path):
        # Generate transcript chunks from the audio file
        chunks = self.chunked_transcriber.chunk_sentences(audio_file_path)
        edited_markdown_file = f"/Users/adi/Documents/GitHub/video_editor/tmp/metaculus_{self.chunk_size}_gpt4.md"

        # Process chunks in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_chunk = {executor.submit(self.process_chunk, chunk): i for i, chunk in enumerate(chunks)}
            results = [None] * len(chunks)
            for future in concurrent.futures.as_completed(future_to_chunk):
                index = future_to_chunk[future]
                try:
                    results[index] = future.result()
                except Exception as e:
                    results[index] = "OpenAI Call Failure"

        # Write results to the markdown file in order
        try:
            with open(edited_markdown_file, 'w') as outfile:
                for result in results:
                    outfile.write(result)
                    outfile.write('\n\n')  # Add separator between chunks
            print(f"Edited markdown file created at: {edited_markdown_file}")
        except Exception as e:
            print(f"An error occurred while writing to the file: {e}")

# Example usage
if __name__ == "__main__":
    audio_file_path = "/Users/adi/Downloads/johsua.mp3"
    processor = AudioTranscriptProcessor(chunk_size=700)
    processor.process_audio_file(audio_file_path)