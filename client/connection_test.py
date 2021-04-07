import socket
import threading
from dotenv import dotenv_values
from common.communication_handler import CommunicationHandler as CH
from common.msg_received_observer import MsgReceivedObserver
from common.msg_codes import ServerCodes


class ConnectionTest(MsgReceivedObserver):
    def __init__(self):
        config = dotenv_values('../.config')
        PORT = int(config['PORT']) if 'PORT' in config else 5555

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), PORT))

        threading.Thread(target=CH.listen_for_messages,
                         args=(self.s, self), daemon=True).start()

        self.waiting_for_msg = False

    def on_msg_received(self, socket, msg):
        code = msg['code']
        data = msg['data']

        if self.waiting_for_msg:
            self.waiting_for_msg = False
            print(f'got response: {code} : {data}')

        print(f'from msg_handler, received: {code} : {data}')

    def emulate_app(self):
        while True:
            if self.waiting_for_msg:
                # view loading icon
                print('waiting for response')
            print(
                """
                0. exit
                1. register
                2. login OK
                3. login failed""")

            x = int(input('choose  '))
            if x == 0:
                break
            if x == 1:
                CH.send_msg(self.s, ServerCodes.REGISTER, {
                    'email': 'test@test.test',
                    'password': 'password'
                })
                self.waiting_for_msg = True
            elif x == 2:
                CH.send_msg(self.s, ServerCodes.LOGIN, {
                    'email': 'test@test.test',
                    'password': 'password'
                })
                self.waiting_for_msg = True
            elif x == 3:
                CH.send_msg(self.s, ServerCodes.LOGIN, {
                    'email': 'test@test.test',
                    'password': 'passw2ord'
                })
                self.waiting_for_msg = True


if __name__ == '__main__':
    ct = ConnectionTest()
    ct.emulate_app()
