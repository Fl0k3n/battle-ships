import mongoengine
from models.user import User
from models.history import History
from models.game_stats import GameStats


class DBHandler:
    def __init__(self, db_uri):
        mongoengine.register_connection(
            alias='main', name='bsdb', host=db_uri)

    def save_user(self, email, password):
        user = User()
        user.email = email
        user.password = password
        user.save()

        return user

    def find_user(self, email):
        return User.objects(email=email).first()
