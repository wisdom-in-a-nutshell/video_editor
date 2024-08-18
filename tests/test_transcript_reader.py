import unittest
from src.transcript_reader import TranscriptReader
import tempfile
import os

class TestTranscriptReader(unittest.TestCase):
    def setUp(self):
        self.reader = TranscriptReader(chunk_size=50)
        self.sample_transcript = """
Nathan (00:00)
have you seen my outline? I assume that made its way to you. Okay. Cool. So we can certainly.

Deger (00:05)
I did, yeah, yeah, look through it. Yeah, also a fan of previous chapters you've done too, so I'm excited to be here for it. Awesome.

Nathan (00:14)
Great, thank you. We can certainly deviate from that if there's anything you want to add or subtract, know, whatever, it's all good, but at least that's a good starting point, hopefully.
"""

    def test_clean_and_normalize_text(self):
        cleaned_text = self.reader._clean_and_normalize_text(self.sample_transcript)
        expected_output = "**Nathan:** have you seen my outline? I assume that made its way to you. Okay. Cool. So we can certainly. **Deger:** I did, yeah, yeah, look through it. Yeah, also a fan of previous chapters you've done too, so I'm excited to be here for it. Awesome. **Nathan:** Great, thank you. We can certainly deviate from that if there's anything you want to add or subtract, know, whatever, it's all good, but at least that's a good starting point, hopefully."
        self.assertEqual(cleaned_text, expected_output)

    def test_tokenize_sentences(self):
        cleaned_text = self.reader._clean_and_normalize_text(self.sample_transcript)
        sentences = self.reader._tokenize_sentences(cleaned_text)
        self.assertEqual(len(sentences), 5)
        self.assertTrue(all(sentence.startswith("**") for sentence in sentences))

    def test_create_chunks(self):
        cleaned_text = self.reader._clean_and_normalize_text(self.sample_transcript)
        sentences = self.reader._tokenize_sentences(cleaned_text)
        chunks = self.reader._create_chunks(sentences)
        self.assertEqual(len(chunks), 2)  # With chunk_size=50, it should create 2 chunks

    def test_read_and_chunk_transcript(self):
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(self.sample_transcript)
            temp_file_path = temp_file.name

        try:
            chunks = self.reader.read_and_chunk_transcript(temp_file_path)
            self.assertEqual(len(chunks), 2)
            self.assertTrue(all("**Nathan:**" in chunk for chunk in chunks))
            self.assertTrue(any("**Deger:**" in chunk for chunk in chunks))
        finally:
            os.unlink(temp_file_path)

    def test_invalid_chunk_size(self):
        with self.assertRaises(ValueError):
            TranscriptReader(chunk_size=0)

    def test_file_not_found(self):
        with self.assertRaises(IOError):
            self.reader.read_and_chunk_transcript("non_existent_file.txt")

if __name__ == '__main__':
    unittest.main()