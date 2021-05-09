from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QColor
from model.cell import Cell
from utils.color import Color
from view.pawn_view import PawnView
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
            self.pawn_view = PawnView(
                int(self.width * 0.8), int(self.height * 0.9))
            self.pawn_view.draw(pawn)
            self.layout.addWidget(self.pawn_view)

    def enterEvent(self, event):
        self.call_listeners(Event.MOUSE_ENTERED)

    def leaveEvent(self, event):
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
