import abc
import functools
import pg8000

from config import Config
from model import Tweet


def uses_db(f):
    @functools.wraps(f)
    def wrapper(cls, *args, **kwargs):
        cursor = cls._conn.cursor()
        res = f(cls, cursor, *args, **kwargs)
        cursor.close()
        cls._conn.commit()
        return res
    return wrapper


class TweetStorage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_all(self):
        pass

    @abc.abstractmethod
    def get(self, id_):
        pass

    @abc.abstractmethod
    def add(self, name, tweet_text):
        pass

    @abc.abstractmethod
    def remove(self, id_):
        pass


class TweetDBStorage(TweetStorage):
    def __init__(self):
        self._conn = pg8000.Connection(**Config.DB_CONFIG)

    @uses_db
    def get_all(self, cursor):
        cursor.execute('SELECT id, name, tweet FROM tweets')

        return [Tweet(*tweet_data) for tweet_data in cursor.fetchall()]

    @uses_db
    def get(self, cursor, id_):
        cursor.execute(
            """
            SELECT id, name, tweet FROM tweets
            WHERE id=%s
            """,
            (id_, )
        )

        tweet_data = cursor.fetchone()

        return Tweet(*tweet_data)

    @uses_db
    def add(self, cursor, name, tweet_text):
        cursor.execute(
            """
            INSERT INTO tweets (name, tweet)
            VALUES ( %s, %s ) RETURNING id, name, tweet
            """,
            (name, tweet_text)
        )
        tweet_data = cursor.fetchone()

        return Tweet(*tweet_data)

    @uses_db
    def remove(self, cursor, id_):
        cursor.execute(
            """
            DELETE FROM tweets
            WHERE id=%s
            """,
            (id_, )
        )


class TweetInMemoryStorage(TweetStorage):
    tweets = {}
    id_counter = 0

    def get_all(self):
        return [tweet for tweet in self.tweets.values()]

    def get(self, id_):
        return self.tweets.get(id_)

    def add(self, name, tweet_text):
        id_ = self.id_counter
        tweet = Tweet(id_, name, tweet_text)
        self.tweets[id_] = tweet
        self.id_counter = self.id_counter + 1
        return tweet

    def remove(self, id_):
        del self.tweets[id_]
