from abc import ABC, abstractmethod


class LoginObserver(ABC):
    @abstractmethod
    def on_login(self, socket, user):
        pass

    @abstractmethod
    def on_logout(self, socket):
        pass
