from utils.color import Color
from model.pawn import Pawn
from typing import Tuple, Any


class Cell:
    def __init__(self, i: int, j: int, color: Color):
        self.i = i
        self.j = j
        self.color = color
        self.pawn = None

    def place_pawn(self, pawn: Pawn) -> None:
        if self.pawn is not None:
            raise AttributeError(
                f"can't place pawn on cell {self}, cell is already occupied.")
        self.pawn = pawn

    def remove_pawn(self) -> Pawn:
        pawn = self.pawn
        self.pawn = None
        return pawn

    def get_pawn(self) -> Pawn:
        return self.pawn

    def has_pawn(self) -> bool:
        return self.pawn is not None

    def get_color(self) -> Color:
        return self.color

    def get_position(self) -> Tuple[int, int]:
        return self.i, self.j

    def __str__(self) -> str:
        return f'({self.i}, {self.j})'

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Cell):
            return self.i == other.i and self.j == other.j
        return False

    def __hash__(self):
        return hash((self.i, self.j))
