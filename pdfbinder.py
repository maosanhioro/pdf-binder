import os
import sys
import traceback
from datetime import datetime

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QCursor, QGuiApplication
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
        screens = QGuiApplication.screens()
        if screens:
            for idx, s in enumerate(screens):
                geo = s.availableGeometry()
                log_line(
                    f"screen[{idx}] name={s.name()} geo={geo} "
                    f"dpi={s.logicalDotsPerInch():.2f}"
                )
        log_line(f"cursor pos={QCursor.pos()}")
        win = MainWindow()
        log_line("window created")
        win.show()

        def bring_to_front() -> None:
            if not win.isVisible():
                win.show()
            screen = QGuiApplication.screenAt(QCursor.pos())
            if not screen:
                screen = QGuiApplication.primaryScreen()
            if screen:
                geometry = screen.availableGeometry()
                width = min(win.width(), geometry.width())
                height = min(win.height(), geometry.height())
                left = geometry.x() + (geometry.width() - width) // 2
                top = geometry.y() + (geometry.height() - height) // 2
                win.setGeometry(left, top, width, height)
            state = win.windowState()
            if state & Qt.WindowMinimized:
                win.setWindowState(state & ~Qt.WindowMinimized)
            win.showNormal()
            win.raise_()
            win.activateWindow()
            if screen:
                log_line(
                    "window visible="
                    f"{win.isVisible()} state={win.windowState()} geometry={win.geometry()}"
                )

        bring_to_front()
        QTimer.singleShot(250, bring_to_front)
        sys.exit(app.exec())
    except Exception:
        log_line("exception")
        log_line(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
