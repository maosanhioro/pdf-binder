@echo off
chcp 65001 > nul
title PdfBinder

REM 現在のディレクトリをスクリプトの場所に設定
cd /d "%~dp0"

echo ================================
echo      PdfBinder 起動中...
echo ================================
echo.

set PYTHON_EXE=python
if exist ".venv\Scripts\python.exe" set PYTHON_EXE=.venv\Scripts\python.exe

REM Pythonの確認
%PYTHON_EXE% --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ! エラー: Pythonがインストールされていません
    echo.
    echo 解決方法:
    echo 1. setup.bat を実行してセットアップ
    echo 2. または https://www.python.org からPythonをインストール
    echo.
    pause
    exit /b 1
)

REM PyPDF2 / PySide6の確認
%PYTHON_EXE% -c "import PyPDF2, PySide6" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ! エラー: 必要なライブラリがインストールされていません
    echo.
    echo 自動インストールを実行しますか？ (Y/N)
    set /p install_choice=
    if /i "%install_choice%"=="Y" (
        echo ライブラリをインストール中...
        %PYTHON_EXE% -m pip install -r requirements.txt
        if %ERRORLEVEL% neq 0 (
            echo ! インストールに失敗しました
            pause
            exit /b 1
        )
        echo ! インストール完了
    ) else (
        echo セットアップがキャンセルされました
        pause
        exit /b 1
    )
)

REM GUIアプリケーションを起動
echo ! PdfBinder を起動しています...
%PYTHON_EXE% pdfbinder.py

REM エラーが発生した場合の処理
if %ERRORLEVEL% neq 0 (
    echo.
    echo ! エラーが発生しました
    echo 詳細なエラー情報を確認するため、以下のコマンドを実行してください:
    echo %PYTHON_EXE% pdfbinder.py
    echo.
    pause
)

echo.
echo PdfBinderを終了しました
pause
