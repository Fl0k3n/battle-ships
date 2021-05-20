from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QVBoxLayout
from PyQt5.QtCore import Qt
from .login_view import LoginView
from .register_view import RegisterView
from utils.events import Event
from utils.event_emitter import EventEmitter
from threading import Timer
from model.player import Player


class AuthWindow(QDialog, EventEmitter):
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__()
        super(EventEmitter, self).__init__()

        self.layout = QVBoxLayout(self)

        self.title_label = QLabel('Checkers Online')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName('title')

        self.setObjectName('auth-window')
        self.layout.addWidget(self.title_label)

        self.login_view = LoginView(self.on_login, self.on_change_view)
        self.layout.addWidget(self.login_view)
        self.layout.setAlignment(self.login_view, Qt.AlignCenter)

        self.register_view = RegisterView(
            self.on_register, self.on_change_view)

        self.current_view = self.login_view

        self.setGeometry(x, y, width, height)
        self.setWindowTitle("Checkers Online")

        self.msg_label = None

    def on_login(self, email: str, passw: str) -> None:
        self._delete_msg()
        self.call_listeners(Event.LOGIN, (email, passw))

    def on_register(self, email: str, passw: str, rep_passw: str) -> None:
        self._delete_msg()
        # TODO validate passwd = rep .. etc
        self.call_listeners(Event.REGISTER, (email, passw))

    def on_change_view(self) -> None:
        self._delete_msg()
        self.layout.removeWidget(self.current_view)
        self.current_view.setParent(None)

        if self.current_view is self.login_view:
            self.current_view = self.register_view
        else:
            self.current_view = self.login_view

        self.layout.addWidget(self.current_view)
        self.layout.setAlignment(self.current_view, Qt.AlignCenter)

    def user_registered(self, email: str) -> None:
        self.on_change_view()
        self._show_msg(f'{email} succesfully registered')

    def register_failed(self, reason: str) -> None:
        self._show_msg(f'Register failed. {reason}')

    def login_failed(self, reason: str) -> None:
        self._show_msg(f'Login failed. {reason}')

    def moveEvent(self, event):
        super(QDialog, self).moveEvent(event)
        x, y = event.pos().x(), event.pos().y()
        self.call_listeners(Event.WINDOW_MOVED, (x, y))

    def _show_msg(self, msg):
        self.msg_label = QLabel(msg)
        self.msg_label.setAlignment(Qt.AlignCenter)
        self.msg_label.setObjectName('auth-msg')
        self.layout.addWidget(self.msg_label)

    def _delete_msg(self):
        if self.msg_label is not None:
            self.layout.removeWidget(self.msg_label)
            self.msg_label.setParent(None)
            self.msg_label = None
