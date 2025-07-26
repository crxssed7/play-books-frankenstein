import json
import webbrowser

from packaging.version import Version

from api.github import Github
from assets import image_base64
from constants import APP_VERSION, SESSION, HARDCOVER
from internal.bridges.asset_bridge import AssetBridge
from internal.bridges.version_bridge import VersionBridge
from internal.matches import MATCHES

# TODO: Add tests
class JSBridge:
    def __init__(self):
        self.assets = AssetBridge()
        self.version = VersionBridge()

    def update_progress_percentage(self, data):
        array_data = json.loads(data["body"])
        SESSION.set_percentage(array_data[-1][-1][-1])
        return "OK"

    def search_hardcover(self, query):
        if HARDCOVER.is_logged_in():
            print(f"Searching Hardcover for: {query}")
            return HARDCOVER.search(query)
        return []

    def save_match(self, google_id, book_id):
        hardcover_book = HARDCOVER.get_book(book_id)
        if hardcover_book == None:
            print(f"Hardcover book not found for ID: {book_id}")
            return "BOOK_NOT_FOUND"

        print(f"Saving match: {google_id} -> {hardcover_book.get('id')}")
        MATCHES.save_match(google_id, hardcover_book)
        if not HARDCOVER.is_logged_in():
            return "NOT_LOGGED_IN"

        user_book, user_book_read = HARDCOVER.get_or_create_user_book_read(hardcover_book)
        if user_book_read and user_book:
            SESSION.start(hardcover_book, google_id, user_book_read, user_book["book"]["pages"])
        return "OK"

    def get_match_from_google_id(self, google_id):
        return MATCHES.get(google_id)

    def set_current_book(self, hardcover_id, google_id):
        if not HARDCOVER.is_logged_in():
            return "NOT_LOGGED_IN"

        user_book, user_book_read = HARDCOVER.get_or_create_user_book_read(hardcover_id)
        if user_book_read and user_book:
            SESSION.start(hardcover_id, google_id, user_book_read, user_book["book"]["pages"])
        return "OK"
