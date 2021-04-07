import socket
import threading
from dotenv import dotenv_values
from msg_handler import MsgHandler


class NetworkHandler:

    def __init__(self):
        self._setup_config()

        self.connection_observers = []
        self.msg_handler = MsgHandler()

        self.connection_observers.append(self.msg_handler)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # localhost
        self.s.bind((socket.gethostname(), self.PORT))
        self.s.listen(self.MAX_CONNECTIONS)

        threading.Thread(target=self.listen_for_connections).start()

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
