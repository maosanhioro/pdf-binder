import os

from PySide6.QtCore import QObject, Qt, QThread, Signal, Slot
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import pdf_operations
from extract_page import ExtractPage
from merge_page import MergePage


class Worker(QObject):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @Slot()
    def run(self):
        try:
            out = self.fn(*self.args, **self.kwargs)
            self.finished.emit(out)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PdfBinder — 複数PDFの結合／ページ抽出")
        self.resize(1000, 700)

        central = QWidget()
        self.setCentralWidget(central)
        # create layouts without parent to avoid parent-warning when nesting
        root = QHBoxLayout()

        # mode selector
        self.btn_merge = QPushButton("まとめる")
        self.btn_extract = QPushButton("抜き出し")
        self.btn_merge.setCheckable(True)
        self.btn_extract.setCheckable(True)
        self.btn_merge.setChecked(True)
        for b in (self.btn_merge, self.btn_extract):
            b.setMinimumHeight(40)
            b.setCheckable(True)
        self.btn_merge.setObjectName("segmentLeft")
        self.btn_extract.setObjectName("segmentRight")
        mode_style = (
            "QPushButton {"
            "font-size:14px; padding:6px 14px;"
            "border:1px solid #D1D5DB; background:#F9FAFB;}"
            "QPushButton:checked {"
            "background:#2B7CD3; color:white; border-color:#2B7CD3;}"
            "#segmentLeft { border-top-left-radius:8px; border-bottom-left-radius:8px; }"
            "#segmentRight { border-top-right-radius:8px; border-bottom-right-radius:8px; }"
        )
        self.btn_merge.setStyleSheet(mode_style)
        self.btn_extract.setStyleSheet(mode_style)

        # center stacked
        self.stack = QStackedWidget()
        self.merge_page = MergePage()
        self.extract_page = ExtractPage()
        self.stack.addWidget(self.merge_page)
        self.stack.addWidget(self.extract_page)

        # right action panel
        action = QVBoxLayout()
        # increase vertical spacing between widgets for comfortable breathing room
        action.setSpacing(14)
        # generous margins: left, top, right, bottom
        action.setContentsMargins(16, 32, 16, 20)

        lbl_out = QLabel("出力先")
        lbl_out.setStyleSheet("font-weight:bold; font-size:13px;")
        action.addWidget(lbl_out)

        # output dir row: lineedit + browse
        dir_row = QHBoxLayout()
        dir_row.setSpacing(8)
        self.output_dir = QLineEdit(os.getcwd())
        self.output_dir.setMinimumHeight(36)
        self.output_dir.setStyleSheet("font-size:13px; padding:8px;")
        # prefer available space but avoid forcing parent widget to expand
        self.output_dir.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        btn_browse = QPushButton("参照")
        btn_browse.setFixedWidth(72)
        btn_browse.setMinimumHeight(36)
        btn_browse.setStyleSheet("font-size:13px;")
        btn_browse.clicked.connect(self.on_choose_dir)
        dir_row.addWidget(self.output_dir, 1)
        dir_row.addWidget(btn_browse, 0)
        action.addLayout(dir_row)

        lbl_name = QLabel("出力名")
        lbl_name.setStyleSheet("font-weight:bold; font-size:13px;")
        action.addWidget(lbl_name)

        name_row = QHBoxLayout()
        self.output_name = QLineEdit("output.pdf")
        self.output_name.setMinimumHeight(36)
        self.output_name.setStyleSheet("font-size:13px; padding:8px;")
        name_row.addWidget(self.output_name)
        action.addLayout(name_row)

        # preview of final output path
        self.preview = QLabel("")
        self.preview.setStyleSheet("color:#6B7280; font-size:12px;")
        action.addWidget(self.preview)

        # execute button stretched
        self.exec_btn = QPushButton("実行")
        self.exec_btn.setMinimumHeight(52)
        self.exec_btn.setStyleSheet(
            "background-color:#2B7CD3; color:white; font-size:15px; padding:10px;"
        )
        action.addWidget(self.exec_btn)

        # update preview when fields change
        self.output_dir.textChanged.connect(lambda: self._update_preview())
        self.output_name.textChanged.connect(lambda: self._update_preview())
        self._update_preview()

        # bottom status
        bottom = QVBoxLayout()
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        self.progress.hide()
        bottom.addWidget(self.progress)

        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        mode_row = QHBoxLayout()
        mode_row.addStretch(1)
        mode_row.addWidget(self.btn_merge)
        mode_row.addWidget(self.btn_extract)
        mode_row.addStretch(1)
        center_layout.addLayout(mode_row)
        center_layout.addWidget(self.stack)

        right_widget = QWidget()
        right_widget.setLayout(action)
        # fix right pane width to keep it stable regardless of content
        right_widget.setFixedWidth(380)

        root.addWidget(center_widget, 1)
        root.addWidget(right_widget, 0)
        root.setAlignment(right_widget, Qt.AlignTop)

        # main vertical layout (central owns it)
        root_main = QVBoxLayout(central)
        root_main.setContentsMargins(12, 12, 12, 12)
        root_main.setSpacing(12)
        root_main.addLayout(root)
        root_main.addLayout(bottom)
        central.setLayout(root_main)

        # connections
        self.btn_merge.clicked.connect(lambda: self.switch(0))
        self.btn_extract.clicked.connect(lambda: self.switch(1))
        self.merge_page.files_changed.connect(self.on_merge_files_changed)
        self.extract_page.file_selected.connect(self.on_extract_file_selected)
        self.exec_btn.clicked.connect(self.on_execute)

        self.current_merge_files = []
        self.current_extract_file = None

    def switch(self, index: int):
        self.stack.setCurrentIndex(index)
        self.btn_merge.setChecked(index == 0)
        self.btn_extract.setChecked(index == 1)
        self.exec_btn.setText("まとめる" if index == 0 else "抜き出し")

    @Slot(list)
    def on_merge_files_changed(self, files):
        self.current_merge_files = files
        # when user selects files for merging, set output dir to the first file's folder
        if files:
            try:
                first_dir = os.path.dirname(files[0])
                if first_dir:
                    self.output_dir.setText(first_dir)
            except Exception:
                pass

    @Slot(str)
    def on_extract_file_selected(self, path):
        self.current_extract_file = path if path else None
        # when a file is selected for extraction, set output dir to that file's folder
        if path:
            try:
                d = os.path.dirname(path)
                if d:
                    self.output_dir.setText(d)
            except Exception:
                pass

    def on_choose_dir(self):
        d = QFileDialog.getExistingDirectory(self, "出力先を選択", os.getcwd())
        if d:
            self.output_dir.setText(d)

    def _normalize_output_name(self, name: str) -> str:
        trimmed = (name or "").strip()
        if not trimmed:
            return ""
        if trimmed.lower().endswith(".pdf"):
            return trimmed
        return f"{trimmed}.pdf"

    def _update_preview(self):
        out_dir = self.output_dir.text() or os.getcwd()
        out_name = self._normalize_output_name(self.output_name.text()) or "output.pdf"
        full = os.path.join(out_dir, out_name)
        # shorten if too long
        if len(full) > 80:
            full = "..." + full[-77:]
        self.preview.setText(f"出力: {full}")

    def _confirm_overwrite(self, out_path: str) -> bool:
        if not os.path.exists(out_path):
            return True
        reply = QMessageBox.question(
            self,
            "上書き確認",
            f"同名のファイルが存在します。\n上書きしますか？\n\n{out_path}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return reply == QMessageBox.Yes

    def start_worker(self, fn, *args, **kwargs):
        self.thread = QThread()
        self.worker = Worker(fn, *args, **kwargs)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)
        self.thread.start()
        self.progress.show()

    @Slot(str)
    def on_finished(self, out_path: str):
        self.progress.hide()
        QMessageBox.information(
            self, "完了", f"{os.path.basename(out_path)} を作成しました。"
        )

    @Slot(str)
    def on_error(self, msg: str):
        self.progress.hide()
        QMessageBox.critical(self, "エラー", msg)

    def on_execute(self):
        idx = self.stack.currentIndex()
        out_dir = self.output_dir.text() or os.getcwd()
        default_name = "merged.pdf" if idx == 0 else "extracted.pdf"
        out_name = self._normalize_output_name(self.output_name.text()) or default_name
        out_path = os.path.join(out_dir, out_name)
        if not self._confirm_overwrite(out_path):
            return
        if idx == 0:
            # merge
            if len(self.current_merge_files) < 2:
                QMessageBox.critical(self, "エラー", "2件以上のPDFを追加してください")
                return
            self.start_worker(
                pdf_operations.merge_pdfs, self.current_merge_files, out_dir, out_name
            )
        else:
            # extract
            if not self.current_extract_file:
                QMessageBox.critical(self, "エラー", "ファイルを選択してください")
                return
            page_spec = self.extract_page.page_input.text()
            pw = self.extract_page.pw_input.text()
            self.start_worker(
                pdf_operations.extract_pages,
                self.current_extract_file,
                page_spec,
                pw,
                out_dir,
                out_name,
            )
