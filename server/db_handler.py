

class DBHandler:
    def __init__(self):
        self.users = {}

    def save_user(self, email, password):
        # w tym momencie dane sa juz poprawne i mozna je zapisac
        # poki co tylko haslo, potem dojda jeszcze rankingi
        self.users[email] = {
            'password': password
        }
        # should raise an exception on failure

    def find_user(self, email):
        # should return None if not found
        return self.users.get(email)
