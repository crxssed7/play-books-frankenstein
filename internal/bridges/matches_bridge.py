import logging
from api.hardcover import HARDCOVER
from constants import SESSION
from internal.matches import Matches

class MatchesBridge:
    def __init__(self):
        self.matches = Matches()
        self.logger = logging.getLogger(__name__)

    def save(self, google_id, book_id):
        hardcover_book = HARDCOVER.get_book(book_id)
        if hardcover_book == None:
            self.logger.info(f"Hardcover book not found for ID: {book_id}")
            return "BOOK_NOT_FOUND"

        self.logger.info(f"Saving match: {google_id} -> {hardcover_book.get('id')}")
        self.matches.save_match(google_id, hardcover_book)
        if not HARDCOVER.is_logged_in():
            return "NOT_LOGGED_IN"

        user_book, user_book_read = HARDCOVER.get_or_create_user_book_read(hardcover_book)
        if user_book_read and user_book:
            SESSION.start(hardcover_book, google_id, user_book_read, user_book["book"]["pages"])
        return "OK"

    def get_match_from_google_id(self, google_id):
        return self.matches.get(google_id)
