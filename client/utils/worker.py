from PyQt5.QtCore import QObject, pyqtSignal
from common.communication_handler import CommunicationHandler as CH

# apparently pyqt doesn't like python threads, this is just a workaround for async listenning for msgs


class Worker(QObject):
    finished = pyqtSignal()
    response = pyqtSignal(dict)

    def __init__(self, server):
        super().__init__()
        self.server = server

    def run(self):
        print('called and waiting')
        res = CH.listen_for_messages(self.server, only_one=True)
        self.response.emit(res)
        self.finished.emit()
