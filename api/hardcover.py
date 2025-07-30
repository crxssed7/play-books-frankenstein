import datetime
import requests

from assets import resource_path
from internal.settings import SETTINGS

class Hardcover:
    def __init__(self, token: str | None):
        self._token = token
        self._headers = {"Authorization": f"Bearer {self._token}"}

    def is_logged_in(self) -> bool:
        return self._token is not None and str(self._token).strip() != ""

    def search(self, text):
        body = self._build_body("Search", {"query": text})
        result = self._send_request(body)
        if result.status_code < 300:
            _json = result.json()
            items = _json["data"]["search"]["results"]["hits"]
            hardcover_items = []
            for item in items:
                document = item["document"]
                i = {
                    "image": document["image"],
                    "id": document["id"],
                    "title": f"{document['title']} ({document.get('release_year', '')})".replace("()", ""),
                    "author": ", ".join(document["author_names"])
                }
                hardcover_items.append(i)
            return hardcover_items
        return []

    def get_book(self, book_id):
        body = self._build_body("Book", {"id": int(book_id)})
        result = self._send_request(body)
        if result.status_code < 300:
            json = result.json()
            if len(json["data"]["books"]) > 0:
                return json["data"]["books"][0]
        return None

    def get_or_create_user_book_read(self, book):
        user_book = self.get_user_book(book.get("id"))
        if user_book:
            if len(user_book["user_book_reads"]) > 0:
                user_book_read = user_book["user_book_reads"][0]
                return user_book, user_book_read
            else:
                return user_book, self.create_user_book_read(book, user_book)
        else:
            user_book = self.create_user_book(book.get("id"))
            if user_book:
                return user_book, user_book["user_book_reads"][0]
            else:
                return None, None

    def get_user_book(self, book_id):
        body = self._build_body("UserBook", {"id": book_id})
        result = self._send_request(body)
        if result.status_code < 300:
            json = result.json()
            user_books = json["data"]["me"][0]["user_books"]
            if len(user_books) == 0:
                return None
            return user_books[0]
        return None

    def create_user_book(self, book_id):
        body = self._build_body("CreateUserBook", {"book_id": int(book_id), "first_started_reading_date": datetime.date.today().strftime('%Y-%m-%d')})
        result = self._send_request(body)
        if result.status_code < 300:
            json = result.json()
            user_book = json["data"]["insert_user_book"]["user_book"]
            return user_book

    def create_user_book_read(self, book, user_book):
        edition = book["editions"][0]["id"]
        body = self._build_body("CreateUserBookRead", {"user_book_id": int(user_book["id"]), "started_at": datetime.date.today().strftime('%Y-%m-%d'), "edition_id": edition})
        result = self._send_request(body)
        if result.status_code < 300:
            json = result.json()
            user_book_read = json["data"]["insert_user_book_read"]["user_book_read"]
            return user_book_read
        return None

    def update_progress(self, user_book_read, progress_pages):
        variables = {
            "id": int(user_book_read.get("id")),
            "progress_pages": int(progress_pages),
            "started_at": user_book_read.get("started_at"),
            "finished_at": user_book_read.get("finished_at"),
            "edition_id": user_book_read.get("edition_id")
        }
        body = self._build_body("UpdateUserBookRead", variables)
        result = self._send_request(body)
        if result.status_code < 300:
            json = result.json()
            return json["data"]["update_user_book_read"]["error"]
        return None

    def _build_body(self, query_name, variables):
        query = self._load_query(query_name)
        return {"query": query, "variables": variables}

    def _send_request(self, body):
        return requests.post(
            "https://api.hardcover.app/v1/graphql",
            json=body,
            headers=self._headers
        )

    def _load_query(self, query):
        asset_path = resource_path(f"api/queries/{query}.graphql")
        with open(asset_path, 'r') as file:
            return file.read()

HARDCOVER = Hardcover(SETTINGS.hardcover_token)
