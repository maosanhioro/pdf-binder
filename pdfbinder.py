import os
import sys
import traceback
from datetime import datetime

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QApplication

from main_window import MainWindow

LOG_ENV = "PDFBINDER_LOG"
LOG_PATH = os.path.join(os.path.dirname(__file__), "pdfbinder.log")


def log_line(message: str) -> None:
    if not os.environ.get(LOG_ENV):
        return
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as handle:
            handle.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass


def main():
    try:
        log_line("start")
        app = QApplication(sys.argv)
        log_line("qapp created")
        win = MainWindow()
        log_line("window created")
        win.show()

        def bring_to_front() -> None:
            if not win.isVisible():
                win.show()
            screen = QGuiApplication.primaryScreen()
            if screen:
                geometry = screen.availableGeometry()
                frame = win.frameGeometry()
                frame.moveCenter(geometry.center())
                win.move(frame.topLeft())
            win.showNormal()
            win.setWindowState((win.windowState() & ~Qt.WindowMinimized) | Qt.WindowActive)
            win.raise_()
            win.activateWindow()
            log_line(f"window visible={win.isVisible()} state={win.windowState()}")

        bring_to_front()
        QTimer.singleShot(250, bring_to_front)
        sys.exit(app.exec())
    except Exception:
        log_line("exception")
        log_line(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
