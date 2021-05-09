from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QColor
from model.cell import Cell
from utils.color import Color
from view.pawn_view import PawnView
from view.queen_pawn_view import QueenPawnView
from utils.event_emitter import EventEmitter
from utils.events import Event
from typing import Tuple


class CellView(QWidget, EventEmitter):
    _BLACK_FIELD_COLOR = QColor(102, 51, 0)
    _WHITE_FIELD_COLOR = QColor(202, 164, 114)
    _MOVABLE_FIELD_COLOR = QColor(255, 0, 0)

    def __init__(self, cell: Cell, width: int, height: int, parent: QWidget = None):
        super().__init__(parent)
        super(EventEmitter, self).__init__()

        self.width = width
        self.height = height

        self.pawn_view_width = int(self.width * 0.95)
        self.pawn_view_height = int(self.height * 0.95)

        self.cell = cell

        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        self.pawn_view = None
        self.setAutoFillBackground(True)
        self.movable = False

    def _get_color(self) -> QColor:
        if self.cell.get_color() == Color.BLACK:
            view_color = self._BLACK_FIELD_COLOR
        else:
            view_color = self._WHITE_FIELD_COLOR

        return view_color

    def draw(self) -> None:
        p = self.palette()
        p.setColor(self.backgroundRole(), self._get_color())
        self.setPalette(p)

        pawn = self.cell.get_pawn()
        if pawn is not None:
            self.pawn_view = pawn.draw(
                self.pawn_view_width, self.pawn_view_height)
            self.layout.addWidget(self.pawn_view)

    def enterEvent(self, event) -> None:
        self.call_listeners(Event.MOUSE_ENTERED)

    def leaveEvent(self, event) -> None:
        self.call_listeners(Event.MOUSE_LEFT)

    def has_pawn(self) -> bool:
        return self.cell.get_pawn() is not None

    def get_pawn_color(self) -> Color:
        return self.cell.get_pawn().get_color()

    def get_position(self) -> Tuple[int, int]:
        return self.cell.get_position()

    def get_cell(self) -> Cell:
        return self.cell

    def toggle_movable(self) -> None:
        self.movable = not self.movable
        p = self.palette()
        p.setColor(self.backgroundRole(
        ), self._MOVABLE_FIELD_COLOR if self.movable else self._get_color())
        self.setPalette(p)

    def mousePressEvent(self, event) -> None:
        self.call_listeners(Event.CELL_CLICKED)

    def update(self) -> None:
        pawn = self.cell.get_pawn()

        if pawn is None and self.pawn_view is not None:
            self.layout.removeWidget(self.pawn_view)
            self.pawn_view = None
        elif pawn is not None:
            if self.pawn_view is not None:
                self.layout.removeWidget(self.pawn_view)

            self.pawn_view = pawn.draw(
                self.pawn_view_width, self.pawn_view_height)
            self.layout.addWidget(self.pawn_view)
