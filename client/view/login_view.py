from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, QPushButton
from typing import Callable, Any


class LoginView(QWidget):
    def __init__(self, on_login_handler: Callable[[str, str], Any],
                 on_change_view_handler: Callable[..., Any]):
        super().__init__()

        self.layout = QGridLayout(self)
        self.layout.addWidget(QLabel("<h2>Login</h2>"), 1, 1, 1, 2)

        self.layout.addWidget(QLabel("email"), 2, 1)
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_input, 2, 2)

        self.layout.addWidget(QLabel("password"), 3, 1)
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.pass_input, 3, 2)

        self.register_btn = QPushButton("Don't have an account?")
        self.layout.addWidget(self.register_btn, 5, 1)

        self.login_btn = QPushButton("Login")
        self.layout.addWidget(self.login_btn, 5, 2)

        self.login_btn.clicked.connect(lambda: on_login_handler(
            self.email_input.text(), self.pass_input.text()))
        self.register_btn.clicked.connect(on_change_view_handler)
