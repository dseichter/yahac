# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import copy_metadata

datas = []
datas += copy_metadata('PySide6')
datas += copy_metadata('ha_mqtt_discoverable')
datas += [('README.md', '.'), ('LICENSE', '.')]


a = Analysis(
    ['src/yahac.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', 'matplotlib', 'numpy',
        'PySide6.QtWebEngine', 'PySide6.QtSql', 'PySide6.QtMultimedia',
        'PySide6.QtNetwork', 'PySide6.QtOpenGL', 'PySide6.QtPdf',
        'PySide6.QtPrintSupport', 'PySide6.QtSvg', 'PySide6.QtTest',
        'PySide6.QtXml', 'PySide6.QtConcurrent', 'PySide6.QtDataVisualization'
    ],
    noarchive=False,
    optimize=2,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='yahac',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
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

