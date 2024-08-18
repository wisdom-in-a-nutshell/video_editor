import os
from dotenv import load_dotenv
from transcript_editor import TranscriptEditor

def main():
    # Load environment variables from .env file
    load_dotenv()

    input_file = "input_transcript.txt"
    output_file = "edited_transcript.txt"
    
    editor = TranscriptEditor(os.getenv("OPENAI_API_KEY"))
    editor.process_transcript(input_file, output_file)
    
    print(f"Edited transcript saved to {output_file}")

if __name__ == "__main__":
    main()