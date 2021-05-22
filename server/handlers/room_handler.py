from models.room import Room
import threading


class RoomHandler:
    def __init__(self, user_handler):
        self.user_handler = user_handler
        self.last_id = -1            # for now ids will be successive ints, starting with 0
        self.joinable_rooms = set()  # room_ids
        self.rooms = {}              # room_id -> Room
        self.leave_queries = set()
        self.room_list_mutex = threading.Lock()

    def remove_room(self, room_id):
        with self.room_list_mutex:
            if room_id not in self.rooms:
                raise AttributeError(
                    f'5xx Server Error | Room {room_id} doesn\'t exist')

            self.leave_queries.add(room_id)

            if room_id in self.joinable_rooms:
                self.joinable_rooms.remove(room_id)

            return self.rooms.pop(room_id)

    def create_room(self, socket):
        """Creates room for user associated with given socket.
        Args:
            socket (socket): user's socket
        Raises:
            AttributeError: if user is not logged in
        Returns:
            int: id of created room
        """
        with self.user_handler.get_user_mutex():
            user = self.user_handler.get_user(socket)
            if user is None:
                raise AttributeError(
                    '5xx Server Error | Cant create room for not logged-in user')

            with self.room_list_mutex:
                if self.user_handler.is_in_room(user.email):
                    raise AttributeError(
                        '5xx Server Error | You have already joined the room')

                self.last_id += 1
                room = Room(self.last_id, user.email, socket)

                self.joinable_rooms.add(self.last_id)
                self.rooms[self.last_id] = room

                self.user_handler.joined_room(user.email, self.last_id)

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
        with self.user_handler.get_user_mutex():
            user = self.user_handler.get_user(socket)

            if user is None:
                raise AttributeError(
                    '5xx Server Error | Only logged-in user can join a room')

            if self.user_handler.is_in_room(user.email):
                raise AttributeError(
                    '5xx Server Error | You have already joined the room')

            with self.room_list_mutex:
                if room_id not in self.rooms:
                    raise AttributeError(f'Room {room_id} doesnt exist')

                if room_id not in self.joinable_rooms:
                    raise AttributeError(f'Room {room_id} is full.')

                room = self.rooms[room_id]

                if user.email == room.get_owner_email():
                    raise AttributeError(
                        '5xx Server Error | Owner cant join the room')

                self.joinable_rooms.remove(room_id)
                self.user_handler.joined_room(user.email, room_id)

                room.join(user.email, socket)

                return room.get_owner_socket(), user.email

    def get_rooms(self):
        return list(self.rooms.values())

    def get_joinable_rooms(self):
        return [self.rooms[room_id] for room_id in self.joinable_rooms]

    def get_opponents_socket(self, socket, room_id):
        with self.room_list_mutex:
            if room_id not in self.rooms:
                raise AttributeError(
                    f'5xx Server Error | Room {room_id} doesn\'t exist')

            room = self.rooms[room_id]
            if room.is_joinable():
                raise AttributeError(
                    f'5xx Server Error | Room {room_id} has only 1 player')

            return room.get_opponents_socket(socket)

    def is_joinable(self, room_id):
        # locked externally
        return room_id in self.joinable_rooms

    def is_queried_for_leave(self, room_id):
        return room_id in self.leave_queries

    def get_rooms_mutex(self):
        return self.room_list_mutex
