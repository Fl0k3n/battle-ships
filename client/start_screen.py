from PyQt5.QtWidgets import QPushButton, QWidget
from login_screen import LoginScreen

from register_screen import RegisterScreen


class StartScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.login_button = QPushButton("Login", parent=self)
        self.login_button.setGeometry(250, 400, 300, 100)
        self.login_button.clicked.connect(self.on_login_button_clicked)

        self.register_button = QPushButton("Register", parent=self)
        self.register_button.setGeometry(250, 600, 300, 100)
        self.register_button.clicked.connect(self.on_register_button_clicked)

        self.login_screen = LoginScreen()
        self.register_screen = RegisterScreen()

        self.login_button.show()
        self.register_button.show()


    def on_login_button_clicked(self):
        print("StartScreen: Login Button pressed")
        self.login_screen.show()

    def on_register_button_clicked(self):
        print("StartScreen: Register Button pressed")
        self.register_screen.show()


