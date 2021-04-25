import datetime


class Room:
    def __init__(self, idx, owner_email, owner_socket):
        self.id = idx
        self.creation_time = datetime.datetime.now()
        self.owner_email = owner_email
        self.owner_socket = owner_socket

        self.guest_email = None
        self.guest_socket = None

    def is_joinable(self):
        return self.guest_socket is None

    def join(self, guest_email, guest_socket):
        self.guest_email = guest_email
        self.guest_socket = guest_socket

    def get_formatted_data(self):
        res = {
            'id': self.id,
            'owner': self.owner_email
        }

        if not self.is_joinable():
            res['guest'] = self.guest_email

        return res
