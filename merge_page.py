from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHBoxLayout,
    QLabel,
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

        self.clear_btn = QPushButton("クリア")
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setStyleSheet("font-size:13px;")

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.clear_btn)

        self.layout.addLayout(btn_row)
        self.layout.addWidget(self.list_widget)

        self.add_btn.clicked.connect(self.on_add)
        self.clear_btn.clicked.connect(self.on_clear)

    def on_add(self):
        from PySide6.QtWidgets import QFileDialog

        paths, _ = QFileDialog.getOpenFileNames(
            self, "PDFを選択", "", "PDF Files (*.pdf)"
        )
        if not paths:
            return
        for p in paths:
            self._add_item(p)
        self.emit_files()

    def _add_item(self, path: str) -> None:
        item = QListWidgetItem()
        item.setSizeHint(QSize(0, 40))
        item.setData(Qt.UserRole, path)
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, self._create_row(item, path))

    def _create_row(self, item: QListWidgetItem, path: str) -> QWidget:
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(8, 0, 8, 0)
        row_layout.setSpacing(8)

        label = QLabel(path)
        label.setToolTip(path)
        label.setStyleSheet("font-size:13px;")
        row_layout.addWidget(label, 1)

        btn_up = QPushButton("▲")
        btn_up.setMinimumHeight(30)
        btn_up.setFixedWidth(28)
        btn_up.setStyleSheet("font-size:10px; padding:2px;")
        btn_up.clicked.connect(lambda _, it=item: self._move_item(it, -1))
        row_layout.addWidget(btn_up, 0)

        btn_down = QPushButton("▼")
        btn_down.setMinimumHeight(30)
        btn_down.setFixedWidth(28)
        btn_down.setStyleSheet("font-size:10px; padding:2px;")
        btn_down.clicked.connect(lambda _, it=item: self._move_item(it, 1))
        row_layout.addWidget(btn_down, 0)

        remove_btn = QPushButton("削除")
        remove_btn.setMinimumHeight(30)
        remove_btn.setStyleSheet("font-size:12px; padding:4px 10px;")
        remove_btn.clicked.connect(lambda _, it=item: self._remove_item(it))
        row_layout.addWidget(remove_btn, 0)

        return row

    def _remove_item(self, item: QListWidgetItem) -> None:
        self.list_widget.takeItem(self.list_widget.row(item))
        self.emit_files()

    def _move_item(self, item: QListWidgetItem, delta: int) -> None:
        current = self.list_widget.row(item)
        target = current + delta
        if target < 0 or target >= self.list_widget.count():
            return
        path = item.data(Qt.UserRole)
        self.list_widget.takeItem(current)
        new_item = QListWidgetItem()
        new_item.setSizeHint(QSize(0, 40))
        new_item.setData(Qt.UserRole, path)
        self.list_widget.insertItem(target, new_item)
        self.list_widget.setItemWidget(new_item, self._create_row(new_item, path))
        self.emit_files()

    def on_clear(self):
        self.list_widget.clear()
        self.emit_files()

    def emit_files(self):
        files = [
            self.list_widget.item(i).data(Qt.UserRole)
            for i in range(self.list_widget.count())
        ]
        self.files_changed.emit(files)
