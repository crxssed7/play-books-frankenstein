class Session:
    def __init__(self):
        self.active_hardcover_book = None
        self.active_google_id = None
        self.active_user_book_read = None
        self.active_user_book_read_id = None
        self.current_page = 0
        self.num_of_pages = 0
        self.percentage = 0

    def start(self, hardcover_book, google_id, user_book_read, num_of_pages):
        print(f"Starting session with Hardcover ID: {hardcover_book.get("id")} and Google ID: {google_id}. Read ID: {user_book_read.get("id")}, pages: {num_of_pages}")
        self.active_hardcover_book = hardcover_book
        self.active_google_id = google_id
        self.active_user_book_read = user_book_read
        self.active_user_book_read_id = user_book_read.get("id")
        self.num_of_pages = num_of_pages
        self._calculate_progress()

    def stop(self):
        self.active_hardcover_book = None
        self.active_google_id = None
        self.active_user_book_read = None
        self.active_user_book_read_id = None
        self.current_page = 0
        self.num_of_pages = 0
        self.percentage = 0

    def set_percentage(self, percentage):
        self.percentage = percentage
        self._calculate_progress()

    def is_active(self):
        return self.active_hardcover_book is not None and self.active_google_id is not None and self.active_user_book_read_id is not None

    def _calculate_progress(self):
        if self.is_active():
            self.current_page = round(self.percentage * self.num_of_pages)
