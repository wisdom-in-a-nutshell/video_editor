import json
from typing import Optional


class TranscriptStorage:
    def __init__(self, storage_path: str = "/Users/adi/Documents/GitHub/video_editor/tmp/transcript_ids.json"):
        self.storage_path = storage_path
        self._load_storage()

    def _load_storage(self):
        try:
            with open(self.storage_path, 'r') as f:
                self.storage = json.load(f)
        except FileNotFoundError:
            self.storage = {}

    def _save_storage(self):
        with open(self.storage_path, 'w') as f:
            json.dump(self.storage, f)

    def get_transcript_id(self, file_hash: str) -> Optional[str]:
        return self.storage.get(file_hash)

    def save_transcript_id(self, file_hash: str, transcript_id: str):
        self.storage[file_hash] = transcript_id
        self._save_storage()
