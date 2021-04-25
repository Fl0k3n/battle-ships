import socket
import threading
from dotenv import dotenv_values
from msg_handler import MsgHandler
from auth_handler import AuthHandler
from db_handler import DBHandler
from user_handler import UserHandler
from room_handler import RoomHandler


class NetworkHandler:

    def __init__(self):
        self._setup_config()

        # init user, room state observers
        self.user_handler = UserHandler()
        self.room_handler = RoomHandler(self.user_handler)
        self.login_observers = [self.user_handler, self.room_handler]

        # init database
        self.db_handler = DBHandler(self.DB_URI)

        self.auth_handler = AuthHandler(
            self.db_handler, self.user_handler, self.login_observers)

        self.msg_handler = MsgHandler(
            self.auth_handler, self.room_handler, self.login_observers)
        self.connection_observers = [self.msg_handler]

        # create server socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # localhost
        self.s.bind((socket.gethostname(), self.PORT))
        self.s.listen(self.MAX_CONNECTIONS)

    def listen_for_connections(self):
        print(f'Server running at port: {self.PORT}')

        while True:
            client_socket, addr = self.s.accept()
            print(f'connection with {addr} has been established!')

            for obs in self.connection_observers:
                obs.on_connected(client_socket)

    def _setup_config(self):
        self.config = dotenv_values('../.config')
        self.PORT = int(self.config['PORT']) if 'PORT' in self.config else 5555
        self.MAX_CONNECTIONS = int(self.config
                                   ['MAX_CONNECTIONS']) if 'MAX_CONNECTIONS' in self.config else 16
        self.DB_URI = self.config['DB_URI']
