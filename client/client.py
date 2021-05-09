from controller.game_engine import GameEngine
from controller.gui_event_handler import GuiEventHandler
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    engine = GameEngine()
    gui_evnt_handler = GuiEventHandler(engine)
    sys.exit(app.exec())
