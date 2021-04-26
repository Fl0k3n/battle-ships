from start_screen import StartScreen
from PyQt5.QtWidgets import QApplication, QWidget
import sys


class Application:
    def __init__(self):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setGeometry(100, 100, 800, 800)

        start_screen = StartScreen(self.window)

        self.window.show()
        sys.exit(self.app.exec())

