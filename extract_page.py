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
        self.file_path.setMinimumHeight(36)
        self.file_path.setStyleSheet("font-size:12px; padding:6px;")
        self.clear_btn = QPushButton("クリア")
        self.clear_btn.setMinimumHeight(36)
        self.clear_btn.setStyleSheet("font-size:12px;")
        self.page_input = QLineEdit()
        self.page_input.setPlaceholderText("例: 1,3-5")
        self.page_input.setMinimumHeight(36)
        self.page_input.setStyleSheet("font-size:13px;")
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw_input.setMinimumHeight(36)
        self.pw_input.setStyleSheet("font-size:13px;")

        label_width = 88
        self.layout.addWidget(self.select_btn)
        file_row = QHBoxLayout()
        file_label = QLabel("選択ファイル")
        file_label.setFixedWidth(label_width)
        file_row.addWidget(file_label)
        file_row.addWidget(self.file_path)
        file_row.addWidget(self.clear_btn)
        self.layout.addLayout(file_row)
        row = QHBoxLayout()
        page_label = QLabel("ページ")
        page_label.setFixedWidth(label_width)
        row.addWidget(page_label)
        row.addWidget(self.page_input)
        self.layout.addLayout(row)
        row2 = QHBoxLayout()
        pw_label = QLabel("パスワード")
        pw_label.setFixedWidth(label_width)
        row2.addWidget(pw_label)
        row2.addWidget(self.pw_input)
        self.layout.addLayout(row2)
        self.layout.addStretch(1)

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
