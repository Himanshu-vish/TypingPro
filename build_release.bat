@echo off
setlocal
cd /d "%~dp0"
title TypingPro v1.0.0 Build

echo ========================================
echo TypingPro v1.0.0 - Windows EXE Build
echo ========================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python launcher ^(py^) not found.
  echo Install Python 3.11/3.12/3.13 from python.org and enable the Python launcher.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/6] Creating clean virtual environment...
  if exist .venv rmdir /s /q .venv
  py -m venv .venv
  if errorlevel 1 goto :error
) else (
  echo [1/6] Existing virtual environment found.
)

set "PY=.venv\Scripts\python.exe"

echo [2/6] Updating pip...
"%PY%" -m pip install --upgrade pip
if errorlevel 1 goto :error

echo [3/6] Installing all required packages...
"%PY%" -m pip install --upgrade -r requirements.txt
if errorlevel 1 goto :error

echo [4/6] Checking required imports...
"%PY%" -c "import PySide6, reportlab, PIL; from reportlab.platypus import SimpleDocTemplate, Paragraph, Table; print('Dependency check OK - PySide6, ReportLab and Pillow are available.')"
if errorlevel 1 goto :error

echo [5/6] Checking Python source files...
"%PY%" -m compileall -q main.py app
if errorlevel 1 goto :error

echo [6/6] Building standalone TypingPro EXE...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
"%PY%" -m PyInstaller --noconfirm --clean TypingPro.spec
if errorlevel 1 goto :error

if not exist "dist\TypingPro\TypingPro.exe" (
  echo ERROR: Build command finished but TypingPro.exe was not created.
  goto :error
)

echo.
echo ========================================
echo BUILD COMPLETE - SUCCESS
echo ========================================
echo EXE: dist\TypingPro\TypingPro.exe
echo.
echo Open the EXE and test it before building the installer.
pause
exit /b 0

:error
echo.
echo ========================================
echo BUILD FAILED
echo ========================================
echo Read the error shown above. Do not build the installer yet.
pause
exit /b 1
