from model.pawn import Pawn
from utils.color import Color
from view.queen_pawn_view import QueenPawnView
from PyQt5.QtWidgets import QWidget


class QueenPawn(Pawn):
    def __init__(self, i: int, j: int, color: Color, board_width: int):
        super().__init__(i, j, color)
        self.neigh_deltas = [(di*x, dj*x) for x in range(1, board_width+1)
                             for di in (-1, 1) for dj in (-1, 1)]

    def draw(self, width: int, height: int) -> QWidget:
        view = QueenPawnView(width, height)
        view.draw(self.color)
        return view
