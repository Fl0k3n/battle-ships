from abc import ABC, abstractmethod


class ConnectionObserver(ABC):
    @abstractmethod
    def on_connected(self, socket):
        pass

    @abstractmethod
    def on_disconnected(self, socket):
        pass
