# -*- mode: python ; coding: utf-8 -*-
import sys
import os

is_macos = sys.platform == "darwin"
is_windows = sys.platform == "win32"
is_linux = sys.platform.startswith("linux")

# Optional: use this for debugging builds on different platforms
# print(f"Building for: {sys.platform}")

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets/css/*', 'assets/css'),
        ('assets/img/*', 'assets/img'),
        ('assets/js/*', 'assets/js'),
        ('api/queries/*.graphql', 'api/queries'),
    ],
    hiddenimports=[
        'webview',
        'webview.platforms.qt',
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
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=is_macos,  # Required on macOS for drag/drop support
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS uses BUNDLE, others just include the EXE
if is_macos:
    app = BUNDLE(
        exe,
        name='frankenstein.app',
        icon=None,  # optionally add .icns path here
        bundle_identifier='com.yourdomain.frankenstein',
        info_plist=None
    )
    coll_input = [app]
else:
    coll_input = [exe]

coll = COLLECT(
    *coll_input,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='frankenstein'
)
