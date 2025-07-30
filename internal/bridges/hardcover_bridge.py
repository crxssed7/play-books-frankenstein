import logging

from api.hardcover import HARDCOVER

class HardcoverBridge:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def search(self, query):
        if HARDCOVER.is_logged_in():
            self.logger.info(f"Searching Hardcover for: {query}")
            return HARDCOVER.search(query)
        return []
