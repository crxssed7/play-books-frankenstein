import webview

from assets import load_asset
from constants import SESSION, START_URL, HARDCOVER
from internal.js_bridge import JSBridge

class App:
    def __init__(self):
        self.js_bridge = JSBridge()
        self.window = webview.create_window("Frankenstein", START_URL, width=1024, height=768, js_api=self.js_bridge, background_color="#202124")
        self.window.events.loaded += self._on_loaded

    def start(self):
        webview.start(private_mode=False)

    def _on_loaded(self):
        if SESSION.is_active() and SESSION.current_page > 0 and HARDCOVER.is_logged_in():
            print(f"Updating Hardcover progress for {SESSION.active_hardcover_id}")
            error = HARDCOVER.update_progress(SESSION.active_user_book_read_id, SESSION.current_page)
            if error:
                print(f"Could not update Hardcover progress: {error}")
            SESSION.stop()

        url = self.window.get_current_url()
        if not url:
            print("No URL loaded")
            return

        if url.startswith("https://play.google.com/store"):
            self.window.load_url(START_URL)

        disable_links_js = load_asset("js/disable_links.js")
        self.window.evaluate_js(disable_links_js)

        if url.startswith("https://play.google.com/books/reader"):
            matcher_css = load_asset("css/matcher.css")
            self.window.load_css(matcher_css)
            reader_js = load_asset("js/reader.js")
            matcher_js = load_asset("js/matcher.js")
            self.window.evaluate_js(reader_js)
            self.window.evaluate_js(matcher_js)
        elif url.startswith("https://play.google.com/books"):
            css = load_asset("css/style.css")
            self.window.load_css(css)
            styling_js = load_asset("js/styling.js")
            self.window.evaluate_js(styling_js)
