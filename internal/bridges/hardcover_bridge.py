from constants import HARDCOVER

class HardcoverBridge:
    def search(self, query):
        if HARDCOVER.is_logged_in():
            print(f"Searching Hardcover for: {query}")
            return HARDCOVER.search(query)
        return []
