from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from model.board import Board
from view.board_view import BoardView


class GameWindow(QDialog):
    def __init__(self, x: int, y: int, width: int, height: int,
                 board_width: int, board_height: int, title: str = 'Checkers'):
        super().__init__()

        self.board_width = board_width
        self.board_height = board_height

        self.board_view = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setGeometry(x, y, width, height)
        self.setWindowTitle(title)

    def draw_board(self, board: Board) -> BoardView:
        self.board_view = BoardView(
            board, self.board_width, self.board_height, True)
        self.board_view.draw()
        self.layout.addWidget(self.board_view)
        return self.board_view
