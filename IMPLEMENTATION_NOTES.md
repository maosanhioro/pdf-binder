# 実装ノート — PdfBinder

## 概要
このプロジェクトは当初 `tkinter` ベースの GUI（旧 `pdfbinder_gui.py`）として始まりましたが、機能の拡張とモダンな見た目のため、`PySide6`（Qt for Python）への移行が行われました。

以下はここまでの主要な実装経緯と現在の構成です。

## 移行ハイライト
- Tkinter 実装は削除済みで、現在は `PySide6` 実装をメインにしています。
- GUI の主要コンポーネントは以下のファイルに分割しています:
  - `pdfbinder.py` — アプリ起点（`QApplication` と `MainWindow` の起動）
  - `main_window.py` — メインウィンドウ（左ナビ、中央スタック、右アクションパネル）
  - `merge_page.py` — 結合（Merge）ページの UI
  - `extract_page.py` — 抜き取り（Extract）ページの UI
- PDF 操作ロジックは `pdf_operations.py` に集約し、GUI 実装から独立して再利用できるように保有しています。
- 長時間処理は QThread / Worker パターンで非同期に実行する設計になっています。

## ファイルの取扱い（変更・削除）
- 削除済み: `pdfbinder_gui.py` は廃止。`pdfbinder.py` を使用してください。
- 仕様変更: ドキュメント・バッチファイルは PySide6 実装 (`pdfbinder.py`) を前提に更新済みです。
  - `build_exe.bat` は `pdfbinder.py` をビルドするように更新しました。
  - `setup.bat`、`run.bat` も `pdfbinder.py` を実行するように変更しました。

## ビルド / 実行（開発者向け）
- 依存ライブラリ（開発）:
  - `PyPDF2`, `PySide6`, `pyinstaller`
- 開発実行:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install PyPDF2 PySide6 pyinstaller
python pdfbinder.py
```
- EXE 作成 (Windows, PySide6):
```powershell
python -m PyInstaller --onefile --windowed --name "PdfBinder" --distpath dist --workpath build pdfbinder.py
```

## 今後の作業候補
- 旧Tkinter実装は削除済み（履歴はGitに残ります）。
- ドキュメントの更なる整備（画面遷移図、主要クラスの責務、API 仕様）
- PyInstaller ビルドの CI 自動化

## 連絡先
- 実装について不明点があれば指示ください。具体的な差し戻しや追加調整を行います。
