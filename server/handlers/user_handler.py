from observers.login_observer import LoginObserver
import threading


class UserHandler(LoginObserver):
    def __init__(self):
        self.logged_in_users = {}  # email  -> User
        self.user_sockets = {}     # socket -> User
        self.users_in_room = {}    # email  -> room_id
        self.users_data_mutex = threading.Lock()

    def is_logged_in(self, email):
        return self.logged_in_users.get(email) is not None

    def on_login(self, socket, user):
        with self.users_data_mutex:
            self.logged_in_users[user.email] = user
            self.user_sockets[socket] = user

    def on_logout(self, socket):
        """Removes user associated with given socket, if one exists, else returns None.
        Args:
            socket (socket): user's socket
        Returns:
            User: Removed user object
        """
        with self.users_data_mutex:
            user = self.user_sockets.pop(socket, None)
            if user is not None:
                self.logged_in_users.pop(user.email)
                if user.email in self.users_in_room:
                    self.users_in_room.pop(user.email)

            return user

    def get_user(self, socket):
        """ Returns logged in user associated with given socket.
        Args:
            socket (socket): user's socket
        Returns:
            User: user associated with socket
        """
        return self.user_sockets.get(socket)

    def is_in_room(self, email=None, socket=None):
        # will be locked externally
        if socket is not None:
            email = self.get_user(socket).email

        return email in self.users_in_room

    def get_users_room(self, email=None, socket=None):
        # will be locked externally
        if socket is not None:
            email = self.get_user(socket).email

        return self.users_in_room[email]

    def joined_room(self, email, room_id):
        # don't lock here, handled in rooms-handler
        self.users_in_room[email] = room_id

    def left_room(self, email=None, socket=None):
        # dont lock here either
        if socket is not None:
            email = self.get_user(socket).email
        self.users_in_room.pop(email)

    def get_user_mutex(self):
        return self.users_data_mutex
