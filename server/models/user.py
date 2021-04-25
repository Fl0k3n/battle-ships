import mongoengine
import datetime
from models.history import History


class User(mongoengine.Document):
    email = mongoengine.EmailField(required=True)
    password = mongoengine.BinaryField(required=True)
    register_date = mongoengine.DateTimeField(default=datetime.datetime.now)

    history = mongoengine.ListField(mongoengine.ReferenceField(History))

    meta = {
        'db_alias': 'main',
        'collection': 'users'
    }
