# Transcript Editor

This project processes transcripts by marking unnecessary words or phrases with strikethrough formatting using OpenAI's language model.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set your OpenAI API key as an environment variable:
   - `export OPENAI_API_KEY=your_api_key_here` (Unix-based systems)
   - `set OPENAI_API_KEY=your_api_key_here` (Windows)

## Usage

1. Place your input transcript in `input_transcript.txt` in the project root
2. Run the script: `python src/main.py`
3. Find the edited transcript in `edited_transcript.txt` in the project root

## Configuration

The chunk size for processing can be adjusted in the `TranscriptEditor` class initialization in `src/main.py`.