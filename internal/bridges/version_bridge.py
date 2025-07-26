import webbrowser

from packaging.version import Version

from api.github import Github
from constants import APP_VERSION

class VersionBridge:
    def __init__(self):
        self.version_checked = False

    def check_for_update(self):
        if self.version_checked:
            return {"new_version_available": False, "new_version": APP_VERSION, "current_version": APP_VERSION}

        version = Github().get_latest_release()
        if not version:
            return {"new_version_available": False, "new_version": APP_VERSION, "current_version": APP_VERSION}

        current_version = Version(APP_VERSION)
        new_version = Version(version)
        self.version_checked = True
        return {"new_version_available": current_version < new_version, "new_version": version, "current_version": APP_VERSION}

    def open_release_page(self):
        webbrowser.open("https://github.com/crxssed7/play-books-frankenstein/releases/latest")
        return "OK"
