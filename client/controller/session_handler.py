from controller.game_engine import GameEngine
from controller.gui_event_handler import GuiEventHandler
from view.game_window import GameWindow
from common.communication_handler import CommunicationHandler as CH
from utils.events import Event
from utils.event_emitter import EventEmitter
from model.player import Player
from model.room import Room
from view.auth_window import AuthWindow
from view.main_window import MainWindow
from dotenv import dotenv_values
from common.msg_codes import ServerCodes, UserCodes
from typing import Tuple
import socket
import time


class SessionHandler:
    def __init__(self, auth_win: AuthWindow, main_win: MainWindow, game_win: GameWindow) -> None:
        self.player = None
        self.request_pending = False
        self.game_engine = None
        self.gui_event_handler = None

        config = dotenv_values('../.config')
        PORT = int(config['PORT']) if 'PORT' in config else 5555

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((socket.gethostname(), PORT))

        self.auth_win = auth_win
        self.main_win = main_win
        self.game_win = game_win

        self._register_listneners()

        self.auth_win.show()
        # self.main_win.show()

    def _register_listneners(self):
        self.auth_win.add_event_listener(Event.REGISTER, self.register)
        self.auth_win.add_event_listener(Event.LOGIN, self.login)

        self.main_win.add_event_listener(Event.CREATE_ROOM, self.create_room)
        # self.main_win.add_event_listener(Event.JOIN_ROOM, self.join_room)
        self.main_win.add_event_listener(
            Event.REFRESH_ROOMS, self.refresh_rooms)

    def register(self, event: Event, emitter: AuthWindow, data: Tuple[str, str]):
        # mutex?
        if self.request_pending or self.player is not None:
            return

        self.request_pending = True

        email, passwd = data
        CH.send_msg(self.server, ServerCodes.REGISTER, {
                    'email': email,
                    'password': passwd
                    })

        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        data = resp['data']

        if code == UserCodes.REGISTER_SUCCESS and \
                data['email'] == email and data['password'] == passwd:
            emitter.user_registered(email)
        else:
            emitter.register_failed(data)

        self.request_pending = False

    def login(self, event: Event, emitter: AuthWindow, data: Tuple[str, str]):
        if self.request_pending or self.player is not None:
            return

        self.request_pending = True
        email, passwd = data

        CH.send_msg(self.server, ServerCodes.LOGIN, {
            'email': email,
            'password': passwd
        })

        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        data = resp['data']

        if code == UserCodes.LOGIN_SUCCESS and \
                data['email'] == email and data['password'] == passwd:
            self.player = Player(email)
            self.auth_win.close()
            self.main_win.show()
        else:
            emitter.login_failed(data)

        self.request_pending = False

    def create_room(self, event: Event, emitter: MainWindow):
        # validate?
        CH.send_msg(self.server, ServerCodes.CREATE_ROOM, '')

        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        if code == UserCodes.ROOM_CREATED:
            self.game_engine = GameEngine(self.game_win)
            self.gui_event_handler = GuiEventHandler(self.game_engine)
            self.main_win.hide()
            self.game_win.show()
        else:
            print('failed to create room')
            print(resp)

    def refresh_rooms(self, event: Event, emitter: MainWindow):
        CH.send_msg(self.server, ServerCodes.GET_ROOMS, '')

        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        rooms = resp['data']
        if code == UserCodes.ROOMS_FETCHED:
            for obj in rooms:
                self.main_win.add_room(Room.from_json(obj))
        else:
            print('failed to fetch rooms')
            print(resp)
