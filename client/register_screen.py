from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QLineEdit


class RegisterScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 400, 400)

        self.label_title = QLabel("Register", parent=self)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setGeometry(100, 50, 200, 50)

        self.label_login = QLabel("Login:", parent=self)
        self.label_login.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login.setGeometry(50, 150, 100, 50)

        self.label_password = QLabel("Password:", parent=self)
        self.label_password.setAlignment(QtCore.Qt.AlignCenter)
        self.label_password.setGeometry(50, 200, 100, 50)

        self.register_button = QPushButton("Register", parent=self)
        self.register_button.clicked.connect(self.on_register_button_pressed)
        self.register_button.setGeometry(100, 300, 200, 50)

        self.login_input = QLineEdit("", parent=self)
        self.login_input.setGeometry(150, 150, 200, 50)

        self.password_input = QLineEdit("", parent=self)
        self.password_input.setGeometry(150, 200, 200, 50)
        self.password_input.setEchoMode(QLineEdit.Password)

    def on_register_button_pressed(self):
        print("RegisterScreen: register")


