from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ExtractPage(QWidget):
    file_selected = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.select_btn = QPushButton("PDFを選択")
        self.select_btn.setMinimumHeight(44)
        self.select_btn.setStyleSheet("font-size:14px; padding:8px;")
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("未選択")
        self.file_path.setReadOnly(True)
        self.file_path.setMinimumHeight(32)
        self.file_path.setStyleSheet("font-size:12px; padding:6px;")
        self.clear_btn = QPushButton("クリア")
        self.clear_btn.setMinimumHeight(32)
        self.clear_btn.setStyleSheet("font-size:12px;")
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("例: 1,3-5")
        self.page_input.setMinimumHeight(36)
        self.page_input.setStyleSheet("font-size:13px;")
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.setMinimumHeight(36)
        self.pw_input.setStyleSheet("font-size:13px;")

        self.layout.addWidget(self.select_btn)
        file_row = QHBoxLayout()
        file_row.addWidget(QLabel("選択ファイル"))
        file_row.addWidget(self.file_path)
        file_row.addWidget(self.clear_btn)
        self.layout.addLayout(file_row)
        row = QHBoxLayout()
        row.addWidget(QLabel("ページ"))
        row.addWidget(self.page_input)
        self.layout.addLayout(row)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("パスワード"))
        row2.addWidget(self.pw_input)
        self.layout.addLayout(row2)

        self.select_btn.clicked.connect(self.on_select)
        self.clear_btn.clicked.connect(self.on_clear)

    def on_select(self):
        from PySide6.QtWidgets import QFileDialog

        path, _ = QFileDialog.getOpenFileName(
            self, "PDFを選択", "", "PDF Files (*.pdf)"
        )
        if not path:
            return
        self.file_path.setText(path)
        self.file_selected.emit(path)

    def on_clear(self):
        self.file_path.clear()
        self.file_selected.emit("")
