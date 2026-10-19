@echo off
setlocal
cd /d "%~dp0"
title TypingPro Installer Builder

echo ================================================
echo        TypingPro Installer Builder
echo ================================================
echo.

set "ISCC="

REM ---- Inno Setup: Only Me installation ----
if exist "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
if exist "%LOCALAPPDATA%\Inno Setup 6\ISCC.exe" set "ISCC=%LOCALAPPDATA%\Inno Setup 6\ISCC.exe"

REM ---- Inno Setup: All Users installation ----
if not defined ISCC if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "C:\Program Files\Inno Setup 6\ISCC.exe" set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"

if not defined ISCC goto :NO_INNO

echo Inno Setup found:
echo "%ISCC%"
echo.

if not exist "dist\TypingPro\TypingPro.exe" goto :NO_MAIN
echo Main TypingPro EXE: OK

if not exist "dist\TypingProLauncher.exe" goto :NO_LAUNCHER
echo Native Launcher: OK

if not exist "installer\TypingPro.iss" goto :NO_ISS
echo Installer Script: OK
echo.

echo Building final TypingPro installer...
echo.

"%ISCC%" "installer\TypingPro.iss"

if errorlevel 1 goto :BUILD_ERROR

echo.
echo ================================================
echo              BUILD SUCCESS
echo ================================================
echo.
echo Final installer:
echo installer\output\TypingPro_Setup_v1.0.0.exe
echo.
pause
exit /b 0

:NO_INNO
echo.
echo ERROR: Inno Setup 6 ISCC.exe not found.
echo.
echo Expected Only Me location:
echo "%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"
echo.
pause
exit /b 1

:NO_MAIN
echo.
echo ERROR: dist\TypingPro\TypingPro.exe not found.
pause
exit /b 1

:NO_LAUNCHER
echo.
echo ERROR: dist\TypingProLauncher.exe not found.
pause
exit /b 1

:NO_ISS
echo.
echo ERROR: installer\TypingPro.iss not found.
pause
exit /b 1

:BUILD_ERROR
echo.
echo ================================================
echo          INSTALLER BUILD FAILED
echo ================================================
echo.
pause
exit /b 1