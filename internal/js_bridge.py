from internal.bridges.asset_bridge import AssetBridge
from internal.bridges.hardcover_bridge import HardcoverBridge
from internal.bridges.matches_bridge import MatchesBridge
from internal.bridges.session_bridge import SessionBridge
from internal.bridges.settings_bridge import SettingsBridge
from internal.bridges.version_bridge import VersionBridge

# TODO: Add tests
class JSBridge:
    def __init__(self):
        self.assets = AssetBridge()
        self.version = VersionBridge()
        self.matches = MatchesBridge()
        self.hardcover = HardcoverBridge()
        self.session = SessionBridge()
        self.settings = SettingsBridge()
