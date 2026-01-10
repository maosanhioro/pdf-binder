@echo off
chcp 65001 > nul
echo ====================================
echo PdfBinder - EXE build
echo ====================================
echo.
echo Checking required libraries...
python -c "import PyPDF2, PySide6; print('OK')"
if %ERRORLEVEL% neq 0 (
    echo Required libraries missing.
echo Run: pip install PyPDF2 PySide6 pyinstaller
    pause
    exit /b 1
)

echo Building EXE (this may take a few minutes)...

if exist "dist\\PdfBinder.exe" del "dist\\PdfBinder.exe"
if exist "build" rmdir /s /q "build"

python -m PyInstaller --onefile --windowed --name "PdfBinder" --distpath dist --workpath build pdfbinder.py

if %ERRORLEVEL% equ 0 (
    echo Build completed: dist\\PdfBinder.exe
    echo Open dist folder? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer dist
) else (
    echo Build failed.
    pause
    exit /b 1
)

pause
