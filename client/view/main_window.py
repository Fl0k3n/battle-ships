from PyQt5.QtWidgets import QPushButton, QWidget, QLabel, QDialog, QVBoxLayout, QHBoxLayout
from utils.events import Event
from utils.event_emitter import EventEmitter
from model.player import Player
from model.room import Room
from .room_list import RoomList
from typing import Any


class MainWindow(QDialog, EventEmitter):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        super(EventEmitter, self).__init__()

        self.setGeometry(x, y, width, height)

        self.layout = QHBoxLayout(self)
        self._build_menu()
        self.layout.addWidget(self.menu)

        self.room_list = RoomList(self.on_join_room)
        self.layout.addWidget(self.room_list)

        self.setWindowTitle("Rooms")

    def _build_menu(self) -> None:
        self.menu = QWidget()
        layout = QVBoxLayout(self.menu)

        labels = ["Profile", "Create Room", "Refresh List", "Quit"]
        handlers = [self.on_show_profile, self.on_create_room,
                    self.on_refresh_rooms, self.on_quit]

        for label, handler in zip(labels, handlers):
            btn = QPushButton(label)
            btn.clicked.connect(handler)
            layout.addWidget(btn)

    def clean_rooms(self) -> None:
        self.room_list.clear_list()

    def add_room(self, room: Room) -> None:
        self.room_list.append_room(room)

    def on_show_profile(self):
        print('profile')

    def on_create_room(self):
        self.call_listeners(Event.CREATE_ROOM)

    def on_refresh_rooms(self):
        self.call_listeners(Event.REFRESH_ROOMS)

    def on_quit(self):
        print('quit')

    def on_join_room(self, idx: int) -> None:
        self.call_listeners(Event.JOIN_ROOM, idx)

    def moveEvent(self, event):
        super(QDialog, self).moveEvent(event)
        x, y = event.pos().x(), event.pos().y()
        self.call_listeners(Event.WINDOW_MOVED, (x, y))
