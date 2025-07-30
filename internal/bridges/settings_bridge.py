from internal.settings import SETTINGS

class SettingsBridge:
    def get_settings(self):
        return SETTINGS.get_settings()

    def save(self, token):
        SETTINGS.save_settings(token)
