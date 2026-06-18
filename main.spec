# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=["."],
    binaries=[],
    datas=[('assets', 'assets'), ('data', 'data')],
    hiddenimports=[
        'PIL._tkinter_finder',
        'PIL.Image',
        'PIL.ImageTk'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='EvoDeckBuilder',  # Name des Executables (wichtig für das Bundle)
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Wichtig für GUI-Apps!
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# --- macOS-.app-Bundle
app = BUNDLE(
    exe,
    name='EvoDeckBuilder.app',  # Name des .app-Bundles
    icon=None,  # Optional: Pfad zu einer .icns-Datei (z. B. 'icon.icns')
    bundle_identifier='com.yourname.evodeckbuilder',  # Eindeutige ID für macOS
)
