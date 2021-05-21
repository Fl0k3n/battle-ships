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
from typing import Tuple, Any
import socket
from utils.worker import Worker
from PyQt5.QtCore import QThread
from utils.color import Color


class SessionHandler(MsgReceivedObserver):
    def __init__(self, auth_win: AuthWindow, main_win: MainWindow, game_win: GameWindow) -> None:
        self.player = None
        self.request_pending = False
        self.game_engine = None
        self.gui_event_handler = None
        self.room_id = None
        self.waiting_for = None

        self.async_msg_handlers = {
            UserCodes.GUEST_JOINED_ROOM: self.on_enemy_joined,
            UserCodes.PLAYER_MOVED: self.on_enemy_moved
        }

        self.rooms = {}  # room_id -> Room

        config = dotenv_values('../.config')
        PORT = int(config['PORT']) if 'PORT' in config else 5555

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((socket.gethostname(), PORT))
        self.threads = []
        self.auth_win = auth_win
        self.main_win = main_win
        self.game_win = game_win

        self._register_listneners()
        self.auth_win.show()
        # self.main_win.show()
        # self._init_game(Player('safasf', Color.WHITE))

    def _register_listneners(self):
        self.auth_win.add_event_listener(Event.REGISTER, self.register)
        self.auth_win.add_event_listener(Event.LOGIN, self.login)

        self.main_win.add_event_listener(Event.CREATE_ROOM, self.create_room)
        self.main_win.add_event_listener(Event.JOIN_ROOM, self.join_room)
        self.main_win.add_event_listener(
            Event.REFRESH_ROOMS, self.refresh_rooms)

        self.game_win.add_event_listener(Event.DISCONNECT, lambda evnt, emittr: print(
            'dc requested session_handler line 60'))

#----------------------------------------------------------------------------------- AUTH

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
            self.refresh_rooms(None, None)
            self.auth_win.close()
            self.main_win.show()
        else:
            emitter.login_failed(data)

        self.request_pending = False

#----------------------------------------------------------------------------------- Rooms

    def create_room(self, event: Event, emitter: MainWindow):
        # validate?
        CH.send_msg(self.server, ServerCodes.CREATE_ROOM, '')

        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        self.room_id = resp['data']['room_id']
        if code == UserCodes.ROOM_CREATED:
            self._init_game(self.player)
            self._async_wait_for_single_msg(UserCodes.GUEST_JOINED_ROOM)
        else:
            print('failed to create room')
            print(resp)

    def refresh_rooms(self, event: Event, emitter: MainWindow):
        CH.send_msg(self.server, ServerCodes.GET_ROOMS, '')

        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        rooms = resp['data']
        if code == UserCodes.ROOMS_FETCHED:
            self.main_win.clean_rooms()
            self.rooms = {}
            for obj in rooms:
                room = Room.from_json(obj)
                self.rooms[room.idx] = room
                self.main_win.add_room(room)
        else:
            print('failed to fetch rooms')
            print(resp)

    def join_room(self,  event: Event, emitter: MainWindow, idx: int) -> None:
        CH.send_msg(self.server, ServerCodes.JOIN_ROOM, {'room_id': idx})
        resp = CH.listen_for_messages(self.server, only_one=True)
        code = resp['code']
        if code == UserCodes.JOINED_ROOM:
            room_id = resp['data']['room_id']
            owner_email = self.rooms[room_id].owner_email
            self.room_id = room_id

            self._init_game(Player(owner_email), self.player)
            self.gui_event_handler = GuiEventHandler(
                self.game_engine, self.player)

            self._async_wait_for_single_msg(UserCodes.PLAYER_MOVED)
        elif code == UserCodes.FAILED_TO_JOIN_ROOM:
            print(f'Failed to join room.\n{resp["data"]}')
        else:
            print(f'got unknown msg: {resp}')

    def on_enemy_joined(self, msg):
        if self.game_engine.is_running():
            raise AttributeError(
                'Guest have joined room when game engine was running')

        guest_email = msg['email']
        self.game_engine.set_guest(Player(guest_email))
        self.gui_event_handler = GuiEventHandler(
            self.game_engine, self.player)

#----------------------------------------------------------------------------------- GAME

    def player_moved(self, event: Event, emitter: GameEngine, move_data: Any):
        data = {
            'move_data': move_data,
            'room_id': self.room_id
        }

        CH.send_msg(self.server, ServerCodes.PLAYER_MOVED, data)
        self.waiting_for = None  # will be set by function below
        if move_data['last_move']:
            self._async_wait_for_single_msg(UserCodes.PLAYER_MOVED)

    def on_enemy_moved(self, msg):
        from_, to_, beaten, last_move = (
            msg[arg] for arg in ['from', 'to', 'beaten', 'last_move'])
        self.game_engine.update_enemy_move(from_, to_)
        if not last_move:
            self._async_wait_for_single_msg(UserCodes.PLAYER_MOVED)

#----------------------------------------------------------------------------------- Utility

    def _init_game(self, owner: Player, guest: Player = None):
        self.game_engine = GameEngine(self.game_win, owner, guest)
        self.main_win.hide()
        self.game_win.show()
        self.game_engine.add_event_listener(
            Event.PLAYER_MOVED, self.player_moved)

    def on_msg_received(self, socket, msg):
        code = msg['code']
        data = msg['data']

        if code == self.waiting_for:
            self.waiting_for = None

        if code in self.async_msg_handlers:
            self.async_msg_handlers[code](data)
        elif code == UserCodes.DISCONNECTED:
            print('server died. aborting')
            exit(1)
        else:
            print(f'received unknown message: {msg}')
            if self.waiting_for is not None:
                print(f'Trying again for {self.waiting_for}')
                self._async_wait_for_single_msg(self.waiting_for)

    def _async_wait_for_single_msg(self, msg_type: UserCodes):
        if self.waiting_for is not None:
            raise AttributeError(
                f'Cant wait for {msg_type}, already waiting for {self.waiting_for}')

        self.thread = QThread()
        self.threads.append(self.thread)
        self.worker = Worker(self.server)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.response.connect(
            lambda resp: self.on_msg_received(self.server, resp))
        self.thread.start()

        self.waiting_for = msg_type
