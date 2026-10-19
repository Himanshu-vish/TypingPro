# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all, collect_submodules


# =========================================================
# PySide6
# =========================================================

hiddenimports = collect_submodules("PySide6")


# =========================================================
# ReportLab
# =========================================================

reportlab_datas, reportlab_binaries, reportlab_hiddenimports = collect_all(
    "reportlab"
)

hiddenimports += reportlab_hiddenimports


# =========================================================
# Analysis
# =========================================================

a = Analysis(
    ["main.py"],

    pathex=[],

    binaries=reportlab_binaries,

    datas=[
        ("assets/paragraphs", "assets/paragraphs"),
        ("assets/icons", "assets/icons"),
    ] + reportlab_datas,

    hiddenimports=hiddenimports,

    hookspath=[],

    hooksconfig={},

    runtime_hooks=[],

    excludes=[],

    noarchive=False,

    optimize=0,
)


# =========================================================
# PYZ
# =========================================================

pyz = PYZ(a.pure)


# =========================================================
# EXE
# =========================================================

exe = EXE(
    pyz,
    a.scripts,
    [],

    exclude_binaries=True,

    name="TypingPro",

    debug=False,

    bootloader_ignore_signals=False,

    strip=False,

    upx=True,

    console=False,

    icon="assets/icons/typingpro.ico",
)


# =========================================================
# COLLECT
# =========================================================

coll = COLLECT(
    exe,

    a.binaries,
    a.datas,

    strip=False,

    upx=True,

    upx_exclude=[],

    name="TypingPro",
)