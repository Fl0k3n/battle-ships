import socket
import threading
from dotenv import dotenv_values
from common.communication_handler import CommunicationHandler as CH
from common.msg_received_observer import MsgReceivedObserver


class ConnectionTest(MsgReceivedObserver):
    def __init__(self):
        config = dotenv_values('../.config')
        PORT = int(config['PORT']) if 'PORT' in config else 5555

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), PORT))

        threading.Thread(target=CH.listen_for_messages,
                         args=(self.s, self)).start()

    def on_msg_received(self, socket, msg):
        code = msg['code']
        data = msg['data']

        print(f'from msg_handler, received: {code} : {data}')

    def emulate_app(self):
        while True:
            print(
                """
                0. exit
                1. register
                2. login
                3. get rooms""")

            x = int(input('choose  '))
            if x == 0:
                break
            if x == 1:
                print('sent register signal')
                CH.send_msg(self.s, 1, 'register me')
            elif x == 2:
                # send message to login
                pass
            else:
                # send message to create room
                pass


if __name__ == '__main__':
    ct = ConnectionTest()
    ct.emulate_app()
