#!/bin/bash
# PdfBinder EXEファイル作成スクリプト

echo "=== PdfBinder EXEファイル作成 ==="
echo ""

# 必要なライブラリの確認
echo "必要なライブラリを確認中..."
/home/ono/.pyenv/versions/3.13.3/bin/python -c "import PyPDF2, tkinter; print('✓ 必要なライブラリが揃っています')"

if [ $? -ne 0 ]; then
    echo "❌ 必要なライブラリが不足しています"
    exit 1
fi

echo ""
echo "EXEファイルを作成中..."
echo "これには数分かかる場合があります..."

# PyInstallerでEXEファイルを作成
/home/ono/.pyenv/versions/3.13.3/bin/python -m PyInstaller --onefile --windowed --name "PdfBinder" pdfbinder_gui.py

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ EXEファイルの作成が完了しました！"
    echo ""
    echo "作成されたファイル:"
    echo "  📁 dist/PdfBinder"
    echo ""
    echo "💡 配布方法:"
    echo "  1. dist/PdfBinder を配布先にコピー"
    echo "  2. ダブルクリックで実行"
    echo "  3. Pythonのインストールは不要です"
    echo ""
else
    echo "❌ EXEファイルの作成に失敗しました"
    exit 1
fi
