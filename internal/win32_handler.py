import os
import ctypes
import ctypes.wintypes as wt
import re
import time
from threading import Thread

# Load user32.dll
user32 = ctypes.windll.user32 # pyright:ignore

# Define Window enumeration callback type
EnumWindowsProc = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM) # pyright:ignore

# Buffer for window titles
GetWindowTextW = user32.GetWindowTextW
GetWindowTextW.argtypes = [wt.HWND, wt.LPWSTR, wt.INT]
GetWindowTextW.restype = wt.INT

GetWindowTextLengthW = user32.GetWindowTextLengthW
GetWindowTextLengthW.argtypes = [wt.HWND]
GetWindowTextLengthW.restype = wt.INT

EnumWindows = user32.EnumWindows
EnumWindows.argtypes = [EnumWindowsProc, wt.LPARAM]
EnumWindows.restype = wt.BOOL

class Win32Handler:
    """Used for setting app icon on Windows. Do not invoke this on Mac or Linux."""
    def __init__(self):
        self._handle = None

    @property
    def handle(self):
        return self._handle

    def set_window_icon(self, icon_path: str, window_name: str, tries: int = 10):
        def _set_window_icon(icon_path: str, window_name: str, tries: int):
            for _ in range(tries):
                handle = self.find_window_wildcard(window_name).handle
                if handle is not None:
                    self._set_icon(icon_path=icon_path, hWnd=handle)
                    break
                time.sleep(1)

        Thread(
            target=_set_window_icon, args=[icon_path, window_name, tries], daemon=True
        ).start()

    def find_window_wildcard(self, wildcard: str):
        """Find a window whose title matches the wildcard regex."""
        self._handle = None
        cb = EnumWindowsProc(self._window_enum_callback)
        EnumWindows(cb, wildcard.encode())
        return self

    def _window_enum_callback(self, hwnd, lParam):
        length = GetWindowTextLengthW(hwnd)
        if not length:
            return True
        buffer = ctypes.create_unicode_buffer(length + 1)
        GetWindowTextW(hwnd, buffer, length + 1)
        title = buffer.value
        if re.match(lParam.decode(), title):
            self._handle = hwnd
            return False  # stop enumeration
        return True  # continue

    def _set_icon(self, icon_path: str, hWnd=None):
        # from https://github.com/zauberzeug/nicegui/issues/620#issuecomment-1483818006
        assert os.path.exists(icon_path), f"Invalid icon file path supplied: {icon_path}"

        # Load the necessary Windows API functions using ctypes
        user32 = ctypes.windll.user32 # pyright:ignore

        # Get the handle of the current process and the current window
        # Ideally replace this to directly reference the created webview window
        if hWnd is None:
            hWnd = user32.GetForegroundWindow()

        # Constants for Win32 API calls
        ICON_SMALL = 0
        ICON_BIG = 1
        WM_SETICON = 0x0080

        # Load the icon file
        hIcon = user32.LoadImageW(None, icon_path, 1, 0, 0, 0x00000010)

        # Set the window icon using WM_SETICON message
        ctypes.windll.user32.SendMessageW(hWnd, WM_SETICON, ICON_SMALL, hIcon) # pyright:ignore
        ctypes.windll.user32.SendMessageW(hWnd, WM_SETICON, ICON_BIG, hIcon) # pyright:ignore
