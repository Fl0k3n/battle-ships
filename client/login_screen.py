from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit


class LoginScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 400)

        self.label_title = QLabel("Login", parent=self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setGeometry(100, 50, 200, 50)

        self.label_login = QLabel("Login:", parent=self)
        self.label_login.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login.setGeometry(50, 150, 100, 50)

        self.label_password = QLabel("Password:", parent=self)
        self.label_password.setAlignment(QtCore.Qt.AlignCenter)
        self.label_password.setGeometry(50, 200, 100, 50)

        self.login_button = QPushButton("Register", parent=self)
        self.login_button.clicked.connect(self.on_login_button_pressed)
        self.login_button.setGeometry(100, 300, 200, 50)

        self.login_input = QLineEdit("", parent=self)
        self.login_input.setGeometry(150, 150, 200, 50)

        self.password_input = QLineEdit("", parent=self)
        self.password_input.setGeometry(150, 200, 200, 50)
        self.password_input.setEchoMode(QLineEdit.Password)

    def on_login_button_pressed(self):
        print("LoginScreen: login")

