TypingPro v1.0.0 - ReportLab Build Fix
======================================

This release fixes the startup crash:
    ModuleNotFoundError: No module named 'reportlab'

Changes:
1. reportlab and Pillow are now included in requirements.txt.
2. TypingPro.spec explicitly collects ReportLab modules/data/binaries.
3. build_release.bat uses the project virtual-environment Python for every step.
4. A dependency smoke-test runs BEFORE PyInstaller.
5. A build is reported successful only if dist\TypingPro\TypingPro.exe exists.

Windows build:
1. Extract this ZIP to a normal folder such as Desktop\TypingPro.
2. Do NOT copy any zero-byte python.exe into the project folder.
3. Double-click build_release.bat.
4. Wait for BUILD COMPLETE - SUCCESS.
5. Run dist\TypingPro\TypingPro.exe.
6. Only after the EXE works, run build_installer.bat.
