from PyQt5.QtWidgets import QWidget
from model.pawn import Pawn
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from utils.color import Color
from pathlib import Path

parent_path = Path(__file__).parent.parent


class PawnView(QWidget):
    _WHITE_PATH = f'{parent_path}/assets/white_pawn.png'
    _BLACK_PATH = f'{parent_path}/assets/black_pawn.png'

    def __init__(self, width, height, parent: QWidget = None):
        super().__init__(parent)
        self.width = width
        self.height = height

    def draw(self, pawn: Pawn) -> None:
        path = self._WHITE_PATH if pawn.get_color() == Color.WHITE else self._BLACK_PATH
        pixmap = QPixmap(path).scaledToWidth(
            self.width).scaledToHeight(self.height)

        label = QLabel(self)
        label.setPixmap(pixmap)
