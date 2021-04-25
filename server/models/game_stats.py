import mongoengine


class GameStats(mongoengine.EmbeddedDocument):
    user_id = mongoengine.ObjectIdField()

    misses = mongoengine.IntField()
    hits = mongoengine.IntField()
    score = mongoengine.IntField()
