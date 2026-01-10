@echo off
chcp 65001 > nul
echo ================================
echo PdfBinder セットアップ
echo ================================
echo.

echo Pythonがインストールされているか確認中...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Pythonがインストールされていません
    echo.
    echo Pythonをインストールしてください:
    echo 1. https://www.python.org/downloads/ にアクセス
    echo 2. 最新版をダウンロードしてインストール
    echo 3. インストール時に「Add Python to PATH」にチェック
    echo.
    pause
    exit /b 1
)

echo ✓ Pythonが見つかりました
python --version

echo.
echo 必要なライブラリをインストール中...
pip install PyPDF2 PySide6 >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✓ ライブラリのインストール完了
) else (
    echo ❌ ライブラリのインストールに失敗しました
    pause
    exit /b 1
)

echo.
echo ✓ セットアップ完了！
echo.
echo PdfBinderを起動しますか？ (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    python pdfbinder_app.py
)

pause
