from observers.login_observer import LoginObserver


class UserHandler(LoginObserver):
    def __init__(self):
        # TODO implement thread safety
        self.logged_in_users = {}  # email  -> User
        self.user_sockets = {}     # socket -> User

    def is_logged_in(self, email):
        return self.logged_in_users.get(email)

    def on_login(self, socket, user):
        self.logged_in_users[user.email] = user
        self.user_sockets[socket] = user

    def on_logout(self, socket):
        user = self.user_sockets.pop(socket, None)
        if user is not None:
            self.logged_in_users.pop(user.email)

        return user

    def get_user(self, socket):
        return self.user_sockets.get(socket)
