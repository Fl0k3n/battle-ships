import socket
import json
from common.msg_codes import ServerCodes


class CommunicationHandler:
    HEADER_SIZE = 10

    @classmethod
    def send_msg(cls, socket, code, data):
        """Sends message with given code and data to given socket.

        Args:
            socket (socket): Socket to send data to
            code (ServerCode|UserCode): Code of data about to send
            data (any): data to send
        """
        msg = json.dumps({
            'code': code,
            'data': data
        })

        socket.send(bytes(f'{len(msg):>{cls.HEADER_SIZE}}{msg}', 'utf-8'))

    @classmethod
    def listen_for_messages(cls, socket, caller):
        """Listens for incoming messages from given socket, calls caller when one is received.

        Args:
            socket (socket): Socket to listen for messages from
            caller (MsgReceivedObserver): Object to react to received data
        """
        while True:
            full_msg = ''
            msg_len = 0
            new_msg = True
            while True:
                try:
                    data = socket.recv(cls.HEADER_SIZE)
                    data = data.decode('utf-8')

                    if new_msg:
                        new_msg = False
                        msg_len = int(data)
                    else:
                        full_msg += data
                        if len(full_msg) >= msg_len:
                            break
                except ValueError as e:
                    # TODO implement more secure way of detecting disconnection
                    if data == '':
                        caller.on_msg_received(socket, {
                            'code': ServerCodes.DISCONNECTED,
                            'data': ''
                        })
                    return

            caller.on_msg_received(socket, json.loads(full_msg))
