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

# Set exclude_binaries=True here to avoid duplication in BUNDLE step
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
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

app = BUNDLE(
    exe,
    name='frankenstein.app',
    icon=None,  # Or path to .icns file
    bundle_identifier='com.yourdomain.frankenstein',
    info_plist=None
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
