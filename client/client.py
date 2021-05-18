from controller.session_handler import SessionHandler
from view.game_window import GameWindow
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import UserCodes
import sys
from PyQt5.QtWidgets import QApplication
from view.auth_window import AuthWindow
from view.main_window import MainWindow


def main():
    CH.set_code_wrapper(UserCodes)
    app = QApplication(sys.argv)

    auth_win = AuthWindow(100, 100, 800, 800)
    main_win = MainWindow(100, 100, 800, 800)
    game_win = GameWindow(100, 100, 800, 800, 640, 640)

    session = SessionHandler(auth_win, main_win, game_win)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
