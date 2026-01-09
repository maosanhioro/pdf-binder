# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pdfbinder_gui.py'],
    pathex=['.'],
    binaries=[],
    # 同梱するドキュメント（配布パッケージで参照できるようにする）
    datas=[('README.md','.'), ('Windows_Setup_Guide.md','.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# PYZ: pure Python modules archive
pyz = PYZ(a.pure)

# EXE: application bundle
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PdfBinder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
