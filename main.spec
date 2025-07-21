# -*- mode: python ; coding: utf-8 -*-
import sys
import os

IS_MAC = sys.platform == 'darwin'
IS_WIN = sys.platform == 'win32'
IS_LINUX = sys.platform.startswith('linux')

ICON_PATH = None
if IS_MAC:
    ICON_PATH = 'assets/icons/frankenstein.icns'
elif IS_WIN:
    ICON_PATH = 'assets/icons/frankenstein.ico'

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/css/*', 'assets/css'),
        ('assets/img/*', 'assets/img'),
        ('assets/js/*', 'assets/js'),
        ('api/queries/*.graphql', 'api/queries')
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.cocoa',
        'webview.platforms.qt'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["gi", "gtk"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='frankenstein',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=IS_MAC,
    icon=ICON_PATH,
)

if IS_MAC:
    app = BUNDLE(
        exe,
        name='frankenstein.app',
        icon=ICON_PATH,
        bundle_identifier='com.yourdomain.frankenstein'
    )
