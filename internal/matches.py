import json
import os

from constants import MATCHES_FILE

class Matches:
    def __init__(self):
        self.matches = self._read_matches_from_file()

    def save_match(self, google_id, hardcover_id):
        self.matches[google_id] = hardcover_id
        self._save_matches_to_file()

    def get(self, google_id):
        return self.matches.get(google_id)

    def _save_matches_to_file(self):
        with open(MATCHES_FILE, 'w') as file:
            json.dump(self.matches, file)

    def _read_matches_from_file(self):
        matches = {}
        if os.path.exists(MATCHES_FILE):
            with open(MATCHES_FILE, 'r') as file:
                matches = json.load(file)
        return matches

MATCHES = Matches()
