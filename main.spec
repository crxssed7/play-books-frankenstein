# -*- mode: python ; coding: utf-8 -*-

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
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# MacOS Test:
app = BUNDLE(
    exe,
    name='frankenstein.app',
    icon=None,
    bundle_identifier='com.crxssed.frankenstein'
)

coll = COLLECT(
    app,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='frankenstein'
)
