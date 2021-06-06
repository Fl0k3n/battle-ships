from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QGridLayout, QGraphicsDropShadowEffect, QWidget
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt
from typing import Callable, Any
from model.room import Room


class RoomList(QFrame):
    MAX_PER_PAGE = 3

    def __init__(self, on_join_room_handler: Callable[[int], Any]):
        super().__init__()
        self.join_handler = on_join_room_handler
        self.layout = QVBoxLayout(self)
        self.msg_label = QLabel("No rooms available")
        self.msg_label.setObjectName('no-rooms')

        self.setGraphicsEffect(self._get_shadow())

        self.setObjectName('room-list')
        self.next_btn = QPushButton('next >')
        self.back_btn = QPushButton('< back')
        self.next_btn.clicked.connect(lambda: self.change_page(1))
        self.back_btn.clicked.connect(lambda: self.change_page(-1))
        for x in (self.next_btn, self.back_btn):
            x.setObjectName('nav-btn')
            x.setCursor(QCursor(Qt.PointingHandCursor))

        self.cur_page = 1

        self.btns = None

        self.layout.addWidget(self.msg_label, alignment=Qt.AlignCenter)
        self.room_widgets = []
        self.rooms = []

    def _clear_widgets(self):
        for widget in self.room_widgets:
            self.layout.removeWidget(widget)
            widget.setParent(None)

        if self.btns is not None:
            self.layout.removeWidget(self.btns)
            self.btns.setParent(None)

        self.btns = None
        self.room_widgets = []

    def clear_list(self) -> None:
        if len(self.room_widgets) > 0:
            self.msg_label = QLabel("No rooms available")
            self.msg_label.setObjectName('no-rooms')
            self.layout.addWidget(self.msg_label, alignment=Qt.AlignCenter)

        self.cur_page = 1
        self._clear_widgets()
        self.rooms = []

    def append_room(self, room: Room, inner_call: bool = False) -> None:
        if not inner_call:
            self.rooms.append(room)

        if not inner_call and len(self.rooms) > self.MAX_PER_PAGE:
            self.handle_pages(False)
            return

        if not inner_call and len(self.room_widgets) == 0:
            self.layout.removeWidget(self.msg_label)
            self.msg_label.setParent(None)
            del self.msg_label

        room_view = QFrame()
        room_view.setObjectName('room')
        self.room_widgets.append(room_view)
        room_layout = QHBoxLayout(room_view)

        room_view.setGraphicsEffect(self._get_shadow())
        owner_label = QLabel(room.owner_email)
        owner_label.setObjectName('owner')
        owner_label.setAlignment(Qt.AlignCenter)

        room_layout.addWidget(owner_label)

        vs_label = QLabel('Vs.')
        vs_label.setObjectName('vs')
        vs_label.setAlignment(Qt.AlignCenter)
        room_layout.addWidget(vs_label)

        if not room.is_joinable():
            guest_label = QLabel(room.guest_email)
            guest_label.setObjectName('guest')
            guest_label.setAlignment(Qt.AlignCenter)
            room_layout.addWidget(guest_label)
        else:
            join_btn = QPushButton("Join")
            room_layout.addWidget(join_btn)
            join_btn.setObjectName('guest')
            join_btn.clicked.connect(lambda: self.join_handler(room.idx))
            join_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.layout.addWidget(room_view)
        self.layout.setAlignment(room_view, Qt.AlignCenter)

    def _get_shadow(self) -> QGraphicsDropShadowEffect:
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(5)
        shadow.setColor(QColor(0, 0, 0, 120))
        return shadow

    def handle_pages(self, inner_call: bool) -> None:
        if not inner_call and len(self.rooms) == self.MAX_PER_PAGE + 1:
            self.btns = self.next_btn

        # there shouldn't be any buttons at this point
        if inner_call:
            if self.cur_page > 1 and len(self.rooms) > self.MAX_PER_PAGE * self.cur_page:
                self.btns = QWidget()
                layout = QHBoxLayout(self.btns)
                layout.addWidget(self.back_btn)
                layout.addWidget(self.next_btn)
            elif self.cur_page > 1:
                self.btns = self.back_btn
            elif len(self.rooms) > self.MAX_PER_PAGE * self.cur_page:
                self.btns = self.next_btn

        if self.btns is not None:
            self.layout.addWidget(self.btns)
            self.layout.setAlignment(self.btns, Qt.AlignCenter)

    def change_page(self, delta: int) -> None:
        self._clear_widgets()
        self.cur_page += delta
        start = max(0, (self.cur_page-1) * self.MAX_PER_PAGE)
        for room in self.rooms[start:start+self.MAX_PER_PAGE]:
            self.append_room(room, inner_call=True)

        self.handle_pages(True)

    def room_searched(self, owner_email: str) -> None:
        # TODO implement better searching algorithm
        self._clear_widgets()
        for room in self.rooms:
            if room.owner_email.startswith(owner_email) and len(self.room_widgets) < self.MAX_PER_PAGE:
                self.append_room(room, True)

        if owner_email == '':
            self.handle_pages(True)
