# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['core\\services\\pipeline.py'],
    pathex=[],
    binaries=[],
    datas=[('../ai', 'ai'), ('../core', 'core')],
    hiddenimports=['engines.stride_engine', 'engines.mitre_engine', 'engines.correlation_engine', 'engines.scoring_engine', 'engines.graph_engine'],
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
    name='DefendX_SOC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
