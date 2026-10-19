@echo off
setlocal
cd /d "%~dp0"
title TypingPro Native Launcher Builder
set "CSC=%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
if not exist "%CSC%" set "CSC=%WINDIR%\Microsoft.NET\Framework\v4.0.30319\csc.exe"
if not exist "%CSC%" (
 echo ERROR: Windows C# compiler csc.exe not found.
 pause
 exit /b 1
)
if not exist "dist" mkdir "dist"
set "ICON_ARG="
if exist "assets\icons\typingpro.ico" set "ICON_ARG=/win32icon:assets\icons\typingpro.ico"
"%CSC%" /nologo /target:winexe /optimize+ /platform:anycpu %ICON_ARG% /reference:System.dll /reference:System.Drawing.dll /reference:System.Windows.Forms.dll /out:"dist\TypingProLauncher.exe" "TypingProLauncher.cs"
if errorlevel 1 (
 echo BUILD FAILED.
 pause
 exit /b 1
)
echo.
echo BUILD SUCCESS: dist\TypingProLauncher.exe
echo First test this launcher before building the installer.
pause
