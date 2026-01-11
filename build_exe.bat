@echo off
setlocal
chcp 65001 > nul

echo ====================================
echo PdfBinder - EXE build
echo ====================================
echo.

set PYTHON_EXE=python
if exist ".venv\Scripts\python.exe" set PYTHON_EXE=.venv\Scripts\python.exe

echo Checking required libraries...
%PYTHON_EXE% -c "import PyPDF2, PySide6; print('OK')"
if %ERRORLEVEL% neq 0 (
    echo Required libraries missing.
    echo Run: pip install PyPDF2 PySide6 pyinstaller
    pause
    exit /b 1
)

echo Building EXE (this may take a few minutes)...

if exist "dist\PdfBinder.exe" del "dist\PdfBinder.exe"
if exist "build" rmdir /s /q "build"

%PYTHON_EXE% -m PyInstaller --onefile --windowed --name "PdfBinder" --distpath dist --workpath build --icon "assets\pdfbinder.ico" pdfbinder.py

if %ERRORLEVEL% equ 0 (
    echo Build completed: dist\PdfBinder.exe
    if /i "%OPEN_DIST%"=="1" explorer dist
    exit /b 0
)

echo Build failed.
exit /b 1
