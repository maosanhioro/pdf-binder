# PdfBinder

## 概要
PdfBinder は、PDF の結合とページ抜き取りを、迷わず操作できる GUI で提供するツールです。
配布先では Python の導入が不要なため、非技術者の利用にも適しています。

## できること
- PDF結合: 複数ファイルを1つにまとめる
- ページ抜き取り: 指定ページだけを新しいPDFとして保存する
- 出力先・出力名の指定
- 既存ファイルへの上書き確認

## 使い方（配布版）
1. `dist/PdfBinder.exe` を起動します。
2. 左側のタブで「まとめる」「抜き出し」を選びます。
3. 画面の指示に従ってファイルと出力先を指定します。
4. 「実行」を押すと処理が開始されます。

## 使い方（開発版）
```powershell
# 仮想環境の作成（任意）
python -m venv .venv
.\.venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 起動
python pdfbinder.py
```

## 操作ガイド

### PDF結合（まとめる）
1. 「PDFを追加」から結合したいPDFを選びます（複数選択可）。
2. 右側の「出力先」と「出力名」を設定します。
3. 「実行」を押すと1つのPDFが作成されます。

### ページ抜き取り（抜き出し）
1. 「PDFを選択」から対象のPDFを選びます。
2. 「ページ」に抜き取りたいページ番号を入力します。
   - 例: `1,3,5`
   - 例: `1-5,8,10-12`
3. 必要なら「パスワード」を入力します（暗号化PDFのみ）。
4. 出力先と出力名を指定して「実行」を押します。

## 出力名のルール
- `.pdf` が付いていない場合、自動で付与されます。
- 同名のファイルがある場合は上書き確認が表示されます。

## トラブルシューティング

### EXEが起動できない
- Windows Defender がブロックしていないか確認してください。
  - 「詳細情報」→「実行」で許可できます。

### 文字が化ける
- Windows 11 は自動対応済みです。
- Windows 10 以前では言語設定やフォント設定を確認してください。

### ページ指定エラー
- ページ番号が範囲内か確認してください。
- 入力形式が正しいか確認してください（例: `1,3-5,7`）。

## ビルド（開発者向け）
```powershell
pyinstaller --onefile --windowed --name "PdfBinder" --distpath dist --workpath build pdfbinder.py
```

## フォルダ構成
```
project/
├── pdfbinder.py
├── main_window.py
├── merge_page.py
├── extract_page.py
├── pdf_operations.py
├── requirements.txt
├── build_exe.bat
├── README.md
├── SETUP.md
└── dist/
  └── PdfBinder.exe
```

## 動作環境
- Windows 11 / Windows 10
- Python 3.8 以降（開発時のみ）
