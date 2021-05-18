from common.communication_handler import CommunicationHandler as CH
from utils.events import Event
from utils.event_emitter import EventEmitter
from model.player import Player
from view.app_window import AppWindow
from dotenv import dotenv_values
from common.msg_codes import ServerCodes, UserCodes
from typing import Tuple
import socket
import time


class SessionHandler:
    def __init__(self) -> None:
        self.player = None
        self.request_pending = False

        config = dotenv_values('../.config')
        PORT = int(config['PORT']) if 'PORT' in config else 5555

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((socket.gethostname(), PORT))

    def register_listneners(self, window: AppWindow):
        window.add_event_listener(Event.REGISTER, self.register)
        window.add_event_listener(Event.LOGIN, self.login)

    def register(self, event: Event, emitter: AppWindow, data: Tuple[str, str]):
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

    def login(self, event: Event, emitter: AppWindow, data: Tuple[str, str]):
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
            emitter.user_logged_in(self.player)
        else:
            emitter.login_failed(data)

        self.request_pending = False
