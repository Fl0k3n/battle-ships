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

    # can also use blocking listen_for_messages without caller, it will return response
    def on_msg_received(self, socket, msg):
        code = UserCodes(msg['code'])
        data = msg['data']

        if code == UserCodes.LOGIN_SUCCESS:
            if self.email != data['email']:
                print('got different email as a login response than the one sent')
            self.logged_in = True

        if code == UserCodes.ROOM_CREATED:
            self.room_id = data['room_id']
            print('waiting for guest...')
            CH.listen_for_messages(self.s, caller=self, only_one=True)
            return

        if code == UserCodes.GUEST_JOINED_ROOM:
            print(f'user ${data} has joined your room')
            # init game...

        if code == UserCodes.JOINED_ROOM:
            print(f'you have joined room owned by {data}')
            # init game...

        if code == UserCodes.ERROR:  # might create more specific error type for that
            self.room_id = -1

        # handle rest of codes appropriately...

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
                4. get rooms
                5. join room""")

            x = int(input('choose  '))
            if x == 0:
                break
            if x == 1:
                email = input('email ')
                password = input('password ')
                CH.send_msg(self.s, ServerCodes.REGISTER, {
                    'email': email,
                    'password': password
                })
            elif x == 2:
                email = input('email ')
                self.email = email
                password = input('password ')
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
            elif x == 5:
                if self.room_id == -1 and self.logged_in:
                    r_id = int(input('room id '))
                    self.room_id = r_id
                    CH.send_msg(self.s, ServerCodes.JOIN_ROOM,
                                {'room_id': r_id})
                else:
                    print('cant join')
                    wait_for_resp = False
            else:
                print('wrong command')
                wait_for_resp = False

            if wait_for_resp:
                CH.listen_for_messages(self.s, caller=self, only_one=True)


if __name__ == '__main__':
    ct = ConnectionTest()
    ct.emulate_app()
