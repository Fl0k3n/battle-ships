from observers.login_observer import LoginObserver
from models.room import Room


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
        """Creates room for user associated with given socket.
        Args:
            socket (socket): user's socket
        Raises:
            AttributeError: if user is not logged in
        Returns:
            int: id of created room
        """
        user = self.user_handler.get_user(socket)
        if user is None:
            raise AttributeError(
                '5xx Server Error | Cant create room for not logged-in user')
        if self.user_handler.is_in_room(user.email):
            raise AttributeError(
                '5xx Server Error | You have already joined the room')

        self.last_id += 1
        room = Room(self.last_id, user.email, socket)

        self.joinable_rooms.add(self.last_id)
        self.rooms[self.last_id] = room
        self.user_handler.joined_room(user.email)

        return self.last_id

    def join_room(self, socket, room_id):
        """User associated with given socket joins room with given room_id.
        Args:
            socket (socket): socket of user that wants to join
            room_id (int): id of room
        Raises:
            AttributeError: if user couldn't have joined the room
        Returns:
            socket: room owner's socket
            string: room guest email
        """
        user = self.user_handler.get_user(socket)

        if user is None:
            raise AttributeError(
                '5xx Server Error | Only logged-in user can join a room')

        if self.user_handler.is_in_room(user.email):
            raise AttributeError(
                '5xx Server Error | You have already joined the room')

        if room_id not in self.rooms:
            raise AttributeError(f'Room {room_id} doesnt exist')

        if room_id not in self.joinable_rooms:
            raise AttributeError(f'Room {room_id} is full.')

        room = self.rooms[room_id]

        if user.email == room.get_owner_email():
            raise AttributeError('5xx Server Error | Owner cant join the room')

        self.joinable_rooms.remove(room_id)
        self.user_handler.joined_room(user.email)

        room.join(user.email, socket)

        return room.get_owner_socket(), user.email

    def leave_room(self, socket):
        pass

    def get_rooms(self):
        return list(self.rooms.values())

    def get_joinable_rooms(self):
        return [rooms[room_id] for room_id in self.joinable_rooms]
