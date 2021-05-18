from controller.game_engine import GameEngine
from controller.gui_event_handler import GuiEventHandler
from controller.session_handler import SessionHandler
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import UserCodes
import sys
from PyQt5.QtWidgets import QApplication
from view.app_window import AppWindow


def main():
    CH.set_code_wrapper(UserCodes)
    app = QApplication(sys.argv)
    # engine = GameEngine()
    # gui_evnt_handler = GuiEventHandler(engine)

    session = SessionHandler()
    win = AppWindow(800, 800)
    session.register_listneners(win)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
