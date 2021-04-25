import socket
import threading
from dotenv import dotenv_values
from common.communication_handler import CommunicationHandler as CH
from common.msg_received_observer import MsgReceivedObserver
from common.msg_codes import ServerCodes, UserCodes
import time


class ConnectionTest(MsgReceivedObserver):
    def __init__(self):
        config = dotenv_values('../.config')
        PORT = int(config['PORT']) if 'PORT' in config else 5555

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((socket.gethostname(), PORT))

        # threading.Thread(target=CH.listen_for_messages,
        #                  args=(self.s, self), daemon=True).start()

        self.logged_in = False
        self.room_id = -1
        self.email = None

    def on_msg_received(self, socket, msg):
        code = UserCodes(msg['code'])
        data = msg['data']

        if code == UserCodes.LOGIN_SUCCESS:
            if self.email != data['email']:
                print('got different email as a login response than the one sent')
            self.logged_in = True

        if code == UserCodes.ROOM_CREATED:
            self.room_id = data['room_id']

        print(f'from msg_handler, received: {code} : {data}')

    def emulate_app(self):
        while True:
            wait_for_resp = True
            print(
                """
                0. exit
                1. register
                2. login
                3. create room
                4. get rooms""")

            x = int(input('choose  '))
            if x == 0:
                break
            if x == 1:
                email = input('email')
                password = input('password')
                CH.send_msg(self.s, ServerCodes.REGISTER, {
                    'email': email,
                    'password': password
                })
            elif x == 2:
                email = input('email')
                self.email = email
                password = input('password')
                CH.send_msg(self.s, ServerCodes.LOGIN, {
                    'email': email,
                    'password': password
                })
            elif x == 3:
                if self.logged_in and self.room_id == -1:
                    CH.send_msg(self.s, ServerCodes.CREATE_ROOM, '')
                elif not self.logged_in:
                    print("you have to login first")
                    wait_for_resp = False
                else:
                    print('you are already in a room')
                    wait_for_resp = False
            elif x == 4:
                CH.send_msg(self.s, ServerCodes.GET_ROOMS, '')
            else:
                print('wrong command')
                wait_for_resp = False

            if wait_for_resp:
                CH.listen_for_messages(self.s, caller=self, only_one=True)


if __name__ == '__main__':
    ct = ConnectionTest()
    ct.emulate_app()
