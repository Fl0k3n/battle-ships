from controller.game_engine import GameEngine
from controller.gui_event_handler import GuiEventHandler
from view.game_window import GameWindow
from common.communication_handler import CommunicationHandler as CH
from utils.events import Event
from model.player import Player
from model.room import Room
from view.auth_window import AuthWindow
from view.main_window import MainWindow
from dotenv import dotenv_values
from common.msg_codes import ServerCodes, UserCodes
from common.msg_received_observer import MsgReceivedObserver
from typing import Tuple
import socket
import threading


class SessionHandler(MsgReceivedObserver):
    def __init__(self, auth_win: AuthWindow, main_win: MainWindow, game_win: GameWindow) -> None:
        self.player = None
        self.request_pending = False
        self.game_engine = None
        self.gui_event_handler = None
        self.rooms = {}  # room_id -> Room

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
        self.main_win.add_event_listener(Event.JOIN_ROOM, self.join_room)
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
            self.game_engine = GameEngine(self.game_win, self.player)
            self.main_win.hide()
            self.game_win.show()
            self.async_wait_for_single_msg()
        else:
            print('failed to create room')
            print(resp)

    def refresh_rooms(self, event: Event, emitter: MainWindow):
        CH.send_msg(self.server, ServerCodes.GET_ROOMS, '')

        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        rooms = resp['data']
        if code == UserCodes.ROOMS_FETCHED:
            emitter.clean_rooms()
            self.rooms = {}
            for obj in rooms:
                room = Room.from_json(obj)
                self.rooms[room.idx] = room
                self.main_win.add_room(room)
        else:
            print('failed to fetch rooms')
            print(resp)

    def on_msg_received(self, socket, msg):
        code = msg['code']

        if code == UserCodes.GUEST_JOINED_ROOM and not self.game_engine.is_running():
            guest_email = msg['data']['email']
            self.game_engine.set_guest(Player(guest_email))
            self.gui_event_handler = GuiEventHandler(self.game_engine)
        elif code == UserCodes.DISCONNECTED:
            print('server died. aborting')
            exit(1)
        elif code == UserCodes.ERROR:
            print(msg['data'])
            exit(1)
        else:
            print(f'received unknown message: {msg}\nwaiting for next...')
            self.async_wait_for_single_msg()

    def async_wait_for_single_msg(self):
        threading.Thread(target=CH.listen_for_messages,
                         args=(self.server, self, True)).start()

    def join_room(self,  event: Event, emitter: MainWindow, idx: int) -> None:
        CH.send_msg(self.server, ServerCodes.JOIN_ROOM, {'room_id': idx})
        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        if code == UserCodes.JOINED_ROOM:
            room_id = resp['data']['room_id']
            owner_email = self.rooms[room_id].owner_email
            self.game_engine = GameEngine(
                self.game_win, Player(owner_email), self.player)
            self.gui_event_handler = GuiEventHandler(self.game_engine)
            self.main_win.hide()
            self.game_win.show()
        elif code == UserCodes.FAILED_TO_JOIN_ROOM:
            print(f'Failed to join room.\n{resp["data"]}')
        else:
            print(f'got unknown msg: {resp}')
