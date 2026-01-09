# 実装ノート — PdfBinder

## 概要
このプロジェクトは当初 `tkinter` ベースの GUI (`pdfbinder_gui.py`) として始まりましたが、機能の拡張とモダンな見た目のため、`PySide6`（Qt for Python）への移行が行われました。

以下はここまでの主要な実装経緯と現在の構成です。

## 移行ハイライト
- Tkinter 実装 (`pdfbinder_gui.py`) は非推奨とし、現在は `PySide6` 実装をメインにしています。
  - 旧ファイルは誤って利用されないようにモジュール読み込み時に例外を投げる形で無効化しています。
- GUI の主要コンポーネントは以下のファイルに分割しています:
  - `app.py` — アプリ起点（`QApplication` と `MainWindow` の起動）
  - `ui_main.py` — メインウィンドウ（左ナビ、中央スタック、右アクションパネル）
  - `ui_merge.py` — 結合（Merge）ページの UI
  - `ui_extract.py` — 抜き取り（Extract）ページの UI
- PDF 操作ロジックは `pdf_ops.py` に集約し、GUI 実装から独立して再利用できるように保有しています。
- 長時間処理は QThread / Worker パターンで非同期に実行する設計になっています。

## ファイルの取扱い（変更・削除）
- 削除・無効化: `pdfbinder_gui.py` は非推奨。直接起動しないでください（`app.py` を使用）。
- 仕様変更: ドキュメント・バッチファイルは PySide6 実装 (`app.py`) を前提に更新済みです。
  - `build_exe_windows.bat` は `app.py` をビルドするように更新しました。
  - `setup_and_run.bat`、`PdfBinder.bat` も `app.py` を実行するように変更しました。

## ビルド / 実行（開発者向け）
- 依存ライブラリ（開発）:
  - `PyPDF2`, `PySide6`, `pyinstaller`
- 開発実行:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install PyPDF2 PySide6 pyinstaller
python app.py
```
- EXE 作成 (Windows, PySide6):
```powershell
python -m PyInstaller --onefile --windowed --name "PdfBinder_PySide6" --distpath dist_ps6 --workpath build_ps6 app.py
```

## 今後の作業候補
- `pdfbinder_gui.py` を完全削除（git 履歴に残すためアーカイブ付きで削除）するか検討。
- ドキュメントの更なる整備（画面遷移図、主要クラスの責務、API 仕様）
- PyInstaller ビルドの CI 自動化

## 連絡先
- 実装について不明点があれば指示ください。具体的な差し戻しや追加調整を行います。
