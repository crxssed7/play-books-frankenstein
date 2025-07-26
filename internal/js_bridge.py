import json

from constants import SESSION, HARDCOVER
from internal.bridges.asset_bridge import AssetBridge
from internal.bridges.hardcover_bridge import HardcoverBridge
from internal.bridges.matches_bridge import MatchesBridge
from internal.bridges.version_bridge import VersionBridge

# TODO: Add tests
class JSBridge:
    def __init__(self):
        self.assets = AssetBridge()
        self.version = VersionBridge()
        self.matches = MatchesBridge()
        self.hardcover = HardcoverBridge()

    def update_progress_percentage(self, data):
        array_data = json.loads(data["body"])
        SESSION.set_percentage(array_data[-1][-1][-1])
        return "OK"

    def set_current_book(self, hardcover_id, google_id):
        if not HARDCOVER.is_logged_in():
            return "NOT_LOGGED_IN"

        user_book, user_book_read = HARDCOVER.get_or_create_user_book_read(hardcover_id)
        if user_book_read and user_book:
            SESSION.start(hardcover_id, google_id, user_book_read, user_book["book"]["pages"])
        return "OK"
