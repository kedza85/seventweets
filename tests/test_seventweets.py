import json
import unittest



import seventweets
from tweetstorage import TweetInMemoryStorage
from model import Tweet


def init_storage():
    pass


class SevenTweetsTestCase(unittest.TestCase):

    def setUp(self):
        seventweets.init_storage = init_storage
        seventweets.storage = TweetInMemoryStorage()
        seventweets.app.config['TESTING'] = True
        self.app = seventweets.app.test_client()

    def test_get_tweets(self):
        seventweets.storage.tweets = {}
        response = self.app.get('/tweets')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        tweets = json.loads(response.get_data())
        assert type(tweets) == list
        assert len(tweets) == 0

        seventweets.storage.tweets = {0: Tweet(0, 'test name', 'test tweet')}
        response = self.app.get('/tweets')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        tweets = json.loads(response.get_data())
        assert type(tweets) == list
        assert len(tweets) == 1
        tweet = tweets[0]
        assert tweet['id'] == 0
        assert tweet['name'] == 'test name'
        assert tweet['tweet'] == 'test tweet'

    def test_get_tweet(self):
        seventweets.storage.tweets = {}
        response = self.app.get('/tweets/1')
        assert response.status_code == 404

        seventweets.storage.tweets = {0: Tweet(0, 'test name', 'test tweet')}
        response = self.app.get('/tweets/0')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        tweet = json.loads(response.get_data())
        assert tweet['id'] == tweet['id']

