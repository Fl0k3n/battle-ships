from observers.login_observer import LoginObserver


class UserHandler(LoginObserver):
    def __init__(self):
        # TODO implement thread safety
        self.logged_in_users = {}  # email  -> User
        self.user_sockets = {}     # socket -> User
        self.users_in_room = set()

    def is_logged_in(self, email):
        return self.logged_in_users.get(email) is not None

    def on_login(self, socket, user):
        self.logged_in_users[user.email] = user
        self.user_sockets[socket] = user

    def on_logout(self, socket):
        """Removes user associated with given socket, if one exists, else returns None.
        Args:
            socket (socket): user's socket
        Returns:
            User: Removed user object
        """
        user = self.user_sockets.pop(socket, None)
        if user is not None:
            self.logged_in_users.pop(user.email)

        return user

    def get_user(self, socket):
        """ Returns logged in user associated with given socket.
        Args:
            socket (socket): user's socket
        Returns:
            User: user associated with socket
        """
        return self.user_sockets.get(socket)

    def is_in_room(self, email):
        return email in self.users_in_room

    def joined_room(self, email):
        self.users_in_room.add(email)

    def left_room(self, email):
        self.users_in_room.remove(email)
