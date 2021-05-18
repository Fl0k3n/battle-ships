from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from utils.color import Color
from utils.assets_loader import AssetsLoader


class PawnView(QWidget):
    _WHITE_PATH = AssetsLoader.get_path('white_pawn.png')
    _BLACK_PATH = AssetsLoader.get_path('black_pawn.png')

    def __init__(self, width, height, parent: QWidget = None):
        super().__init__(parent)
        self.width = width
        self.height = height

    def draw(self, color: Color) -> None:
        path = self._WHITE_PATH if color == Color.WHITE else self._BLACK_PATH
        pixmap = QPixmap(path).scaledToWidth(
            self.width).scaledToHeight(self.height)

        label = QLabel(self)
        label.setPixmap(pixmap)
