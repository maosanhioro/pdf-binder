from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MergePage(QWidget):
    files_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.add_btn = QPushButton("PDFを追加")
        self.add_btn.setMinimumHeight(44)
        self.add_btn.setStyleSheet("font-size:14px; padding:8px;")

        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_widget.setDragDropMode(QAbstractItemView.InternalMove)
        self.list_widget.setMinimumHeight(320)
        self.list_widget.setStyleSheet("font-size:13px;")

        self.remove_btn = QPushButton("削除")
        self.remove_btn.setMinimumHeight(40)
        self.remove_btn.setStyleSheet("font-size:13px;")
        self.clear_btn = QPushButton("クリア")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setStyleSheet("font-size:13px;")

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.remove_btn)
        btn_row.addWidget(self.clear_btn)

        self.layout.addLayout(btn_row)
        self.layout.addWidget(self.list_widget)

        self.add_btn.clicked.connect(self.on_add)
        self.remove_btn.clicked.connect(self.on_remove)
        self.clear_btn.clicked.connect(self.on_clear)

    def on_add(self):
        from PySide6.QtWidgets import QFileDialog

        paths, _ = QFileDialog.getOpenFileNames(
            self, "PDFを選択", "", "PDF Files (*.pdf)"
        )
        if not paths:
            return
        for p in paths:
            item = QListWidgetItem(p)
            item.setSizeHint(QSize(0, 40))
            self.list_widget.addItem(item)
        self.emit_files()

    def on_remove(self):
        for item in list(self.list_widget.selectedItems()):
            self.list_widget.takeItem(self.list_widget.row(item))
        self.emit_files()

    def on_clear(self):
        self.list_widget.clear()
        self.emit_files()

    def emit_files(self):
        files = [
            self.list_widget.item(i).text() for i in range(self.list_widget.count())
        ]
        self.files_changed.emit(files)
