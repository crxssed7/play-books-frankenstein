import os

from api.hardcover import Hardcover
from internal.matches import Matches
from internal.session import Session

START_URL = 'https://play.google.com/books'
SESSION = Session()
MATCHES = Matches()
HARDCOVER = Hardcover(os.getenv("HARDCOVER_TOKEN"))
