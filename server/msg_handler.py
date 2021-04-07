import threading
from connection_observer import ConnectionObserver
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import ServerCodes
from common.msg_received_observer import MsgReceivedObserver


class MsgHandler(ConnectionObserver, MsgReceivedObserver):
    def __init__(self):
        pass

    def on_connected(self, socket):
        threading.Thread(target=CH.listen_for_messages,
                         args=(socket, self)).start()

    def on_disconnected(self, socket):
        pass

    def on_msg_received(self, socket, msg):
        code = msg['code']
        data = msg['data']

        if code == ServerCodes.DISCONNECTED:
            print('disconnected!')

        print(f'from msg_handler, received: {code} : {data}')
