from PyQt5.QtWidgets import QWidget, QLabel, QDialog, QVBoxLayout
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
        self.msg_label = QLabel('')
        self.layout.addWidget(self.msg_label)

        self.login_view = LoginView(self.on_login, self.on_change_view)
        self.register_view = RegisterView(
            self.on_register, self.on_change_view)

        self.layout.addWidget(self.login_view)
        self.current_view = self.login_view

        self.setGeometry(x, y, width, height)
        self.setWindowTitle("Auth")

    def on_login(self, email: str, passw: str) -> None:
        self.msg_label.setText('')
        self.call_listeners(Event.LOGIN, (email, passw))

    def on_register(self, email: str, passw: str, rep_passw: str) -> None:
        self.msg_label.setText('')
        # validate passwd = rep .. etc
        self.call_listeners(Event.REGISTER, (email, passw))

    def on_change_view(self) -> None:
        self.layout.removeWidget(self.current_view)
        self.current_view.setParent(None)

        if self.current_view is self.login_view:
            self.current_view = self.register_view
        else:
            self.current_view = self.login_view

        self.layout.addWidget(self.current_view)

    def user_registered(self, email: str) -> None:
        self.on_change_view()
        self.msg_label.setText(f'{email} succesfully registered')

    def register_failed(self, reason: str) -> None:
        self.msg_label.setText(f'Register failed.\n{reason}')

    def login_failed(self, reason: str) -> None:
        self.msg_label.setText(f'Login failed.\n{reason}')
