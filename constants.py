import platformdirs
import os

from api.hardcover import Hardcover
from internal.session import Session

START_URL = 'https://play.google.com/books'
SESSION = Session()
HARDCOVER = Hardcover(os.getenv("HARDCOVER_TOKEN"))
DATA_DIR = platformdirs.user_config_dir("gpb-frankenstein")
MATCHES_FILE = os.path.join(DATA_DIR, "matches.json")
