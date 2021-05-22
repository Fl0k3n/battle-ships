import socket
import json
from common.msg_codes import ServerCodes, UserCodes
from typing import Union


class CommunicationHandler:
    HEADER_SIZE = 10
    CODE_WRAPPER = None

    @classmethod
    def set_code_wrapper(cls, wrapper: Union[ServerCodes, UserCodes]) -> None:
        cls.CODE_WRAPPER = wrapper

    @classmethod
    def send_msg(cls, socket, code, data):
        """Sends message with given code and data to given socket.

        Args:
            socket (socket): Socket to send data to
            code (ServerCode|UserCode): Code of data about to send
            data (any): data to send, conversion to JSON has to be possible
        """
        msg = json.dumps({
            'code': code.value,
            'data': data
        })

        socket.send(bytes(f'{len(msg):>{cls.HEADER_SIZE}}{msg}', 'utf-8'))

    @classmethod
    def listen_for_messages(cls, socket, caller=None, only_one=False):
        """Listens for incoming messages from given socket.
           If caller is specified, calls it after message is received,
           if only_one is True, returns first received message.

        Args:
            socket (socket): Socket to listen for messages from
            caller (MsgReceivedObserver): Object to react to received data
            only_one (bool): if True, listening ends once first message is received
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
                except (ValueError, ConnectionResetError) as e:
                    # TODO implement more secure way of detecting disconnection
                    if data == '':
                        caller.on_msg_received(socket, {
                            'code': ServerCodes.DISCONNECTED,
                            'data': ''
                        })
                    return

            msg_dict = json.loads(full_msg)
            # wrap integer code response in Enum code
            if cls.CODE_WRAPPER is not None:
                msg_dict['code'] = cls.CODE_WRAPPER(msg_dict['code'])

            if caller is not None:
                caller.on_msg_received(socket, msg_dict)
            if only_one:
                return msg_dict
