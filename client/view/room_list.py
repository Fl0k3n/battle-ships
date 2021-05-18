from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout
from typing import Callable, Any
from model.room import Room


class RoomList(QWidget):
    def __init__(self, on_join_room_handler: Callable[[int], Any]):
        super().__init__()
        self.join_handler = on_join_room_handler
        self.layout = QVBoxLayout(self)
        self.msg_label = QLabel("No rooms available")
        self.layout.addWidget(self.msg_label)
        self.room_widgets = []
        self.room_count = 0

    def clear_list(self):
        if self.room_count > 0:
            self.msg_label = QLabel("No rooms available")
            self.layout.addWidget(self.msg_label)

        self.room_count = 0
        for widget in self.room_widgets:
            self.layout.removeWidget(widget)
            widget.setParent(None)

        self.room_widgets = []

    def append_room(self, room: Room) -> None:
        if self.room_count == 0:
            self.layout.removeWidget(self.msg_label)
            self.msg_label.setParent(None)
            del self.msg_label

        self.room_count += 1
        room_view = QWidget()
        self.room_widgets.append(room_view)
        room_layout = QGridLayout(room_view)

        room_layout.addWidget(QLabel(f'owner: {room.owner_email}'), 1, 1)
        room_layout.addWidget(
            QLabel(f'guest: {"Free" if room.is_joinable() else room.guest_email}'), 2, 1)

        join_btn = QPushButton("Join")
        room_layout.addWidget(join_btn, 1, 2, 2, 1)
        join_btn.clicked.connect(lambda: self.join_handler(room.idx))

        self.layout.addWidget(room_view)
