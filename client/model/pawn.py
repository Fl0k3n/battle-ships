from utils.color import Color
from typing import Tuple
from view.pawn_view import PawnView
from PyQt5.QtWidgets import QWidget


class Pawn:
    def __init__(self, i: int, j: int, color: Color):
        self.i = i
        self.j = j
        self.color = color
        self.neigh_deltas = [(di, dj) for di in (-1, 1) for dj in (-1, 1)]

    def move(self, i: int, j: int) -> None:
        self.i = i
        self.j = j

    def get_color(self) -> Color:
        return self.color

    def get_position(self) -> Tuple[int, int]:
        return self.i, self.j

    def draw(self, width: int, height: int) -> QWidget:
        view = PawnView(width, height)
        view.draw(self.color)
        return view

    def get_neigh_deltas(self):
        return self.neigh_deltas
