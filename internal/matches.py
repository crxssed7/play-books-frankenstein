import json
import os

class Matches:
    def __init__(self):
        self.matches = self._read_matches_from_file()

    def save_match(self, google_id, hardcover_id):
        self.matches[google_id] = hardcover_id
        self._save_matches_to_file()

    def get(self, google_id):
        return self.matches.get(google_id)

    def _save_matches_to_file(self):
        file_path = "matches.json"
        with open(file_path, 'w') as file:
            json.dump(self.matches, file)

    def _read_matches_from_file(self):
        file_path = "matches.json"
        matches = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                matches = json.load(file)
        return matches
