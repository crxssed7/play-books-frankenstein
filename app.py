import logging
import atexit
import os
import webview
import sys

from assets import load_asset
from constants import DATA_DIR, LOG_FILE, SESSION, START_URL, HARDCOVER
from internal.js_bridge import JSBridge

# TODO: Figure out how to do end-to-end tests
class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
        self.js_bridge = JSBridge()
        self.window = webview.create_window("Frankenstein", START_URL, width=1024, height=768, js_api=self.js_bridge, background_color="#202124")
        self.window.events.loaded += self._on_loaded

    def start(self):
        self._setup_config_dir()
        atexit.register(self._on_exit)
        gui = "qt" if sys.platform == "linux" else None
        webview.start(private_mode=False, gui=gui, storage_path=DATA_DIR)

    def _setup_config_dir(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def _on_loaded(self):
        self._update_hardcover()

        url = self.window.get_current_url()
        if not url:
            self.logger.info("No URL loaded")
            return

        if url.startswith("https://play.google.com/store") or url.startswith("https://myaccount.google.com"):
            self.window.load_url(START_URL)

        disable_links_js = load_asset("js/disable_links.js")
        self.window.evaluate_js(disable_links_js)
        styling_js = load_asset("js/styling.js")
        self.window.evaluate_js(styling_js)

        if url.startswith("https://play.google.com/books/reader"):
            matcher_css = load_asset("css/matcher.css")
            self.window.load_css(matcher_css)
            reader_js = load_asset("js/reader.js")
            matcher_js = load_asset("js/matcher.js")
            self.window.evaluate_js(reader_js)
            self.window.evaluate_js(matcher_js)
        elif url.startswith("https://play.google.com/books"):
            version = load_asset("js/version.js")
            self.window.evaluate_js(version)
            css = load_asset("css/style.css")
            self.window.load_css(css)

    def _update_hardcover(self):
        if SESSION.is_active() and SESSION.current_page > 0 and HARDCOVER.is_logged_in():
            if SESSION.active_hardcover_book: # This should always be true
                self.logger.info(f"Updating Hardcover progress for {SESSION.active_hardcover_book.get('id')}")
            error = HARDCOVER.update_progress(SESSION.active_user_book_read, SESSION.current_page)
            if error:
                self.logger.info(f"Could not update Hardcover progress: {error}")
            SESSION.stop()

    def _on_exit(self):
        self._update_hardcover()
