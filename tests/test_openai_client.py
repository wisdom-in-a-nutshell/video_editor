import json
import unittest
from unittest.mock import patch
from src.openai_client import OpenAIClient, ChainOfThought

class TestOpenAIClient(unittest.TestCase):

    def setUp(self):
        self.client = OpenAIClient()
        self.chunk = "**Nathan:** Deritron CEO of Metaculous. Welcome to the cognitive revolution. **Deger:** Thank you. Big fun here."
        self.chain_of_thought = ChainOfThought(
            initial_analysis="Initial analysis",
            editing_goals="Editing goals",
            editing_process="Editing process",
            conclusion="Conclusion"
        )

    def test_create_and_format_reasoning_input(self):
        expected_output = [
            {"role": "system", "content": json.dumps(self.client.REASONING_PROMPT)},
            {"role": "user", "content": json.dumps({
                "raw_transcript": self.chunk,
                "instructions": "Extra guidelines for this specific transcript editing.",
                "additional_context": "Additional context for this specific transcript editing."
            })}
        ]
        result = self.client.create_and_format_reasoning_input(self.chunk)
        self.assertEqual(result, expected_output)

    def test_create_and_format_editing_input(self):
        expected_output = [
            {"role": "system", "content": json.dumps(self.client.EDITING_PROMPT)},
            {"role": "user", "content": json.dumps({
                "raw_transcript": self.chunk,
                "chain_of_thought": self.chain_of_thought.dict(),
                "instructions": "Extra guidelines for this specific transcript editing."
            })}
        ]
        result = self.client.create_and_format_editing_input(self.chunk, self.chain_of_thought)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()