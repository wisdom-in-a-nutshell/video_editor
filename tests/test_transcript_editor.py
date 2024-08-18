import unittest
from unittest.mock import Mock, patch
from src.transcript_editor import TranscriptEditor
from src.openai_client import OpenAIClient

class TestTranscriptEditor(unittest.TestCase):

    def setUp(self):
        self.api_key = "test_api_key"
        self.editor = TranscriptEditor(self.api_key, chunk_size=5)

    def test_split_into_chunks(self):
        text = "This is a test transcript for splitting"
        expected_chunks = ["This is a test transcript", "for splitting"]
        result = self.editor._split_into_chunks(text)
        self.assertEqual(result, expected_chunks)

    def test_combine_chunks(self):
        chunks = ["This is", "a test", "transcript"]
        expected_result = "This is a test transcript"
        result = self.editor._combine_chunks(chunks)
        self.assertEqual(result, expected_result)

    @patch('builtins.open', unittest.mock.mock_open(read_data="This is a test transcript"))
    def test_read_transcript(self):
        result = self.editor._read_transcript("dummy_path")
        self.assertEqual(result, "This is a test transcript")

    @patch('builtins.open', unittest.mock.mock_open())
    def test_write_transcript(self):
        self.editor._write_transcript("Edited transcript", "dummy_path")
        open.assert_called_once_with("dummy_path", "w")
        open().write.assert_called_once_with("Edited transcript")

if __name__ == '__main__':
    unittest.main()