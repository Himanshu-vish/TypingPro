@echo off
setlocal
cd /d "%~dp0"
if not exist "%LOCALAPPDATA%\TypingPro" mkdir "%LOCALAPPDATA%\TypingPro"
if exist "data\typing_reports.json" (
  if not exist "%LOCALAPPDATA%\TypingPro\typing_reports.json" copy /Y "data\typing_reports.json" "%LOCALAPPDATA%\TypingPro\typing_reports.json" >nul
)
echo Current reports copied only if no LocalAppData report file already existed.
echo Data folder: %LOCALAPPDATA%\TypingPro
pause
