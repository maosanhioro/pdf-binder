@echo off
chcp 65001 > nul
echo ================================
echo PdfBinder EXEファイル作成
echo ================================
echo.

echo 必要なライブラリを確認中...
python -c "import PyPDF2, tkinter; print('✓ 必要なライブラリが揃っています')"

if %ERRORLEVEL% neq 0 (
    echo ❌ 必要なライブラリが不足しています
    echo 以下のコマンドでインストールしてください:
    echo pip install PyPDF2 pyinstaller
    pause
    exit /b 1
)

echo.
echo EXEファイルを作成中...
echo これには数分かかる場合があります...

REM 古いファイルを削除
if exist "dist\PdfBinder.exe" del "dist\PdfBinder.exe"
if exist "build" rmdir /s /q "build"

REM PyInstallerでEXEファイルを作成
python -m PyInstaller --onefile --windowed --name "PdfBinder" --distpath dist --workpath build pdfbinder_gui.py

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✓ EXEファイルの作成が完了しました！
    echo.
    echo 作成されたファイル:
    echo   📁 dist\PdfBinder.exe
    echo.
    echo 💡 配布方法:
    echo   1. dist\PdfBinder.exe を配布先にコピー
    echo   2. ダブルクリックで実行
    echo   3. Pythonのインストールは不要です
    echo.
    echo 📂 distフォルダを開きますか？ ^(Y/N^)
    set /p choice=
    if /i "%choice%"=="Y" explorer dist
) else (
    echo ❌ EXEファイルの作成に失敗しました
    pause
    exit /b 1
)

pause
