from view.pawn_view import PawnView
from pathlib import Path
from PyQt5.QtWidgets import QWidget
from utils.assets_loader import AssetsLoader


class QueenPawnView(PawnView):
    _WHITE_PATH = AssetsLoader.get_path('white_queen_pawn.png')
    _BLACK_PATH = AssetsLoader.get_path('black_queen_pawn.png')

    def __init__(self, width, height, parent: QWidget = None):
        super().__init__(width, height, parent)
