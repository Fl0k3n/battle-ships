from login_observer import LoginObserver
from room import Room


class RoomHandler(LoginObserver):
    def __init__(self, user_handler):
        # TODO implement thread safety

        self.user_handler = user_handler
        self.last_id = -1            # for now ids will be successive ints, starting with 0
        self.joinable_rooms = set()  # room_ids
        self.rooms = {}              # room_id -> Room

    def on_login(self, socket, user):
        pass

    def on_logout(self, socket):
        pass

    def create_room(self, socket):
        user = self.user_handler.get_user(socket)
        if user is None:
            raise AttributeError(f'Cant create room for not logged-in user')

        self.last_id += 1
        room = Room(self.last_id, user.email, socket)

        self.joinable_rooms.add(self.last_id)
        self.rooms[self.last_id] = room

        return self.last_id

    def join_room(self, socket, room_id):
        pass

    def leave_room(self, socket):
        pass

    def get_rooms(self):
        return list(self.rooms.values())

    def get_joinable_rooms(self):
        return [rooms[room_id] for room_id in self.joinable_rooms]
