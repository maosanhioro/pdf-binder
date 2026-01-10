@echo off
chcp 65001 > nul
echo ====================================
echo PdfBinder - EXE build (Windows only)
echo ====================================
echo.
echo Checking required libraries...
python -c "import PyPDF2, PySide6; print('OK')"
if %ERRORLEVEL% neq 0 (
    echo Required libraries missing.
    echo Run: pip install PyPDF2 pyinstaller
    pause
    exit /b 1
)

echo Building EXE (this may take a few minutes)...

if exist "dist_ps6\\PdfBinder_PySide6.exe" del "dist_ps6\\PdfBinder_PySide6.exe"
if exist "build_ps6" rmdir /s /q "build_ps6"

python -m PyInstaller --onefile --windowed --name "PdfBinder_PySide6" --distpath dist_ps6 --workpath build_ps6 pdfbinder_app.py

if %ERRORLEVEL% equ 0 (
    echo Build completed: dist_ps6\\PdfBinder_PySide6.exe
    echo Open dist folder? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer dist_ps6
) else (
    echo Build failed.
    pause
    exit /b 1
)

pause
