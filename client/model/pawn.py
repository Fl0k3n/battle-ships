from utils.color import Color


class Pawn:
    def __init__(self, i: int, j: int, color: Color):
        self.i = i
        self.j = j
        self.color = color

    def move(self, i: int, j: int) -> None:
        self.i = i
        self.j = j

    def get_color(self) -> Color:
        return self.color
