import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget


class Main(QMainWindow):
    def __init__(self, parent: QWidget | None = ..., flags: Qt.WindowType = ...) -> None:
        super().__init__(parent, flags)