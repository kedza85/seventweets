import json
import unittest
import seventweets


class SevenTweetsTestCase(unittest.TestCase):

    def setUp(self):
        seventweets.app.config['TESTING'] = True
        self.app = seventweets.app.test_client()
        seventweets.storage.tweets = {}

    def test_get_tweets(self):
        response = self.app.get('/tweets')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        tweets = json.loads(response.get_data())
        assert type(tweets) == list
        assert len(tweets) == 0

        seventweets.storage.tweets = {0: {'id': 0, 'name': 'test name', 'tweet': 'test tweet'}}
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
        response = self.app.get('/tweets/1')
        assert response.status_code == 404

        seventweets.storage.tweets = {0: {'id': 0, 'name': 'test name', 'tweet': 'test tweet'}}
        response = self.app.get('/tweets/0')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        tweet = json.loads(response.get_data())
        assert tweet['id'] == tweet['id']
