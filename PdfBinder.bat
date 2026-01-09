@echo off
chcp 65001 > nul
title PdfBinder

REM 現在のディレクトリをスクリプトの場所に設定
cd /d "%~dp0"

echo ================================
echo      PdfBinder 起動中...
echo ================================
echo.

REM Pythonの確認
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ エラー: Pythonがインストールされていません
    echo.
    echo 解決方法:
    echo 1. setup_and_run.bat を実行してセットアップ
    echo 2. または https://www.python.org からPythonをインストール
    echo.
    pause
    exit /b 1
)

REM PyPDF2の確認
python -c "import PyPDF2" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ エラー: PyPDF2ライブラリがインストールされていません
    echo.
    echo 自動インストールを実行しますか？ (Y/N)
    set /p install_choice=
    if /i "%install_choice%"=="Y" (
        echo PyPDF2をインストール中...
        pip install PyPDF2
        if %ERRORLEVEL% neq 0 (
            echo ❌ インストールに失敗しました
            pause
            exit /b 1
        )
        echo ✓ インストール完了
    ) else (
        echo セットアップがキャンセルされました
        pause
        exit /b 1
    )
)

REM GUIアプリケーションを起動 (PySide6 実装)
echo ✓ PdfBinder (PySide6) を起動しています...
python app.py

REM エラーが発生した場合の処理
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ エラーが発生しました
    echo 詳細なエラー情報を確認するため、以下のコマンドを実行してください:
    echo python app.py
    echo.
    pause
)

echo.
echo PdfBinderを終了しました
pause
