from view.pawn_view import PawnView
from pathlib import Path
from PyQt5.QtWidgets import QWidget

parent_path = Path(__file__).parent.parent


class QueenPawnView(PawnView):
    _WHITE_PATH = f'{parent_path}/assets/white_queen_pawn.png'
    _BLACK_PATH = f'{parent_path}/assets/black_queen_pawn.png'

    def __init__(self, width, height, parent: QWidget = None):
        super().__init__(width, height, parent)
