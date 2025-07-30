import logging
import atexit
import os
import webview
import sys
import threading

from api.hardcover import HARDCOVER
from assets import load_asset
from constants import DATA_DIR, LOG_FILE, SESSION, START_URL
from internal.js_bridge import JSBridge
from internal.settings import SETTINGS

# TODO: Figure out how to do end-to-end tests
class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
        self.js_bridge = JSBridge()
        self.window = webview.create_window(
            "Frankenstein",
            START_URL,
            width=1024,
            height=768,
            js_api=self.js_bridge,
            background_color="#202124",
            hidden=True
        )
        self.window.events.loaded += self._on_loaded
        self.critical_js = [
            "js/disable_links.js",
            "js/theming.js"
        ]

    def start(self):
        self._setup_config_dir()
        atexit.register(self._on_exit)
        gui = "qt" if sys.platform == "linux" else None
        webview.start(private_mode=False, gui=gui, storage_path=DATA_DIR)

    def _setup_config_dir(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def _on_loaded(self):
        threading.Thread(target=self._update_hardcover).start()

        css = load_asset("css/style.css")
        self.window.load_css(css)

        url = self.window.get_current_url()
        if not url:
            self.logger.info("No URL loaded")
            return

        if url.startswith("https://play.google.com/store") or url.startswith("https://myaccount.google.com"):
            self.window.load_url(START_URL)

        self._evaluate_critical_js()
        if self.window.hidden:
            self.window.show()

        if url.startswith("https://play.google.com/books/reader"):
            self._run_js("js/reader.js")
            self._run_js("js/matcher.js")
        elif url.startswith("https://play.google.com/books"):
            self._run_js("js/components/app_icon.js")
            self._run_js("js/components/settings.js")
            self._run_js("js/components/theme_toggler.js")
            self._run_js("js/version.js")

    def _evaluate_critical_js(self):
        for asset in self.critical_js:
            js = load_asset(asset)
            self.window.evaluate_js(js)

    def _run_js(self, asset):
        js = load_asset(asset)
        self.window.run_js(js)

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
        SETTINGS.save_settings()
