from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from view.cell_view import CellView
from typing import Iterable
from model.cell import Cell
from model.board import Board
from utils.event_emitter import EventEmitter


class BoardView(QWidget):
    def __init__(self, board: Board, width: int, height: int, white_bottom: bool, parent: QWidget = None):
        super().__init__(parent)
        self.white_bottom = white_bottom
        self.width = width
        self.height = height
        self.board = board

        self.layout = QGridLayout()
        self.resize(width, height)

        self.setLayout(self.layout)
        self.layout.setSpacing(0)

        self.cell_views = []
        self.hovered_cells = []

    def draw(self) -> None:
        n = self.board.get_n_fields()
        if self.width % n != 0 or self.height % n != 0:
            raise AttributeError(
                'Board\'s width and height has to be divisible by number of fields')

        cell_w = self.width // n
        cell_h = self.height // n

        for i, row in enumerate(self.board.get_board()):
            arr = []
            for j, cell in enumerate(row):
                cv = CellView(cell, cell_w, cell_h)
                cv.draw()
                self.layout.addWidget(cv, i, j)
                arr.append(cv)
            self.cell_views.append(arr)

    def get_cell_views(self) -> Iterable[CellView]:
        return [cell_view for row in self.cell_views for cell_view in row]

    def get_cell_view(self, cell: Cell) -> CellView:
        i, j = cell.get_position()
        return self.cell_views[i][j]

    def highlight_valid_cells(self, cell_view: CellView) -> None:
        for path in self.board.get_valid_moves_from(cell_view.get_cell()):
            cell = path[0]
            i, j = cell.get_position()
            self.hovered_cells.append((i, j))
            self.cell_views[i][j].toggle_movable()

    def clear_highlight(self) -> None:
        for i, j in self.hovered_cells:
            self.cell_views[i][j].toggle_movable()
        self.hovered_cells = []

    def update_view_after_move(self, from_: Cell, to_: Cell, beaten_: Cell) -> None:
        for cell in (from_, to_, beaten_):
            if cell is not None:
                i, j = cell.get_position()
                self.cell_views[i][j].update()
