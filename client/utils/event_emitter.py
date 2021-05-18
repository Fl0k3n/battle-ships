from utils.events import Event
from typing import Callable, Any


class EventEmitter:
    def __init__(self):
        self.listeners = {}

    def add_event_listener(self, event: Event, listener: Callable[..., None]) -> None:
        if event not in self.listeners:
            self.listeners[event] = [listener]
        else:
            self.listeners[event].append(listener)

    def call_listeners(self, event: Event, data: Any = None) -> None:
        listeners = self.listeners.get(event)

        if listeners is not None:
            for listener in listeners:
                if data is None:
                    listener(event, self)
                else:
                    listener(event, self, data)
