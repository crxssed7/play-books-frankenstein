import platformdirs
import os

from internal.session import Session

APP_VERSION = "0.0.8"
DATA_DIR = platformdirs.user_config_dir("gpb-frankenstein")
MATCHES_FILE = os.path.join(DATA_DIR, "matches.json")
LOG_FILE = os.path.join(DATA_DIR, f"frankenstein_{APP_VERSION}.log")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")
START_URL = 'https://play.google.com/books'
SESSION = Session()
