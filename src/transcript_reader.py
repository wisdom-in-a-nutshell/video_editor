import re
from nltk.tokenize import sent_tokenize

class TranscriptReader:
    def __init__(self, chunk_size=1000):
        if chunk_size <= 0:
            raise ValueError("Chunk size must be a positive integer.")
        self.chunk_size = chunk_size

    def read_and_chunk_transcript(self, file_path):
        text = self._read_file(file_path)
        cleaned_text = self._clean_and_normalize_text(text)
        sentences = self._tokenize_sentences(cleaned_text)
        return self._create_chunks(sentences)

    def _read_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except IOError as e:
            raise IOError(f"Error reading file: {e}")

    def _clean_and_normalize_text(self, text):
        cleaned_text = self._clean_transcript(text)
        return self._normalize_spaces(cleaned_text)

    def _tokenize_sentences(self, text):
        return [s.strip() for s in sent_tokenize(text) if s.strip()]

    def _create_chunks(self, sentences):
        chunks = []
        current_chunk = []
        current_word_count = 0

        for sentence in sentences:
            sentence_word_count = len(sentence.split())

            if current_word_count + sentence_word_count > self.chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_word_count = 0

            current_chunk.append(sentence)
            current_word_count += sentence_word_count

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks

    def _clean_transcript(self, text):
        """
        Performs initial cleaning of the transcript:
        1. Replaces speaker tags with timestamps with a formatted version
        2. Removes newlines
        """
        # Regular expression to match speaker tags with timestamps
        pattern = r'(\w+)\s*\(\d{2}:\d{2}\)\s*\n'
        
        # Replace speaker tags and remove newlines
        cleaned_text = re.sub(pattern, r'**\1:** ', text)
        
        return cleaned_text.replace('\n', ' ')

    def _normalize_spaces(self, text):
        """
        Normalizes spaces in the text:
        1. Replaces multiple spaces with a single space
        2. Removes any remaining newlines and replaces them with a space
        """
        # Replace multiple spaces with a single space
        normalized_text = re.sub(r'\s+', ' ', text)
        
        # Remove any remaining newlines and replace with a space
        normalized_text = normalized_text.replace('\n', ' ')
        
        return normalized_text.strip()

if __name__ == "__main__":
    reader = TranscriptReader()
    # Add a test case here if needed
    chunks = reader.read_and_chunk_transcript("/Users/adi/Documents/GitHub/video_editor/tmp/metaculus.txt")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:")
        print(chunk)
        print("-" * 50)  # Separator between chunks
    print("TranscriptReader initialized successfully.")