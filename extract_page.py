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
        self.file_label = QLabel("選択ファイル: なし")
        self.file_label.setStyleSheet("font-size:12px;")
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("例: 1,3-5")
        self.page_input.setMinimumHeight(36)
        self.page_input.setStyleSheet("font-size:13px;")
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.setMinimumHeight(36)
        self.pw_input.setStyleSheet("font-size:13px;")

        self.layout.addWidget(self.select_btn)
        self.layout.addWidget(self.file_label)
        row = QHBoxLayout()
        row.addWidget(QLabel("ページ"))
        row.addWidget(self.page_input)
        self.layout.addLayout(row)
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("パスワード"))
        row2.addWidget(self.pw_input)
        self.layout.addLayout(row2)

        self.select_btn.clicked.connect(self.on_select)

    def on_select(self):
        from PySide6.QtWidgets import QFileDialog

        path, _ = QFileDialog.getOpenFileName(
            self, "PDFを選択", "", "PDF Files (*.pdf)"
        )
        if not path:
            return
        self.file_label.setText(f"選択ファイル: {path}")
        self.file_selected.emit(path)
