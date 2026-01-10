# Windows環境でのPdfBinder セットアップ手順

## 前提条件
- Windows 11 (または Windows 10)
- インターネット接続

## 1. Pythonのインストール
1. https://www.python.org/downloads/ からPython 3.8以降をダウンロード
2. インストール時に「Add Python to PATH」にチェックを入れる
3. インストール完了後、コマンドプロンプトで以下を実行して確認：
   ```
   python --version
   ```

## 2. 必要なライブラリのインストール
コマンドプロンプトまたはPowerShellで以下を実行：
```powershell
pip install PyPDF2 pyinstaller
```

## 3. ソースファイルの準備
1. `pdfbinder_gui.py` をWindowsのフォルダにコピー
1. `app.py` をWindowsのフォルダにコピー（PySide6 実装）

## 4. EXEファイルの作成
ソースファイルがあるフォルダで以下を実行：
```powershell
# 基本のビルド（PySide6 実装）
pyinstaller --onefile --windowed --name "PdfBinder_PySide6" app.py

# または、より詳細な設定でビルド
pyinstaller --onefile --windowed --name "PdfBinder_PySide6" --distpath dist_ps6 --workpath build_ps6 --specpath . app.py
```

## 5. 実行ファイルの確認
- `dist` フォルダ内に `PdfBinder.exe` が作成されます
- このファイルはWindows上で実行可能です

## トラブルシューティング

### Pythonが認識されない
- Pythonのインストール時に「Add Python to PATH」にチェックが入っているか確認
- コマンドプロンプトを管理者として実行
- PCを再起動してから再試行

### pipが認識されない
```powershell
python -m pip install PyPDF2 pyinstaller
```

### ビルドエラーが発生する
```powershell
# 仮想環境を作成して実行
python -m venv venv
venv\Scripts\activate
pip install PyPDF2 pyinstaller
pyinstaller --onefile --windowed --name "PDF管理ツール" pdf_manager_gui.py
```

## 配布時の注意
- 作成された `PDF管理ツール.exe` のみを配布
- 他のユーザーのPCにはPythonのインストールは不要
- Windows Defenderの警告が出る場合は「詳細情報」→「実行」で許可
