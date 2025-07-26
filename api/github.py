import requests

class Github:
    def __init__(self):
        self._owner = "crxssed7"
        self._repo = "play-books-frankenstein"
        self._api_url = 'https://api.github.com'
        self._headers = {'Accept': 'application/vnd.github+json'}

    def get_latest_release(self):
        response = requests.get(f"{self._api_url}/repos/{self._owner}/{self._repo}/releases/latest", headers=self._headers)
        if not response.ok:
            return None

        data = response.json()
        return data.get("tag_name")
