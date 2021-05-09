from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from view.board_view import BoardView


class GameView(QDialog):
    def __init__(self, board_view: BoardView, x: int, y: int, width: int, height: int, title: str = 'Checkers'):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setGeometry(x, y, width, height)
        self.setWindowTitle(title)

        self.layout.addWidget(board_view)
        self.show()
