from PyQt5 import QtCore
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QVBoxLayout, QGraphicsDropShadowEffect, QLabel, QGridLayout, QLineEdit, QPushButton, QFrame, QWidget
from PyQt5.QtCore import Qt
from typing import Callable, Any


class RegisterView(QFrame):
    def __init__(self, on_register_handler: Callable[[str, str, str], Any],
                 on_change_view_handler: Callable[..., Any]):
        super().__init__()

        self.layout = QGridLayout(self)
        self.title_label = QLabel("Sign up")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName('login-label')

        self.layout.addWidget(self.title_label, 1, 1, 1, 2)
        self.layout.setAlignment(Qt.AlignCenter)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(6)
        shadow.setOffset(5)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)

        self.layout.addWidget(QLabel("email"), 2, 1)
        self.email_input = QLineEdit()
        self.layout.addWidget(self.email_input, 2, 2)

        self.layout.addWidget(QLabel("password"), 3, 1)
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.pass_input, 3, 2)

        self.layout.addWidget(QLabel("repeat password"), 4, 1)
        self.rep_pass_input = QLineEdit()
        self.rep_pass_input.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.rep_pass_input, 4, 2)

        self.inner_layout = QWidget()
        self.vbox = QVBoxLayout()
        self.inner_layout.setLayout(self.vbox)
        self.layout.addWidget(self.inner_layout, 5, 1, 1, 2, Qt.AlignCenter)

        self.login_btn = QPushButton("Already Signed Up?")
        self.register_btn = QPushButton("register")
        self.register_btn.setObjectName('login-btn')
        self.login_btn.setObjectName('register-btn')

        self.login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.register_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.vbox.addWidget(self.login_btn)
        self.vbox.addWidget(self.register_btn)

        self.login_btn.clicked.connect(on_change_view_handler)
        self.register_btn.clicked.connect(lambda: on_register_handler(
            self.email_input.text(), self.pass_input.text(), self.rep_pass_input.text()))

        self.setObjectName('login')
