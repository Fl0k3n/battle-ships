from controller.session_handler import SessionHandler
from view.game_window import GameWindow
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import UserCodes
import sys
from PyQt5.QtWidgets import QApplication
from view.auth_window import AuthWindow
from view.main_window import MainWindow
from utils.events import Event
from utils.assets_loader import AssetsLoader


def main():
    CH.set_code_wrapper(UserCodes)
    app = QApplication(sys.argv)

    with open(AssetsLoader.get_path('style.css')) as f:
        app.setStyleSheet(f.read())

    auth_win = AuthWindow(100, 100, 700, 800)
    main_win = MainWindow(100, 100, 800, 800)
    game_win = GameWindow(100, 100, 800, 800, 640, 640)

    auth_win.add_event_listener(
        Event.WINDOW_MOVED, lambda event, emitter, pos: main_win.move(*pos))
    main_win.add_event_listener(
        Event.WINDOW_MOVED, lambda event, emitter, pos: game_win.move(*pos))

    session = SessionHandler(auth_win, main_win, game_win)

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
