import json
import os

from constants import SETTINGS_FILE

class Settings:
    def __init__(self):
        self.json = self._read_settings_from_file()
        self.hardcover_token = self.json.get("HARDCOVER_TOKEN") or os.getenv("HARDCOVER_TOKEN")

    def save_settings(self, hardcover_token = None):
        new_token = hardcover_token
        if new_token is None: # You can't explicitly set the token to None, this allows for a call to save_settings() without params
            new_token = self.hardcover_token
        self.hardcover_token = new_token
        self.json["HARDCOVER_TOKEN"] = new_token
        self._save_settings_to_file()

    def get_settings(self):
        return {
            "HARDCOVER_TOKEN": self.hardcover_token
        }

    def _save_settings_to_file(self):
        with open(SETTINGS_FILE, 'w') as file:
            json.dump(self.json, file)

    def _read_settings_from_file(self):
        data = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as file:
                data = json.load(file)
        return data

SETTINGS = Settings()
