from abc import ABC, abstractmethod


class MsgReceivedObserver(ABC):
    @abstractmethod
    def on_msg_received(self, socket, msg):
        """Reacts to message received from given socket.

        Args:
            socket (socket): socket from which msg was received
            msg (plain object): object of type {code: (Server/User Code), data: (any)}
        """
        pass
