import os
from dotenv import load_dotenv
from transcript_editor import TranscriptEditor

def main():
    # Load environment variables from .env file
    load_dotenv()

    input_file = "/tmp/metaculus.md"
    output_file = "/tmp/metaculus_edited.md"
    
    editor = TranscriptEditor(os.getenv("OPENAI_API_KEY"))
    editor.process_transcript(input_file, output_file)
    
    print(f"Edited transcript saved to {output_file}")

if __name__ == "__main__":
    main()