from PyQt5.QtWidgets import QFrame, QPushButton, QWidget, QLabel, QDialog, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QColor, QCursor
from utils.events import Event
from utils.event_emitter import EventEmitter
from PyQt5.QtCore import Qt
from model.room import Room
from .room_list import RoomList
from .search_frame import SearchFrame
from typing import Any


class MainWindow(QDialog, EventEmitter):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        super(EventEmitter, self).__init__()

        self.setGeometry(x, y, width, height)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self._build_menu()

        self.room_list = RoomList(self.on_join_room)

        self.search_frame = SearchFrame(
            lambda text: self.room_list.room_searched(text))

        self.layout.addWidget(self.search_frame)
        self.layout.setAlignment(self.search_frame, Qt.AlignCenter)

        self.layout.addWidget(self.room_list)
        self.layout.setAlignment(self.room_list, Qt.AlignCenter)

        self.setWindowTitle("Rooms")
        self.setObjectName('main-win')

    def _build_menu(self) -> None:
        self.menu = QFrame()
        self.menu.setObjectName('menu')

        self.layout.addWidget(self.menu)
        layout = QHBoxLayout(self.menu)

        title_label1 = QLabel("Checkers")
        title_label2 = QLabel("Online")
        title_label1.setAlignment(Qt.AlignCenter)
        title_label2.setAlignment(Qt.AlignCenter)
        title = QFrame()
        title.setObjectName('menu-title')
        title_layout = QVBoxLayout(title)
        title_layout.addWidget(title_label1)
        title_layout.addWidget(title_label2)

        layout.addWidget(title)

        labels = ["Refresh List", "Create Room", "Profile", "Quit"]
        handlers = [self.on_refresh_rooms, self.on_create_room,
                    self.on_show_profile, self.on_quit]

        for label, handler in zip(labels, handlers):
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            layout.addWidget(btn)

    def clean_rooms(self) -> None:
        self.room_list.clear_list()

    def add_room(self, room: Room) -> None:
        self.room_list.append_room(room)

    def on_show_profile(self):
        print('profile')

    def on_create_room(self):
        # print('create')
        self.call_listeners(Event.CREATE_ROOM)

    def on_refresh_rooms(self):
        # print('refresh')
        self.call_listeners(Event.REFRESH_ROOMS)

    def on_quit(self):
        print('quit')

    def on_join_room(self, idx: int) -> None:
        self.call_listeners(Event.JOIN_ROOM, idx)

    def moveEvent(self, event):
        super(QDialog, self).moveEvent(event)
        x, y = event.pos().x(), event.pos().y()
        self.call_listeners(Event.WINDOW_MOVED, (x, y))
