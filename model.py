class Tweet:
    def __init__(self, id, name, tweet):
        self.id = id
        self.name = name
        self.tweet = tweet

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'tweet': self.tweet}


class Node:
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def to_dict(self):
        return {'name': self.name, 'address': self.address}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(self.address)