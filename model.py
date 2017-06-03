class Tweet:
    def __init__(self, id, name, tweet):
        self.id = id
        self.name = name
        self.tweet = tweet

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'tweet': self.tweet}
