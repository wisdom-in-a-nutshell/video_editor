from typing import List
from src.transcriber.assemblyai_transcriber import AssemblyAITranscriber
import assemblyai as aai

class ChunkedTranscriber:
    def __init__(self, chunk_size: int = 10):
        self.transcriber = AssemblyAITranscriber()
        self.chunk_size = chunk_size

    def chunk_sentences(self, file_path: str) -> List[str]:
        sentences = self.transcriber.get_sentences(file_path)
        chunks = []
        current_chunk = []
        current_word_count = 0
        last_speaker = None

        for sentence in sentences:
            words = sentence.words
            word_count = len(words)
            speaker_tag = f"**Speaker {sentence.speaker or 'Unknown'}:** "
            sentence_text = f"{sentence.text}"

            if sentence.speaker != last_speaker or not current_chunk:
                sentence_text = f"{speaker_tag} {sentence_text}"
                last_speaker = sentence.speaker

            if current_word_count + word_count > self.chunk_size:
                chunks.append(" ".join(current_chunk))
                current_chunk = [speaker_tag + sentence_text]
                current_word_count = word_count
            else:
                current_chunk.append(sentence_text)
                current_word_count += word_count

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks


if __name__ == "__main__":
    chunked_transcriber = ChunkedTranscriber(chunk_size=700)
    chunks = chunked_transcriber.chunk_sentences("/Users/adi/Downloads/final_audio.mp3")

    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1}:\n{chunk}\n")