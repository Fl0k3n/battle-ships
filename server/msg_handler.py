import threading
from connection_observer import ConnectionObserver
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import ServerCodes
from common.msg_received_observer import MsgReceivedObserver


class MsgHandler(ConnectionObserver, MsgReceivedObserver):
    def __init__(self, auth_handler):
        self.auth_handler = auth_handler

        self.handlers = {
            ServerCodes.REGISTER: self.on_register,
            ServerCodes.LOGIN: self.on_login
        }

    def on_connected(self, socket):
        threading.Thread(target=CH.listen_for_messages,
                         args=(socket, self)).start()

    def on_disconnected(self, socket):
        pass

    def on_msg_received(self, socket, msg):
        code = msg['code']
        data = msg['data']

        # should be handled differently
        if code == ServerCodes.DISCONNECTED:
            print('disconnected!')
            self.on_disconnected(socket)
        else:
            self.handlers[code](socket, data)

    def on_register(self, socket, data):
        email = data['email']
        password = data['password']

        threading.Thread(target=self.auth_handler.register_user,
                         args=(socket, email, password)).start()

    def on_login(self, socket, data):
        email = data['email']
        password = data['password']

        threading.Thread(target=self.auth_handler.login_user,
                         args=(socket, email, password)).start()
