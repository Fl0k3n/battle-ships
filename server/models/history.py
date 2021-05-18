import mongoengine
from models.game_stats import GameStats


class History(mongoengine.Document):
    winner = mongoengine.EmbeddedDocumentField(GameStats)
    loser = mongoengine.EmbeddedDocumentField(GameStats)

    game_len = mongoengine.IntField()
    start_date = mongoengine.DateTimeField()

    meta = {
        'db_alias': 'main',
        'collection': 'history'
    }
