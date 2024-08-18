import sys
from nltk.tokenize import sent_tokenize
import nltk

print(f"Python version: {sys.version}")
print(f"NLTK version: {nltk.__version__}")

nltk.download('punkt', quiet=True)

# Test the tokenizer
test_sentence = "This is a test sentence. This is another one."
tokens = sent_tokenize(test_sentence)
print(f"Tokenization test: {tokens}")