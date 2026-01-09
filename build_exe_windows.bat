@echo off
chcp 65001 > nul
echo ================================
echo PdfBinder EXEファイル作成
echo ================================
echo.
echo 必要なライブラリを確認中...
python -c "import PyPDF2, PySide6; print('✓ 必要なライブラリが揃っています')"

if %ERRORLEVEL% neq 0 (
    echo 必要なライブラリが不足しています
    echo 以下のコマンドでインストールしてください:
    echo pip install PyPDF2 pyinstaller
    pause
    exit /b 1
@echo off
chcp 65001 >nul
echo ====================================
echo PdfBinder - EXE build (Windows only)
echo ====================================

echo Checking required libraries...
python -c "import PyPDF2, PySide6; print('OK')"
if %ERRORLEVEL% neq 0 (
    echo Required libraries missing.
    echo Run: pip install PyPDF2 pyinstaller
    pause
    exit /b 1
)

echo Building EXE (this may take a few minutes)...

if exist "dist\PdfBinder.exe" del "dist\PdfBinder.exe"
if exist "build" rmdir /s /q "build"

python -m PyInstaller --onefile --windowed --name "PdfBinder_PySide6" --distpath dist_ps6 --workpath build_ps6 app.py

if %ERRORLEVEL% equ 0 (
    echo Build completed: dist\PdfBinder.exe
    echo Open dist folder? (Y/N)
    set /p choice=
    if /i "%choice%"=="Y" explorer dist
) else (
    echo Build failed.
    pause
    exit /b 1
)

pause

