@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: .venv not found.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm TypingProLauncher.spec
if errorlevel 1 (
  echo Launcher build failed.
  pause
  exit /b 1
)
echo.
echo Launcher ready: dist\TypingProLauncher.exe
echo Copy TypingProLauncher.exe beside dist\TypingPro\TypingPro.exe for final packaging.
pause
